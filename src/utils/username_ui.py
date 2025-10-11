def set_employee_info(username_label, employee_name):
    username_lb = employee_name.upper()
    username_label.setText(f"👤 <b>{username_lb}</b>")

def set_employee_role(role_label, employee_id):
    employee_role = employee_id.upper()
    role_label.setText(f"<b>{employee_role}</b>")