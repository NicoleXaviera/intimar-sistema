app_name = "intimar_erp"
app_title = "intimar_erp"
app_publisher = "Intimar"
app_description = "Sistema de gestión y reservas para Intimar"
app_email = "nicole.argueda@gmail.com"
app_license = "mit"
app_version = "1.0.0"

# Includes in <head>
# ------------------
# include js, css files in header of desk.html
# app_include_css = "/assets/intimar_erp/css/intimar_erp.css"
# app_include_js = "/assets/intimar_erp/js/intimar_erp.js"

# Scheduled Tasks
# ---------------
scheduler_events = {
	"all": [
		"intimar_erp.intimar.doctype.reserva_intimar.reserva_intimar.check_occupied_tables_duration"
	],
	"hourly": [
		"intimar_erp.intimar.whatsapp.notify_waitlist_2_hours_before",
		"intimar_erp.api.auto_cancel_expired_reservations"
	],
}

# Document Events
# ---------------
doc_events = {
	"Reserva Intimar": {
		"before_save": "intimar_erp.api.sync_fecha_hora_reserva"
	}
}
# website_route_rules
# -------------------
website_route_rules = [
	{"from_route": "/intimar/<path:app_path>", "to_route": "intimar"},
	{"from_route": "/intimar", "to_route": "intimar"},
]

before_request = "intimar_erp.api.bypass_csrf"
