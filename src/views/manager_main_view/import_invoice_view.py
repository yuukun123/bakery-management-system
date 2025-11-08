from PyQt5 import uic
from PyQt5.QtCore import Qt, QEvent, QDate
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QAbstractScrollArea, QLabel
from  src.controllers.manager_main_controller.import_invoice_controller import ImportInvoiceController
from  src.services.query_data_manager.manager_query_data import QueryData

class ImportInvoiceViewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Lấy các widget cần thiết từ cửa sổ cha (ManagerMainWindow)
        self.import_invoice_tableWidget = parent.import_invoice_tableWidget
        self.detail_btn = parent.detail_btn
        self.export_btn = parent.export_btn
        self.comboBox_employee = parent.comboBox_employee
        self.from_date = parent.from_date
        self.to_date = parent.to_date
        self.query_data = QueryData()
        self.load_employee_comboBox()
        self.detail_btn.setEnabled(False)

        today = QDate.currentDate()
        oldest_date_str = self.query_data.get_date_oldest_import_invoice()
        if oldest_date_str:
            oldest_date = QDate.fromString(oldest_date_str, "yyyy-MM-dd")
        else:
            oldest_date = QDate(today.year(), today.month(), 1)
        self.from_date.setDate(oldest_date)
        self.to_date.setDate(today)
        self.from_date.setMaximumDate(today)
        self.to_date.setMinimumDate(oldest_date)

        viewport = self.import_invoice_tableWidget.viewport()
        self.placeholder_label = QLabel("Không tìm thấy dữ liệu phù hợp", viewport)
        self.placeholder_label.setStyleSheet("border-radius: none; background: #ffffff;")
        self.placeholder_label.setAlignment(Qt.AlignCenter)
        self.placeholder_label.setStyleSheet("color: grey; font-size: 14px;")
        self.placeholder_label.setWordWrap(True)
        self.placeholder_label.hide()

        self.parent().installEventFilter(self)
        self.import_invoice_tableWidget.installEventFilter(self)
        self.import_invoice_tableWidget.viewport().installEventFilter(self)
        self.import_invoice_controller = ImportInvoiceController(parent,self)

        self.detail_btn.clicked.connect(self.import_invoice_controller.open_import_detail_dialog)

        self.import_invoice_tableWidget.itemSelectionChanged.connect(self.handle_selection_change)

    def import_invoice_table(self,data):
        print(f"DEBUG (importInvoiceView): import invoice product: {data}")
        if not data:
            print("Không có dữ liệu sản phẩm")
            self.import_invoice_tableWidget.setRowCount(0) # Xóa bảng
            self.placeholder_label.resize(self.import_invoice_tableWidget.viewport().size())
            self.placeholder_label.show()
            return
        else:
            self.placeholder_label.hide()
        table = self.import_invoice_tableWidget
        headers = ["Mã phiếu", "Loại phiếu", "Nhân viên tạo", "Thời gian tạo", "Tổng tiền"]
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setRowCount(len(data))

        price_col_index = headers.index("Tổng tiền")

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

    def handle_selection_change(self):
        selected_rows = self.import_invoice_tableWidget.selectionModel().selectedRows()
        is_selection_non_empty = bool(selected_rows)
        self.detail_btn.setEnabled(is_selection_non_empty)


    def eventFilter(self, obj, event):
        table = self.import_invoice_tableWidget
        try:
            if not table or not table.viewport():
                return super().eventFilter(obj, event)
        except RuntimeError:
            return super().eventFilter(obj, event)
        if (obj == table or obj == table.viewport()) and event.type() == QEvent.Resize:
            self.placeholder_label.resize(table.viewport().size())
        if obj == self.parent() and event.type() == QEvent.MouseButtonPress:
            mapped_pos = self.mapFromParent(event.pos())
            table_rect = table.geometry()

            # Nếu click ngoài bảng -> bỏ chọn
            if not table_rect.contains(mapped_pos):
                table.clearSelection()

        return super().eventFilter(obj, event)

    def load_employee_comboBox(self):
        try:
            self.comboBox_employee.addItem("Tất cả")
            employees = self.query_data.get_all_name_employee()
            for name in employees:
                self.comboBox_employee.addItem(name[0])
        except Exception as e:
            print(f"Lỗi khi nạp nhân viên: {e}")


