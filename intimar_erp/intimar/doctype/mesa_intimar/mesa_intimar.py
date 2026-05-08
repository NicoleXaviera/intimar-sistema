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
			
		# Format naming
		num = float(self.numero_mesa or 0)
		num_str = f"{int(num):02d}" if num % 1 == 0 else f"{num}"
		
		# Format as CODE-01 or CODE-6.1
		self.name = f"{codigo}-{num_str}"
