import frappe
import xml.etree.ElementTree as ET

@frappe.whitelist()
def importar_ubl_desde_listado(xml_string):
    try:
        root = ET.fromstring(xml_string)

        ns = {
            "cbc": "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2",
            "cac": "urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
        }

        supplier_name = root.find(".//cac:AccountingSupplierParty//cbc:Name", ns).text.strip()
        invoice_id = root.find("cbc:ID", ns).text
        issue_date = root.find("cbc:IssueDate", ns).text
        amount = root.find(".//cbc:PayableAmount", ns).text

        # Crear proveedor si no existe
        supplier = frappe.db.exists("Supplier", supplier_name)
        if not supplier:
            new_supplier = frappe.get_doc({
                "doctype": "Supplier",
                "supplier_name": supplier_name,
                "supplier_type": "Company"
            })
            new_supplier.insert(ignore_permissions=True)
            supplier = new_supplier.name

        # Verificar duplicados
        existing_invoice = frappe.db.exists("Purchase Invoice", {"bill_no": invoice_id})
        if existing_invoice:
            return f"Factura ya existente: {existing_invoice}"

        # Obtener cuenta de gastos disponible
        company = frappe.get_doc("Company", frappe.defaults.get_user_default("Company"))
        expense_account = frappe.db.get_value("Account", {
            "company": company.name,
            "root_type": "Expense",
            "is_group": 0
        }, "name")

        if not expense_account:
            return "No se encontró una cuenta de gastos válida para registrar la factura."

        # === Impuestos ===
        taxes = []
        for tax_total in root.findall(".//cac:TaxTotal", ns):
            for tax_sub in tax_total.findall(".//cac:TaxSubtotal", ns):
                tax_amount = tax_sub.find("cbc:TaxAmount", ns).text
                taxable_amount = tax_sub.find("cbc:TaxableAmount", ns).text
                percent_node = tax_sub.find(".//cbc:Percent", ns)
                percent = percent_node.text if percent_node is not None else "0"

                tax_entry = {
                    "charge_type": "On Net Total",
                    "account_head": "VAT - " + company.abbr,
                    "rate": percent,
                    "tax_amount": tax_amount,
                    "tax_amount_after_discount_amount": tax_amount,
                    "total": taxable_amount
                }
                taxes.append(tax_entry)

        # === Pagos ===
        references = root.findall(".//cac:PaymentMeans", ns)
        references_text = []
        for pay in references:
            pay_id = pay.find("cbc:PaymentID", ns)
            if pay_id is not None and pay_id.text:
                references_text.append(pay_id.text.strip())

        # Crear factura
        purchase_invoice = frappe.get_doc({
            "doctype": "Purchase Invoice",
            "supplier": supplier,
            "posting_date": issue_date,
            "bill_no": invoice_id,
            "bill_date": issue_date,
            "items": [{
                "item_name": "Importado de UBL",
                "qty": 1,
                "rate": amount,
                "amount": amount,
                "expense_account": expense_account
            }],
            "taxes": taxes,
            "remarks": "Pagos: " + ", ".join(references_text) if references_text else None
        })
        purchase_invoice.insert(ignore_permissions=True)
        purchase_invoice.submit()

        return f"Factura creada: {purchase_invoice.name}"

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error al importar UBL")
        return f"Error: {str(e)}"
