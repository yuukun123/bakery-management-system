from PyQt5 import uic
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QAbstractItemView, QHeaderView, \
    QAbstractScrollArea

from src.services.query_data_manager.manager_query_data import QueryData
from src.controllers.buttonController import buttonController
from src.services.query_user_name import QueryUserName
from src.utils.username_ui import set_employee_info, set_employee_role
from src.views.moveable_window import MoveableWindow
from src.views.manager_main_view.employee_view import EmployeeViewWidget
from src.views.manager_main_view.product_view import ProductViewWidget
from src.views.manager_main_view.import_invoice_view import ImportInvoiceViewWidget
from src.views.manager_main_view.add_invoice_view import addInvoiceViewWidget
from src.views.manager_main_view.statistical_view import statisticalView
from resources import resources_rc

class ManagerMainWindow(QMainWindow):
    def __init__(self, employee_id):
        # self.username = username
        super().__init__()
        self.employee_id = employee_id
        uic.loadUi("UI/forms/manager/manager_main_screen.ui", self)
        MoveableWindow.__init__(self)

        # Thêm frameless + trong suốt
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1.0)

        self.query_data = QueryData()

        # Vô hiệu hóa các nút xóa sửa
        self.quit_employee_btn.setEnabled(False)
        self.update_employee_btn.setEnabled(False)
        self.update_product_btn.setEnabled(False)
        self.stop_product_btn.setEnabled(False)

        self.setup_views()

        self.query_username = QueryUserName()
        self._employee_context = None
        self._employee_role = None
        self.load_employee_context(self.employee_id)

        self.set_default_stack(0, self.employee_btn)
        self.employee_btn.clicked.connect(lambda: self.handle_nav_click(0, self.employee_btn))
        self.product_btn.clicked.connect(lambda: self.handle_nav_click(1, self.product_btn))
        self.import_invoice_btn.clicked.connect(lambda: self.handle_nav_click(2, self.import_invoice_btn))
        self.add_import_btn.clicked.connect(lambda: self.handle_nav_click(3,self.add_import_btn))
        self.statistical_btn.clicked.connect(lambda: self.handle_nav_click(4, self.statistical_btn))
        self.statistical_invenue_tab.clicked.connect(self.show_revenue_tab)
        self.statistical_product_tab.clicked.connect(self.show_product_tab)
        self.statistical_destroy_tab.clicked.connect(self.show_destroy_tab)

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
        self.import_invoice_view = ImportInvoiceViewWidget(self)
        self.add_invoice_view = addInvoiceViewWidget(parent = self, employee_id = self.employee_id)
        self.statistical_view = statisticalView(parent=self)


    def handle_nav_click(self, index, button):
        self.switch_stack(index, button)
        # Nếu có bảng nhân sự thì clear
        if index == 0 and hasattr(self.employee_view, "employee_tableWidget"):
            self.employee_view.employee_tableWidget.clearSelection()
            if hasattr(self, 'filter_employee'):
                self.filter_employee.setCurrentIndex(0)
            if hasattr(self, 'status_filter'):
                self.status_filter.setCurrentIndex(0)
            if hasattr(self, 'display_filter'):
                self.display_filter.setCurrentIndex(0)
            if hasattr(self, 'search_input'):
                self.search_input.clear()
        if index == 1 and hasattr(self.product_view, "product_tableWidget"):
            self.product_view.product_tableWidget.clearSelection()
            if hasattr(self, 'comboBox_category'):
                self.comboBox_category.setCurrentIndex(0)
            if hasattr(self, 'status_comboBox'):
                self.status_comboBox.setCurrentIndex(0)
            if hasattr(self, 'comboBox_display'):
                self.comboBox_display.setCurrentIndex(0)
            if hasattr(self, 'search_product'):
                self.search_product.clear()
        if index == 2 and hasattr(self.import_invoice_view, "import_invoice_tableWidget"):
            self.import_invoice_view.import_invoice_tableWidget.clearSelection()
            if hasattr(self, 'comboBox_employee'):
                self.comboBox_employee.setCurrentIndex(0)
            if hasattr(self, 'type_invoice_filter'):
                self.type_invoice_filter.setCurrentIndex(0)
            if hasattr(self, 'display_import'):
                self.display_import.setCurrentIndex(0)
            if hasattr(self, 'search_import_invoice'):
                self.search_import_invoice.clear()
            if hasattr(self, 'from_date') and hasattr(self, 'to_date'):
                controller = self.import_invoice_view.import_invoice_controller
                self.comboBox_employee.blockSignals(True)
                self.type_invoice_filter.blockSignals(True)
                self.display_import.blockSignals(True)
                self.search_import_invoice.blockSignals(True)
                self.from_date.blockSignals(True)
                self.to_date.blockSignals(True)

                self.import_invoice_view.import_invoice_tableWidget.clearSelection()
                self.comboBox_employee.setCurrentIndex(0)
                self.type_invoice_filter.setCurrentIndex(0)
                self.display_import.setCurrentIndex(0)
                self.search_import_invoice.clear()

                today = QDate.currentDate()
                oldest_date_str = self.query_data.get_date_oldest_import_invoice()

                if oldest_date_str:
                    oldest_date = QDate.fromString(oldest_date_str, "yyyy-MM-dd")
                else:
                    oldest_date = QDate(today.year(), today.month(), 1)

                self.from_date.setDate(oldest_date)
                self.to_date.setDate(today)

                self.comboBox_employee.blockSignals(False)
                self.type_invoice_filter.blockSignals(False)
                self.display_import.blockSignals(False)
                self.search_import_invoice.blockSignals(False)
                self.from_date.blockSignals(False)
                self.to_date.blockSignals(False)

                controller.load_employee_data()
        if index == 3:
            self.add_invoice_view.reset_view()

        if index == 4:
            self.statistical_stack.setCurrentIndex(0)
            self.update_subtab_style(self.statistical_invenue_tab)

    def show_revenue_tab(self):
        self.stackedWidget.setCurrentIndex(4)
        self.statistical_stack.setCurrentIndex(0)
        self.update_subtab_style(self.statistical_invenue_tab)

    def show_product_tab(self):
        self.stackedWidget.setCurrentIndex(4)
        self.statistical_stack.setCurrentIndex(1)
        self.update_subtab_style(self.statistical_product_tab)

    def show_destroy_tab(self):
        self.stackedWidget.setCurrentIndex(4)
        self.statistical_stack.setCurrentIndex(2)
        self.update_subtab_style(self.statistical_destroy_tab)

    def update_subtab_style(self, active_button):
        normal_style = "QToolButton { color: rgb(255, 255, 255); background-color: rgb(0, 111, 162);font: 15px \"Segoe UI\"; border-radius:5px; }"
        active_style = "QToolButton { background-color: rgb(0, 88, 129); color: rgb(255, 255, 255);font: 15px \"Segoe UI\"; border-radius:5px;  }"

        for btn in [self.statistical_invenue_tab, self.statistical_product_tab, self.statistical_destroy_tab]:
            btn.setStyleSheet(active_style if btn == active_button else normal_style)