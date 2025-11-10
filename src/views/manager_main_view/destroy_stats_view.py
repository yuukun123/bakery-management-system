import numpy as np
from PyQt5.QtCore import QDate, Qt, QEvent
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy, QHeaderView, QTableWidgetItem, QAbstractItemView, \
    QAbstractScrollArea, QLabel
from src.services.query_data_manager.manager_query_data import QueryData


class DestroyStatsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = parent
        self.query_data = QueryData()
        self.init_table()

        self.placeholder = QLabel("Không tìm thấy dữ liệu phù hợp", self.ui.table_destroyed_product.viewport())
        self.setup_placeholder(self.placeholder)

        self.ui.table_destroyed_product.viewport().installEventFilter(self)

    def setup_placeholder(self, label):
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: grey; font-size: 14px; background: white;")
        label.hide()

    def eventFilter(self, source, event):
        if event.type() == QEvent.Resize and source == self.ui.table_destroyed_product.viewport():
            self.placeholder.resize(event.size())
        return super().eventFilter(source, event)

    def init_table(self):
        table = self.ui.table_destroyed_product
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Mã SP", "Tên Sản Phẩm", "Số Lượng Hủy", "Ngày hủy"])
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

    def update_stats(self):
        start_date, end_date = self.get_date_range()
        self.update_table(start_date, end_date)

    def update_table(self, start_date, end_date):
        rows = self.query_data.get_destroyed_product(start_date, end_date)
        table = self.ui.table_destroyed_product
        table.setRowCount(0)

        if not rows:
            self.placeholder.show()
            self.placeholder.resize(table.viewport().size())
            return
        else:
            self.placeholder.hide()

        for r_idx, row_data in enumerate(rows):
            table.insertRow(r_idx)
            for c_idx, val in enumerate(row_data):
                text = str(val)
                if c_idx == 2:
                     text = f"{int(val):,}"
                item = QTableWidgetItem(text)
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

                table.setItem(r_idx, c_idx, item)
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

    def get_date_range(self):
        time_option = self.ui.time_statiscal_destroy.currentText()
        today = QDate.currentDate()
        start_date = today
        end_date = today

        if time_option == "Hôm nay":
            pass
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
             start_date = self.ui.date_option_destroy.date()
             end_date = start_date

        return start_date.toString("yyyy-MM-dd"), end_date.toString("yyyy-MM-dd")