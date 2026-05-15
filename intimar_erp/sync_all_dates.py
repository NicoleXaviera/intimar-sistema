import frappe
from intimar_erp.api import sync_fecha_hora_reserva

def run():
    reservas = frappe.get_all("Reserva Intimar")
    for r in reservas:
        doc = frappe.get_doc("Reserva Intimar", r.name)
        sync_fecha_hora_reserva(doc)
        doc.db_update()
    frappe.db.commit()
    print(f"Total procesados: {len(reservas)}")

if __name__ == "__main__":
    run()
