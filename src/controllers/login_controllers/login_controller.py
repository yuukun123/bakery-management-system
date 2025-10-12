from PyQt5.QtWidgets import QMessageBox
from src.services.login_query.login_query import Login
from src.services.query_user_name import QueryUserName
from src.windows.manager_window.manager_window_manage import open_manager_main_window


class LoginController:
    def __init__(self, view):
        self.view = view
        self.main_window_instance = None
        self.query_data = QueryUserName()
        self.role = ""

    def handle_login(self, employee_id, password_login):
        if employee_id == "" or password_login == "":
            self.on_login_null()
            return
        model = Login()
        print(f"DEBUG: Trying login_query with {employee_id}/{password_login}")
        user = model.check_login(employee_id, password_login)
        if user["success"]:
            print("DEBUG: Login success")
            self.role = user["user"]["role"]
            self.on_login_success(employee_id)
            print(f"DEBUG: {self.role}")
        else:
            if user["error"] == "invalid_credentials":
                self.on_login_wrong_name_and_password()  # hoặc riêng username
                print("DEBUG: Login failed - user not found")
            elif user["error"] == "incorrect_password":
                self.on_login_wrong_name_and_password()  # hoặc riêng password
                print("DEBUG: Login failed - invalid credentials")
            elif user["error"] == "account_inactive":
                self.on_inactive_account()  # hoặc riêng password
                print("DEBUG: Login failed - invalid credentials")
            else:
                self.on_login_failed()
                print("DEBUG: Login failed - unknown error:", user)
        model.close()

    def on_login_success(self, employee_id):
        from src.windows.employee_window.employee_window_manage import open_employee_main_window
        from src.windows.manager_window.manager_window_manage import open_manager_main_window
        QMessageBox.information(self.view, "Login", "✅ login_query success!")
        try:
            print(f"DEBUG: Login success for user '{employee_id}'")
            user_context = self.query_data.get_employee_by_employee_id(employee_id)
            if not user_context:
                print(f"LỖI: Không tìm thấy thông tin user '{employee_id}'.")
                return
            print(f"DEBUG: {self.role}")
            if self.role == "Manager":
                self.main_window_instance = open_manager_main_window(employee_id)
                self.view.close()
                print("DEBUG: MainWindow instance created via window_manage and shown.")

            elif self.role == "Employee":
                self.main_window_instance = open_employee_main_window(employee_id)
                self.view.close()
                print("DEBUG: MainWindow instance created via window_manage and shown.")
        except Exception as e:
            print("ERROR while opening main window:", e)
            self.view.show()

    def on_login_wrong_name_and_password(self):
        self.view.errors_5.setText("wrong username")
        self.view.errors_6.setText("wrong password")
        self.view.errors_5.show()
        self.view.errors_6.show()
        print("wrong username and password")

    def on_login_null(self):
        self.view.errors_5.setText("please enter username and password!")
        self.view.errors_6.setText("please enter username and password!")
        self.view.errors_5.show()
        self.view.errors_6.show()
        print("please enter username and password!")

    def on_login_failed(self):
        QMessageBox.warning(self.view, "Login", "❌ login_query failed!")

    def on_inactive_account(self):
        QMessageBox.warning(self.view, "Login", "❌ account is inactive!")