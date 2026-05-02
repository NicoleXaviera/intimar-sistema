import frappe
import requests
import json
from frappe import _

def send_whatsapp_message(reserva_name, template_name="info_reserva"):
    """
    Envía un mensaje de WhatsApp utilizando la API de Meta (Cloud API).
    """
    reserva = frappe.get_doc("Reserva Intimar", reserva_name)
    config = frappe.get_doc("Configuracion Intimar")

    if not config.whatsapp_token or not config.whatsapp_number_id:
        frappe.log_error("Configuración de WhatsApp incompleta", "WhatsApp Error")
        return False

    token = config.get_password("whatsapp_token")
    number_id = config.whatsapp_number_id
    
    # Obtener el teléfono del cliente
    cliente = frappe.get_doc("Cliente Intimar", reserva.cliente)
    phone = cliente.phone
    if not phone:
        return False
    
    # Limpiar el número (asumimos código de país ya incluido o lo agregamos)
    # En el back anterior usaban client.countryCode + client.cellphone
    clean_phone = "".join(filter(str.isdigit, phone))
    
    # URL de la API de Meta v21.0
    url = f"https://graph.facebook.com/v21.0/{number_id}/messages"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # Parámetros del template (basado en whatsapp.helpers.js del backend anterior)
    # info_reserva esperaba: [Nombre, ID, Fecha, Hora, Adultos, Niños, Estado, Motivo]
    params = [
        {"type": "text", "text": str(cliente.name1 or "Cliente")},
        {"type": "text", "text": str(reserva.name)},
        {"type": "text", "text": str(reserva.fecha_reserva)},
        {"type": "text", "text": str(reserva.hora_reserva)},
        {"type": "text", "text": str(reserva.cant_adultos)},
        {"type": "text", "text": str(reserva.cant_ninos)},
        {"type": "text", "text": str(reserva.estado_reserva)},
        {"type": "text", "text": str(reserva.motivo_reserva or "-")}
    ]

    payload = {
        "messaging_product": "whatsapp",
        "to": clean_phone,
        "type": "template",
        "template": {
            "name": template_name,
            "language": {
                "code": "es"
            },
            "components": [
                {
                    "type": "body",
                    "parameters": params
                }
            ]
        }
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=10)
        response.raise_for_status()
        return True
    except Exception as e:
        frappe.log_error(f"Error enviando WhatsApp a {clean_phone}: {str(e)}", "WhatsApp API Error")
        return False

def notify_waitlist_2_hours_before():
    """
    Busca reservas en 'Lista de espera' que sean para hoy y falten 2-3 horas.
    """
    from frappe.utils import now_datetime, add_to_date, get_time
    
    now = now_datetime()
    today = now.date()
    
    # Rango de 2 a 3 horas desde ahora
    time_min = add_to_date(now, hours=2).time()
    time_max = add_to_date(now, hours=3).time()

    waiting = frappe.get_all("Reserva Intimar", filters={
        "fecha_reserva": today,
        "estado_reserva": "Lista de espera",
        "hora_reserva": ["between", [time_min, time_max]],
        "notificado_espera": 0
    }, fields=["name"])

    for w in waiting:
        if send_whatsapp_message(w.name, "info_reserva"):
            frappe.db.set_value("Reserva Intimar", w.name, "notificado_espera", 1)
            frappe.db.commit()
