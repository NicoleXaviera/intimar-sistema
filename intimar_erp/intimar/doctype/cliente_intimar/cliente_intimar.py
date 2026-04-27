import frappe
from frappe.model.document import Document

class ClienteIntimar(Document):
    def before_save(self):
        # Concatenar nombre y apellido automáticamente
        nombres = self.name1 or ""
        apellidos = self.lastname or ""
        self.nombre_y_apellido_completo = f"{nombres} {apellidos}".strip()
