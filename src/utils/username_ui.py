def set_employee_info(username_label, employee_name):
    username_lb = employee_name.upper()
    username_label.setText(f"👤 <b>{username_lb}</b>")

def set_employee_role(role_label, employee_role):
    employee_rl = employee_role
    if employee_rl == "Manager":
        employee_rl = "Quản lý"
        print(f"Debug: {employee_rl}")
        role_label.setText(f"<b>{employee_rl}</b>")
        return employee_rl
    elif employee_rl == "Employee":
        employee_rl = "Nhân viên"
        print(f"Debug: {employee_rl}")
        role_label.setText(f"<b>{employee_rl}</b>")
        return employee_rl
    return None