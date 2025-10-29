from PyQt5 import uic
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QAbstractScrollArea, QDialog, \
    QMessageBox
from src.services.query_data_manager.manager_query_data import QueryData
from src.controllers.manager_main_controller.employee_controller import open_add_employee_dialog

class EmployeeViewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Lấy các widget cần thiết từ cửa sổ cha (ManagerMainWindow)
        self.employee_tableWidget = parent.employee_tableWidget
        self.delete_employee_btn = parent.delete_employee_btn
        self.update_employee_btn = parent.update_employee_btn
        self.add_employee_btn = parent.add_employee_btn

        self.parent().installEventFilter(self)

        self.add_employee_btn.clicked.connect(lambda: open_add_employee_dialog(parent))

        # Khởi tạo các service cần thiết
        self.query_data = QueryData()

        # Tải dữ liệu
        self.load_employee_data()

        # Kết nối tín hiệu (signals) với các hành động (slots)
        self.employee_tableWidget.itemSelectionChanged.connect(self.handle_selection_change)

    def load_employee_data(self):
        data = self.query_data.get_data_manager()
        print(f"DEBUG (EmployeeView): data manager: {data}")
        if not data:
            print("Không có dữ liệu nhân viên")
            self.employee_tableWidget.setRowCount(0) # Xóa dữ liệu cũ nếu không có dữ liệu mới
            return

        table = self.employee_tableWidget
        headers = ["Mã nhân viên", "Tên", "Giới tính", "Chức danh", "Trạng thái", "Email", "Số điện thoại", "Địa chỉ", "Ngày vào làm", "Ngày nghỉ việc"]
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setRowCount(len(data))

        for row_index, row_data in enumerate(data):
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                table.setItem(row_index, col_index, item)

        # Cấu hình giao diện cho bảng
        table.resizeColumnsToContents()
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setAlternatingRowColors(True)
        table.setSortingEnabled(True)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        table.verticalHeader().setVisible(False)
        table.setFocusPolicy(Qt.NoFocus)
        table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)

    def handle_selection_change(self):
        """Kích hoạt/Vô hiệu hóa các nút dựa trên lựa chọn trong bảng."""
        selected_rows = self.employee_tableWidget.selectionModel().selectedRows()
        is_selection_non_empty = bool(selected_rows)
        self.delete_employee_btn.setEnabled(is_selection_non_empty)
        self.update_employee_btn.setEnabled(is_selection_non_empty)

    def eventFilter(self, obj, event):
        table = self.employee_tableWidget
        if obj == self.parent() and event.type() == QEvent.MouseButtonPress:
            mapped_pos = self.mapFromParent(event.pos())
            table_rect = table.geometry()

            # Nếu click ngoài bảng -> bỏ chọn
            if not table_rect.contains(mapped_pos):
                table.clearSelection()

        return super().eventFilter(obj, event)

