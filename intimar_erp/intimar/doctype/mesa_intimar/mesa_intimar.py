import frappe
from frappe.model.document import Document

class MesaIntimar(Document):
	def autoname(self):
		# Fetch code if not present (e.g. during first save)
		codigo = self.codigo_ubicacion
		if not codigo and self.ubicacion_mesa:
			codigo = frappe.db.get_value("Ubicacion Mesa Intimar", self.ubicacion_mesa, "codigo_ubicacion")
		
		if not codigo:
			codigo = "INV" # Invalid/Missing
			
		# Format as CODE-M01
		self.name = f"{codigo}-M{int(self.numero_mesa):02d}"
