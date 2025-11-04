from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHeaderView, QAbstractItemView, QMessageBox, QTableWidgetItem

from src.constants.table_header import INVOICE_DETAIL_HEADER
from src.services.query_data_employee.employee_query_data import EmployeeQueryData

class InvoiceDetailController:
    def __init__(self, parent, invoice_code):
        self.parent = parent
        self.query_data = EmployeeQueryData()
        self._initialized = False  # Cờ để chắc rằng chúng ta chỉ setup 1 lần
        self.invoice_code = invoice_code
        self.summary_table = self.parent.summary_table
        self.invoice_code_label = self.parent.invoice_code_label
        self.employee_name_label = self.parent.employee_name_label
        self.customer_name_label = self.parent.customer_name_label
        self.invoice_date_label = self.parent.invoice_date_label
        self.total_quantity = self.parent.total_quantity
        self.total_amount = self.parent.total_amount
        self.total_pay = self.parent.total_pay
        self.pay_method = self.parent.pay_method
        self.change_label = self.parent.change_label
        self.change_frame = self.parent.change_frame
        self.change_frame.hide()

    def setup_dialog(self):
        """
        Hàm này sẽ được gọi từ MainWindow để thiết lập toàn bộ trang.
        """
        if not self._initialized:
            print("DEBUG: ProductController setup is running for the first time.")
            self._setup_table_header_and_properties()
            self.load_invoice_detail()
            self._initialized = True

    def _setup_table_header_and_properties(self):
        if not self.summary_table:
            print("WARNING: Không tìm thấy QTableWidget.")
            return

        # === BƯỚC 1: THIẾT LẬP CẤU TRÚC CƠ BẢN CỦA BẢNG ===

        # Đặt số lượng cột và tên header TRƯỚC TIÊN
        self.summary_table.setColumnCount(len(INVOICE_DETAIL_HEADER))
        self.summary_table.setHorizontalHeaderLabels(INVOICE_DETAIL_HEADER)

    def load_invoice_detail(self):
        if self.invoice_code is None:  # Giả sử invoice_code được truyền vào khi tạo
            return

            # Gọi hàm truy vấn mới
        details = self.query_data.get_invoice_detail_by_code(self.invoice_code)

        if not details:
            QMessageBox.warning(self, "Lỗi", f"Không thể tải chi tiết cho hóa đơn {self.invoice_code}.")
            return

        # `details` là một dict có 'info' và 'products'

        # --- A. ĐIỀN THÔNG TIN CHUNG ---
        info = details.get('info', {})
        self.invoice_code_label.setText(str(info.get('invoice_code', 'N/A')))
        self.employee_name_label.setText(str(info.get('employee_name', 'N/A')))
        self.customer_name_label.setText(str(info.get('customer_name', 'N/A')))
        self.invoice_date_label.setText(str(info.get('invoice_date', 'N/A')))
        self.total_quantity.setText(str(info.get('total_quantity', 'N/A')))

        total_amount = info.get('total_amount', 'N/A')
        self.total_amount.setText(f"{total_amount:,.0f}")
        cash_received = info.get('cash_received', 0)
        self.total_pay.setText(f"{cash_received:,.0f}")
        payment_method = info.get('payment_method', 'N/A')
        self.pay_method.setText(payment_method)  # Sửa lỗi setText

        # 2. Hiển thị/Ẩn khu vực Tiền thối tùy theo phương thức
        # Giả sử bạn có một QFrame tên là 'change_frame' chứa label 'Tiền thối' và giá trị
        if payment_method == "Tiền mặt":
            # Nếu là tiền mặt, hiển thị khu vực này
            self.change_frame.show()
            # Lấy và format giá trị tiền thối
            change_amount = info.get('change_given', 0)
            self.change_label.setText(f"{change_amount:,.0f}")  # Format cho đẹp

        # --- B. ĐIỀN DANH SÁCH SẢN PHẨM ---
        column_order = [
            'product_name',
            'quantity',
            'unit_price',
            'subtotal_amount_invoice'
        ]

        products = details.get('products', [])
        print(f"DEBUG: [InvoiceDetailController] Products: {products}")
        self.summary_table.setRowCount(len(products))

        for row_index, product_dict in enumerate(products):
            # 3. LẶP QUA TỪNG CỘT THEO THỨ TỰ ĐÃ ĐỊNH
            for col_index, key in enumerate(column_order):

                # a. Lấy giá trị từ dictionary dựa vào key
                value = product_dict.get(key)

                # b. Tạo chuỗi hiển thị và áp dụng format nếu cần
                if value is None:
                    display_text = ""
                elif key in ['unit_price', 'subtotal_amount_invoice']:
                    # Nếu là cột tiền tệ
                    try:
                        display_text = f"{float(value):,.0f}"
                    except (ValueError, TypeError):
                        display_text = "0"
                else:
                    # Các cột khác (tên, số lượng)
                    display_text = str(value)

                # c. Tạo widget item
                item = QTableWidgetItem(display_text)

                # d. Căn lề dựa trên key hoặc col_index
                if key == 'product_name':
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                else:
                    # Căn phải cho các cột số/tiền
                    item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)

                # e. Đặt item vào bảng
                self.summary_table.setItem(row_index, col_index, item)