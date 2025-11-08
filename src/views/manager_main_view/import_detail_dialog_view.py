import os
import re
import shutil
from PyQt5 import uic
from PyQt5.QtGui import QColor, QRegExpValidator, QPixmap, QIntValidator
from PyQt5.QtWidgets import QDialog, QGraphicsDropShadowEffect, QWidget, QMessageBox, QLineEdit, QFileDialog, \
    QTableWidgetItem, QAbstractItemView, QHeaderView, QAbstractScrollArea
from src.services.query_data_manager.manager_query_data import QueryData
from PyQt5.QtCore import Qt, QPoint, QDateTime, QDate, QRegExp
from src.views.moveable_window import MoveableWindow
from src.services.pdf_service import PDFService

class importDetail(QDialog,MoveableWindow):
    def __init__(self, parent=None, invoice_code=None):
        MoveableWindow.__init__(self)
        super(importDetail, self).__init__(parent)
        uic.loadUi("UI/forms/manager/import_invoice_detail.ui", self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.view = parent
        self.invoice_code = invoice_code

        self.query_data = QueryData()
        self.pdf_service = PDFService()
        self.cancel_btn.clicked.connect(self.reject)
        self.export_pdf_btn.clicked.connect(self.export_pdf)
        self.load_product_invoice_table()
        self.set_information()

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 150))
        self.findChild(QWidget, "mainFrame").setGraphicsEffect(shadow)

    def set_information(self):
        data = self.query_data.get_invoice_information(self.invoice_code)
        self.import_id_output.setText(data["import_code"])
        self.type_invoice.setText(data["invoice_type"])
        self.employee_ouput.setText(data["employee_name"])
        self.time_create.setText(data["import_date"])

    def load_product_invoice_table(self):
        data = self.query_data.get_product_import_detail(self.invoice_code)
        if data:
            print("DEBUG: ĐÃ NHẬN ĐƯỢC DATA")
        else:
            print("DEBUG: CHƯA NHẬN ĐƯỢC DATA")
        table = self.detailImportTable
        headers = ["Mã sản phẩm", "Tên sản phẩm", "Loại", "Đơn giá", "Số lượng"]
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setRowCount(len(data))

        price_col_index = headers.index("Đơn giá")

        for row_index, row_data in enumerate(data):
            for col_index, cell_data in enumerate(row_data):
                if col_index == price_col_index:
                    # Cột giá: Format tiền
                    try:
                        numeric_value = int(float(cell_data))
                        display_text = f"{numeric_value:,}đ".replace(",", ".")
                    except (ValueError, TypeError):
                        display_text = str(cell_data) if cell_data is not None else ""
                    item = QTableWidgetItem(display_text)
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                else:
                    item = QTableWidgetItem(str(cell_data))
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

                if item is not None:
                    table.setItem(row_index, col_index, item)
        # Cấu hình giao diện cho bảng
        table.resizeColumnsToContents()
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setAlternatingRowColors(False)
        table.setSortingEnabled(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        table.verticalHeader().setVisible(False)
        table.setFocusPolicy(Qt.NoFocus)
        table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)

    def export_pdf(self):
            print("DEBUG: Bắt đầu xuất PDF")
            table = self.view.import_invoice_tableWidget
            selected_row = table.currentRow()

            if selected_row < 0:
                QMessageBox.warning(self.view, "Cảnh báo", "Vui lòng chọn phiếu cần in!")
                return
            import_code_item = table.item(selected_row, 0)
            if not import_code_item:
                 return
            import_code = import_code_item.text()

            invoice_info_row = self.query_data.get_invoice_information(import_code)
            invoice_details_rows = self.query_data.get_product_import_detail(import_code)

            if not invoice_info_row or not invoice_details_rows:
                QMessageBox.critical(self.view, "Lỗi", "Không tìm thấy dữ liệu của phiếu này.")
                return

            invoice_info = dict(invoice_info_row)
            invoice_type = invoice_info.get('invoice_type', '').lower()
            if invoice_type == 'phiếu hủy':
                prefix = "PhieuHuy"
            else:
                prefix = "PhieuNhap"
            invoice_details = []
            for row in invoice_details_rows:
                row_dict = dict(row)
                if 'type_name' in row_dict and 'product_type' not in row_dict:
                     row_dict['product_type'] = row_dict['type_name']
                invoice_details.append(row_dict)
            default_filename = f"{prefix}_{import_code}_{QDateTime.currentDateTime().toString('yyyyMMdd_hhmmss')}.pdf"
            file_path, _ = QFileDialog.getSaveFileName(
                self.view,
                "Lưu Phiếu Nhập",
                default_filename,
                "PDF Files (*.pdf)"
            )

            if file_path:
                try:
                    success = self.pdf_service.export_import_invoice(file_path, invoice_info, invoice_details)
                    if success:
                        QMessageBox.information(self.view, "Thành công", f"Đã xuất file PDF thành công tới:\n{file_path}")

                    else:
                         QMessageBox.warning(self.view, "Cảnh báo", "Có lỗi xảy ra trong quá trình tạo file PDF.")
                except Exception as e:
                    print(f"Lỗi xuất PDF Controller: {e}")
                    QMessageBox.critical(self.view, "Lỗi Exception", f"Lỗi không mong muốn:\n{e}")

