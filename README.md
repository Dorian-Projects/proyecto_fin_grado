# Automatización de Facturación Electrónica UBL entre Instancias ERPNext

**Autor:** Dorian Miguel Flores Bonilla  
**Centro:** IES Martínez Montañés  
**Fecha:** Junio 2025

---

## Índice

1. [Introducción](#1-introducción)  
2. [Objetivos del proyecto](#2-objetivos-del-proyecto)  
3. [Tecnologías utilizadas](#3-tecnologías-utilizadas)  
4. [Estructura general del sistema](#4-estructura-general-del-sistema)  
5. [Exportación de facturas UBL](#5-exportación-de-facturas-ubl)  
6. [Problemas encontrados](#6-problemas-encontrados)  
7. [Mejoras futuras](#7-mejoras-futuras)  
8. [Código fuente comentado](#8-código-fuente-comentado)  
9. [Conclusiones](#9-conclusiones)  
10. [Anexos](#10-anexos)

---

## 1. Introducción

En un mundo donde la interoperabilidad entre sistemas es crucial, este proyecto busca automatizar el intercambio de facturas electrónicas entre dos instancias ERPNext. ¿Cómo? A través del estándar internacional **UBL 2.1** y el uso de APIs REST.

La aplicación desarrollada permite generar un XML UBL desde una factura de venta y enviarlo automáticamente a otra instancia, donde se convierte en una factura de compra. Todo esto sin intervención manual, cumpliendo normas y ganando eficiencia.

>![imagen](https://github.com/user-attachments/assets/5e01aba9-291a-4c77-ab2b-c0edbc022b3c)


---

## 2. Objetivos del proyecto

###  Objetivo general
Desarrollar una integración entre instancias ERPNext para enviar y recibir facturas en formato UBL usando API REST.

###  Objetivos específicos
- Generar archivos XML válidos con estructura UBL 2.1.  
- Añadir un botón de exportación en el formulario de factura.  
- Enviar automáticamente el XML a la instancia cliente.  
- Verificar y crear proveedores en la instancia receptora.  
- Prevenir facturas duplicadas.  
- Registrar automáticamente la factura de compra.  
- Permitir importación manual de facturas UBL.

---

## 3. Tecnologías utilizadas

-  ERPNext v14  
-  Frappe Framework  
-  Python 3.10  
-  JavaScript  
-  XML UBL 2.1 + PEPPOL BIS Billing 3.0  
-  API RESTful  
  
> ![imagen](https://github.com/user-attachments/assets/cc3a5548-cb90-4f12-b6c8-91d8b249d4cb)


---

## 4. Estructura general del sistema

###  Sitios utilizados

- `proveedor.localhost`: instancia emisora.  
- `hospital.localhost`: instancia receptora.  
- `development.localhost`: entorno de pruebas.

###  App personalizada: `proyecto_fin_grado`
 
- `api.py`: envío automático vía API y genera XML para exportar o enviar.  
- `purchase_invoice_import.py`: analiza y registra factura.  
- `sales_invoice_ubl.js`: botón “Exportar UBL”, "Enviar a Cliente".  
- `purchase_invoice_ubl_form.js`: botón “Importar UBL”.

###  Flujo de trabajo

1. Se crea y valida una factura de venta.  
2. Se genera un archivo XML con formato UBL.  
3. Se envía automáticamente vía API REST.  
4. El receptor interpreta el XML y crea la factura de compra.

> ![imagen](https://github.com/user-attachments/assets/dae60f94-af90-42cb-9815-3063b9355c3b)
>![imagen](https://github.com/user-attachments/assets/58f04792-cb36-4de6-a9a2-466a81582eb4)


---

## 5. Exportación de facturas UBL

El botón "Exportar UBL" se integra directamente en el formulario “Sales Invoice”. Al activarlo, se genera un XML UBL con todas las etiquetas necesarias: `<cbc:ID>`, `<cbc:IssueDate>`, `<cac:AccountingSupplierParty>`, etc.

La exportación asegura:
- Validación de campos obligatorios.  
- Escapado de caracteres especiales.  
- Formato correcto de fechas y divisas.

> ![imagen](https://github.com/user-attachments/assets/e07f3f86-5dd7-4bb6-a5d6-05dd1de79661)
> ![imagen](https://github.com/user-attachments/assets/007601d4-6396-4ea8-8c58-5dfcc540ba70)



---

## 6. Problemas encontrados

-  Problemas con caracteres especiales como `&`, `<`, `>`.  
-  Falta de etiquetas requeridas por validadores UBL.  
-  Detección de duplicados al importar.  
-  Necesidad de crear proveedores nuevos automáticamente.  
-  Fallos de autenticación API resueltos con tokens personalizados.


---

## 7 Mejoras futuras

- Notificaciones automáticas por correo al enviar o recibir una factura.  
- Integración con PEPPOL para compatibilidad con plataformas europeas.  
- Historial de versiones de facturas con trazabilidad de cambios.

---

## 8. Código fuente comentado

### Envío del XML al cliente
Se usa `requests.post()` con el XML como cuerpo y un token de autorización en cabecera.

### Importación del XML en hospital.localhost
Se recibe el XML, se analiza, se comprueba si el proveedor existe, y si no, se crea. Luego se registra la `Purchase Invoice`.

---

## 9. Conclusiones

Este proyecto demuestra que es totalmente viable automatizar el proceso de facturación entre ERPNexts usando tecnologías abiertas, APIs REST y el estándar UBL. Los beneficios hablan por sí solos:

- Menos errores.  
- Menos tareas repetitivas.  
- Más integración.  
- Y más tiempo para lo que realmente importa.

ERPNext y Frappe han demostrado ser herramientas potentes y flexibles para este tipo de soluciones.

> ![imagen](https://github.com/user-attachments/assets/6176c57f-af26-46a4-8537-f2a70ecbc4b8)

---

## 10. Anexos

###  Fragmento del XML UBL generado
<Invoice>
<cbc:UBLVersionID>2.1</cbc:UBLVersionID>
<cbc:CustomizationID>urn:cen.eu:en16931:2017</cbc:CustomizationID>
<cbc:ProfileID>urn:fdc:peppol.eu:2017:poacc:billing:01:1.0</cbc:ProfileID>
<cbc:ID>ACC-SINV-2025-00012</cbc:ID>
<cbc:IssueDate>2025-06-09</cbc:IssueDate>
<cac:AccountingSupplierParty>
<cac:Party>
<cac:PartyName>
<cbc:Name>Medicamentos SL (Demo)</cbc:Name>
</cac:PartyName>
</cac:Party>
</cac:AccountingSupplierParty>
<cac:AccountingCustomerParty>
<cac:Party>
<cac:PartyName>
<cbc:Name>Hospital Flobon</cbc:Name>
</cac:PartyName>
</cac:Party>
</cac:AccountingCustomerParty>
<cac:LegalMonetaryTotal>
<cbc:PayableAmount currencyID="EUR">800.0</cbc:PayableAmount>
</cac:LegalMonetaryTotal>
<cac:InvoiceLine>
<cbc:ID>1</cbc:ID>
<cbc:InvoicedQuantity unitCode="EA">1.0</cbc:InvoicedQuantity>
<cbc:LineExtensionAmount currencyID="EUR">800.0</cbc:LineExtensionAmount>
<cac:Item>
<cbc:Description>Viagra</cbc:Description>
</cac:Item>
<cac:Price>
<cbc:PriceAmount currencyID="EUR">800.0</cbc:PriceAmount>
</cac:Price>
</cac:InvoiceLine>
</Invoice>
