frappe.ui.form.on('Sales Invoice', {
    refresh: function(frm) {
        if (frappe.boot.sitio_rol == "proveedor" || frappe.boot.sitio_rol == "admin") {
            if (frm.doc.docstatus === 1 && !frm.doc.is_return) {
            frm.add_custom_button(__('Exportar UBL'), function() {
                frappe.call({
                    method: 'proyecto_fin_grado.api.exportar_ubl',
                    args: {
                        sales_invoice_name: frm.doc.name
                    },
                    callback: function(r) {
                        if (r.message) {
                            let blob = new Blob([r.message], { type: 'application/xml' });
                            let url = URL.createObjectURL(blob);
                            let a = document.createElement('a');
                            a.href = url;
                            a.download = frm.doc.name + ".xml";
                            document.body.appendChild(a);
                            a.click();
                            document.body.removeChild(a);
                        }
                    }
                });
            });
            }
        }

        
    }
});
