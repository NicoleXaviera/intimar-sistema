import frappe
from frappe.model.document import Document

class ConfiguracionIntimar(Document):
	def on_update(self):
		# Al guardar, comparar el estado anterior y registrar los cambios en la sección de Comentarios/Actividad
		if not self.get_doc_before_save():
			return
			
		before = self.get_doc_before_save()
		changes = []
		
		# Campos a vigilar
		fields_to_track = {
			"anticipo_persona": "Límite de Personas para Anticipo",
			"monto_anticipo_persona": "Monto de Anticipo por Persona",
			"duracion_reserva": "Duración Estimada (Horas)",
			"duracion_reserva_grande": "Duración Grupos >8 (Horas)",
			"margen_limpieza": "Margen de Limpieza (Minutos)",
			"aforo_maximo": "Aforo Máximo (Sillas)",
			"capacidad_cocina_30min": "Capacidad Cocina (Pax por Intervalo)",
			"intervalo_flujo_cocina": "Intervalo de Flujo (Minutos)",
			"hora_minima": "Hora Apertura",
			"hora_maxima": "Hora Cierre",
			"whatsapp_number_id": "WhatsApp Phone Number ID",
			"cierres_especiales": "Cierres Especiales"
		}
		
		for field, label in fields_to_track.items():
			val_before = before.get(field)
			val_after = self.get(field)
			
			# Normalizar valores vacíos/None para evitar falsos positivos
			if val_before is None: val_before = ""
			if val_after is None: val_after = ""
			
			if str(val_before).strip() != str(val_after).strip():
				changes.append(f"• <b>{label}</b>: de '{val_before}' a '{val_after}'")
				
		if changes:
			summary = "<br>".join(changes)
			self.add_comment("Comment", f"<b>Cambios en la Configuración:</b><br>{summary}")

