# 📦 Automatización de Facturación Electrónica UBL entre Instancias ERPNext

**Autor:** Dorian Miguel Flores Bonilla  
**Centro:** IES Martínez Montañés  
**Fecha:** Junio 2025

---

## 📑 Índice

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

> 📷 *Captura sugerida:* factura original en ERPNext antes de la exportación.

---

## 2. Objetivos del proyecto

### 🎯 Objetivo general
Desarrollar una integración entre instancias ERPNext para enviar y recibir facturas en formato UBL usando API REST.

### 🔍 Objetivos específicos
- Generar archivos XML válidos con estructura UBL 2.1.  
- Añadir un botón de exportación en el formulario de factura.  
- Enviar automáticamente el XML a la instancia cliente.  
- Verificar y crear proveedores en la instancia receptora.  
- Prevenir facturas duplicadas.  
- Registrar automáticamente la factura de compra.  
- Permitir importación manual de facturas UBL.

---

## 3. Tecnologías utilizadas

- ✅ ERPNext v14  
- ✅ Frappe Framework  
- ✅ Python 3.10  
- ✅ JavaScript (Client Side)  
- ✅ XML UBL 2.1 + PEPPOL BIS Billing 3.0  
- ✅ API RESTful  
- ✅ Herramientas de prueba: Postman, curl

> 📷 *Captura sugerida:* consola de pruebas con Postman o curl.

---

## 4. Estructura general del sistema

### 🖥 Sitios utilizados

- `proveedor.localhost`: instancia emisora.  
- `hospital.localhost`: instancia receptora.  
- `development.localhost`: entorno de pruebas.

### 📁 App personalizada: `proyecto_fin_grado`

- `exportar_ubl.py`: genera XML desde factura.  
- `api.py`: envío automático vía API.  
- `purchase_invoice_import.py`: analiza y registra factura.  
- `sales_invoice_ubl.js`: botón “Exportar UBL”.  
- `purchase_invoice_ubl_form.js`: botón “Importar UBL”.

### 🔄 Flujo de trabajo

1. Se crea y valida una factura de venta.  
2. Se genera un archivo XML con formato UBL.  
3. Se envía automáticamente vía API REST.  
4. El receptor interpreta el XML y crea la factura de compra.

> 📷 *Captura sugerida:* diagrama del flujo de datos entre instancias.

---

## 5. Exportación de facturas UBL

El botón "Exportar UBL" se integra directamente en el formulario “Sales Invoice”. Al activarlo, se genera un XML UBL con todas las etiquetas necesarias: `<cbc:ID>`, `<cbc:IssueDate>`, `<cac:AccountingSupplierParty>`, etc.

La exportación asegura:
- Validación de campos obligatorios.  
- Escapado de caracteres especiales.  
- Formato correcto de fechas y divisas.

> 📷 *Captura sugerida:* botón "Exportar UBL" y fragmento del XML generado.

---

## 6. Problemas encontrados

- ❗ Problemas con caracteres especiales como `&`, `<`, `>`.  
- ❗ Falta de etiquetas requeridas por validadores UBL.  
- ❗ Detección de duplicados al importar.  
- ❗ Necesidad de crear proveedores nuevos automáticamente.  
- ❗ Fallos de autenticación API resueltos con tokens personalizados.

> 📷 *Captura sugerida:* error de validación y solución aplicada.

---

## 7. Mejoras futuras

- 🔐 Firma digital de los XML con certificados X.509.  
- 🧪 Validación automática contra esquemas XSD.  
- 📊 Panel de seguimiento visual de facturas.  
- 🧾 Registro detallado de logs en cada fase del proceso.  
- 🌐 Soporte multicliente y autenticación avanzada.

> 📷 *Captura sugerida:* mockup del panel de seguimiento de facturas.

---

## 8. Código fuente comentado

### Envío del XML al cliente
Se usa `requests.post()` con el XML como cuerpo y un token de autorización en cabecera.

### Importación del XML en hospital.localhost
Se recibe el XML, se analiza, se comprueba si el proveedor existe, y si no, se crea. Luego se registra la `Purchase Invoice`.

> 📷 *Captura sugerida:* fragmento de `exportar_ubl.py` y `purchase_invoice_import.py`.

---

## 9. Conclusiones

Este proyecto demuestra que es totalmente viable automatizar el proceso de facturación entre ERPNexts usando tecnologías abiertas, APIs REST y el estándar UBL. Los beneficios hablan por sí solos:

- Menos errores.  
- Menos tareas repetitivas.  
- Más integración.  
- Y más tiempo para lo que realmente importa.

ERPNext y Frappe han demostrado ser herramientas potentes y flexibles para este tipo de soluciones.

> 📷 *Captura sugerida:* mensaje de éxito al importar una factura.

---

## 10. Anexos

### 📄 Fragmento del XML UBL generado

```xml
<Invoice xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2">
  <cbc:ID>INV-0001</cbc:ID>
  <cbc:IssueDate>2025-06-01</cbc:IssueDate>
  <cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
  <cbc:DocumentCurrencyCode>EUR</cbc:DocumentCurrencyCode>
  ...
</Invoice>
