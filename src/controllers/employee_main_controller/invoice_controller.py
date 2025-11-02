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
        self.filter_btn = self.parent.filter_btn
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
            # self.load_invoice_data()
            self.load_all_invoices()
            self._initialized = True

    def setup_ui_connections(self):
        """Kết nối tất cả các signal và slot cho trang này."""
        self.filter_btn.clicked.connect(self.apply_filters)
        self.search_invoice_btn.clicked.connect(self.apply_filters)
        self.clear_btn.clicked.connect(self.clear_search_input)

    def search_customer_invoice(self):
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

    def apply_filters(self):
        # 1. Lấy ngày tháng
        start_date = self.start_day.date().toPyDate()
        end_date = self.end_day.date().toPyDate()

        # 2. Lấy các từ khóa
        invoice_code_keyword = self.invoice_code.text().strip()
        customer_name_keyword = self.customer_name_invoice.text().strip()
        customer_phone_keyword = self.customer_phone_invoice.text().strip()

        # 3. Gọi hàm lọc linh hoạt mới
        results = self.query_data.filter_invoices(
            start_date=start_date,
            end_date=end_date,
            invoice_code=invoice_code_keyword,
            customer_name=customer_name_keyword,
            customer_phone=customer_phone_keyword
        )

        # 4. Hiển thị kết quả
        if results is not None:
            self.populate_invoice_table(results)
            if not results:
                QMessageBox.information(self.parent, "Thông báo", "Không tìm thấy kết quả nào phù hợp.")
        else:
            QMessageBox.critical(self.parent, "Lỗi", "Có lỗi xảy ra khi lọc hóa đơn.")

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
        Xóa nội dung trong các ô tìm kiếm, reset ngày về hiện tại,
        và tải lại toàn bộ danh sách hóa đơn ban đầu.
        """
        # 1. Reset các ô input
        self.invoice_code.clear()
        self.customer_name_invoice.clear()
        self.customer_phone_invoice.clear()
        self.start_day.setDate(QDate.currentDate())
        self.end_day.setDate(QDate.currentDate())
        print("DEBUG: Search inputs cleared and dates reset.")

        # 2. Tải lại toàn bộ dữ liệu (để xóa kết quả lọc cũ)
        # Giả sử bạn có một hàm tên là `load_all_invoices`
        self.load_all_invoices()

    def load_all_invoices(self):
        """Tải tất cả các hóa đơn từ CSDL và hiển thị lên bảng."""
        print("DEBUG: Loading all invoices...")
        all_invoices = self.query_data.get_all_invoices()  # Bạn cần tạo hàm này
        if all_invoices is not None:
            self.populate_invoice_table(all_invoices)
        else:
            QMessageBox.critical(self.parent, "Lỗi", "Không thể tải danh sách hóa đơn.")