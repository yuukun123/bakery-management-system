from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QMessageBox

from src.controllers.buttonController import buttonController
from src.controllers.employee_main_controller.check_warehouse_controller import WarehouseController
from src.controllers.employee_main_controller.checkout_controller import CheckoutController
from src.controllers.employee_main_controller.customer_controller import CustomerController
from src.controllers.employee_main_controller.invoice_controller import InvoiceController
from src.controllers.employee_main_controller.product_controller import ProductController
from src.models.order_service import OrderService
from src.services.query_user_name import QueryUserName
from src.utils.employee_tab.changeTab import MenuNavigator
from src.utils.username_ui import set_employee_info, set_employee_role
from resources import resources_rc

class EmployeeMainWindow(QMainWindow):
    def __init__(self, employee_id):
        # self.username = username
        super().__init__()
        uic.loadUi("UI/forms/employee/employee_main_screen.ui", self)

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

        employee_name = self._employee_context.get('employee_name') if self._employee_context else 'Unknown'
        employee_role = self._employee_role.get('role') if self._employee_role else 'Unknown'

        print(f"DEBUG: Employee name: {employee_name}")
        print(f"DEBUG: Employee role: {employee_role}")

        set_employee_info(self.username_label, employee_name)
        set_employee_role(self.role_label, employee_role)

        self.buttonController = buttonController(self)
        self.closeBtn.clicked.connect(buttonController.handle_close)
        self.hideBtn.clicked.connect(self.buttonController.handle_hidden)
        self.logout.clicked.connect(self.buttonController.handle_logout)

        buttons = [ self.product_btn, self.customer_btn, self.invoice_btn, self.warehouse_btn ]
        index_map = {btn: i for i, btn in enumerate(buttons)}
        self.menu_nav = MenuNavigator(self.stackedWidget, buttons, index_map, default_button=self.product_btn)

        self.order_service = OrderService()
        self.product_controller = ProductController(self.product_page, self, self.order_service)
        self.checkout_controller = CheckoutController(self.checkout_page, self, self.order_service)

        self.customer_controller = CustomerController(self)
        self.invoice_controller = InvoiceController(self)
        self.warehouse_controller = WarehouseController(self)

        self.stackedWidget.currentChanged.connect(self.on_tab_changed)
        # Chủ động tải Dashboard lần đầu tiên nếu nó là tab mặc định
        if self.stackedWidget.currentWidget() == self.product_page:
            self.on_tab_changed(self.stackedWidget.currentIndex())
        self.on_tab_changed(self.stackedWidget.currentIndex())

    def get_employee_context(self):
        """Get the employee context data."""
        return self._employee_context

    def load_employee_context(self, employee_id):
        print(f"DEBUG: Đang tải user context cho employee id: {employee_id}")
        self._employee_context = self.query_username.get_employee_field_by_id(employee_id, 'employee_name')
        print(f"DEBUG: User context đã tải: {self._employee_context}")
        self._employee_role = self.query_username.get_employee_field_by_id(employee_id, 'role')
        print(f"DEBUG: User role đã tải: {self._employee_role}")

    def on_tab_changed(self, index):
        current_widget = self.stackedWidget.widget(index)

        if current_widget == self.product_page:
            print("Đã chuyển đến trang Product")
            # if not self.dashboardController._initialized_for_user:
            #     self.dashboardController.setup_for_user(self.teacher_context)
            self.product_controller.setup_page()
            self.checkout_controller.setup_page()

        elif current_widget == self.customer_page:
            print("Đã chuyển đến trang Customer")
            self.customer_controller.setup_page()

        elif current_widget == self.invoice_page:
            print("Đã chuyển đến trang Invoice")
            self.invoice_controller.setup_page()

        elif current_widget == self.check_warehouse_page:
            print("Đã chuyển đến trang Warehouse")
            self.warehouse_controller.setup_page()


