import frappe
from frappe import _

@frappe.whitelist()
def exportar_ubl(sales_invoice_name):
    invoice = frappe.get_doc('Sales Invoice', sales_invoice_name)
    
    ubl_xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Invoice xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"
         xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
         xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2">

    <cbc:ID>{invoice.name}</cbc:ID>
    <cbc:IssueDate>{invoice.posting_date}</cbc:IssueDate>
    
    <cac:AccountingSupplierParty>
        <cac:Party>
            <cac:PartyName>
                <cbc:Name>{invoice.company}</cbc:Name>
            </cac:PartyName>
        </cac:Party>
    </cac:AccountingSupplierParty>

    <cac:AccountingCustomerParty>
        <cac:Party>
            <cac:PartyName>
                <cbc:Name>{invoice.customer_name}</cbc:Name>
            </cac:PartyName>
        </cac:Party>
    </cac:AccountingCustomerParty>

    <cac:LegalMonetaryTotal>
        <cbc:PayableAmount currencyID="{invoice.currency}">{invoice.rounded_total}</cbc:PayableAmount>
    </cac:LegalMonetaryTotal>

</Invoice>"""
    
    return ubl_xml
