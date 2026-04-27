import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime, get_time

class ReservaIntimar(Document):
	def validate(self):
		self.validate_opening_hours()
		self.validate_aforo()
		self.validate_anticipo()
		self.handle_status_change()

	def on_update(self):
		# Notificar cambios de estado o actualizaciones
		frappe.publish_realtime("reserva_actualizada", {
			"reserva": self.name,
			"cliente": self.cliente,
			"estado": self.estado_reserva
		}, user=frappe.session.user)

	def after_insert(self):
		# Notificar nueva reserva
		frappe.publish_realtime("nueva_reserva", {
			"reserva": self.name,
			"cliente": self.cliente,
			"fecha": self.fecha_reserva,
			"hora": self.hora_reserva
		})

	def validate_anticipo(self):
		config = frappe.get_doc("Configuracion Intimar")
		total_personas = (self.cant_adultos or 0) + (self.cant_ninos or 0)
		
		if config.anticipo_persona and total_personas >= config.anticipo_persona:
			self.anticipo_required = 1
		else:
			self.anticipo_required = 0

	def validate_opening_hours(self):
		config = frappe.get_doc("Configuracion Intimar")
		if not config.hora_minima or not config.hora_maxima:
			return
		
		if self.hora_reserva:
			res_time = get_time(self.hora_reserva)
			if res_time < get_time(config.hora_minima) or res_time > get_time(config.hora_maxima):
				frappe.throw(f"La hora de reserva debe estar entre {config.hora_minima} y {config.hora_maxima}")

	def validate_aforo(self):
		config = frappe.get_doc("Configuracion Intimar")
		if not config.aforo_maximo:
			return
			
		reservas_hoy = frappe.get_all("Reserva Intimar", filters={
			"fecha_reserva": self.fecha_reserva,
			"name": ["!=", self.name],
			"estado_reserva": ["!=", "Cancelada"]
		}, fields=["cant_adultos", "cant_ninos"])
		
		total_hoy = sum((r.cant_adultos or 0) + (r.cant_ninos or 0) for r in reservas_hoy)
		total_hoy += (self.cant_adultos or 0) + (self.cant_ninos or 0)
		
		if total_hoy > config.aforo_maximo:
			frappe.msgprint(f"Advertencia: Se ha superado el aforo m\u00e1ximo de {config.aforo_maximo} personas.")

	def handle_status_change(self):
		if not self.name: return # Solo para documentos existentes
		
		old_doc = self.get_doc_before_save()
		if not old_doc: return
		
		if old_doc.estado_reserva != self.estado_reserva:
			now = now_datetime()
			if self.estado_reserva == "En proceso":
				self.hora_llegada = now.strftime("%H:%M:%S")
				self.am_pm = now.strftime("%p")
			elif self.estado_reserva == "Finalizada":
				self.hora_salida = now.strftime("%H:%M:%S")
