import frappe

def add_rol_to_boot(bootinfo):
    bootinfo.sitio_rol = frappe.get_conf().get("sitio_rol", "desconocido")
