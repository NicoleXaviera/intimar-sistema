import frappe
from datetime import timedelta
from frappe import _
import json
import re

def clean_phone(phone):
    if not phone: return ""
    # Remove everything except + and digits
    return re.sub(r"[^\d+]", "", phone)

@frappe.whitelist()
def create_cierres_custom_field():
    if not frappe.db.exists("Custom Field", "Configuracion Intimar-cierres_especiales"):
        frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Configuracion Intimar",
            "fieldname": "cierres_especiales",
            "label": "Cierres Especiales (Fechas y Horarios)",
            "fieldtype": "Small Text",
            "insert_after": "capacidad_cocina_30min",
            "description": "Indique días de la semana o fechas específicas a cerrar. Ej:\nmiércoles\n2026-05-25\n2026-05-26: 12:00, 12:30"
        }).insert(ignore_permissions=True)
        frappe.db.commit()
        return "Created"
    return "Exists"

def expand_horas(horas_raw):
    all_slots = ['11:00', '11:30', '12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '15:45']
    expanded = []
    
    if isinstance(horas_raw, str):
        parts = [p.strip() for p in horas_raw.split(",") if p.strip()]
    elif isinstance(horas_raw, list):
        parts = []
        for h in horas_raw:
            parts.extend([p.strip() for p in str(h).split(",") if p.strip()])
    else:
        return []
        
    for part in parts:
        if "-" in part:
            subparts = part.split("-", 1)
            if len(subparts) == 2:
                start = subparts[0].strip()
                end = subparts[1].strip()
                for slot in all_slots:
                    if start <= slot <= end:
                        if slot not in expanded:
                            expanded.append(slot)
        else:
            if part in all_slots and part not in expanded:
                expanded.append(part)
                
    return expanded

@frappe.whitelist(allow_guest=True)
def get_cierres_especiales():
    config = frappe.get_doc("Configuracion Intimar", ignore_permissions=True)
    texto = config.get("cierres_especiales") or ""
    
    cierres = {
        "fechas": {},
        "dias_semana_python": {"2": "todo"},
        "dias_semana_js": {"3": "todo"}
    }
    
    # Si el campo está completamente vacío, retornar por defecto
    if not texto.strip():
        return cierres
        
    import re
    dias_map = {
        "lunes": 0, "monday": 0,
        "martes": 1, "tuesday": 1,
        "miercoles": 2, "miércoles": 2, "wednesday": 2,
        "jueves": 3, "thursday": 3,
        "viernes": 4, "friday": 4,
        "sabado": 5, "sábado": 5, "saturday": 5,
        "domingo": 6, "sunday": 6
    }
    
    # 1. Intentar parsear como JSON estructurado (Tabla)
    import json
    try:
        items = json.loads(texto)
        if isinstance(items, list):
            for item in items:
                tipo = item.get("tipo")
                valor = str(item.get("valor", "")).strip().lower()
                cobertura = item.get("cobertura", "todo")
                horas = item.get("horas", [])
                
                val_res = "todo" if cobertura == "todo" else expand_horas(horas)
                
                if tipo == "fecha":
                    cierres["fechas"][valor] = val_res
                elif tipo == "dia_semana":
                    if valor in dias_map:
                        dia_val = dias_map[valor]
                    else:
                        try:
                            dia_val = int(valor)
                        except ValueError:
                            continue
                    
                    js_val = 0 if dia_val == 6 else (dia_val + 1)
                    cierres["dias_semana_python"][str(dia_val)] = val_res
                    cierres["dias_semana_js"][str(js_val)] = val_res
            return cierres
    except Exception:
        pass
        
    # 2. Fallback a texto plano por compatibilidad
    for line in texto.strip().split("\n"):
        line = line.strip().lower()
        if not line:
            continue
            
        # Buscar fecha YYYY-MM-DD
        match_fecha = re.match(r'^(\d{4}-\d{2}-\d{2})', line)
        if match_fecha:
            fecha = match_fecha.group(1)
            if ":" in line[10:]:
                parts = line.split(":", 1)
                cierres["fechas"][fecha] = expand_horas(parts[1])
            else:
                cierres["fechas"][fecha] = "todo"
            continue
            
        # Buscar día de la semana
        for dia_nombre, dia_val in dias_map.items():
            if line.startswith(dia_nombre):
                js_val = 0 if dia_val == 6 else (dia_val + 1)
                if ":" in line:
                    parts = line.split(":", 1)
                    val_res = expand_horas(parts[1])
                    cierres["dias_semana_python"][str(dia_val)] = val_res
                    cierres["dias_semana_js"][str(js_val)] = val_res
                else:
                    cierres["dias_semana_python"][str(dia_val)] = "todo"
                    cierres["dias_semana_js"][str(js_val)] = "todo"
                break
                
    return cierres

def bypass_csrf():
    if "intimar_erp.api.crear_reserva_publica" in frappe.request.path:
        frappe.local.conf.ignore_csrf = True

def process_virtual_filters(filters):
    if not filters: return filters
    
    if isinstance(filters, dict):
        return filters
        
    processed = []
    for f in filters:
        if isinstance(f, list) and len(f) >= 3 and f[0] == 'total_pagado':
            op = f[1]
            val = f[2]
            
            # Consultamos directamente el DocType de Anticipos
            reservas_con_pago = frappe.get_all("Anticipo Reserva Intimar", 
                filters={"estado_anticipo": "Pagado"}, 
                pluck="parent"
            )
            
            if op == '>' and val == 0:
                # Mostrar solo los que están en la lista de pagos
                processed.append(['name', 'in', reservas_con_pago if reservas_con_pago else ['']])
            elif op == '<=' and val == 0:
                # Mostrar los que NO están en la lista
                processed.append(['name', 'not in', reservas_con_pago if reservas_con_pago else ['']])
        else:
            processed.append(f)
    return processed

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
            # Buscar la reserva activa que actualmente ocupa esta mesa usando Frappe ORM
            child_records = frappe.get_all("Mesa Reserva Intimar",
                filters={"mesa": mesa.name, "parenttype": "Reserva Intimar"},
                fields=["parent"],
                order_by="creation desc"
            )
            parent_ids = [c.parent for c in child_records] if child_records else []
            
            reserva_parent = None
            if parent_ids:
                active_parents = frappe.get_all("Reserva Intimar",
                    filters={
                        "name": ["in", parent_ids],
                        "estado_reserva": ["in", ["Confirmada", "En proceso"]]
                    },
                    fields=["name"],
                    order_by="creation desc",
                    limit=1
                )
                if active_parents:
                    reserva_parent = active_parents[0].name
                else:
                    # Fallback a cualquier reserva activa no finalizada
                    active_parents_any = frappe.get_all("Reserva Intimar",
                        filters={
                            "name": ["in", parent_ids],
                            "estado_reserva": ["not in", ["Finalizada", "Cancelada", "Atrasada"]]
                        },
                        fields=["name"],
                        order_by="creation desc",
                        limit=1
                    )
                    if active_parents_any:
                        reserva_parent = active_parents_any[0].name

            if reserva_parent:
                res = frappe.get_doc("Reserva Intimar", reserva_parent)
                cliente = frappe.get_value("Cliente Intimar", res.cliente, ["nombre_y_apellido_completo", "phone"], as_dict=1)
                mozo_nombre = frappe.get_value("Mozo Intimar", res.mozo, "nombre") or "Sin Mozo"
                
                # Obtener IDs de mesa completos de todas las mesas asignadas a esta reserva
                otras_mesas = [m.mesa for m in res.mesas if m.mesa]
                
                mesa.reserva = {
                    "name": res.name,
                    "cliente_nombre": cliente.nombre_y_apellido_completo if cliente and cliente.nombre_y_apellido_completo else "Cliente sin nombre",
                    "cliente_telefono": (cliente.phone or "") if cliente else "",
                    "hora_llegada": res.hora_llegada,
                    "mozo_nombre": mozo_nombre,
                    "cant_adultos": res.cant_adultos,
                    "cant_ninos": res.cant_ninos,
                    "mesas_asignadas": sorted(otras_mesas) if otras_mesas else []
                }
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
    h_fin = h_inicio + timedelta(hours=duracion)
    
    reservas = frappe.get_all("Reserva Intimar", 
        filters={
            "fecha_reserva": fecha,
            "estado_reserva": ["not in", ["Cancelada", "Finalizada", "Lista de espera", "Atrasada"]],
            "name": ["!=", excluir_reserva] if excluir_reserva else ["!=", ""]
        },
        fields=["name", "hora_reserva", "cant_adultos", "cant_ninos", "estado_reserva", "hora_llegada"]
    )
    
    puntos_de_tiempo = [h_inicio]
    rango_reservas = []
    
    for r in reservas:
        start_str = r.hora_llegada if (r.estado_reserva == "En proceso" and r.hora_llegada) else r.hora_reserva
        if (isinstance(start_str, (bytes, str))):
            r_start = frappe.utils.get_datetime(f"{fecha} {start_str}")
        else:
            # Handle timedelta or other time objects
            r_start = frappe.utils.get_datetime(f"{fecha} {str(start_str)}")
            
        # Lógica de Tolerancia: Si es hoy, no ha llegado y pasaron 20 min, NO ocupa aforo
        if r.estado_reserva == "Confirmada" and not r.hora_llegada:
            limite_tolerancia = frappe.utils.add_to_date(r_start, minutes=tolerancia_mins)
            if str(fecha) == frappe.utils.today() and now > limite_tolerancia:
                continue # Se ignora esta reserva tarde
                
        r_end = r_start + timedelta(hours=duracion)
        rango_reservas.append({
            "start": r_start,
            "end": r_end,
            "pax": (r.cant_adultos or 0) + (r.cant_ninos or 0)
        })
        puntos_de_tiempo.append(r_start)
        puntos_de_tiempo.append(r_end) # También chequear el punto de salida
    
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
        "mesas_fisicas_libres": mesas_libres,
        "detalle": rango_reservas # Devolvemos los rangos para el desglose
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
            # Obtener detalles de reservas que solapan ahora mismo
            now_dt = frappe.utils.now_datetime()
            detalle_txt = []
            
            # Buscar las reservas que están solapadas AHORA
            reservas_ahora = frappe.get_all("Reserva Intimar",
                filters={
                    "fecha_reserva": frappe.utils.today(),
                    "estado_reserva": ["not in", ["Cancelada", "Finalizada", "Lista de espera", "Atrasada"]]
                },
                fields=["name", "nombre", "cliente", "hora_reserva", "cant_adultos", "cant_ninos", "hora_llegada", "estado_reserva"]
            )
            
            duracion_res = config.duracion_reserva or 2
            for r in reservas_ahora:
                start_str = r.hora_llegada if (r.estado_reserva == "En proceso" and r.hora_llegada) else r.hora_reserva
                r_start = frappe.utils.get_datetime(f"{frappe.utils.today()} {start_str}")
                
                # Tolerancia
                if r.estado_reserva == "Confirmada" and not r.hora_llegada:
                    if (now_dt - r_start).total_seconds() / 60 > 20:
                        continue
                
                r_end = r_start + timedelta(hours=duracion_res)
                
                if r_start <= now_dt < r_end:
                    pax = (r.cant_adultos or 0) + (r.cant_ninos or 0)
                    nombre_cli = r.nombre or frappe.get_value("Cliente Intimar", r.cliente, "nombre_y_apellido_completo") or "Cliente"
                    detalle_txt.append(f"• <b>{frappe.utils.format_time(start_str, 'HH:mm')}</b> - {nombre_cli} ({pax} pers.)")

            res_list_html = "<div style='margin-top: 10px; font-size: 0.9em;'>" + "".join([f"<div>{d}</div>" for d in detalle_txt]) + "</div>"

            frappe.throw(
                f"<div style='text-align: center; margin-bottom: 15px;'><span style='font-size: 1.5em; font-weight: 900; color: #d32f2f;'>⚠️ AFORO EXCEDIDO</span></div>"
                f"<b>Capacidad Máxima:</b> {estado['limite']} personas<br>"
                f"<b>Ocupación Actual:</b> {estado['ocupado']} personas<br>"
                f"<b>Espacio Libre:</b> {estado['disponible']} personas<br><br>"
                f"<div style='background: #f5f5f5; padding: 15px; border-radius: 12px; border-left: 4px solid #00938f;'>"
                f"<b>Reservas activas en este momento:</b><br>"
                f"{res_list_html}"
                f"</div>"
                f"<br>No hay espacio para registrar este nuevo grupo de <b>{pax_nuevo}</b> personas."
            )
        
        celular = clean_phone(celular)
        
        # 1. Buscar o crear cliente
        clientes = frappe.get_all('Cliente Intimar', 
            filters={'phone': celular}, 
            fields=['name', 'name1', 'lastname', 'email'],
            limit=1)
        cliente = clientes[0] if clientes else None
        
        if cliente:
            # SI EXISTE: Actualizamos con la nueva información que se ha ingresado
            cliente_id = cliente.name
            cliente_doc = frappe.get_doc('Cliente Intimar', cliente_id)
            changed = False
            
            if nombre and cliente_doc.name1 != nombre:
                cliente_doc.name1 = nombre
                changed = True
            if apellido is not None and cliente_doc.lastname != apellido:
                cliente_doc.lastname = apellido
                changed = True
            
            full_name = f"{nombre} {apellido if apellido else ''}".strip()
            if cliente_doc.nombre_y_apellido_completo != full_name:
                cliente_doc.nombre_y_apellido_completo = full_name
                changed = True
                
            if email and cliente_doc.email != email:
                cliente_doc.email = email
                changed = True
                
            if changed:
                cliente_doc.save(ignore_permissions=True)
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
            'estado_reserva': 'Confirmada',
            'motivo_reserva': '[RÁPIDA]'
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
    
    # Validar estado: Solo permitir asignación a reservas Confirmadas o Atrasadas
    if reserva.estado_reserva not in ["Confirmada", "Atrasada"]:
        frappe.throw(f"No se puede asignar mesa. La reserva debe estar en estado 'Confirmada' o 'Atrasada' (Estado actual: {reserva.estado_reserva})")
    
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
    # Buscar la reserva activa que actualmente ocupa esta mesa usando Frappe ORM
    child_records = frappe.get_all("Mesa Reserva Intimar",
        filters={"mesa": mesa_id, "parenttype": "Reserva Intimar"},
        fields=["parent"],
        order_by="creation desc"
    )
    parent_ids = [c.parent for c in child_records] if child_records else []
    
    reserva_parent = None
    if parent_ids:
        active_parents = frappe.get_all("Reserva Intimar",
            filters={
                "name": ["in", parent_ids],
                "estado_reserva": ["in", ["Confirmada", "En proceso"]]
            },
            fields=["name"],
            order_by="creation desc",
            limit=1
        )
        if active_parents:
            reserva_parent = active_parents[0].name
        else:
            # Fallback a cualquier activa
            active_parents_any = frappe.get_all("Reserva Intimar",
                filters={
                    "name": ["in", parent_ids],
                    "estado_reserva": ["not in", ["Finalizada", "Cancelada", "Atrasada"]]
                },
                fields=["name"],
                order_by="creation desc",
                limit=1
            )
            if active_parents_any:
                reserva_parent = active_parents_any[0].name

    if reserva_parent:
        res = frappe.get_doc("Reserva Intimar", reserva_parent)
        res.estado_reserva = "Finalizada"
        res.hora_salida = frappe.utils.nowtime()
        res.save(ignore_permissions=True)
    
    m_doc = frappe.get_doc("Mesa Intimar", mesa_id)
    m_doc.estado_mesa = 1
    m_doc.save(ignore_permissions=True)
    return {"status": "success"}

def parse_name_filters(filters):
    db_filters = []
    or_filters = None
    nombre_query = None
    
    if filters:
        for f in filters:
            if isinstance(f, list) and len(f) >= 3 and f[0] == "nombre":
                nombre_query = f[2].strip("%") if isinstance(f[2], str) else f[2]
            else:
                db_filters.append(f)
    else:
        db_filters = filters

    if nombre_query:
        or_filters = []
        or_filters.append(["nombre", "like", f"%{nombre_query}%"])
        or_filters.append(["apellido", "like", f"%{nombre_query}%"])
        
        words = [w.strip() for w in nombre_query.split() if w.strip()]
        if len(words) >= 2:
            for w in words:
                or_filters.append(["nombre", "like", f"%{w}%"])
                or_filters.append(["apellido", "like", f"%{w}%"])
                
    return db_filters, or_filters

@frappe.whitelist()
def get_reservas_list(filters=None, limit_start=0, limit_page_length=20, order_by="creation desc"):
    if isinstance(filters, str):
        filters = json.loads(filters)
        
    filters = process_virtual_filters(filters)
    
    db_filters, or_filters = parse_name_filters(filters)
        
    # Si ordenamos por llegada, usamos un orden base para la DB y luego refinamos en Python
    db_order = order_by
    if "hora_llegada" in order_by:
        db_order = "hora_llegada asc"
        
    # Primero obtenemos los nombres que cumplen los filtros
    kwargs = {
        "filters": db_filters,
        "limit_start": limit_start,
        "limit_page_length": limit_page_length,
        "order_by": db_order,
        "pluck": "name"
    }
    if or_filters:
        kwargs["or_filters"] = or_filters
        
    reserva_names = frappe.get_all("Reserva Intimar", **kwargs)
    
    if not reserva_names:
        return []
        
    # Usamos el ORM nativo de Frappe
    data = frappe.get_list("Reserva Intimar",
        filters={"name": ["in", reserva_names]},
        fields=[
            "name", "cliente", "nombre", "apellido", "celular", "fecha_reserva", 
            "hora_reserva", "cant_adultos", "cant_ninos", "estado_reserva", 
            "anticipo_required", "mozo", "hora_llegada", "hora_salida", 
            "am_pm", "requerimientos", "necesidades", "alergias", "motivo_reserva",
            "creation"
        ],
        order_by=db_order
    )

    # 2. Ordenar en Python si es por llegada (para poner NULLS al final)
    if "hora_llegada" in order_by:
        data.sort(key=lambda x: (x.hora_llegada is None, x.hora_llegada))

    # Calculamos los totales pagados para estas reservas
    for r in data:
        # Sumar pagos desde Anticipo Reserva Intimar (forma segura ORM)
        pagos = frappe.get_all("Anticipo Reserva Intimar", 
            filters={"parent": r.name, "estado_anticipo": "Pagado"}, 
            fields=["monto_anticipo"]
        )
        r.total_pagado = sum(p.monto_anticipo for p in pagos)
        
        # Sumar anticipos pagados por moneda y medio de pago
        anticipos = frappe.get_all("Anticipo Reserva Intimar", 
            filters={"parent": r.name, "estado_anticipo": "Pagado"},
            fields=["monto_anticipo", "moneda", "banco", "nro_operacion"]
        )
        
        resumen = []
        total_pen = 0
        total_usd = 0
        
        for a in anticipos:
            if a.moneda == "PEN": total_pen += a.monto_anticipo
            if a.moneda == "USD": total_usd += a.monto_anticipo
            
            # Formato: "Yape: S/ 50 (Op: 123)"
            txt = f"{a.banco or 'Pago'}: {a.moneda} {a.monto_anticipo}"
            if a.nro_operacion:
                txt += f" ({a.nro_operacion})"
            resumen.append(txt)
        
        r["total_pagado_txt"] = " | ".join(resumen) if resumen else ""
        r["total_pagado"] = total_pen + (total_usd * 3.7)
        r["anticipos"] = anticipos
        
        # Obtener mesas asignadas
        r["mesas"] = frappe.get_all("Mesa Reserva Intimar",
            filters={"parent": r.name},
            fields=["name", "mesa"]
        )

    return data



@frappe.whitelist(allow_guest=True)
def crear_reserva_publica(cliente_nombre, cliente_celular, fecha, hora, adultos, ninos=0, 
                          email=None, dni=None, alergias=None, ocasion=None, 
                          requerimientos=None, necesidades=None, apellido=None, 
                          codigo_pais=None, acepta_politicas=0, acepta_promociones=0,
                          aceptar_lista_espera=0):
    
    # Bypass CSRF handled in hooks.py via bypass_csrf
    
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
    else:
        # Actualizar toda la información del cliente si ya existe para que esté al día y funcione fetch_from correctamente
        cliente_doc = frappe.get_doc('Cliente Intimar', cliente_id)
        changed = False
        
        if cliente_nombre and cliente_doc.name1 != cliente_nombre:
            cliente_doc.name1 = cliente_nombre
            changed = True
        if apellido is not None and cliente_doc.lastname != apellido:
            cliente_doc.lastname = apellido
            changed = True
            
        full_name = f"{cliente_nombre} {apellido if apellido else ''}".strip()
        if cliente_doc.nombre_y_apellido_completo != full_name:
            cliente_doc.nombre_y_apellido_completo = full_name
            changed = True
            
        if email and cliente_doc.email != email:
            cliente_doc.email = email
            changed = True
        if dni and cliente_doc.dni_ruc != dni:
            cliente_doc.dni_ruc = dni
            changed = True
            
        if changed:
            cliente_doc.save(ignore_permissions=True)
    
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
        filters={"fecha_reserva": ["between", [start_date, end_date]], "mozo": ["is", "set"]},
        fields=["mozo"]
    )
    mozos_stats = {}
    for r in reservas_mozos:
        mozos_stats[r.mozo] = mozos_stats.get(r.mozo, 0) + 1
    
    mozos_ranking = sorted([{"mozo": k, "total": v} for k, v in mozos_stats.items()], 
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
def get_reservas_summary(filters=None):
    if isinstance(filters, str):
        filters = json.loads(filters)
    
    filters = process_virtual_filters(filters)
    
    # Traemos solo los campos necesarios para sumar en Python
    res = frappe.get_all("Reserva Intimar", 
        filters=filters, 
        fields=["cant_adultos", "cant_ninos"]
    )
    
    total_reservas = len(res)
    total_personas = sum((r.cant_adultos or 0) + (r.cant_ninos or 0) for r in res)
    
    return {
        "reservas": total_reservas,
        "personas": total_personas
    }

@frappe.whitelist()
def get_ocupacion_proyectada(fecha=None):
    if not fecha:
        fecha = frappe.utils.today()
    
    config = frappe.get_doc("Configuracion Intimar", ignore_permissions=True)
    aforo_max = config.get("aforo_maximo") or 162
    duracion = config.duracion_reserva or 2
    tolerancia_mins = 20
    
    # Horas base de consulta (desde apertura a cierre estimado)
    # Horas cada 30 min para mayor precisión con duraciones de 1.5h
    horas_check = [
        "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", 
        "14:00", "14:30", "15:00", "15:30", "15:45", "16:00", "16:30", 
        "17:00", "17:30", "18:00"
    ]
    
    # Obtener todas las reservas del día (excluyendo canceladas/finalizadas)
    reservas = frappe.get_all("Reserva Intimar",
        filters={
            "fecha_reserva": fecha,
            "estado_reserva": ["not in", ["Cancelada", "Finalizada", "Lista de espera", "Atrasada"]]
        },
        fields=["name", "nombre", "cliente", "hora_reserva", "cant_adultos", "cant_ninos", "estado_reserva", "hora_llegada"]
    )
    
    proyeccion = []
    now = frappe.utils.now_datetime()
    today = frappe.utils.today()
    
    for h in horas_check:
        h_dt = frappe.utils.get_datetime(f"{fecha} {h}")
        # El slot de simulación también considera el margen de limpieza configurado
        h_end = h_dt + timedelta(hours=duracion + (config.margen_limpieza or 0)/60.0)
        
        ocupado = 0
        detalles = []
        
        for r in reservas:
            start_str = r.hora_llegada if (r.estado_reserva == "En proceso" and r.hora_llegada) else r.hora_reserva
            r_start = frappe.utils.get_datetime(f"{fecha} {start_str}")
            
            # Tolerancia: si no ha llegado y pasaron 20 min, no ocupa aforo
            if r.estado_reserva == "Confirmada" and not r.hora_llegada:
                limite_tolerancia = frappe.utils.add_to_date(r_start, minutes=tolerancia_mins)
                if fecha == today and now > limite_tolerancia:
                    continue
            
            pax = (r.cant_adultos or 0) + (r.cant_ninos or 0)
            
            # LÓGICA DE TIEMPO DINÁMICO
            r_dur = config.duracion_reserva or 2
            if pax > 8:
                r_dur = config.duracion_reserva_grande or r_dur
            
            r_margen = (config.margen_limpieza or 0) / 60.0
            r_end = r_start + timedelta(hours=r_dur + r_margen)
            
            # Si la reserva está activa en este punto 'h'
            if r_start <= h_dt < r_end:
                pax = (r.cant_adultos or 0) + (r.cant_ninos or 0)
                ocupado += pax
                nombre_cli = r.nombre or frappe.get_value("Cliente Intimar", r.cliente, "nombre_y_apellido_completo") or "Cliente"
                detalles.append({
                    "reserva": r.name,
                    "nombre": nombre_cli,
                    "pax": pax,
                    "hora": frappe.utils.format_time(start_str, "HH:mm"),
                    "hora_fin": frappe.utils.format_time(r_end, "HH:mm"),
                    "estado": r.estado_reserva
                })
        
        # CÁLCULO DE FLUJO DE COCINA (LLEGADAS EN ESTE BLOQUE)
        # Agrupamos por bloques dinámicos según configuración (ej: 13:15 -> 13:00)
        llegando = 0
        intervalo = config.get("intervalo_flujo_cocina") or 30
        for res in reservas:
            r_time = frappe.utils.get_time(res.hora_reserva)
            # Redondeamos hacia abajo al intervalo más cercano
            r_slot_mins = (r_time.hour * 60 + r_time.minute) // intervalo * intervalo
            r_slot = f"{r_slot_mins // 60:02d}:{r_slot_mins % 60:02d}"
            
            if r_slot == h:
                llegando += (res.cant_adultos or 0) + (res.cant_ninos or 0)
        
        limite_cocina = config.get("capacidad_cocina_30min") or 30
        
        proyeccion.append({
            "hora": h,
            "ocupado": ocupado,
            "llegando": llegando,
            "limite": aforo_max,
            "limite_cocina": limite_cocina,
            "porcentaje": round((ocupado / aforo_max * 100), 1) if aforo_max > 0 else 0,
            "porcentaje_cocina": round((llegando / limite_cocina * 100), 1) if limite_cocina > 0 else 0,
            "detalles": detalles
        })
        
    return proyeccion

@frappe.whitelist()
def sync_fecha_hora_reserva(doc, method=None):
    """Combina fecha y hora en un solo campo Datetime para alertas de Frappe."""
    if doc.fecha_reserva and doc.hora_reserva:
        from frappe.utils import get_datetime
        try:
            doc.fecha_hora_reserva = get_datetime(f"{doc.fecha_reserva} {doc.hora_reserva}")
        except Exception:
            pass

@frappe.whitelist()
def auto_cancel_expired_reservations():
    """Cancela automáticamente las reservas que no llegaron después de 30 minutos."""
    from frappe.utils import now_datetime, get_datetime, add_to_date
    
    now = now_datetime()
    reservas = frappe.get_all("Reserva Intimar", 
        filters={
            "fecha_reserva": frappe.utils.today(),
            "estado_reserva": "Confirmada"
        },
        fields=["name", "hora_reserva"]
    )
    
    for r in reservas:
        try:
            reserva_time = get_datetime(f"{frappe.utils.today()} {r.hora_reserva}")
            # Si pasaron más de 30 minutos de la hora citada
            if now > add_to_date(reserva_time, minutes=30):
                frappe.db.set_value("Reserva Intimar", r.name, "estado_reserva", "Atrasada")
                frappe.get_doc("Reserva Intimar", r.name).add_comment("Comment", "Estado cambiado a Atrasada automáticamente por inasistencia (30 min tarde).")
        except Exception:
            continue
    
    frappe.db.commit()

def close_atrasadas_at_end_of_day():
    """Al final del día, convierte las reservas Atrasadas a Canceladas"""
    import frappe
    reservas = frappe.get_all("Reserva Intimar", 
        filters={"estado_reserva": "Atrasada"},
        fields=["name"]
    )
    for r in reservas:
        try:
            frappe.db.set_value("Reserva Intimar", r.name, "estado_reserva", "Cancelada")
            frappe.get_doc("Reserva Intimar", r.name).add_comment("Comment", "Cierre del día: La reserva quedó Atrasada y no se presentó, se marca como Cancelada definitivamente.")
        except Exception:
            continue
    
    frappe.db.commit()

@frappe.whitelist()
def get_all_mesas_list():
    """Retorna todas las mesas del sistema sin restricciones de listado para el select."""
    import frappe
    return frappe.get_all("Mesa Intimar", fields=["name", "numero_mesa", "ubicacion_mesa"], order_by="numero_mesa asc")


