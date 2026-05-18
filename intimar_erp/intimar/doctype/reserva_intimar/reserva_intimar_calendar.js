frappe.views.calendar["Reserva Intimar"] = {
	field_map: {
		start: "fecha_reserva",
		end: "fecha_reserva",
		id: "name",
		allDay: "allDay",
		title: "cliente",
		status: "estado_reserva",
	},
	style_map: {
		"Solicitud de reserva": "warning",
		"Pendiente a confirmar": "warning",
		"Confirmada": "info",
		"En proceso": "primary",
		"Finalizada": "success",
		"Cancelada": "danger",
		"Atrasada": "danger",
		"Lista de espera": "orange",
	},
	order_by: "hora_reserva",
	get_events_method: "frappe.desk.calendar.get_events",
};
