from functools import total_ordering

from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QToolButton, QStackedWidget, QLabel, QPushButton, QFrame, QLineEdit, QMessageBox, QComboBox

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
        self.cash_change = self.page.findChild(QLineEdit, 'cash_change')
        self.clean_btn = self.page.findChild(QToolButton, 'clean_btn')
        self.pay_method_CB = self.page.findChild(QComboBox, 'pay_method_CB')

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
        self.show_add_customer_btn.clicked.connect(self.toggle_show_add_customer)
        print("DEBUG: Cancel button connected to show_product_selection_page.")
        self.add_customer.clicked.connect(self.handle_add_customer_infor)
        print("DEBUG: Cancel button connected to show_product_selection_page.")
        self.clean_btn.clicked.connect(self.clean_input)
        print("DEBUG: Cancel button connected to show_product_selection_page.")
        self.pay_bt.clicked.connect(self.process_payment)
        print("DEBUG: Cancel button connected to show_product_selection_page.")

    def search_customer_with_phone(self):
        customer_phone = self.search_customer.text().strip()
        customer_data = self.query_data.get_customer_with_phone(customer_phone)

        if not customer_phone:
            print("DEBUG: Vui lòng nhập số điện thoại khách hàng.")
            return

        if not customer_data:
            QMessageBox.warning(self.main_window, "Thông báo", "Không tìm thấy khách hàng hãy thêm mới vào")
            self.contain_customer.show()
            return

        self.fill_customer(customer_data)

    def fill_customer(self, customer_data):
        if not customer_data: return

        self.customer_name_label.setText(customer_data.get('customer_name'))
        self.customer_phone_label.setText(customer_data.get('customer_phone'))

        self.order_service.customer_info = customer_data
        print(f"DEBUG: OrderService updated with customer: {customer_data.get('customer_name')}")

    def toggle_show_add_customer(self):
        # Lấy trạng thái hiển thị hiện tại
        is_currently_visible = self.contain_customer.isVisible()

        # Đặt trạng thái mới là giá trị NGƯỢC LẠI của trạng thái hiện tại
        self.contain_customer.setVisible(not is_currently_visible)

        print(f"DEBUG: Toggled 'add customer' container to be visible: {not is_currently_visible}")

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
        if new_customer:
            self.fill_customer(new_customer)
            print("Debug: add customer successful")

        else: return

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

    def calculate_change(self):  # Bỏ tham số new_amount
        """Hàm tính và hiển thị tiền thối lại, đọc trực tiếp từ UI."""
        try:
            total_amount = self.order_service.get_total_amount()
            cash_received_text = self.cash_received_input.text().replace('.', '')
            if not cash_received_text:
                cash_received = 0
            else:
                cash_received = float(cash_received_text)

            current_method = self.pay_method_CB.currentText()

            if cash_received < total_amount or current_method == "Chuyển khoản":
                self.cash_change.setText("0")
                return

            change = cash_received - total_amount
            self.cash_change.setText(f"{change:,.0f}".replace(',', '.'))
        except ValueError:
            self.cash_change.setText("Lỗi")

    def clean_input(self):
        self.cash_received_input.clear()
        self.cash_change.clear()

    def process_payment(self):
        """
        Hàm được gọi khi nhân viên bấm nút "Thanh Toán".
        Thu thập thông tin và gọi service để lưu vào CSDL.
        """
        # --- 1. THU THẬP DỮ LIỆU ---

        # Lấy thông tin từ OrderService (nguồn chân lý)
        total_amount = self.order_service.get_total_amount()
        items = self.order_service.items
        customer_info = self.order_service.customer_info

        # Lấy thông tin từ context
        employee_id = self.main_window.employee_id
        print(f"Debug: xem id nhân viên {employee_id}")

        # --- 2. VALIDATE DỮ LIỆU ---

        if not items:
            QMessageBox.warning(self.main_window, "Lỗi", "Giỏ hàng đang trống!")
            return

        if customer_info is None:
            # Gán khách vãng lai nếu chưa chọn khách
            # Bạn cần một hàm để lấy thông tin khách vãng lai
            customer_info = self.query_data.get_guest_customer_info()  # Giả sử ID=1
            if customer_info is None:
                QMessageBox.critical(self.main_window, "Lỗi CSDL", "Không tìm thấy thông tin 'Khách vãng lai'.")
                return

        customer_id = customer_info.get('customer_id')

        # Lấy thông tin thanh toán từ giao diện
        payment_method, cash_received, change_given = self.get_payment_details_from_ui()
        if payment_method is None:  # Hàm get_payment_details_from_ui sẽ trả về None nếu có lỗi
            return

        # --- 3. GỌI HÀM LƯU TRỮ ---

        new_invoice_code = self.query_data.save_invoice(
            employee_id=employee_id,
            customer_id=customer_id,
            total_amount=total_amount,
            payment_method=payment_method,
            cash_received=cash_received,
            change_given=change_given,
            items=items
        )

        # --- 4. XỬ LÝ KẾT QUẢ ---

        if new_invoice_code:
            # Thành công!
            QMessageBox.information(self.main_window, "Thành công", f"Đã lưu hóa đơn {new_invoice_code} thành công!")

            # Dọn dẹp cho hóa đơn tiếp theo
            self.order_service.clear_order()
            self.reset_checkout_ui()  # Một hàm để xóa các input, item card...

            # Chuyển về trang bán hàng
            self.main_window.product_controller.show_product_selection_page()
        else:
            # Thất bại
            QMessageBox.critical(self.main_window, "Thất bại", "Đã có lỗi xảy ra. Không thể lưu hóa đơn vào cơ sở dữ liệu.")

    def get_payment_details_from_ui(self):
        """Lấy thông tin thanh toán từ giao diện và kiểm tra tính hợp lệ."""
        try:
            payment_method = self.pay_method_CB.currentText()
            print(f"debug: {payment_method}")
            total_amount = self.order_service.get_total_amount()
            cash_received = 0
            change_given = 0

            if payment_method == 'Tiền mặt':
                cash_received_text = self.cash_received_input.text().replace('.', '')
                if not cash_received_text: cash_received_text = '0'
                cash_received = float(cash_received_text)

                if cash_received < total_amount:
                    QMessageBox.warning(self.main_window, "Thiếu tiền", "Số tiền khách đưa không đủ.")
                    return None, None, None  # Trả về None để báo lỗi

                change_given = cash_received - total_amount
            else:  # Chuyển khoản
                cash_received = total_amount
                change_given = 0

            return payment_method, cash_received, change_given

        except Exception as e:
            QMessageBox.critical(self.main_window, "Lỗi", f"Dữ liệu thanh toán không hợp lệ: {e}")
            return None, None, None

    def reset_checkout_ui(self):
        """Dọn dẹp giao diện sau khi thanh toán thành công."""
        # Xóa thông tin khách hàng
        self.search_customer.clear()
        self.customer_name_label.setText("Khách vãng lai")
        self.customer_phone_label.setText("")
        self.contain_customer.hide()

        # Xóa thông tin thanh toán
        self.cash_received_input.clear()
        self.cash_change.clear()
        self.pay_method_CB.setCurrentIndex(0)  # Đặt lại về phương thức đầu tiên

        # Xóa các item card trong giỏ hàng (phần này cần ProductController xử lý)
        self.main_window.product_controller.clear_order_display()