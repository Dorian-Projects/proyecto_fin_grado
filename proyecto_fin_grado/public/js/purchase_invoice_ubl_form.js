frappe.listview_settings['Purchase Invoice'] = {
    onload: function (listview) {
        listview.page.add_inner_button(__('Importar UBL'), function () {
            const dialog = new frappe.ui.Dialog({
                title: 'Importar Factura UBL',
                fields: [
                    {
                        label: 'Contenido XML',
                        fieldname: 'xml_content',
                        fieldtype: 'Text',
                        reqd: 1
                    }
                ],
                primary_action_label: 'Importar',
                primary_action(values) {
                    frappe.call({
                        method: 'proyecto_fin_grado.purchase_invoice_import.importar_ubl_desde_listado',
                        args: {
                            xml_string: values.xml_content
                        },
                        callback: function (r) {
                            if (r.message) {
                                frappe.msgprint(__('Resultado: ') + r.message);
                                dialog.hide();
                                listview.refresh();
                            }
                        }
                    });
                }
            });
            dialog.show();
        });
    }
};
