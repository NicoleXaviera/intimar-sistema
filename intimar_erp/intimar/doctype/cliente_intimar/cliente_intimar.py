import frappe
from frappe.model.document import Document

class ClienteIntimar(Document):
    def before_save(self):
        # Concatenar nombre y apellido automáticamente
        nombres = self.name1 or ""
        apellidos = self.lastname or ""
        self.nombre_y_apellido_completo = f"{nombres} {apellidos}".strip()

    def validate(self):
        if self.phone:
            # Limpiar teléfono para consistencia
            import re
            self.phone = re.sub(r"[^\d+]", "", self.phone)
            
            # Buscar si ya existe otro cliente con el mismo teléfono
            duplicate = frappe.db.get_value("Cliente Intimar", 
                {"phone": self.phone, "name": ["!=", self.name]}, "name")
            
            if duplicate:
                frappe.throw(f"No se puede registrar: el número {self.phone} ya pertenece a otro cliente.")
