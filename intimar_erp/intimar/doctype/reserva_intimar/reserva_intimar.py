import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime, get_time, get_datetime, add_to_date, format_time, get_weekday
from frappe import _

@frappe.whitelist()
def test_realtime_connection():
	"""Envía una notificación de prueba desde el servidor para verificar el cableado."""
	frappe.publish_realtime(
		event="intimar_notification",
		message={
			"type": "nueva_reserva",
			"message": "¡CONEXIÓN REAL ESTABLECIDA! El servidor y el navegador se hablan correctamente.",
			"timestamp": frappe.utils.now()
		}
	)
	return "OK"

class ReservaIntimar(Document):
	def notify_event(self, event_type, message):
		full_message = f"[{self.name}] {message}"
		frappe.publish_realtime(
			event="intimar_notification",
			message={
				"type": event_type,
				"message": full_message,
				"reserva_id": self.name,
				"timestamp": frappe.utils.now()
			},
			after_commit=True
		)

	def validate(self):
		self.validate_past_date()
		self.validate_wednesday()
		self.validate_aforo()
		self.validate_opening_hours()
		self.handle_status_change()
		self.validate_mesas_disponibles()
		self.validate_anticipo()

	def on_update(self):
		self.handle_table_states()
		
		# En on_update usamos frappe.flags para saber si es nuevo
		if self.is_new():
			self.notify_event("nueva_reserva", _("Nueva reserva de {0} para las {1}").format(self.nombre, self.hora_reserva))
		# Notificar cambios de estado o actualizaciones
		frappe.publish_realtime("reserva_actualizada", {
			"reserva": self.name,
			"cliente": self.cliente,
			"estado": self.estado_reserva
		}, user=frappe.session.user)

	def after_insert(self):
		self.handle_table_states()
		# Notificar nueva reserva
		frappe.publish_realtime("nueva_reserva", {
			"reserva": self.name,
			"cliente": self.cliente,
			"fecha": self.fecha_reserva,
			"hora": self.hora_reserva
		})

	def validate_past_date(self):
		if self.is_new():
			res_datetime = get_datetime(f"{self.fecha_reserva} {self.hora_reserva}")
			if res_datetime < now_datetime():
				frappe.throw(_("La fecha y hora de reserva deben ser posteriores a la actual."))

	def validate_wednesday(self):
		# En Python/Frappe, get_weekday() retorna 0 para Lunes, ..., 2 para Miércoles
		# Pero ojo, depende de la configuración. Usualmente 0=Lunes.
		# Mejor usar el nombre o verificar el índice.
		date_obj = get_datetime(self.fecha_reserva)
		if date_obj.weekday() == 2: # 2 es Miércoles (0=Lunes)
			frappe.throw(_("Los miércoles no hay atención. Por favor, seleccione otra fecha."))

	def validate_anticipo(self):
		config = frappe.get_doc("Configuracion Intimar")
		total_personas = (self.cant_adultos or 0) + (self.cant_ninos or 0)
		
		if config.anticipo_persona and total_personas >= config.anticipo_persona:
			self.anticipo_required = 1
			# Si es requerido pero no hay registros en la tabla de anticipos
			if not self.anticipos:
				frappe.msgprint(_("Atención: Esta reserva tiene {0} personas y requiere un anticipo (Mínimo: {1} personas). No se han registrado pagos aún.").format(
					total_personas, config.anticipo_persona), indicator='orange')
		else:
			self.anticipo_required = 0

	def validate_mesas_disponibles(self):
		"""Valida que las mesas asignadas no estén ocupadas por otras reservas en el mismo horario."""
		if not self.mesas:
			return

		config = frappe.get_doc("Configuracion Intimar")
		duracion = config.duracion_reserva or 2
		res_datetime = get_datetime(f"{self.fecha_reserva} {self.hora_reserva}")
		hora_min = add_to_date(res_datetime, hours=-duracion).time()
		hora_max = add_to_date(res_datetime, hours=duracion).time()

		for item in self.mesas:
			if not item.mesa: continue
			
			# Buscar otras reservas que tengan esta misma mesa en el mismo horario
			conflictos = frappe.db.sql("""
				SELECT parent 
				FROM `tabMesa Reserva Intimar` mr
				JOIN `tabReserva Intimar` r ON mr.parent = r.name
				WHERE mr.mesa = %s 
				AND r.fecha_reserva = %s
				AND r.hora_reserva > %s AND r.hora_reserva < %s
				AND r.name != %s
				AND r.estado_reserva NOT IN ('Cancelada', 'Finalizada')
			""", (item.mesa, self.fecha_reserva, hora_min, hora_max, self.name or ""), as_dict=1)

			if conflictos:
				frappe.throw(_("La mesa {0} ya está asignada a la reserva {1} en este horario.").format(
					item.mesa, conflictos[0].parent))

	def validate_opening_hours(self):
		config = frappe.get_doc("Configuracion Intimar")
		if not config.hora_minima or not config.hora_maxima:
			return
		
		if self.hora_reserva:
			res_time = get_time(self.hora_reserva)
			if res_time < get_time(config.hora_minima) or res_time > get_time(config.hora_maxima):
				frappe.throw(_("La hora de reserva debe estar entre {0} y {1}").format(
					config.hora_minima, config.hora_maxima))

	def validate_aforo(self):
		# Si la reserva está cancelada, finalizada o en lista de espera, no bloqueamos ni validamos aforo para ella
		if self.estado_reserva in ["Cancelada", "Finalizada", "Lista de espera"]:
			return

		config = frappe.get_doc("Configuracion Intimar")
		if not config.aforo_maximo:
			return
		
		# Duración en horas
		duracion = config.duracion_reserva or 2
		
		res_datetime = get_datetime(f"{self.fecha_reserva} {self.hora_reserva}")
		hora_min = add_to_date(res_datetime, hours=-duracion).time()
		hora_max = add_to_date(res_datetime, hours=duracion).time()
		
		# Buscar reservas que se solapan en esa fecha
		filters = [
			["Reserva Intimar", "fecha_reserva", "=", self.fecha_reserva],
			["Reserva Intimar", "hora_reserva", ">", hora_min],
			["Reserva Intimar", "hora_reserva", "<", hora_max],
			["Reserva Intimar", "estado_reserva", "in", ["Confirmada", "En proceso", "Solicitud de reserva"]]
		]
		
		if self.name:
			filters.append(["Reserva Intimar", "name", "!=", self.name])

		reservas_solapadas = frappe.get_all("Reserva Intimar", filters=filters, fields=["cant_adultos", "cant_ninos"])
		aforo_ocupado = sum((r.cant_adultos or 0) + (r.cant_ninos or 0) for r in reservas_solapadas)
		personas_nuevas = (self.cant_adultos or 0) + (self.cant_ninos or 0)
		total_proyectado = aforo_ocupado + personas_nuevas
		
		# Solo bloqueamos si estamos intentando CONFIRMAR algo nuevo o que estaba en espera
		# Si la reserva ya existe, permitimos cambios (como asignar mesa) sin importar el aforo total
		if not self.is_new():
			old_doc = self.get_doc_before_save()
			if old_doc and old_doc.estado_reserva in ["Confirmada", "En proceso", "Solicitud de reserva", "Pendiente a confirmar"]:
				# Si ya existía, permitimos el cambio siempre que no aumenten personas
				old_personas = (old_doc.cant_adultos or 0) + (old_doc.cant_ninos or 0)
				if personas_nuevas <= old_personas:
					return 

		if total_proyectado > config.aforo_maximo:
			if self.aceptar_lista_espera:
				self.estado_reserva = "Lista de espera"
				self.notify_event("aforo_lleno", _("Aforo lleno. Reserva de {0} enviada a Lista de Espera.").format(self.nombre))
			else:
				exceso = total_proyectado - config.aforo_maximo
				msg = _("Aforo excedido. Faltan {0} lugares.").format(exceso)
				self.notify_event("aforo_lleno", msg)
				frappe.throw(msg)
		
		# Alerta de aforo al 90%
		if total_proyectado >= config.aforo_maximo * 0.9 and self.estado_reserva != "Lista de espera":
			porcentaje = int((total_proyectado / config.aforo_maximo) * 100)
			self.notify_event("aforo_limite", _("¡Atención! El aforo está al {0}% para las {1}").format(porcentaje, self.hora_reserva))

	def handle_status_change(self):
		if not self.name: return # Solo para documentos existentes
		
		# En validate, self.get_doc_before_save() nos da el estado anterior
		old_doc = self.get_doc_before_save()
		if not old_doc: return
		
		if old_doc.estado_reserva != self.estado_reserva:
			now = now_datetime()
			if self.estado_reserva == "En proceso":
				if not self.hora_llegada:
					self.hora_llegada = now.strftime("%H:%M:%S")
					self.am_pm = now.strftime("%p")
					self.notify_event("cliente_llego", _("El cliente {0} ha llegado al restaurante").format(self.nombre))
			elif self.estado_reserva == "Finalizada":
				if not self.hora_salida:
					self.hora_salida = now.strftime("%H:%M:%S")
					self.notify_event("mesa_liberada", _("Mesa liberada por {0}").format(self.nombre))

	def handle_table_states(self):
		"""Marca las mesas como ocupadas o disponibles según el estado de la reserva."""
		if not self.mesas:
			return

		# Si la reserva está en proceso, las mesas no están disponibles
		# Si está finalizada o cancelada, se liberan
		disponible = 1
		if self.estado_reserva == "En proceso":
			disponible = 0
		elif self.estado_reserva in ["Finalizada", "Cancelada"]:
			disponible = 1
		else:
			return

		for item in self.mesas:
			if item.mesa:
				frappe.db.set_value("Mesa Intimar", item.mesa, "estado_mesa", disponible)
		
		frappe.db.commit()

		# LOGICA DE LISTA DE ESPERA:
		# Si liberamos mesas, avisamos si hay alguien esperando
		if disponible == 1:
			self.check_waitlist_and_notify()

	def check_waitlist_and_notify(self):
		"""Busca si hay personas en lista de espera que podrían ocupar el lugar liberado."""
		config = frappe.get_doc("Configuracion Intimar")
		
		# Buscamos reservas en lista de espera para HOY y que se solapen con la hora actual
		now = now_datetime()
		hora_actual = now.time()
		
		esperando = frappe.get_all("Reserva Intimar", filters={
			"fecha_reserva": self.fecha_reserva,
			"estado_reserva": "Lista de espera",
			"name": ["!=", self.name]
		}, fields=["name", "cliente", "nombre", "cant_adultos", "cant_ninos", "hora_reserva"])

		if esperando:
			# Notificar al personal por tiempo real (Socket.io)
			total_esperando = len(esperando)
			proxima = esperando[0] # El primero que llegó
			
			msg = _("¡Mesa Liberada! Hay {0} reservas en lista de espera. La próxima es de {1} ({2} pers.)").format(
				total_esperando, proxima.nombre or proxima.cliente, (proxima.cant_adultos or 0) + (proxima.cant_ninos or 0)
			)
			
			frappe.publish_realtime("mesa_disponible_espera", {
				"message": msg,
				"reserva_espera": proxima.name,
				"total_esperando": total_esperando
			})
			
			# También podemos dejar un mensaje en el sistema
			frappe.msgprint(msg, indicator='green', alert=True)
@frappe.whitelist()
def check_occupied_tables_duration():
	"""Busca mesas que llevan más de el tiempo permitido 'En proceso' y notifica."""
	from frappe.utils import now_datetime
	import datetime

	config = frappe.get_doc("Configuracion Intimar")
	max_hours = config.duracion_reserva or 2
	
	now = now_datetime()
	today = now.date()
	
	# Reservas actualmente en proceso
	occupied = frappe.get_all("Reserva Intimar", filters={
		"estado_reserva": "En proceso",
		"fecha_reserva": today,
		"hora_llegada": ["is", "set"]
	}, fields=["name", "nombre", "hora_llegada"])
	
	for res in occupied:
		try:
			# Convertir hora_llegada string a objeto time para comparar
			h, m, s = map(int, res.hora_llegada.split(':'))
			llegada_dt = datetime.datetime.combine(today, datetime.time(h, m, s))
			
			diff = (now - llegada_dt).total_seconds() / 3600
			
			if diff >= max_hours:
				msg = _("La mesa de {0} ya cumplió {1} horas. ¿Desea finalizar la reserva?").format(
					res.nombre, round(diff, 1)
				)
				
				frappe.publish_realtime("tiempo_excedido_mesa", {
					"message": msg,
					"reserva_id": res.name,
					"nombre": res.nombre,
					"horas": round(diff, 1)
				})
		except Exception as e:
			frappe.log_error(f"Error en check_occupied_tables_duration: {str(e)}")
