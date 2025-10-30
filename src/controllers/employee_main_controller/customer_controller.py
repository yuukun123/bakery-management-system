from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem

from src.services.query_data_employee.employee_query_data import EmployeeQueryData
from src.constants.table_header import CUSTOMER_HEADER
from src.utils.validators import is_valid_phone_number


class CustomerController:
    def __init__(self, parent):
        self.customer_info = {}
        self.parent = parent
        self._initialized = False  # Cờ để chắc rằng chúng ta chỉ setup 1 lần
        self.query_data = EmployeeQueryData()

        self.contain_update_customer = self.parent.contain_update_customer
        self.show_update_customer_btn = self.parent.show_update_customer_btn
        self.search_customer_2 = self.parent.search_customer_2
        self.search_customer_btn_2 = self.parent.search_customer_btn_2
        self.customer_id = self.parent.customer_id
        self.new_customer_name = self.parent.new_customer_name
        self.new_customer_phone = self.parent.new_customer_phone
        self.update_customer_btn = self.parent.update_customer_btn
        self.contain_update_customer.hide()

        self.table = self.parent.table_customer

        regex = QRegExp("^0[0-9]{9}$")
        self.new_customer_phone.setValidator(QRegExpValidator(regex))
        self.search_customer_2.setValidator(QRegExpValidator(regex))

    def setup_page(self):
        """
        Hàm này sẽ được gọi từ MainWindow để thiết lập toàn bộ trang.
        """
        if not self._initialized:
            print("DEBUG: ProductController setup is running for the first time.")
            self.setup_ui_connections()
            self._setup_table_header()
            self.load_customer_data()
            self._initialized = True

    def setup_ui_connections(self):
        """Kết nối tất cả các signal và slot cho trang này."""
        self.search_customer_btn_2.clicked.connect(self.search_customer_with_phone)
        print("DEBUG: Checkout button connected to show_checkout_page.")
        self.show_update_customer_btn.clicked.connect(self.toggle_show_add_customer)
        print("DEBUG: Cancel button connected to show_product_selection_page.")
        self.update_customer_btn.clicked.connect(self.handle_update_customer_infor)
        print("DEBUG: Cancel button connected to show_product_selection_page.")
        self.table.selectionModel().selectionChanged.connect(self.handle_selection_change)

    def search_customer_with_phone(self):
        customer_phone = self.search_customer_2.text().strip()
        customer_data = self.query_data.get_customer_with_phone(customer_phone)

        if not customer_phone:
            print("DEBUG: Vui lòng nhập số điện thoại khách hàng.")
            return

        if not customer_data:
            QMessageBox.warning(self.parent, "Thông báo", "Không tìm thấy khách hàng hãy thêm mới vào")
            return
        else:
            self.contain_update_customer.show()
            self.fill_customer(customer_data)

    def fill_customer(self, customer_data):
        if not customer_data: return

        self.customer_id.setText(f"{customer_data.get('customer_id')}")
        self.new_customer_name.setText(customer_data.get('customer_name'))
        self.new_customer_phone.setText(customer_data.get('customer_phone'))

        self.customer_info = customer_data
        print(f"Debug: Customer updated with customer: {customer_data.get('customer_name')} and stored in customer_info: {self.customer_info}")


    def toggle_show_add_customer(self):
        # Lấy trạng thái hiển thị hiện tại
        is_currently_visible = self.contain_update_customer.isVisible()

        # Đặt trạng thái mới là giá trị NGƯỢC LẠI của trạng thái hiện tại
        self.contain_update_customer.setVisible(not is_currently_visible)

        print(f"DEBUG: Toggled 'add customer' container to be visible: {not is_currently_visible}")

    def _setup_table_header(self):
        self.table.setColumnCount(len(CUSTOMER_HEADER))
        self.table.setHorizontalHeaderLabels(CUSTOMER_HEADER)

        self.table.horizontalHeader().setVisible(True)
        self.table.verticalHeader().setVisible(True)

    def load_customer_data(self):
        customer_data = self.query_data.get_all_customer()
        print(f"DEBUG (EmployeeView): data manager: {customer_data}")
        if not customer_data:
            print("Không có dữ liệu nhân viên")
            self.table.setRowCount(0) # Xóa dữ liệu cũ nếu không có dữ liệu mới
            return

        self.table.setRowCount(len(customer_data))

        for row_index, row_data in enumerate(customer_data):
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                if item:
                    item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_index, col_index, item)

        # # Cấu hình giao diện cho bảng
        # table.resizeColumnsToContents()
        # table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # table.setSelectionBehavior(QAbstractItemView.SelectRows)
        # table.setAlternatingRowColors(True)
        # table.setSortingEnabled(True)
        # table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        # table.verticalHeader().setVisible(False)
        # table.setFocusPolicy(Qt.NoFocus)
        # table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)

    def handle_update_customer_infor(self):
        new_customer_name = self.new_customer_name.text()
        new_customer_phone = self.new_customer_phone.text()

        customer_phone_in_db = self.query_data.get_customer_phone()

        if not new_customer_name or not new_customer_phone:
            print("DEBUG: Vui lòng nhập đầy đủ thông tin khách hàng.")
            QMessageBox.warning(self.parent, "Thông báo", "Nhập đầy đủ thông tin khách hàng")
            return
        elif not is_valid_phone_number(new_customer_phone):
            print("DEBUG: Số điện thoại không hợp lệ.")
            QMessageBox.warning(self.parent, "Thông báo", "Số điện thoại không hợp lệ.")
            return
        elif new_customer_phone in customer_phone_in_db:
            print("DEBUG: Số điện thoại đã tồn tại.")
            QMessageBox.warning(self.parent, "Thông báo", "Số điện thoại đã tồn tại.")
            return

        self.query_data.update_customer(self.customer_info['customer_id'], new_customer_name, new_customer_phone)
        print(f"Debug: update customer successful")
        QMessageBox.information(self.parent, "Thông báo", "Cập nhật thông tin khách hàng thành công.")
        self.load_customer_data()

    def handle_selection_change(self):
        """
        Được gọi khi người dùng thay đổi lựa chọn (click vào một dòng khác) trên bảng.
        Lấy dữ liệu từ dòng được chọn và điền vào form cập nhật.
        """
        selected_rows = self.table.selectionModel().selectedRows()

        if not selected_rows:
            # Nếu không có dòng nào được chọn (ví dụ: người dùng click ra ngoài)
            # thì ẩn form và dừng lại.
            self.contain_update_customer.hide()
            # (Tùy chọn) Bạn có thể xóa dữ liệu trên form ở đây
            # self.clear_update_form()
            return

        # --- LẤY DỮ LIỆU TỪ DÒNG ĐƯỢC CHỌN ---

        # 1. Lấy chỉ số của dòng đầu tiên được chọn
        # Vì thường chỉ cho chọn 1 dòng, nên ta lấy phần tử đầu tiên của list
        first_selected_row_index = selected_rows[0].row()

        # 2. Tạo một dictionary để chứa dữ liệu
        customer_data = {}

        # 3. Ánh xạ từ chỉ số cột sang tên key trong dictionary
        # QUAN TRỌNG: Thứ tự và tên key phải khớp với dữ liệu bạn cần
        # Ví dụ: Cột 0 là customer_id, Cột 1 là customer_name, ...
        column_map = {
            0: 'customer_id',
            1: 'customer_name',
            2: 'customer_phone',
            3: 'customer_address',
            4: 'customer_email',
            5: 'points',
            6: 'created_at',
            7: 'updated_at'
        }

        # 4. Lặp qua các cột để lấy dữ liệu
        for col_index, key_name in column_map.items():
            # Lấy item (ô) tại dòng và cột tương ứng
            item = self.table.item(first_selected_row_index, col_index)

            if item:
                # Lấy nội dung text từ item và gán vào dictionary
                customer_data[key_name] = item.text()
            else:
                # Nếu ô đó trống, gán giá trị rỗng
                customer_data[key_name] = ""

        print(f"DEBUG: Selected customer data: {customer_data}")

        # --- BÂY GIỜ BẠN ĐÃ CÓ `customer_data`, HÃY SỬ DỤNG NÓ ---
        # Hiển thị form cập nhật
        self.contain_update_customer.show()
        self.fill_customer(customer_data)

