def set_employee_info(username_label, employee_name):
    username_lb = employee_name.upper()
    username_label.setText(f"👤 <b>{username_lb}</b>")

def set_employee_role(role_label, employee_role):
    employee_rl = employee_role
    role_label.setText(f"<b>{employee_rl}</b>")
    return employee_rl
