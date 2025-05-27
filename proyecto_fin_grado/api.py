import frappe
from frappe import _
from frappe.utils import flt

@frappe.whitelist()
def exportar_ubl(sales_invoice_name):
    invoice = frappe.get_doc('Sales Invoice', sales_invoice_name)
    company = frappe.get_doc('Company', invoice.company)
    customer = frappe.get_doc('Customer', invoice.customer)

    #Impuestos
    tax_lines = ""
    for tax in invoice.taxes:
        tax_lines += f"""
        <cac:TaxTotal>
            <cbc:TaxAmount currencyID="{invoice.currency}">{flt(tax.tax_amount, 2)}</cbc:TaxAmount>
            <cac:TaxSubtotal>
                <cbc:TaxableAmount currencyID="{invoice.currency}">{flt(tax.total, 2)}</cbc:TaxableAmount>
                <cbc:TaxAmount currencyID="{invoice.currency}">{flt(tax.tax_amount, 2)}</cbc:TaxAmount>
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

    #Pagos
    payment_lines = ""
    for idx, p in enumerate(invoice.payments, start=1):
        payment_lines += f"""
        <cac:PaymentMeans>
            <cbc:PaymentMeansCode>42</cbc:PaymentMeansCode> <!-- Transferencia -->
            <cbc:PaymentID>{p.reference_no or f"PAY-{idx}"}</cbc:PaymentID>
            <cac:PayeeFinancialAccount>
                <cbc:ID>{p.account}</cbc:ID>
            </cac:PayeeFinancialAccount>
        </cac:PaymentMeans>
        """

    #XML UBL básico + secciones insertadas
    ubl_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Invoice xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"
         xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2">
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
        <cbc:PayableAmount currencyID="{invoice.currency}">{invoice.rounded_total}</cbc:PayableAmount>
    </cac:LegalMonetaryTotal>

    {payment_lines}

    <cac:InvoiceLine>
        <cbc:ID>1</cbc:ID>
        <cbc:InvoicedQuantity unitCode="EA">1.0</cbc:InvoicedQuantity>
        <cbc:LineExtensionAmount currencyID="{invoice.currency}">1.0</cbc:LineExtensionAmount>
        <cac:Item>
            <cbc:Name>Ejemplo</cbc:Name>
        </cac:Item>
        <cac:Price>
            <cbc:PriceAmount currencyID="{invoice.currency}">1.0</cbc:PriceAmount>
        </cac:Price>
    </cac:InvoiceLine>
</Invoice>
"""

    return ubl_xml
