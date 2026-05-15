import frappe

def run():
    fields = [
        {"fieldname": "fecha_hora_reserva", "label": "Fecha y Hora Combinada", "fieldtype": "Datetime"},
        {"fieldname": "reminder_sent", "label": "Recordatorio Enviado", "fieldtype": "Check"}
    ]
    
    for f in fields:
        if not frappe.db.exists("Custom Field", {"dt": "Reserva Intimar", "fieldname": f["fieldname"]}):
            cf = frappe.new_doc("Custom Field")
            cf.dt = "Reserva Intimar"
            cf.fieldname = f["fieldname"]
            cf.label = f["label"]
            cf.fieldtype = f["fieldtype"]
            cf.insert(ignore_permissions=True)
            print(f"Campo {f['fieldname']} creado.")
        else:
            print(f"Campo {f['fieldname']} ya existía.")
            
    frappe.db.commit()
    frappe.clear_cache(doctype="Reserva Intimar")

if __name__ == "__main__":
    run()
