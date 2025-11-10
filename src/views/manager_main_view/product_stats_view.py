import numpy as np
from PyQt5.QtCore import QDate, Qt, QEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QHeaderView, QTableWidgetItem, QAbstractItemView, \
    QAbstractScrollArea, QLabel
from src.services.query_data_manager.manager_query_data import QueryData


class ProductStatsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = parent
        self.query_data = QueryData()
        self.init_best_seller_table()
        self.init_low_table()

        # Placeholder cho bảng Best Seller
        self.placeholder_best = QLabel("Không tìm thấy dữ liệu phù hợp", self.ui.table_best_seller_product)
        self.setup_placeholder(self.placeholder_best)

        # Placeholder cho bảng Low Product
        self.placeholder_low = QLabel("Không tìm thấy dữ liệu phù hợp", self.ui.table_low_product)
        self.setup_placeholder(self.placeholder_low)

        self.ui.table_best_seller_product.viewport().installEventFilter(self)
        self.ui.table_low_product.viewport().installEventFilter(self)

    def setup_placeholder(self, label):
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: grey; font-size: 14px; background: transparent;")
        label.hide()

    def eventFilter(self, source, event):
        if event.type() == QEvent.Resize:
            if source == self.ui.table_best_seller_product.viewport():
                self.placeholder_best.resize(event.size())
            elif source == self.ui.table_low_product.viewport():
                self.placeholder_low.resize(event.size())
        return super().eventFilter(source, event)

    def init_best_seller_table(self):
        table = self.ui.table_best_seller_product
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Mã SP", "Tên Sản Phẩm", "Loại", "Số Lượng bán ", "Tổng Tiền bán"])

        # Tùy chỉnh độ rộng cột cho đẹp
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

    def init_low_table(self):
        table = self.ui.table_low_product
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Mã SP", "Tên Sản Phẩm", "Loại", "Số Lượng bán ", "Tổng Tiền bán"])

        # Tùy chỉnh độ rộng cột cho đẹp
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)

    def update_best_seller_table(self):
        rows = self.load_top_5_best_seller_data()
        print(f"DEBUG: DATA FOR TOP 5 BEST SELLER: {rows}")
        table = self.ui.table_best_seller_product
        table.setRowCount(0)

        if not rows:
            self.placeholder_best.show()
            self.placeholder_best.setGeometry(table.rect())
            return
        else:
            self.placeholder_best.hide()

        for row_idx, row_data in enumerate(rows):
            table.insertRow(row_idx)
            for col_idx, data in enumerate(row_data):
                if col_idx == 3:
                    text = f"{int(data):,}"
                elif col_idx == 4:
                    text = f"{int(data):,}đ"
                else:
                    text = str(data)

                item = QTableWidgetItem(text)
                if col_idx in [3, 4]:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                table.setItem(row_idx, col_idx, item)
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

    def update_low_product_table(self):
        rows = self.load_top_5_low_product_data()
        print(f"DEBUG: DATA FOR TOP 5 BEST SELLER: {rows}")
        table = self.ui.table_low_product
        table.setRowCount(0)

        if not rows:
            self.placeholder_low.show()
            self.placeholder_low.setGeometry(table.rect())
            return
        else:
            self.placeholder_low.hide()

        for row_idx, row_data in enumerate(rows):
            table.insertRow(row_idx)
            for col_idx, data in enumerate(row_data):
                if col_idx == 3:
                    text = f"{int(data):,}"
                elif col_idx == 4:
                    text = f"{int(data):,}đ"
                else:
                    text = str(data)

                item = QTableWidgetItem(text)
                if col_idx in [3, 4]:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

                table.setItem(row_idx, col_idx, item)
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

    def load_top_5_best_seller_data(self):
        today = QDate.currentDate()
        time_option = self.ui.time_statiscal_product.currentText()

        start_date = today
        end_date = today

        if time_option == "Hôm nay":
            start_date = today
            end_date = today
        elif time_option == "Tuần này":
            start_date = today.addDays(-(today.dayOfWeek() - 1))
            end_date = start_date.addDays(6)
        elif time_option == "Tháng này":
            start_date = QDate(today.year(), today.month(), 1)
            end_date = start_date.addMonths(1).addDays(-1)
        elif time_option == "Năm này":
            start_date = QDate(today.year(), 1, 1)
            end_date = QDate(today.year(), 12, 31)
        elif time_option == "Tùy chỉnh":
             # Nếu chỉ chọn 1 ngày
             start_date = self.ui.dateOption.date()
             end_date = start_date

        # Gọi truy vấn với chuỗi ngày đã chuẩn hóa
        values = self.query_data.get_5_best_seller_product(
            start_date.toString("yyyy-MM-dd"),
            end_date.toString("yyyy-MM-dd")
        )
        return values

    def load_top_5_low_product_data(self):
        today = QDate.currentDate()
        time_option = self.ui.time_statiscal_product.currentText()

        start_date = today
        end_date = today

        if time_option == "Hôm nay":
            start_date = today
            end_date = today
        elif time_option == "Tuần này":
            start_date = today.addDays(-(today.dayOfWeek() - 1))
            end_date = start_date.addDays(6)
        elif time_option == "Tháng này":
            start_date = QDate(today.year(), today.month(), 1)
            end_date = start_date.addMonths(1).addDays(-1)
        elif time_option == "Năm này":
            start_date = QDate(today.year(), 1, 1)
            end_date = QDate(today.year(), 12, 31)
        elif time_option == "Tùy chỉnh":
             # Nếu chỉ chọn 1 ngày
             start_date = self.ui.dateOption.date()
             end_date = start_date

        # Gọi truy vấn với chuỗi ngày đã chuẩn hóa
        values = self.query_data.get_5_low_product(
            start_date.toString("yyyy-MM-dd"),
            end_date.toString("yyyy-MM-dd")
        )
        return values
