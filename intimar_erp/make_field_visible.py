import frappe

def run():
    # Buscar el campo personalizado
    custom_field = frappe.get_all("Custom Field", 
        filters={"dt": "Reserva Intimar", "fieldname": "fecha_hora_reserva"},
        limit=1
    )
    
    if custom_field:
        # Hacerlo visible
        frappe.db.set_value("Custom Field", custom_field[0].name, "hidden", 0)
        # Limpiar cache para que aparezca en el UI
        frappe.clear_cache(doctype="Reserva Intimar")
        frappe.db.commit()
        print("Campo 'fecha_hora_reserva' ahora es visible.")
    else:
        print("No se encontró el campo.")

if __name__ == "__main__":
    run()
