
Automatización de Facturación Electrónica UBL entre Instancias ERPNext

Autor: Dorian Miguel Flores Bonilla
Centro: IES Martínez Montañés
Fecha: Junio 2025
Índice

    Introducción

    Objetivos del proyecto

    Tecnologías utilizadas

    Estructura general del sistema

    Exportación de facturas UBL

    Problemas encontrados

    Mejoras futuras

    Código fuente comentado

    Conclusiones

    Anexos

1. Introducción

En un mundo donde la interoperabilidad entre sistemas es cada vez más crucial, este proyecto nace con una meta clara: automatizar el intercambio de facturas electrónicas entre dos instancias independientes de ERPNext. ¿La clave? Usar el estándar internacional UBL 2.1 para estructurar las facturas en formato XML y conectar todo mediante APIs REST.

A lo largo de este trabajo, se ha desarrollado una aplicación personalizada que permite generar el archivo XML a partir de una factura de venta. Este documento, una vez listo, se envía de forma automática a otra instancia, donde es interpretado y convertido en una factura de compra válida. Todo esto sin intervención manual. Todo esto, funcionando como debe.

(Aquí iría una captura de pantalla de una factura original en ERPNext antes de exportarse)
2. Objetivos del proyecto

Objetivo general:

    Implementar una integración entre dos instancias de ERPNext que permita el envío y la recepción de facturas electrónicas en formato UBL utilizando una API RESTful.

Objetivos específicos:

    Generar archivos XML válidos con estructura UBL 2.1 a partir de facturas de venta.

    Incorporar un botón de exportación directa en la interfaz de ERPNext.

    Enviar automáticamente los XML al cliente correspondiente.

    Verificar si el proveedor existe en la instancia receptora y crearlo si no.

    Evitar duplicados validando el identificador de la factura.

    Registrar automáticamente la factura de compra en el sistema receptor.

    Permitir, además, una importación manual alternativa.

3. Tecnologías utilizadas

Este proyecto se construyó sobre herramientas potentes y modernas:

    ERPNext v14

    Frappe Framework

    Python 3.10

    JavaScript (JS del lado cliente)

    XML UBL 2.1, perfil PEPPOL BIS Billing 3.0

    API REST

    Postman y curl para pruebas de endpoints

(Aquí se recomienda insertar una captura del entorno de desarrollo: por ejemplo, usando Postman para probar la API)
4. Estructura general del sistema
Sitios utilizados

    proveedor.localhost: es la instancia emisora; genera y envía la factura.

    hospital.localhost: recibe el XML e importa la factura como una factura de compra.

    development.localhost: entorno seguro de pruebas y validaciones.

Aplicación personalizada: proyecto_fin_grado

La app desarrollada incluye los siguientes archivos clave:

    exportar_ubl.py: genera el XML desde la factura.

    api.py: se encarga de enviar el XML al cliente mediante una solicitud POST.

    purchase_invoice_import.py: recibe el XML, lo analiza y genera la factura de compra.

    sales_invoice_ubl.js: añade el botón "Exportar UBL" en la interfaz de la factura.

    purchase_invoice_ubl_form.js: añade el botón "Importar UBL" para carga manual.

Flujo de trabajo

    El proveedor genera y valida una factura de venta.

    El sistema genera automáticamente un archivo XML con formato UBL.

    Ese archivo se envía al sistema hospital.localhost vía API.

    El sistema receptor analiza el contenido, verifica el proveedor y crea la factura de compra.

(Aquí iría una imagen o esquema visual del flujo de datos entre ambas instancias)
5. Exportación de facturas UBL

Se incorporó un botón directamente en el formulario “Sales Invoice”. Al hacer clic, se realiza una llamada al servidor para generar el archivo XML siguiendo las especificaciones UBL.

Se utilizaron etiquetas clave como <cbc:ID>, <cbc:IssueDate>, <cac:AccountingSupplierParty> y <cac:LegalMonetaryTotal>. El sistema también se encarga de validar campos obligatorios, escapar caracteres especiales y formatear fechas/divisas correctamente.

*(Captura recomendada: botón “Exportar UBL” en una factura)
*(Otra captura: fragmento del XML generado)
6. Problemas encontrados

Como en todo desarrollo real, nos topamos con obstáculos. Aquí van los más relevantes:

    Caracteres especiales como &, < y > invalidaban el XML. Se solucionó aplicando funciones de escape.

    Algunos validadores requerían campos opcionales como <TaxTotal>. Se añadieron condicionalmente.

    Se implementó un sistema para detectar y evitar la creación de facturas duplicadas.

    La creación automática de proveedores implicó validar por nombre y, si era necesario, crear uno nuevo.

    En cuanto a la seguridad, los problemas con la autenticación inicial de la API se resolvieron usando tokens personalizados.

(Captura sugerida: error de validación UBL y cómo se solucionó)
7. Mejoras futuras

Este sistema es funcional, pero aún tiene margen para crecer. Estas son algunas ideas para versiones futuras:

    Incorporar firma digital (X.509) a los XML generados.

    Validar automáticamente el XML usando esquemas XSD.

    Añadir un panel visual para ver el estado de las facturas enviadas y recibidas.

    Registrar logs detallados por cada paso del proceso.

    Hacer el sistema escalable para múltiples clientes/proveedores, con claves de autenticación por separado.

(Captura recomendada: diseño simulado o mockup del panel de seguimiento)
8. Código fuente comentado
Envío del XML al cliente

    Se usa requests.post() desde el servidor del proveedor.

    Se adjunta el token de autenticación en las cabeceras HTTP.

    El archivo XML se envía como cuerpo de la solicitud.

Recepción e importación del XML

    El endpoint receptor analiza el archivo, lo convierte en cadena, y extrae los datos.

    Si el proveedor no está registrado, se crea automáticamente.

    Si el ID de factura ya existe, se cancela el proceso.

    Finalmente, se genera la factura de compra (Purchase Invoice).

(Captura recomendada: fragmentos clave de código en exportar_ubl.py y purchase_invoice_import.py)
9. Conclusiones

Este proyecto demuestra que es completamente viable automatizar la facturación electrónica entre dos instancias ERP distintas, usando estándares internacionales como UBL y tecnologías abiertas.

Los beneficios son claros:

    Menos errores humanos.

    Mayor eficiencia.

    Comunicación sin barreras técnicas.

    Cumplimiento normativo.

ERPNext y Frappe han respondido de forma flexible y potente, permitiendo desarrollar soluciones a medida con rapidez y estabilidad.

(Captura sugerida: mensaje de éxito tras importar una factura en hospital.localhost)
10. Anexos
Fragmento del XML UBL generado

<Invoice xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2">
  <cbc:ID>INV-0001</cbc:ID>
  <cbc:IssueDate>2025-06-01</cbc:IssueDate>
  <cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
  <cbc:DocumentCurrencyCode>EUR</cbc:DocumentCurrencyCode>
  ...
</Invoice>

Capturas sugeridas

    Factura de venta con botón “Exportar UBL”

    Vista previa del XML generado

    Registro de factura de compra en el sistema receptor

    Interfaz de importación manual

    Diagrama del flujo general

    Código fuente de funciones clave
