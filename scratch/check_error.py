import frappe
try:
    log = frappe.get_last_doc('Error Log')
    print(f"METHOD: {log.method}")
    print("-" * 40)
    print(f"ERROR: {log.error}")
except Exception as e:
    print(f"Error reading log: {str(e)}")
