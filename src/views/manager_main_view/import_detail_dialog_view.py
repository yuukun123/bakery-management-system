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
        self.cancel_btn.clicked.connect(self.reject)
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



