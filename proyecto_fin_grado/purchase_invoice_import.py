import frappe
import xml.etree.ElementTree as ET
from frappe import _
from frappe.utils.password import check_password


@frappe.whitelist(allow_guest=True, methods=["POST"])
def recibir_ubl():
    try:
        if not frappe.request.authorization:
            frappe.local.response.http_status_code = 401
            return "Falta cabecera Authorization."

        if frappe.session.user == "Guest":
            frappe.local.response.http_status_code = 403
            return "Autenticación fallida."

        xml_data = frappe.request.data.decode("utf-8")
        return importar_ubl_desde_string(xml_data)

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error al recibir factura UBL")
        frappe.local.response.http_status_code = 500
        return f"Error: {str(e)}"

@frappe.whitelist()
def importar_ubl_desde_listado(xml_string):
    try:
        return importar_ubl_desde_string(xml_string)
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error en importar_ubl_desde_listado")
        return f"Error: {str(e)}"

def importar_ubl_desde_string(xml_string):
    ns = {
        "cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
        "cac": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
    }

    root = ET.fromstring(xml_string)

    supplier_name = root.find(".//cac:AccountingSupplierParty//cbc:Name", ns).text.strip()
    invoice_id = root.find("cbc:ID", ns).text
    issue_date = root.find("cbc:IssueDate", ns).text

    company = frappe.get_doc("Company", frappe.defaults.get_user_default("Company"))
    expense_account = frappe.db.get_value("Account", {
        "company": company.name,
        "root_type": "Expense",
        "is_group": 0
    }, "name")

    amount = root.find(".//cbc:PayableAmount", ns).text
    if not expense_account:
        return "No se encontró cuenta de gastos válida."

    supplier = frappe.db.exists("Supplier", supplier_name)
    if not supplier:
        new_supplier = frappe.get_doc({
            "doctype": "Supplier",
            "supplier_name": supplier_name,
            "supplier_type": "Company"
        })
        new_supplier.insert(ignore_permissions=True)
        supplier = new_supplier.name

    if frappe.db.exists("Purchase Invoice", {"bill_no": invoice_id}):
        return f"Factura ya existente: {invoice_id}"

    taxes = []
    for tax_total in root.findall(".//cac:TaxTotal", ns):
        for tax_sub in tax_total.findall(".//cac:TaxSubtotal", ns):
            tax_amount = tax_sub.find("cbc:TaxAmount", ns).text
            taxable_amount = tax_sub.find("cbc:TaxableAmount", ns).text
            percent_node = tax_sub.find(".//cbc:Percent", ns)
            percent = percent_node.text if percent_node is not None else "0"

            taxes.append({
                "charge_type": "On Net Total",
                "account_head": "VAT - " + company.abbr,
                "rate": percent,
                "tax_amount": tax_amount,
                "tax_amount_after_discount_amount": tax_amount,
                "total": taxable_amount
            })

    items = []
    for line in root.findall(".//cac:InvoiceLine", ns):
        quantity = line.find("cbc:InvoicedQuantity", ns).text
        price = line.find(".//cbc:PriceAmount", ns).text
        description_node = line.find(".//cbc:Description", ns)
        description = description_node.text if description_node is not None else "Producto sin descripción"

        items.append({
            "item_name": description,
            "qty": float(quantity),
            "rate": float(price),
            "amount": float(quantity) * float(price),
            "expense_account": expense_account
        })

    references_text = []
    for pay in root.findall(".//cac:PaymentMeans", ns):
        pay_id = pay.find("cbc:PaymentID", ns)
        if pay_id is not None and pay_id.text:
            references_text.append(pay_id.text.strip())

    purchase_invoice = frappe.get_doc({
        "doctype": "Purchase Invoice",
        "supplier": supplier,
        "posting_date": issue_date,
        "bill_no": invoice_id,
        "bill_date": issue_date,
        "items": items,
        "taxes": taxes,
        "remarks": "Pagos: " + ", ".join(references_text) if references_text else None
    })
    purchase_invoice.insert(ignore_permissions=True)
    purchase_invoice.submit()

    return f"Factura importada: {purchase_invoice.name}"