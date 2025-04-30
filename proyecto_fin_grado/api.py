import frappe
from frappe import _
from datetime import date

@frappe.whitelist()
def exportar_ubl(sales_invoice_name):
    invoice = frappe.get_doc('Sales Invoice', sales_invoice_name)

    ubl_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<Invoice xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"
         xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
         xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2">
  <cbc:UBLVersionID>2.1</cbc:UBLVersionID>
  <cbc:CustomizationID>urn:cen.eu:en16931:2017</cbc:CustomizationID>
  <cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID>
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
'''

    for i, item in enumerate(invoice.items, start=1):
        ubl_xml += f'''
  <cac:InvoiceLine>
    <cbc:ID>{i}</cbc:ID>
    <cbc:InvoicedQuantity unitCode="EA">{item.qty}</cbc:InvoicedQuantity>
    <cbc:LineExtensionAmount currencyID="{invoice.currency}">{item.amount}</cbc:LineExtensionAmount>
    <cac:Item>
      <cbc:Name>{item.item_name}</cbc:Name>
    </cac:Item>
    <cac:Price>
      <cbc:PriceAmount currencyID="{invoice.currency}">{item.rate}</cbc:PriceAmount>
    </cac:Price>
  </cac:InvoiceLine>
'''

    ubl_xml += '\n</Invoice>'
    return ubl_xml
