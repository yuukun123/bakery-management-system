from PyQt5.QtWidgets import QToolButton, QStackedWidget, QLabel, QPushButton, QFrame, QLineEdit

from src.services.query_data_employee.employee_query_data import EmployeeQueryData


class CheckoutController:
    def __init__(self, ui_page, main_window, order_service):
        self.order_service = order_service
        self.page = ui_page
        self.main_window = main_window
        self._initialized = False  # Cờ để chắc rằng chúng ta chỉ setup 1 lần
        self.query_data = EmployeeQueryData()

        # Lấy các widget con từ trang sản phẩm để tiện truy cập
        # Tên widget phải khớp với tên bạn đặt trong Qt Designer
        self.product_stackedWidget = self.page.findChild(QStackedWidget, 'product_stackedWidget')
        self.search_customer = self.page.findChild(QToolButton, 'search_customer')
        self.customer_name_label = self.page.findChild(QLabel, 'customer_name_label')
        self.customer_phone_label = self.page.findChild(QLabel, 'customer_phone_label')
        self.search_customer_btn = self.page.findChild(QPushButton, 'search_customer_btn')
        self.contain_customer = self.page.findChild(QFrame, 'contain_customer')
        self.contain_customer.hide()
        self.show_add_customer_btn = self.page.findChild(QToolButton, 'add_customer')
        self.customer_name = self.page.findChild(QLineEdit, 'customer_name')
        self.customer_phone = self.page.findChild(QLineEdit, 'customer_phone')
        self.add_customer = self.page.findChild(QToolButton, 'add_customer')
        self.pay_bt = self.page.findChild(QToolButton, 'pay_btn')
        self.cancel_btn = self.page.findChild(QToolButton, 'cancel_btn')

    def setup_page(self):
        """
        Hàm này sẽ được gọi từ MainWindow để thiết lập toàn bộ trang.
        """
        if not self._initialized:
            print("DEBUG: ProductController setup is running for the first time.")
            self.setup_ui_connections()
            self._initialized = True

    def setup_ui_connections(self):
        """Kết nối tất cả các signal và slot cho trang này."""
        self.search_customer_btn.clicked.connect(self.search_customer_with_phone)
        print("DEBUG: Checkout button connected to show_checkout_page.")
        self.show_add_customer_btn.clicked.connect(self.show_add_customer)
        print("DEBUG: Cancel button connected to show_product_selection_page.")
        self.add_customer.clicked.connect(self.add_customer)
        print("DEBUG: Cancel button connected to show_product_selection_page.")

    def search_customer_with_phone(self):
        customer_phone = self.search_customer
        customers = self.query_data.get_customer_with_phone(customer_phone)
        if not customers:
            self.contain_customer.show()
            customer_name = self.customer_name.text()
            customer_phone = self.customer_phone.text()
            self.query_data.add_customer(customer_name, customer_phone)
            self.contain_customer.hide()

        self.customer_name_label.setText(customers[0]['customer_name'])
        self.customer_phone_label.setText(customers[0]['customer_phone'])

    def show_add_customer(self):
        self.contain_customer.show()

    def add_customer(self):
        customer_name = self.customer_name.text()
        customer_phone = self.customer_phone.text()
        self.query_data.add_customer(customer_name, customer_phone)
        self.contain_customer.hide()

    def save_invoice(self):
        pass



