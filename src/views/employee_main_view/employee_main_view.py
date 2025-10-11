from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication

# from src.services.query_data.query_data import QueryData
from src.controllers.buttonController import buttonController
from src.services.query_user_name import QueryUserName
from src.utils.username_ui import set_employee_info, set_employee_role
# from src.utils.username_ui import set_user_info
from src.views.moveable_window import MoveableWindow
from resources import resources_rc

class EmployeeMainWindow(QMainWindow, MoveableWindow):
    def __init__(self, employee_id):
        # self.username = username
        super().__init__()
        uic.loadUi("UI/forms/employee/employee_main_screen.ui", self)
        MoveableWindow.__init__(self)

        # Thêm frameless + trong suốt
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1.0)

        self.query_username = QueryUserName()
        self._employee_context = None
        self._employee_role = None
        self.employee_id = employee_id
        self.load_employee_context(self.employee_id)

        if not self._employee_context:
            QMessageBox.critical(self, "Lỗi nghiêm trọng", f"Không thể tìm thấy dữ liệu cho người dùng '{self.employee_id}'.")
            return
        employee_name = self._employee_context.get('employee_name', 'Unknown')
        employee_role = self._employee_role.get('role', 'Unknown')

        set_employee_info(self.username_label, employee_name)
        set_employee_role(self.role_label, employee_role)

        self.buttonController = buttonController(self)
        self.closeBtn.clicked.connect(buttonController.handle_close)
        self.hideBtn.clicked.connect(self.buttonController.handle_hidden)
        self.logout.clicked.connect(self.buttonController.handle_logout)

    def load_employee_context(self, employee_id):
        print(f"DEBUG: Đang tải user context cho employee id: {employee_id}")
        self._employee_context = self.query_username.get_employee_by_employee_id(employee_id)
        self._employee_role = self.query_username.get_employee_role_by_employee_id(employee_id)
        print(f"DEBUG: User context đã tải: {self._employee_context}")