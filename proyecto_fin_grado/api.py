import frappe
import requests
from frappe.utils import flt
from requests.auth import HTTPBasicAuth

@frappe.whitelist()
def exportar_ubl(sales_invoice_name):
    invoice = frappe.get_doc('Sales Invoice', sales_invoice_name)
    company = frappe.get_doc('Company', invoice.company)
    customer = frappe.get_doc('Customer', invoice.customer)

    line_total = sum(flt(d.amount, 2) for d in invoice.items)
    tax_total = sum(flt(tax.tax_amount, 2) for tax in invoice.taxes)
    grand_total = flt(line_total + tax_total, 2)

    tax_lines = ""
    for tax in invoice.taxes:
        tax_lines += f"""
        <cac:TaxTotal>
            <cbc:TaxAmount currencyID=\"{invoice.currency}\">{flt(tax.tax_amount, 2)}</cbc:TaxAmount>
            <cac:TaxSubtotal>
                <cbc:TaxableAmount currencyID=\"{invoice.currency}\">{flt(tax.total, 2)}</cbc:TaxableAmount>
                <cbc:TaxAmount currencyID=\"{invoice.currency}\">{flt(tax.tax_amount, 2)}</cbc:TaxAmount>
                <cac:TaxCategory>
                    <cbc:ID>S</cbc:ID>
                    <cbc:Percent>{flt(tax.rate, 2)}</cbc:Percent>
                    <cac:TaxScheme>
                        <cbc:ID>VAT</cbc:ID>
                        <cbc:Name>{tax.description or 'IVA'}</cbc:Name>
                    </cac:TaxScheme>
                </cac:TaxCategory>
            </cac:TaxSubtotal>
        </cac:TaxTotal>
        """

    payment_lines = ""
    for idx, p in enumerate(invoice.payments, start=1):
        payment_lines += f"""
        <cac:PaymentMeans>
            <cbc:PaymentMeansCode>42</cbc:PaymentMeansCode>
            <cbc:PaymentID>{p.reference_no or f"PAY-{idx}"}</cbc:PaymentID>
            <cac:PayeeFinancialAccount>
                <cbc:ID>{p.account}</cbc:ID>
            </cac:PayeeFinancialAccount>
        </cac:PaymentMeans>
        """

    invoice_lines = ""
    for idx, item in enumerate(invoice.items, start=1):
        invoice_lines += f"""
        <cac:InvoiceLine>
            <cbc:ID>{idx}</cbc:ID>
            <cbc:InvoicedQuantity unitCode=\"EA\">{flt(item.qty, 2)}</cbc:InvoicedQuantity>
            <cbc:LineExtensionAmount currencyID=\"{invoice.currency}\">{flt(item.amount, 2)}</cbc:LineExtensionAmount>
            <cac:Item>
                <cbc:Description>{item.item_name}</cbc:Description>
            </cac:Item>
            <cac:Price>
                <cbc:PriceAmount currencyID=\"{invoice.currency}\">{flt(item.rate, 2)}</cbc:PriceAmount>
            </cac:Price>
        </cac:InvoiceLine>
        """

    ubl_xml = f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>
<Invoice xmlns=\"urn:oasis:names:specification:ubl:schema:xsd:Invoice-2\"
         xmlns:cbc=\"urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2\"
         xmlns:cac=\"urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2\">
    <cbc:UBLVersionID>2.1</cbc:UBLVersionID>
    <cbc:CustomizationID>urn:cen.eu:en16931:2017</cbc:CustomizationID>
    <cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID>
    <cbc:ID>{invoice.name}</cbc:ID>
    <cbc:IssueDate>{invoice.posting_date}</cbc:IssueDate>

    <cac:AccountingSupplierParty>
        <cac:Party>
            <cac:PartyName>
                <cbc:Name>{company.name}</cbc:Name>
            </cac:PartyName>
        </cac:Party>
    </cac:AccountingSupplierParty>

    <cac:AccountingCustomerParty>
        <cac:Party>
            <cac:PartyName>
                <cbc:Name>{customer.customer_name}</cbc:Name>
            </cac:PartyName>
        </cac:Party>
    </cac:AccountingCustomerParty>

    {tax_lines}

    <cac:LegalMonetaryTotal>
        <cbc:PayableAmount currencyID=\"{invoice.currency}\">{grand_total}</cbc:PayableAmount>
    </cac:LegalMonetaryTotal>

    {payment_lines}
    {invoice_lines}
</Invoice>
"""
    return ubl_xml

@frappe.whitelist()
def enviar_factura_a_cliente(sales_invoice_name, customer_name):
    try:
        customer = frappe.get_doc("Customer", customer_name)
        endpoint = customer.custom_apiendpoint
        api_key = customer.custom_apikey
        api_secret = customer.get_password("custom_apisecret")

        if not endpoint or not api_key or not api_secret:
            return "El cliente no tiene configurado endpoint o claves API."

        xml_content = exportar_ubl(sales_invoice_name)
        headers = {
            "Content-Type": "application/xml",
            "Authorization": f"token {api_key}:{api_secret}"
        }

        response = requests.post(url=endpoint, headers=headers, data=xml_content.encode("utf-8"))

        if response.status_code == 200:
            return f"Factura enviada correctamente a {customer.customer_name}"
        else:
            frappe.log_error(response.text, "Error al enviar factura UBL")
            return f"Error del cliente ({response.status_code}): {response.text}"

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Excepción al enviar factura UBL")
        return f"Error al enviar: {str(e)}"