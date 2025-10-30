from datetime import datetime

from PyQt5.QtCore import Qt, QRegExp, QDate
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem, QAbstractItemView

from src.services.query_data_employee.employee_query_data import EmployeeQueryData
from src.constants.table_header import INVOICE_HEADER

class InvoiceController:
    def __init__(self, parent):
        self.parent = parent
        self._initialized = False  # Cờ để chắc rằng chúng ta chỉ setup 1 lần
        self.query_data = EmployeeQueryData()

        self.start_day = self.parent.start_day
        self.end_day = self.parent.end_day
        self.invoice_code = self.parent.invoice_code
        self.customer_name_invoice = self.parent.customer_name_invoice
        self.customer_phone_invoice = self.parent.customer_phone_invoice
        self.search_invoice_btn = self.parent.search_invoice_btn
        self.clear_btn = self.parent.clear_btn

        self.start_day.setDate(QDate.currentDate())
        self.end_day.setDate(QDate.currentDate())

        self.table = self.parent.table_invoice

        regex = QRegExp("^0[0-9]{9}$")
        self.customer_phone_invoice.setValidator(QRegExpValidator(regex))

    def setup_page(self):
        """
        Hàm này sẽ được gọi từ MainWindow để thiết lập toàn bộ trang.
        """
        if not self._initialized:
            print("DEBUG: ProductController setup is running for the first time.")
            self.setup_ui_connections()
            self._setup_table_header_and_properties()
            self.load_invoice_data()
            self._initialized = True

    def setup_ui_connections(self):
        """Kết nối tất cả các signal và slot cho trang này."""
        self.start_day.dateChanged.connect(self.filter_date)
        self.end_day.dateChanged.connect(self.filter_date)
        self.search_invoice_btn.clicked.connect(self.filter_date)
        self.clear_btn.clicked.connect(self.clear_search_input)

    def search_customer_with_phone(self):
        customer_name = self.customer_name_invoice.text().strip()
        customer_phone = self.customer_phone_invoice.text().strip()
        invoice_code = self.invoice_code.text().strip()

        # customer_data = self.query_data.get_customer_with_phone(customer_phone)
        #
        # if not customer_phone:
        #     print("DEBUG: Vui lòng nhập số điện thoại khách hàng.")
        #     return
        #
        # if not customer_data:
        #     QMessageBox.warning(self.parent, "Thông báo", "Không tìm thấy khách hàng hãy thêm mới vào")
        #     return

    def _setup_table_header_and_properties(self):
        if not self.table:
            print("WARNING: Không tìm thấy QTableWidget.")
            return

            # YÊU CẦU 1: CHỌN CẢ DÒNG KHI CLICK
            # --------------------------------------------------
            # setSelectionBehavior sẽ quyết định đơn vị lựa chọn là Ô (Item), Dòng (Row), hay Cột (Column)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        print("DEBUG: Table selection behavior set to SelectRows.")
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)

        self.table.setColumnCount(len(INVOICE_HEADER))
        self.table.setHorizontalHeaderLabels(INVOICE_HEADER)

    def load_invoice_data(self):
        invoice_data = self.query_data.get_all_invoice()
        print(f"DEBUG (EmployeeView): data manager: {invoice_data}")
        if not invoice_data:
            print("Không có dữ liệu nhân viên")
            self.table.setRowCount(0) # Xóa dữ liệu cũ nếu không có dữ liệu mới
            return

        self.table.setRowCount(len(invoice_data))

        for row_index, row_data in enumerate(invoice_data):
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                if item:
                    item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_index, col_index, item)

    def filter_date(self):
        """
        Lấy ngày bắt đầu và kết thúc từ giao diện,
        gọi hàm truy vấn CSDL và hiển thị kết quả lên bảng.
        """
        # --- BƯỚC 1: LẤY VÀ CHUYỂN ĐỔI NGÀY THÁNG ---

        # .date() trả về một đối tượng QDate
        start_qdate = self.start_day.date()
        end_qdate = self.end_day.date()

        # (Tùy chọn nhưng khuyến nghị) Chuyển đổi QDate thành đối tượng date của Python
        # để truyền vào hàm truy vấn. Điều này giúp lớp QueryData không phụ thuộc vào PyQt.
        start_date_py = start_qdate.toPyDate()
        end_date_py = end_qdate.toPyDate()

        print(f"DEBUG: Filtering invoices from {start_date_py} to {end_date_py}")

        # --- BƯỚC 2: GỌI HÀM TRUY VẤN CSDL ---

        # Giả sử self.query_data là instance của lớp QueryData của bạn
        # Gọi hàm filter_invoices_by_date mà chúng ta đã tạo
        filtered_invoices = self.query_data.filter_invoices_by_date(start_date_py, end_date_py)

        # --- BƯỚC 3: HIỂN THỊ KẾT QUẢ LÊN BẢNG ---

        if filtered_invoices is None:
            # Lỗi CSDL đã xảy ra
            QMessageBox.critical(self.parent, "Lỗi", "Đã có lỗi xảy ra khi truy vấn cơ sở dữ liệu.")
            return

        if not filtered_invoices:
            # Không tìm thấy hóa đơn nào
            print("INFO: No invoices found in the selected date range.")
            # Xóa sạch bảng
            self.table.setRowCount(0)
            QMessageBox.information(self.parent, "Thông báo", "Không tìm thấy hóa đơn nào trong khoảng thời gian đã chọn.")
            return

        # Nếu có dữ liệu, đổ nó vào bảng
        self.populate_invoice_table(filtered_invoices)

    def populate_invoice_table(self, invoices_data):
        """
        Hàm này nhận một danh sách các dictionary hóa đơn và hiển thị chúng lên QTableWidget.
        """
        self.table.setRowCount(len(invoices_data))

        # Định nghĩa thứ tự các cột để hiển thị
        column_order = [
            'invoice_code', 'invoice_date', 'employee_name',
            'customer_name', 'payment_method', 'total_amount'
        ]

        for row_index, invoice in enumerate(invoices_data):
            for col_index, key in enumerate(column_order):
                value = invoice.get(key)

                # Định dạng lại các giá trị cho đẹp trước khi hiển thị
                if key == 'total_amount':
                    # Định dạng số tiền
                    display_text = f"{value:,.0f}đ".replace(',', '.')
                elif key == 'invoice_date':
                    # Định dạng lại ngày giờ (nếu cần)
                    # Ví dụ: '2024-05-22 10:30:00' -> '10:30 22-05-2024'
                    try:
                        dt_object = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                        display_text = dt_object.strftime('%H:%M %d-%m-%Y')
                    except (ValueError, TypeError):
                        display_text = str(value)
                else:
                    display_text = str(value if value is not None else '')

                item = QTableWidgetItem(display_text)
                if item:
                    item.setTextAlignment(Qt.AlignCenter)

                self.table.setItem(row_index, col_index, item)

        print(f"DEBUG: Displayed {len(invoices_data)} invoices in the table.")



    def clear_search_input(self):
        """
        Xóa nội dung trong ô tìm kiếm.
        """
        if self.invoice_code or self.customer_name_invoice or self.customer_phone_invoice:
            self.invoice_code.clear()
            self.customer_name_invoice.clear()
            self.customer_phone_invoice.clear()
            print("DEBUG: Search input cleared.")