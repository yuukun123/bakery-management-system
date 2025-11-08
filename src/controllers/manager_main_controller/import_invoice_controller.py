import pandas as pd
from PyQt5.QtCore import QDate, QDateTime
from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog
from src.views.manager_main_view.import_detail_dialog_view import importDetail
from src.services.query_data_manager.manager_query_data import QueryData

class ImportInvoiceController:
        def __init__(self, mainview, tableview):
            self.query_data = QueryData()
            self.view = mainview
            self.table = tableview
            self.connect_filter_signal()
            self.load_employee_data()
            self.view.from_date.dateChanged.connect(self.update_to_date_limit)
            self.view.to_date.dateChanged.connect(self.update_from_date_limit)
            self.view.export_btn.clicked.connect(self.export_excel)

        def open_import_detail_dialog(self):
            print("DEBUG: BẮT ĐẦU MỞ DETAIL DIALOG")
            table = self.view.import_invoice_tableWidget
            selected_row = table.currentRow()
            if selected_row >= 0:
                import_code_item = table.item(selected_row, 0)
                if import_code_item:
                    import_code = import_code_item.text()
                    dialog = importDetail(parent=self.view, invoice_code=import_code)
                    result = dialog.exec_()

        def connect_filter_signal(self):
            try:
                self.view.comboBox_employee.currentIndexChanged.connect(self.load_employee_data)
                self.view.display_import.currentIndexChanged.connect(self.load_employee_data)
                self.view.filter_btn.clicked.connect(self.load_employee_data)
                self.view.search_import_btn.clicked.connect(self.load_employee_data)
                self.view.type_invoice_filter.currentIndexChanged.connect(self.load_employee_data)
                self.view.search_input.textChanged.connect(self.load_employee_data)
            except AttributeError as e:
                print(f"LỖI: Không tìm thấy widget filter trong View. Tên widget có đúng không? {e}")

        def reset_search(self):
            if self.view.search_input.text() == "":
                self.load_employee_data()

        def load_employee_data(self):
            try:
                employee = self.view.comboBox_employee.currentText()
                from_date = self.view.from_date.date()
                to_date = self.view.to_date.date()
                type_invoice = self.view.type_invoice_filter.currentText()
                display = self.view.display_import.currentText()
                search_term = self.view.search_import_invoice.text().strip()

                from_date_str = from_date.toString("yyyy-MM-dd")
                to_date_str = to_date.toString("yyyy-MM-dd")

                if not employee:
                    employee = "Tất cả"
                print("----DỮ LIỆU IMPORT INVOICE TRƯỚC KHI LỌC----")
                print(employee, from_date_str, to_date_str, display, search_term)
                filtered_data = self.query_data.search_import(employee,from_date_str,to_date_str, type_invoice, display,search_term)
                print(f"DEBUG(IMPORT CONTROLLER): FILTER DATA: {filtered_data}")
                self.table.import_invoice_table(filtered_data)
            except Exception as e:
                print(f"Lỗi khi tải/filter dữ liệu phiếu nhập: {e}")

        def update_to_date_limit(self, date):
            self.view.to_date.setMinimumDate(date)
        def update_from_date_limit(self, date):
            self.view.from_date.setMaximumDate(date)

        def export_excel(self):
            print("DEBUG: Bắt đầu xuất Excel")
            table = self.view.import_invoice_tableWidget
            row_count = table.rowCount()
            col_count = table.columnCount()

            if row_count == 0:
                QMessageBox.warning(self.view, "Cảnh báo", "Không có dữ liệu để xuất file Excel!")
                return

            # 1. Lấy tiêu đề cột
            headers = []
            for col in range(col_count):
                header_item = table.horizontalHeaderItem(col)
                if header_item:
                    headers.append(header_item.text())
                else:
                    headers.append(f"Column {col + 1}")

            # 2. Lấy dữ liệu từng hàng
            data = []
            for row in range(row_count):
                row_data = []
                for col in range(col_count):
                    item = table.item(row, col)
                    if item:
                        row_data.append(item.text())
                    else:
                        row_data.append("")
                data.append(row_data)

            # 3. Tạo DataFrame từ dữ liệu
            df = pd.DataFrame(data, columns=headers)

            # 4. Mở hộp thoại chọn nơi lưu file
            default_filename = "DanhSachPhieu.xlsx"
            file_path, _ = QFileDialog.getSaveFileName(
                self.view,
                "Lưu file Excel",
                default_filename,
                "Excel Files (*.xlsx)"
            )

            # 5. Lưu xuống file Excel
            if file_path:
                try:
                    # Dùng engine='openpyxl' để hỗ trợ file .xlsx tốt nhất
                    df.to_excel(file_path, index=False, engine='openpyxl')
                    QMessageBox.information(self.view, "Thành công", f"Đã xuất file Excel thành công!\n{file_path}")
                except Exception as e:
                    print(f"Lỗi khi xuất Excel: {e}")
                    QMessageBox.critical(self.view, "Lỗi", f"Không thể xuất file Excel:\n{e}")


