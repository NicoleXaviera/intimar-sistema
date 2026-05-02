import frappe
from frappe import _
import json
import re

def clean_phone(phone):
    if not phone: return ""
    # Remove everything except + and digits
    return re.sub(r"[^\d+]", "", phone)

@frappe.whitelist()
def get_mesas_with_reserva(limit_start=0, limit_page_length=0, with_pagination=0, search_query="", ubicacion_mesa=""):
    kwargs = {
        "fields": ["name", "numero_mesa", "ubicacion_mesa", "estado_mesa"],
        "order_by": "numero_mesa asc",
        "filters": {}
    }
    
    if ubicacion_mesa:
        kwargs["filters"]["ubicacion_mesa"] = ubicacion_mesa
        
    if search_query:
        kwargs["or_filters"] = [
            ["name", "like", f"%{search_query}%"],
            ["numero_mesa", "like", f"%{search_query}%"]
        ]
        
    if int(limit_page_length) > 0:
        kwargs["limit_start"] = int(limit_start)
        kwargs["limit_page_length"] = int(limit_page_length)

    mesas = frappe.get_all("Mesa Intimar", **kwargs)
    
    for mesa in mesas:
        if not mesa.estado_mesa: 
            reserva_parent = frappe.db.get_value("Mesa Reserva Intimar", 
                {"mesa": mesa.name, "parenttype": "Reserva Intimar"}, "parent")
            
            if reserva_parent:
                res = frappe.get_doc("Reserva Intimar", reserva_parent)
                if res.estado_reserva not in ["Finalizada", "Cancelada"]:
                    cliente = frappe.get_value("Cliente Intimar", res.cliente, ["nombre_y_apellido_completo", "phone"], as_dict=1)
                    mozo_nombre = frappe.db.get_value("Mozo Intimar", res.mozo, "nombre") or "Sin Mozo"
                    
                    mesa.reserva = {
                        "name": res.name,
                        "cliente_nombre": cliente.nombre_y_apellido_completo if cliente and cliente.nombre_y_apellido_completo else "Cliente sin nombre",
                        "cliente_telefono": (cliente.phone or "") if cliente else "",
                        "hora_llegada": res.hora_llegada,
                        "mozo_nombre": mozo_nombre,
                        "cant_adultos": res.cant_adultos,
                        "cant_ninos": res.cant_ninos
                    }
                else:
                    mesa.reserva = None
            else:
                mesa.reserva = None
                
    if int(with_pagination) == 1:
        count_kwargs = {}
        if kwargs.get("filters"): count_kwargs["filters"] = kwargs["filters"]
        if kwargs.get("or_filters"): count_kwargs["or_filters"] = kwargs["or_filters"]
        
        # We use frappe.get_all with count instead of db.count to support or_filters
        total_count = frappe.get_all("Mesa Intimar", **count_kwargs, limit=1, as_list=True)
        # Wait, get_all without fields returns a list of dicts.
        total_list = frappe.get_all("Mesa Intimar", **count_kwargs)
        total_count = len(total_list)
        return {"data": mesas, "total_count": total_count}
        
    return mesas

@frappe.whitelist()
def get_reservas_pendientes_hoy():
    reservas = frappe.get_all("Reserva Intimar",
        filters={
            "estado_reserva": ["in", ["Confirmada", "Pendiente a confirmar", "Solicitud de reserva", "Lista de espera"]],
            "fecha_reserva": frappe.utils.today()
        },
        fields=["name", "cliente", "hora_reserva", "cant_adultos", "cant_ninos", "mozo"],
        order_by="hora_reserva asc"
    )
    
    for r in reservas:
        cliente = frappe.get_value("Cliente Intimar", r.cliente, ["nombre_y_apellido_completo", "phone"], as_dict=1)
        if cliente:
            r.cliente_nombre = cliente.nombre_y_apellido_completo or "Cliente sin nombre"
            r.cliente_telefono = cliente.phone or ""
        else:
            r.cliente_nombre = "Cliente sin nombre"
            r.cliente_telefono = ""
    return reservas

@frappe.whitelist()
def get_mozos():
    return frappe.get_all("Mozo Intimar", fields=["name", "nombre", "apellido"])

@frappe.whitelist()
def asignar_mesa_a_reserva(reserva_id, mesa_id, mozo_id=None):
    frappe.db.set_value("Mesa Intimar", mesa_id, "estado_mesa", 0)
    reserva = frappe.get_doc("Reserva Intimar", reserva_id)
    
    if not any(m.mesa == mesa_id for m in reserva.mesas):
        reserva.append("mesas", {"mesa": mesa_id})
    
    reserva.estado_reserva = "En proceso"
    reserva.hora_llegada = frappe.utils.nowtime()
    if mozo_id:
        reserva.mozo = mozo_id
        
    reserva.save(ignore_permissions=True)
    frappe.db.commit()
    return {"status": "success"}

@frappe.whitelist()
def liberar_mesa(mesa_id):
    reserva_parent = frappe.db.get_value("Mesa Reserva Intimar", {"mesa": mesa_id}, "parent")
    if reserva_parent:
        res = frappe.get_doc("Reserva Intimar", reserva_parent)
        res.estado_reserva = "Finalizada"
        res.hora_salida = frappe.utils.nowtime()
        res.save(ignore_permissions=True)
    
    frappe.db.set_value("Mesa Intimar", mesa_id, "estado_mesa", 1)
    frappe.db.commit()
    return {"status": "success"}

@frappe.whitelist()
def get_reservas_list(filters=None, limit_start=0, limit_page_length=20, order_by="creation desc"):
    if isinstance(filters, str):
        import json
        filters = json.loads(filters)
        
    # Primero obtenemos los nombres que cumplen los filtros para manejar la paginación correctamente
    reserva_names = frappe.get_all("Reserva Intimar", 
        filters=filters, 
        limit_start=limit_start, 
        limit_page_length=limit_page_length, 
        order_by=order_by,
        pluck="name"
    )
    
    if not reserva_names:
        return []
        
    # Ahora obtenemos los detalles incluyendo el total pagado
    query = f"""
        SELECT 
            r.name, r.cliente, r.nombre, r.celular, r.fecha_reserva, r.hora_reserva, 
            r.cant_adultos, r.cant_ninos, r.estado_reserva, r.anticipo_required, 
            r.mozo, r.hora_llegada, r.hora_salida, r.am_pm,
            (SELECT SUM(monto_anticipo) 
             FROM `tabAnticipo Reserva Intimar` 
             WHERE parent = r.name AND estado_anticipo = 'Pagado') as total_pagado
        FROM 
            `tabReserva Intimar` r
        WHERE 
            r.name IN ({', '.join(['%s'] * len(reserva_names))})
        ORDER BY 
            {order_by}
    """
    
    data = frappe.db.sql(query, tuple(reserva_names), as_dict=1)
    
    return data



@frappe.whitelist(allow_guest=True)
def crear_reserva_publica(cliente_nombre, cliente_celular, fecha, hora, adultos, ninos=0, 
                          email=None, dni=None, alergias=None, ocasion=None, 
                          requerimientos=None, necesidades=None, apellido=None, 
                          codigo_pais=None, acepta_politicas=0, acepta_promociones=0,
                          aceptar_lista_espera=0):
    
    # 1. Buscar o crear cliente
    # Limpiamos el celular para consistencia
    cliente_celular = clean_phone(cliente_celular)
    
    # Usamos el celular como identificador único
    cliente_id = frappe.db.get_value('Cliente Intimar', {'phone': cliente_celular}, 'name')
    
    if not cliente_id:
        nuevo_cliente = frappe.get_doc({
            'doctype': 'Cliente Intimar',
            'name1': cliente_nombre,
            'lastname': apellido,
            'nombre_y_apellido_completo': f"{cliente_nombre} {apellido if apellido else ''}".strip(),
            'phone': cliente_celular,
            'email': email,
            'dni_ruc': dni
        })
        nuevo_cliente.insert(ignore_permissions=True)
        cliente_id = nuevo_cliente.name
    
    # 2. Crear la reserva
    reserva = frappe.get_doc({
        'doctype': 'Reserva Intimar',
        'cliente': cliente_id,
        'nombre': cliente_nombre,
        'apellido': apellido,
        'celular': cliente_celular,
        'codigo_pais': codigo_pais,
        'email': email,
        'dni': dni,
        'fecha_reserva': fecha,
        'hora_reserva': hora,
        'cant_adultos': adultos,
        'cant_ninos': ninos,
        'motivo_reserva': ocasion,
        'requerimientos': requerimientos,
        'necesidades': necesidades,
        'alergias': alergias,
        'acepta_politicas': acepta_politicas,
        'acepta_promociones': acepta_promociones,
        'aceptar_lista_espera': aceptar_lista_espera,
        'estado_reserva': 'Solicitud de reserva'
    })
    
    try:
        reserva.insert(ignore_permissions=True)
        return {
            'status': 'success',
            'reserva_name': reserva.name
        }
    except frappe.ValidationError as e:
        msg = str(e).split(':', 1)[-1].strip() if ':' in str(e) else str(e)
        return {
            'status': 'error',
            'message': msg
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error en crear_reserva_publica")
        return {
            'status': 'error',
            'message': 'Ocurrió un error inesperado al procesar su reserva.'
        }


@frappe.whitelist()
def get_user_details(user_id):
    # Verificación de permisos básica: solo System Manager o el propio usuario
    if "System Manager" not in frappe.get_roles() and frappe.session.user != "Administrator" and frappe.session.user != user_id:
        frappe.throw(_("No tienes permiso para ver los detalles de este usuario"))
        
    doc = frappe.get_doc("User", user_id)
    roles = [r.role for r in doc.roles]
    
    return {
        "name": doc.name,
        "email": doc.email,
        "full_name": doc.full_name,
        "user_image": doc.user_image,
        "enabled": doc.enabled,
        "last_login": doc.last_login,
        "creation": doc.creation,
        "roles": roles
    }

@frappe.whitelist()
def update_user_details(user_id, full_name=None, enabled=None, roles=None, password=None):
    if "System Manager" not in frappe.get_roles() and frappe.session.user != "Administrator":
        frappe.throw(_("No tienes permiso para editar usuarios"))
        
    doc = frappe.get_doc("User", user_id)
    
    if full_name is not None:
        doc.first_name = full_name
        doc.last_name = ""
        
    if enabled is not None:
        doc.enabled = int(enabled)
        
    if password:
        from frappe.utils.password import update_password
        update_password(user_id, password)
        
    if roles is not None:
        if isinstance(roles, str):
            import json
            roles = json.loads(roles)
            
        doc.set("roles", [])
        for role in roles:
            doc.append("roles", {"role": role})
            
    doc.save(ignore_permissions=True)
    frappe.db.commit()
    return {"status": "success"}

@frappe.whitelist()
def create_new_user(email, full_name, password, roles=None):
    if "System Manager" not in frappe.get_roles() and frappe.session.user != "Administrator":
        frappe.throw(_("No tienes permiso para crear usuarios"))
        
    doc = frappe.get_new_doc("User")
    doc.email = email
    doc.first_name = full_name
    doc.enabled = 1
    doc.send_welcome_email = 0
    
    if roles:
        if isinstance(roles, str):
            import json
            roles = json.loads(roles)
        for role in roles:
            doc.append("roles", {"role": role})
            
    doc.insert(ignore_permissions=True)
    
    from frappe.utils.password import update_password
    update_password(email, password)
    
    frappe.db.commit()
    return {"status": "success"}

@frappe.whitelist()
def get_dashboard_stats(start_date=None, end_date=None):
    if "System Manager" not in frappe.get_roles() and frappe.session.user != "Administrator":
        frappe.throw(_("No tienes permiso para ver las estadísticas"))
    
    if not start_date:
        start_date = frappe.utils.today()
    if not end_date:
        end_date = start_date
        
    # Todas las reservas en el rango
    reservas = frappe.get_all("Reserva Intimar", 
        filters={
            "fecha_reserva": ["between", [start_date, end_date]]
        },
        fields=["estado_reserva", "cant_adultos", "cant_ninos", "name", "fecha_reserva", "hora_reserva"]
    )
    
    # 1. Personas en el restaurante (Solo si el rango incluye HOY)
    today = frappe.utils.today()
    personas_en_restaurante = 0
    if start_date <= today <= end_date:
        en_proceso = [r for r in reservas if r.estado_reserva == 'En proceso' and str(r.fecha_reserva) == today]
        personas_en_restaurante = sum([r.cant_adultos + r.cant_ninos for r in en_proceso])
    
    # 2. Reservas CONFIRMADAS
    confirmadas = [r for r in reservas if r.estado_reserva == 'Confirmada']
    count_confirmadas = len(confirmadas)
    
    # 3. Total Comensales (Confirmadas)
    comensales_confirmados = sum([r.cant_adultos + r.cant_ninos for r in confirmadas])
    
    # 4. Total Anticipos Pagados (En el rango)
    anticipos_query = """
        SELECT SUM(monto_anticipo) as total
        FROM `tabAnticipo Reserva Intimar`
        WHERE estado_anticipo = 'Pagado'
        AND creation BETWEEN %s AND %s
    """
    total_anticipos = frappe.db.sql(anticipos_query, (start_date + " 00:00:00", end_date + " 23:59:59"), as_dict=1)[0].total or 0
    
    # Rankings de Mozos
    mozos_query = """
        SELECT m.nombre as mozo, COUNT(r.name) as total
        FROM `tabReserva Intimar` r
        JOIN `tabMozo Intimar` m ON r.mozo = m.name
        WHERE r.estado_reserva != 'Cancelada'
        AND r.fecha_reserva BETWEEN %s AND %s
        GROUP BY r.mozo
        ORDER BY total DESC
        LIMIT 5
    """
    mozos_ranking = frappe.db.sql(mozos_query, (start_date, end_date), as_dict=1)
    
    # Ocupación por Hora
    hourly_query = """
        SELECT hora_reserva, COUNT(name) as total
        FROM `tabReserva Intimar`
        WHERE fecha_reserva BETWEEN %s AND %s
        GROUP BY hora_reserva
        ORDER BY hora_reserva ASC
    """
    ocupacion_horas = frappe.db.sql(hourly_query, (start_date, end_date), as_dict=1)
    
    # Desglose de estados
    status_counts = {}
    for r in reservas:
        status = r.estado_reserva or "Sin Estado"
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # KPIs adicionales para tiempo real
    aforo_maximo = frappe.db.get_single_value("Configuracion Intimar", "aforo_maximo") or 0
    mesas_disponibles = frappe.db.count("Mesa Intimar", {"estado_mesa": 1})
    
    en_espera = [r for r in reservas if r.estado_reserva == 'Lista de espera']
    personas_en_espera = sum([r.cant_adultos + r.cant_ninos for r in en_espera])
    
    reservas_en_proceso = len([r for r in reservas if r.estado_reserva == 'En proceso'])

    return {
        "kpis": {
            "personas_en_restaurante": personas_en_restaurante,
            "reservas_confirmadas": count_confirmadas,
            "comensales_confirmados": comensales_confirmados,
            "total_reservas": len(reservas),
            "aforo_total": aforo_maximo,
            "mesas_disponibles": mesas_disponibles,
            "personas_en_espera": personas_en_espera,
            "reservas_en_espera": len(en_espera),
            "reservas_en_proceso": reservas_en_proceso
        },
        "financials": {
            "total_anticipos": total_anticipos
        },
        "rankings": {
            "mozos": mozos_ranking
        },
        "hourly": ocupacion_horas,
        "status_counts": status_counts,
        "raw_data": reservas # Para la descarga
    }

@frappe.whitelist()
def get_recent_activity():
    """Devuelve las últimas 10 actividades significativas para el Centro de Control."""
    reservas = frappe.get_all("Reserva Intimar", 
        fields=["name", "nombre", "estado_reserva", "modified", "hora_reserva"],
        order_by="modified desc",
        limit=10
    )
    
    activities = []
    for r in reservas:
        msg = ""
        msg_type = "nueva_reserva"
        prefix = f"[{r.name}] "
        
        if r.estado_reserva == "En proceso":
            msg = prefix + _("El cliente {0} ya llegó.").format(r.nombre)
            msg_type = "cliente_llego"
        elif r.estado_reserva == "Solicitud de reserva":
            msg = prefix + _("Nueva solicitud de {0} para las {1}.").format(r.nombre, r.hora_reserva)
        elif r.estado_reserva == "Confirmada":
            msg = prefix + _("Reserva de {0} confirmada para las {1}.").format(r.nombre, r.hora_reserva)
        elif r.estado_reserva == "Lista de espera":
            msg = prefix + _("Aforo completo: {0} en lista de espera.").format(r.nombre)
            msg_type = "aforo_lleno"
        elif r.estado_reserva == "Finalizada":
            msg = prefix + _("Mesa liberada de {0}.").format(r.nombre)
            msg_type = "mesa_liberada"
        
        if msg:
            activities.append({
                "type": msg_type,
                "message": msg,
                "timestamp": r.modified,
                "reserva_id": r.name
            })
            
    return activities
