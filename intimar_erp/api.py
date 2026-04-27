import frappe
from frappe import _
from frappe.utils import now_datetime, nowtime

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
    reserva.hora_llegada = nowtime()
    if mozo_id:
        reserva.mozo = mozo_id
        
    reserva.save()
    frappe.db.commit()
    return {"status": "success"}

@frappe.whitelist()
def liberar_mesa(mesa_id):
    reserva_parent = frappe.db.get_value("Mesa Reserva Intimar", {"mesa": mesa_id}, "parent")
    if reserva_parent:
        res = frappe.get_doc("Reserva Intimar", reserva_parent)
        res.estado_reserva = "Finalizada"
        res.hora_salida = nowtime()
        res.save()
    
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
