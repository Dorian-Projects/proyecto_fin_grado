frappe.listview_settings['Purchase Invoice'] = {
    refresh: function (listview) {
     
        if (frappe.boot.sitio_rol === "cliente" || frappe.boot.sitio_rol === "admin") {
            listview.page.add_inner_button(__('Importar UBL'), function () {
                const dialog = new frappe.ui.Dialog({
                    title: 'Importar Factura UBL',
                    fields: [
                        {
                            label: 'Archivo XML',
                            fieldname: 'archivo_xml',
                            fieldtype: 'Attach',
                            options: 'File',
                            reqd: 1
                        }
                    ],
                    primary_action_label: 'Importar',
                    primary_action(values) {
                        if (!values.archivo_xml) {
                            frappe.msgprint('Por favor, sube un archivo XML.');
                            return;
                        }

                        const full_url = window.location.origin + values.archivo_xml;

                        fetch(full_url)
                            .then(res => {
                                if (!res.ok) throw new Error("No se pudo leer el archivo.");
                                return res.text();
                            })
                            .then(xml_string => {
                                frappe.call({
                                    method: 'proyecto_fin_grado.purchase_invoice_import.importar_ubl_desde_listado',
                                    args: { xml_string },
                                    callback: function(r) {
                                        if (r.message) {
                                            frappe.msgprint(__('Resultado: ') + r.message);
                                            dialog.hide();
                                            listview.refresh();
                                        }
                                    }
                                });
                            })
                            .catch(err => {
                                frappe.msgprint('Error al leer el archivo: ' + err.message);
                            });
                    }
                });

                dialog.show();
            });
        }
    }
};
