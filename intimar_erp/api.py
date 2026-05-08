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
            reserva_parent = frappe.get_value("Mesa Reserva Intimar", 
                {"mesa": mesa.name, "parenttype": "Reserva Intimar"}, "parent")
            
            if reserva_parent:
                res = frappe.get_doc("Reserva Intimar", reserva_parent)
                if res.estado_reserva not in ["Finalizada", "Cancelada"]:
                    cliente = frappe.get_value("Cliente Intimar", res.cliente, ["nombre_y_apellido_completo", "phone"], as_dict=1)
                    mozo_nombre = frappe.get_value("Mozo Intimar", res.mozo, "nombre") or "Sin Mozo"
                    
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
        fields=["name", "cliente", "hora_reserva", "cant_adultos", "cant_ninos", "mozo", "requerimientos", "necesidades", "alergias"],
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
            
        # Sumar anticipos pagados por moneda
        anticipos = frappe.get_all("Anticipo Reserva Intimar", 
            filters={"parent": r.name, "estado_anticipo": "Pagado"},
            fields=["monto_anticipo", "moneda"]
        )
        
        resumen = []
        total_pen = sum(a.monto_anticipo for a in anticipos if a.moneda == "PEN")
        total_usd = sum(a.monto_anticipo for a in anticipos if a.moneda == "USD")
        
        if total_pen > 0: resumen.append(f"S/ {total_pen}")
        if total_usd > 0: resumen.append(f"$ {total_usd}")
        
        r.total_pagado_txt = " + ".join(resumen) if resumen else ""
        r.total_pagado = total_pen + (total_usd * 3.7) # Solo para lógica de aviso, no para mostrar
    return reservas

@frappe.whitelist()
def get_cliente_by_phone(phone):
    phone = clean_phone(phone)
    if not phone: return None
    cliente = frappe.get_value("Cliente Intimar", {"phone": phone}, 
        ["name", "name1", "lastname", "email", "dni_ruc"], as_dict=1)
    return cliente

@frappe.whitelist()
def get_aforo_ocupado(fecha, hora, excluir_reserva=None):
    """
    Calcula el aforo máximo ocupado considerando:
    1. Reservas que NO han llegado y ya pasaron su tolerancia de 20 min (se liberan).
    2. Reservas en proceso y confirmadas a tiempo.
    """
    config = frappe.get_doc("Configuracion Intimar", ignore_permissions=True)
    duracion = config.duracion_reserva or 2
    aforo_max = config.aforo_maximo or 0
    tolerancia_mins = 20
    
    now = frappe.utils.now_datetime()
    h_inicio = frappe.utils.get_datetime(f"{fecha} {hora}")
    h_fin = h_inicio + frappe.utils.get_timedelta(f"{duracion}:00:00")
    
    reservas = frappe.get_all("Reserva Intimar", 
        filters={
            "fecha_reserva": fecha,
            "estado_reserva": ["not in", ["Cancelada", "Finalizada", "Lista de espera"]],
            "name": ["!=", excluir_reserva] if excluir_reserva else ["!=", ""]
        },
        fields=["name", "hora_reserva", "cant_adultos", "cant_ninos", "estado_reserva", "hora_llegada"]
    )
    
    puntos_de_tiempo = [h_inicio]
    rango_reservas = []
    
    for r in reservas:
        start_str = r.hora_llegada if (r.estado_reserva == "En proceso" and r.hora_llegada) else r.hora_reserva
        r_start = frappe.utils.get_datetime(f"{fecha} {start_str}")
        
        # Lógica de Tolerancia: Si es hoy, no ha llegado y pasaron 20 min, NO ocupa aforo
        if r.estado_reserva == "Confirmada" and not r.hora_llegada:
            limite_tolerancia = frappe.utils.add_to_date(r_start, minutes=tolerancia_mins)
            if fecha == frappe.utils.today() and now > limite_tolerancia:
                continue # Se ignora esta reserva tarde
        
        r_end = r_start + frappe.utils.get_timedelta(f"{duracion}:00:00")
        rango_reservas.append({
            "start": r_start,
            "end": r_end,
            "pax": (r.cant_adultos or 0) + (r.cant_ninos or 0)
        })
        puntos_de_tiempo.append(r_start)
    
    max_ocupacion = 0
    for p in puntos_de_tiempo:
        if h_inicio <= p < h_fin:
            ocupacion_en_p = sum(r["pax"] for r in rango_reservas if r["start"] <= p < r["end"])
            if ocupacion_en_p > max_ocupacion:
                max_ocupacion = ocupacion_en_p
                
    # Validar mesas físicas disponibles ahora
    mesas_libres = len(frappe.get_all("Mesa Intimar", filters={"estado_mesa": 1}))
                
    return {
        "ocupado": max_ocupacion,
        "limite": aforo_max,
        "disponible": max(0, aforo_max - max_ocupacion) if aforo_max > 0 else 999,
        "mesas_fisicas_libres": mesas_libres
    }

@frappe.whitelist()
def crear_reserva_rapida(nombre, apellido, celular, adultos, ninos=0, email=None, codigo_pais=None):
    try:
        # 1. Validar Horario de Atención
        config = frappe.get_doc("Configuracion Intimar", ignore_permissions=True)
        now_t = frappe.utils.get_time(frappe.utils.nowtime())
        if config.hora_minima and config.hora_maxima:
            if now_t < frappe.utils.get_time(config.hora_minima) or now_t > frappe.utils.get_time(config.hora_maxima):
                frappe.throw(f"<b>ERROR DE HORARIO</b><br><br>El restaurante está fuera de horario de atención.<br>Atención: {config.hora_minima} - {config.hora_maxima}")

        # 2. Validar Aforo y Mesas
        pax_nuevo = int(adultos) + int(ninos)
        estado = get_aforo_ocupado(frappe.utils.today(), frappe.utils.nowtime())
        
        if estado["mesas_fisicas_libres"] <= 0:
            frappe.throw("<b>SIN MESAS DISPONIBLES</b><br><br>No hay mesas físicas desocupadas en este momento. Por favor, espere a que se libere una.")

        if estado["limite"] > 0 and (estado["ocupado"] + pax_nuevo) > estado["limite"]:
            frappe.throw(
                f"<b>AFORO EXCEDIDO</b><br><br>"
                f"Capacidad Máxima: {estado['limite']}<br>"
                f"Ocupación (con tolerancia 20m): {estado['ocupado']}<br>"
                f"Espacio Libre: {estado['disponible']}<br><br>"
                f"No hay espacio para {pax_nuevo} personas."
            )
        
        celular = clean_phone(celular)
        
        # 1. Buscar o crear cliente
        clientes = frappe.get_all('Cliente Intimar', 
            filters={'phone': celular}, 
            fields=['name', 'name1', 'lastname', 'email'],
            limit=1)
        cliente = clientes[0] if clientes else None
        
        if cliente:
            # SI EXISTE: "Jalamos" la data registrada y NO creamos nada nuevo
            cliente_id = cliente.name
            nombre = cliente.name1 # Prioridad absoluta a la data registrada
            apellido = cliente.lastname
            email = cliente.email or email
        else:
            nuevo_cliente = frappe.get_doc({
                'doctype': 'Cliente Intimar',
                'name1': nombre,
                'lastname': apellido,
                'nombre_y_apellido_completo': f"{nombre} {apellido if apellido else ''}".strip(),
                'phone': celular,
                'email': email
            })
            nuevo_cliente.insert(ignore_permissions=True)
            cliente_id = nuevo_cliente.name
        
        # 2. Crear la reserva hoy, ahora, estado Confirmada
        reserva = frappe.get_doc({
            'doctype': 'Reserva Intimar',
            'cliente': cliente_id,
            'nombre': nombre,
            'apellido': apellido,
            'celular': celular,
            'codigo_pais': codigo_pais,
            'email': email,
            'fecha_reserva': frappe.utils.today(),
            'hora_reserva': frappe.utils.now_datetime().strftime("%H:%M"),
            'cant_adultos': int(adultos),
            'cant_ninos': int(ninos),
            'estado_reserva': 'Confirmada'
        })
        
        reserva.insert(ignore_permissions=True)
        
        # Devolvemos el doc con los datos necesarios para el frontend
        res_data = reserva.as_dict()
        res_data.cliente_nombre = f"{nombre} {apellido if apellido else ''}".strip()
        res_data.total_pagado = 0
        res_data.total_pagado_txt = ""
        res_data.cliente_reconocido = True if cliente else False
        
        return res_data
    except frappe.ValidationError:
        raise
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error en crear_reserva_rapida")
        frappe.throw(_("No se pudo crear la reserva rápida: {0}").format(str(e)))

@frappe.whitelist()
def get_mozos():
    return frappe.get_all("Mozo Intimar", fields=["name", "nombre", "apellido", "telefono", "email"])

@frappe.whitelist()
def get_mesas_libres():
    return frappe.get_all("Mesa Intimar", filters={"estado_mesa": 1}, fields=["name", "numero_mesa", "ubicacion_mesa"], order_by="numero_mesa asc")

@frappe.whitelist()
def save_mozo(name=None, nombre=None, apellido=None, telefono=None, email=None):
    if not name:
        # Check if mozo with same name/lastname already exists if it's new
        existing = frappe.get_value("Mozo Intimar", {"nombre": nombre, "apellido": apellido})
        if existing:
            frappe.throw(_("Ya existe un mozo registrado como {0} {1}").format(nombre, apellido))
        doc = frappe.new_doc("Mozo Intimar")
    else:
        doc = frappe.get_doc("Mozo Intimar", name)
        
    doc.nombre = nombre
    doc.apellido = apellido
    doc.telefono = telefono
    doc.email = email
    doc.save(ignore_permissions=True)
    return {"status": "success", "name": doc.name}

@frappe.whitelist()
def delete_mozo(name):
    frappe.delete_doc("Mozo Intimar", name, ignore_permissions=True)
    return {"status": "success"}

@frappe.whitelist()
def delete_reserva(name):
    if "System Manager" not in frappe.get_roles() and frappe.session.user != "Administrator":
        frappe.throw(_("No tienes permiso para eliminar reservas"))
    
    frappe.delete_doc("Reserva Intimar", name, ignore_permissions=True)
    return {"status": "success"}

@frappe.whitelist()
def asignar_mesa_a_reserva(reserva_id, mesa_id, mozo_id=None, adultos=None, ninos=None):
    # mesa_id puede venir como string o como lista desde el mapa de mesas
    mesas_ids = mesa_id if isinstance(mesa_id, list) else [mesa_id]
    
    reserva = frappe.get_doc("Reserva Intimar", reserva_id)
    
    # Validar estado: Solo permitir asignación a reservas Confirmadas
    if reserva.estado_reserva != "Confirmada":
        frappe.throw(f"No se puede asignar mesa. La reserva debe estar en estado 'Confirmada' (Estado actual: {reserva.estado_reserva})")
    
    # Actualizar PERS. si han cambiado
    if adultos is not None or ninos is not None:
        adultos = int(adultos) if adultos is not None else reserva.cant_adultos
        ninos = int(ninos) if ninos is not None else reserva.cant_ninos
        
        if adultos != reserva.cant_adultos or ninos != reserva.cant_ninos:
            reserva.cant_adultos = adultos
            reserva.cant_ninos = ninos

    for m_id in mesas_ids:
        # 1. Marcar mesa como ocupada (0)
        m_doc = frappe.get_doc("Mesa Intimar", m_id)
        m_doc.estado_mesa = 0
        m_doc.save(ignore_permissions=True)
        
        # 2. Agregar a la sub-tabla de la reserva si no existe ya
        if not any(m.mesa == m_id for m in reserva.mesas):
            reserva.append("mesas", {"mesa": m_id})
    
    reserva.estado_reserva = "En proceso"
    reserva.hora_llegada = frappe.utils.nowtime()
    if mozo_id:
        reserva.mozo = mozo_id
        
    reserva.save(ignore_permissions=True)
    return {"status": "success"}

@frappe.whitelist()
def liberar_mesa(mesa_id):
    reserva_parent = frappe.get_value("Mesa Reserva Intimar", {"mesa": mesa_id}, "parent")
    if reserva_parent:
        res = frappe.get_doc("Reserva Intimar", reserva_parent)
        res.estado_reserva = "Finalizada"
        res.hora_salida = frappe.utils.nowtime()
        res.save(ignore_permissions=True)
    
    m_doc = frappe.get_doc("Mesa Intimar", mesa_id)
    m_doc.estado_mesa = 1
    m_doc.save(ignore_permissions=True)
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
        
    # Usamos el ORM nativo de Frappe
    data = frappe.get_list("Reserva Intimar",
        filters={"name": ["in", reserva_names]},
        fields=[
            "name", "cliente", "nombre", "apellido", "celular", "fecha_reserva", 
            "hora_reserva", "cant_adultos", "cant_ninos", "estado_reserva", 
            "anticipo_required", "mozo", "hora_llegada", "hora_salida", 
            "am_pm", "requerimientos", "necesidades", "alergias", "motivo_reserva"
        ],
        order_by=order_by
    )

    # Calculamos los totales pagados para estas reservas
    for r in data:
        # Sumar pagos desde Anticipo Reserva Intimar (forma segura ORM)
        pagos = frappe.get_all("Anticipo Reserva Intimar", 
            filters={"parent": r.name, "estado_anticipo": "Pagado"}, 
            fields=["monto_anticipo"]
        )
        r.total_pagado = sum(p.monto_anticipo for p in pagos)
        
        # Sumar anticipos pagados por moneda
        anticipos = frappe.get_all("Anticipo Reserva Intimar", 
            filters={"parent": r.name, "estado_anticipo": "Pagado"},
            fields=["monto_anticipo", "moneda"]
        )
        
        resumen = []
        total_pen = sum(a.monto_anticipo for a in anticipos if a.moneda == "PEN")
        total_usd = sum(a.monto_anticipo for a in anticipos if a.moneda == "USD")
        
        if total_pen > 0: resumen.append(f"S/ {total_pen}")
        if total_usd > 0: resumen.append(f"$ {total_usd}")
        
        r["total_pagado_txt"] = " + ".join(resumen) if resumen else ""
        r["total_pagado"] = total_pen + (total_usd * 3.7) # Para lógica de aviso

    return data



@frappe.whitelist(allow_guest=True)
def crear_reserva_publica(cliente_nombre, cliente_celular, fecha, hora, adultos, ninos=0, 
                          email=None, dni=None, alergias=None, ocasion=None, 
                          requerimientos=None, necesidades=None, apellido=None, 
                          codigo_pais=None, acepta_politicas=0, acepta_promociones=0,
                          aceptar_lista_espera=0):
    
    # Bypass CSRF for public guest requests
    if frappe.session.user == "Guest":
        frappe.local.conf.ignore_csrf = True
    
    # Validar Aforo
    pax_nuevo = int(adultos) + int(ninos)
    estado_aforo = get_aforo_ocupado(fecha, hora)
    if estado_aforo["limite"] > 0 and (estado_aforo["ocupado"] + pax_nuevo) > estado_aforo["limite"]:
        if not int(aceptar_lista_espera):
            frappe.throw(
                f"Lo sentimos, el aforo está completo para este horario.<br>"
                f"Disponibilidad: {estado_aforo['disponible']} de {estado_aforo['limite']} personas.<br><br>"
                f"¿Deseas unirte a la lista de espera?"
            )

    # 1. Buscar o crear cliente
    # Limpiamos el celular para consistencia
    cliente_celular = clean_phone(cliente_celular)
    
    # Usamos el celular como identificador único
    cliente_id = frappe.get_value('Cliente Intimar', {'phone': cliente_celular}, 'name')
    
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
    # Determinar estado inicial basado en aforo y cantidad de personas
    if estado_aforo["limite"] > 0 and (estado_aforo["ocupado"] + pax_nuevo) > estado_aforo["limite"]:
        estado_inicial = 'Lista de espera'
    elif pax_nuevo >= 8:
        # Grupos de 8 o más personas requieren revisión manual
        estado_inicial = 'Solicitud de reserva'
    else:
        estado_inicial = 'Confirmada'

    # Grupos de 8 o más requieren anticipo
    requires_anticipo = 1 if pax_nuevo >= 8 else 0
    
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
        'motivo_reserva': f"[WEB] {ocasion if ocasion else ''}".strip(),
        'requerimientos': requerimientos,
        'necesidades': necesidades,
        'alergias': alergias,
        'acepta_politicas': acepta_politicas,
        'acepta_promociones': acepta_promociones,
        'aceptar_lista_espera': aceptar_lista_espera,
        'estado_reserva': estado_inicial,
        'anticipo_required': requires_anticipo
    })
    
    try:
        reserva.insert(ignore_permissions=True)
        return {
            'status': 'success',
            'reserva_name': reserva.name,
            'requires_anticipo': requires_anticipo
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
def get_current_user_roles():
    return frappe.get_roles(frappe.session.user)

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
    return {"status": "success"}

@frappe.whitelist()
def create_new_user(email, full_name, password, roles=None):
    if "System Manager" not in frappe.get_roles() and frappe.session.user != "Administrator":
        frappe.throw(_("No tienes permiso para crear usuarios"))
        
    if frappe.get_value("User", email):
        frappe.throw(_("El usuario con el correo {0} ya existe").format(email))
        
    doc = frappe.new_doc("User")
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
    
    return {"status": "success"}

@frappe.whitelist()
def get_dashboard_stats(start_date=None, end_date=None):
    allowed_roles = ["System Manager", "Anfitriona", "Recepcionista"]
    user_roles = frappe.get_roles()
    if not any(role in user_roles for role in allowed_roles) and frappe.session.user != "Administrator":
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
    anticipos = frappe.get_all("Anticipo Reserva Intimar", 
        filters={
            "estado_anticipo": "Pagado",
            "creation": ["between", [start_date + " 00:00:00", end_date + " 23:59:59"]]
        },
        fields=["monto_anticipo"]
    )
    total_anticipos = sum([a.monto_anticipo or 0 for a in anticipos])
    
    # Ranking de Mozos (Procesado en Python desde DocTypes)
    reservas_mozos = frappe.get_all("Reserva Intimar",
        filters={"fecha_reserva": ["between", [start_date, end_date]], "mozo_asignado": ["is", "set"]},
        fields=["mozo_asignado"]
    )
    mozos_stats = {}
    for r in reservas_mozos:
        mozos_stats[r.mozo_asignado] = mozos_stats.get(r.mozo_asignado, 0) + 1
    
    mozos_ranking = sorted([{"mozo_asignado": k, "total": v} for k, v in mozos_stats.items()], 
                           key=lambda x: x['total'], reverse=True)[:5]
    
    # Ocupación por Hora
    hourly_stats = {}
    for r in reservas:
        h = r.hora_reserva
        hourly_stats[h] = hourly_stats.get(h, 0) + 1
    
    ocupacion_horas = sorted([{"hora_reserva": k, "total": v} for k, v in hourly_stats.items()], 
                             key=lambda x: x['hora_reserva'])
    
    # Desglose de estados
    status_counts = {}
    for r in reservas:
        status = r.estado_reserva or "Sin Estado"
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # KPIs adicionales para tiempo real
    config = frappe.get_doc("Configuracion Intimar", ignore_permissions=True)
    aforo_maximo = config.aforo_maximo or 0
    mesas_disponibles = len(frappe.get_all("Mesa Intimar", filters={"estado_mesa": 1}))
    
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
def get_user_display(user_id):
    if not user_id or user_id == "Administrator":
        return "Admin"
    
    user_info = frappe.get_value("User", user_id, ["full_name", "name"], as_dict=1)
    roles = frappe.get_roles(user_id)
    
    # Jerarquía de roles para mostrar el más importante
    priority = ["System Manager", "Anfitriona", "Vigilante", "Mozo"]
    role_to_show = "Usuario"
    for p in priority:
        if p in roles:
            role_to_show = p
            break
            
    name = user_info.full_name if user_info and user_info.full_name else user_id
    return f"{name} ({role_to_show})"

@frappe.whitelist()
def get_recent_activity():
    """Devuelve las últimas 15 actividades con autoría y detalle de cambios."""
    reservas = frappe.get_all("Reserva Intimar", 
        fields=["name", "nombre", "estado_reserva", "modified", "hora_reserva", "modified_by", "cant_adultos", "cant_ninos"],
        order_by="modified desc",
        limit=15
    )
    
    activities = []
    for r in reservas:
        msg = ""
        msg_type = "info"
        prefix = f"[{r.name}] "
        author = get_user_display(r.modified_by)
        
        # Detectar cambios específicos vía comentarios recientes
        last_comment = frappe.get_value("Comment", 
            {"reference_doctype": "Reserva Intimar", "reference_name": r.name}, 
            "content", order_by="creation desc")
        
        if last_comment and "PERS. actualizadas" in last_comment:
            msg = prefix + f"{author} ajustó comensales: " + last_comment.split(":")[-1].strip()
            msg_type = "pax_change"
        elif last_comment and "HORARIO actualizado" in last_comment:
            msg = prefix + f"{author} cambió horario: " + last_comment.split(":")[-1].strip()
            msg_type = "time_change"
        elif r.estado_reserva == "En proceso":
            msg = prefix + f"{author} registró llegada de {r.nombre}."
            msg_type = "cliente_llego"
        elif r.estado_reserva == "Solicitud de reserva":
            msg = prefix + f"Nueva solicitud de {r.nombre} ({r.hora_reserva})."
            msg_type = "nueva_reserva"
        elif r.estado_reserva == "Confirmada":
            msg = prefix + f"{author} confirmó a {r.nombre}."
            msg_type = "confirmada"
        elif r.estado_reserva == "Lista de espera":
            msg = prefix + f"Aforo lleno: {r.nombre} a espera."
            msg_type = "aforo_lleno"
        elif r.estado_reserva == "Finalizada":
            msg = prefix + f"{author} liberó mesa de {r.nombre}."
            msg_type = "mesa_liberada"
        
        if msg:
            activities.append({
                "type": msg_type,
                "message": msg,
                "timestamp": r.modified,
                "reserva_id": r.name,
                "author": author
            })
            
    return activities

@frappe.whitelist()
def get_occupancy_alerts():
    config = frappe.get_doc("Configuracion Intimar", ignore_permissions=True)
    duracion_maxima_horas = config.duracion_reserva or 2
    
    reservas = frappe.get_all("Reserva Intimar", 
        filters={"estado_reserva": "En proceso", "fecha_reserva": frappe.utils.today()},
        fields=["name", "cliente", "hora_llegada"]
    )
    
    alerts = []
    now = frappe.utils.now_datetime()
    
    for r in reservas:
        if not r.hora_llegada: continue
        
        # Combinar fecha de hoy con hora de llegada
        llegada_dt = frappe.utils.get_datetime(f"{frappe.utils.today()} {r.hora_llegada}")
        diff = (now - llegada_dt).total_seconds() / 60 # en minutos
        
        if diff > (duracion_maxima_horas * 60):
            cliente_nombre = frappe.get_value("Cliente Intimar", r.cliente, "nombre_y_apellido_completo")
            
            # Obtener la mesa asignada (puede ser más de una, tomamos la primera para el alert)
            mesa_id = frappe.get_value("Mesa Reserva Intimar", {"parent": r.name}, "mesa")
            mesa_numero = frappe.get_value("Mesa Intimar", mesa_id, "numero_mesa") if mesa_id else "S/N"
            
            alerts.append({
                "reserva_id": r.name,
                "cliente": cliente_nombre,
                "duracion_minutos": int(diff),
                "mesa_id": mesa_id,
                "mesa_numero": mesa_numero
            })
            
    return alerts

@frappe.whitelist()
def get_ubicaciones_mesas():
    return frappe.get_all("Ubicacion Mesa Intimar", fields=["name"], order_by="name asc")

@frappe.whitelist()
def get_reservas_pax_stats(filters=None):
    if isinstance(filters, str):
        import json
        filters = json.loads(filters)
    
    return frappe.get_all("Reserva Intimar", 
        filters=filters,
        fields=["cant_adultos", "cant_ninos"]
    )
