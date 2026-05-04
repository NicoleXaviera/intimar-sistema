import frappe

def get_context(context):
    from frappe.boot import get_bootinfo
    import json
    from frappe.utils.response import json_handler
    
    boot = get_bootinfo()
    boot['csrf_token'] = frappe.sessions.get_csrf_token()
    context.boot = json.loads(json.dumps(boot, default=json_handler))
