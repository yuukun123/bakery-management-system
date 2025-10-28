from functools import total_ordering

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QToolButton, QStackedWidget, QLabel, QPushButton, QFrame, QLineEdit, QMessageBox

from src.services.query_data_employee.employee_query_data import EmployeeQueryData
from src.utils.employee_tab.validators import is_valid_phone_number

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
        self.search_customer = self.page.findChild(QLineEdit, 'search_customer')
        self.customer_name_label = self.page.findChild(QLabel, 'customer_name_label')
        self.customer_phone_label = self.page.findChild(QLabel, 'customer_phone_label')
        self.search_customer_btn = self.page.findChild(QPushButton, 'search_customer_btn')
        self.contain_customer = self.page.findChild(QFrame, 'contain_customer')
        self.contain_customer.hide()
        self.show_add_customer_btn = self.page.findChild(QToolButton, 'show_add_customer_btn')
        self.customer_name = self.page.findChild(QLineEdit, 'customer_name')
        self.customer_phone = self.page.findChild(QLineEdit, 'customer_phone')
        self.add_customer = self.page.findChild(QPushButton, 'add_customer')
        self.cash_received_input = self.page.findChild(QLineEdit, 'cash_received_input')
        self.cash_change = self.page.findChild(QLabel, 'cash_change')
        self.clean_btn = self.page.findChild(QToolButton, 'clean_btn')

        self.pay_bt = self.page.findChild(QToolButton, 'pay_btn')
        self.cancel_btn = self.page.findChild(QToolButton, 'cancel_btn')

        regex = QRegExp("^0[0-9]{9}$")
        self.customer_phone.setValidator(QRegExpValidator(regex))
        self.search_customer.setValidator(QRegExpValidator(regex))

        cash_values = {
            'btn_1000': 1000, 'btn_2000': 2000, 'btn_5000': 5000,
            'btn_10000': 10000, 'btn_20000': 20000, 'btn_50000': 50000,
            'btn_100000': 100000, 'btn_200000': 200000, 'btn_500000': 500000
        }

        for btn_name, value in cash_values.items():
            # Tìm widget nút bấm dựa theo tên trong dictionary
            button = self.page.findChild(QToolButton, btn_name)

            if button:
                # Kết nối tín hiệu 'clicked' của nút với hàm xử lý
                # Dùng lambda để truyền giá trị (value) tương ứng vào hàm
                # Kỹ thuật `val=value` rất quan trọng để "bắt" đúng giá trị trong vòng lặp
                button.clicked.connect(lambda _, val=value: self.on_cash_button_clicked(val))
            else:
                print(f"WARNING: Không tìm thấy nút có tên '{btn_name}'")

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
        self.add_customer.clicked.connect(self.handle_add_customer_infor)
        print("DEBUG: Cancel button connected to show_product_selection_page.")

    def search_customer_with_phone(self):
        customer_phone = self.search_customer.text().strip()
        customers = self.query_data.get_customer_with_phone(customer_phone)

        if not customer_phone:
            print("DEBUG: Vui lòng nhập số điện thoại khách hàng.")
            return

        if not customers:
            self.contain_customer.show()
            return

        self.fill_customer(customers)

    def fill_customer(self, customers):
        self.customer_name_label.setText(customers[0]['customer_name'])
        self.customer_phone_label.setText(customers[0]['customer_phone'])

    def show_add_customer(self):
        self.contain_customer.show()

    def handle_add_customer_infor(self):
        customer_name = self.customer_name.text()
        customer_phone = self.customer_phone.text()

        if not customer_name or not customer_phone:
            print("DEBUG: Vui lòng nhập đầy đủ thông tin khách hàng.")
            QMessageBox.warning(self.main_window, "Thông báo", "Nhập đầy đủ thông tin khách hàng")
            return

        if not is_valid_phone_number(customer_phone):
            print("DEBUG: Số điện thoại không hợp lệ.")
            QMessageBox.warning(self.main_window, "Thông báo", "Số điện thoại không hợp lệ.")
            return

        self.query_data.add_customer(customer_name, customer_phone)
        self.contain_customer.hide()
        new_customer = self.query_data.get_customer_with_phone(customer_phone)
        self.fill_customer(new_customer)
        print("Debug: add customer successful")

    def on_cash_button_clicked(self, amount_to_add):
        """
        Hàm này được gọi khi bất kỳ nút tiền gợi ý nào được bấm.
        Nó sẽ cộng dồn số tiền vào ô "Tiền khách đưa".

        Args:
            amount_to_add (int): Số tiền từ nút được bấm (ví dụ: 1000, 50000).
        """
        print(f"DEBUG: Cash button clicked. Adding {amount_to_add}")

        try:
            # Lấy giá trị hiện tại từ ô nhập liệu
            current_text = self.cash_received_input.text().replace('.', '')  # Xóa dấu chấm phân cách
            print(f"Debug {current_text}")
            if not current_text:
                current_amount = 0
            else:
                current_amount = int(current_text)

            # Cộng thêm số tiền mới
            new_amount = current_amount + amount_to_add

            # Cập nhật lại ô nhập liệu với định dạng số cho đẹp
            self.cash_received_input.setText(f"{new_amount:,.0f}".replace(',', '.'))

            # (Tùy chọn) Sau khi cập nhật, bạn có thể gọi hàm tính tiền thối lại
            self.calculate_change()

        except ValueError:
            # Nếu người dùng nhập chữ vào ô, đặt lại giá trị
            self.cash_received_input.setText(f"{amount_to_add:,.0f}".replace(',', '.'))
            self.calculate_change()

    def calculate_change(self, new_amount):
        total_amount = self.order_service.get_total_amount()
        change = new_amount - total_amount

        self.cash_change.setText()

    #
    # def screen_money(self):
    #
    #
    # def handle_add_money(self):
    #
    #
    # def save_invoice(self):
    #     pass



