from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QAbstractItemView, QHeaderView, \
    QAbstractScrollArea

from src.services.query_data_manager.manager_query_data import QueryData
from src.controllers.buttonController import buttonController
from src.services.query_user_name import QueryUserName
from src.utils.username_ui import set_employee_info, set_employee_role
from src.views.moveable_window import MoveableWindow
from src.views.manager_main_view.employee_view import EmployeeViewWidget
from src.views.manager_main_view.product_view import ProductViewWidget
from resources import resources_rc

class ManagerMainWindow(QMainWindow):
    def __init__(self, employee_id):
        # self.username = username
        super().__init__()
        uic.loadUi("UI/forms/manager/manager_main_screen.ui", self)
        MoveableWindow.__init__(self)

        # Thêm frameless + trong suốt
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1.0)

        # Vô hiệu hóa các nút xóa sửa
        self.delete_employee_btn.setEnabled(False)
        self.update_employee_btn.setEnabled(False)
        self.update_product_btn.setEnabled(False)
        self.delete_product_btn.setEnabled(False)

        self.setup_views()

        self.query_username = QueryUserName()
        self._employee_context = None
        self._employee_role = None
        self.employee_id = employee_id
        self.load_employee_context(self.employee_id)

        self.set_default_stack(0, self.employee_btn)
        self.employee_btn.clicked.connect(lambda: self.handle_nav_click(0, self.employee_btn))
        self.product_btn.clicked.connect(lambda: self.handle_nav_click(1, self.product_btn))
        self.import_invoice_btn.clicked.connect(lambda: self.handle_nav_click(2, self.import_invoice_btn))
        self.statistical_btn.clicked.connect(lambda: self.handle_nav_click(3, self.statistical_btn))

        if not self._employee_context:
            QMessageBox.critical(self, "Lỗi nghiêm trọng", f"Không thể tìm thấy dữ liệu cho người dùng '{self.employee_id}'.")
            return
        employee_name = self._employee_context.get('employee_name', 'Unknown')
        employee_role = self._employee_role.get('role', 'Unknown')

        set_employee_info(self.username_label, employee_name)
        set_employee_role(self.role_label, employee_role)
    #
        self.buttonController = buttonController(self)
        self.closeBtn.clicked.connect(buttonController.handle_close)
        self.hideBtn.clicked.connect(self.buttonController.handle_hidden)
        self.logout.clicked.connect(self.buttonController.handle_logout)

    def load_employee_context(self, employee_id):
        print(f"DEBUG: Đang tải user context cho employee id: {employee_id}")
        self._employee_context = self.query_username.get_employee_field_by_id(employee_id,'employee_name')
        self._employee_role = self.query_username.get_employee_field_by_id(employee_id, 'role')
        print(f"DEBUG: User context đã tải: {self._employee_context}")

    def get_nav_buttons(self):
        return [
            self.employee_btn,
            self.product_btn,
            self.import_invoice_btn,
            self.statistical_btn
        ]

    def reset_button_styles(self):
        normal_style = """
            QPushButton {
                color: rgb(255, 255, 255);
	            background-color: rgb(0, 104, 153);
            }
        """
        for btn in self.get_nav_buttons():
            btn.setStyleSheet(normal_style)

    def set_active_button_style(self, active_button):
        active_style = """
            QPushButton {
            color: rgb(255, 255, 255);
                background-color: rgb(0, 68, 100);
            }
        """
        active_button.setStyleSheet(active_style)
    def update_navigation_styles(self, active_button):
        self.reset_button_styles()
        self.set_active_button_style(active_button)

    def switch_stack(self, index, button):
        self.stackedWidget.setCurrentIndex(index)
        self.update_navigation_styles(button)

    def set_default_stack(self, index, button):
        self.switch_stack(index, button)

    def setup_views(self):
        self.employee_view = EmployeeViewWidget(self)
        self.product_view = ProductViewWidget(self)

    def handle_nav_click(self, index, button):
        self.switch_stack(index, button)
        # Nếu có bảng nhân sự thì clear
        if index == 0 and hasattr(self.employee_view, "employee_tableWidget"):
            self.employee_view.employee_tableWidget.clearSelection()
        if index == 1 and hasattr(self.product_view, "product_tableWidget"):
            self.product_view.product_tableWidget.clearSelection()