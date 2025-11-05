from PyQt5 import uic
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QAbstractScrollArea, QDialog, \
    QMessageBox, QLabel
from src.services.query_data_manager.manager_query_data import QueryData
from src.controllers.manager_main_controller.employee_controller import employeeController


class EmployeeViewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Lấy các widget cần thiết từ cửa sổ cha (ManagerMainWindow)
        self.employee_tableWidget = parent.employee_tableWidget
        self.quit_employee_btn = parent.quit_employee_btn
        self.update_employee_btn = parent.update_employee_btn
        self.add_employee_btn = parent.add_employee_btn

        viewport = self.employee_tableWidget.viewport()
        self.placeholder_label = QLabel("Không tìm thấy dữ liệu phù hợp", viewport)
        self.placeholder_label.setStyleSheet("border-radius: none; background: #ffffff;")
        self.placeholder_label.setAlignment(Qt.AlignCenter)
        self.placeholder_label.setStyleSheet("color: grey; font-size: 14px;")
        self.placeholder_label.setWordWrap(True)
        self.placeholder_label.hide()

        self.parent().installEventFilter(self)
        self.employee_tableWidget.installEventFilter(self)

        self.employee_controller = employeeController(parent, self)



        self.add_employee_btn.clicked.connect(lambda: self.employee_controller.open_add_employee_dialog())
        self.quit_employee_btn.clicked.connect(lambda: self.employee_controller.handle_quit_employee())
        self.update_employee_btn.clicked.connect(lambda: self.employee_controller.open_update_employee_dialog())

        self.employee_tableWidget.itemSelectionChanged.connect(self.handle_selection_change)

        # Kết nối tín hiệu (signals) với các hành động (slots)
        self.employee_tableWidget.itemSelectionChanged.connect(self.handle_selection_change)

    def handle_selection_change(self):
        """Kích hoạt/Vô hiệu hóa các nút dựa trên lựa chọn trong bảng."""
        selected_rows = self.employee_tableWidget.selectionModel().selectedRows()
        is_selection_non_empty = bool(selected_rows)

        employee_data = self.get_selected_employee_data()

        can_modify = is_selection_non_empty

        if employee_data:
            # Vô hiệu hóa nút nếu trạng thái là "đã nghỉ"
            if employee_data.get("status", "").lower() == "đã nghỉ":
                can_modify = False

        # Thiết lập trạng thái cho nút
        self.quit_employee_btn.setEnabled(can_modify) # Không thể cho nhân viên "đã nghỉ" nghỉ thêm lần nữa
        self.update_employee_btn.setEnabled(can_modify) # Không thể sửa thông tin nhân viên "đã nghỉ" trừ khi có logic khác
        self.add_employee_btn.setEnabled(True) # Nút thêm luôn được kích hoạt

        # Nếu không có dòng nào được chọn, cả hai nút đều bị vô hiệu hóa
        if not is_selection_non_empty:
             self.quit_employee_btn.setEnabled(False)
             self.update_employee_btn.setEnabled(False)

    def eventFilter(self, obj, event):
        table = self.employee_tableWidget
        if (obj == table or obj == table.viewport()) and event.type() == QEvent.Resize:
            self.placeholder_label.resize(table.viewport().size())
        if obj == self.parent() and event.type() == QEvent.MouseButtonPress:
            mapped_pos = self.mapFromParent(event.pos())
            table_rect = table.geometry()

            # Nếu click ngoài bảng -> bỏ chọn
            if not table_rect.contains(mapped_pos):
                table.clearSelection()

        return super().eventFilter(obj, event)

    def get_selected_employee_data(self):
        selected_rows = self.employee_tableWidget.selectionModel().selectedRows()
        if not selected_rows:
            return None
        row_index = selected_rows[0].row()
        headers = ["employee_id", "name", "gender", "role", "status", "email", "phone_number", "address", "start_date", "end_date"]
        employee_data = {}
        table = self.employee_tableWidget
        for col_index in range(table.columnCount()):
            item = table.item(row_index, col_index)
            if item is not None:
                # Sử dụng header làm key, và giá trị ô làm value
                key = headers[col_index]
                value = item.text().lower()
                employee_data[key] = value
        employee_data["name"] = employee_data["name"].capitalize()
        return employee_data

    def populate_employee_table(self, data):
        if not data:
            self.employee_tableWidget.setRowCount(0)
            self.placeholder_label.resize(self.employee_tableWidget.viewport().size())
            self.placeholder_label.show()
        else:
            self.placeholder_label.hide()
            print(f"--- DEBUG: Đang cập nhật bảng: {self.employee_tableWidget.objectName()} ---")
            print("---DEBUG: DATA HIỂN THỊ TRÊN BẢNG---")
            print(data)
            table = self.employee_tableWidget
            capitalize_columns = [2, 3, 4]
            headers = ["Mã nhân viên", "Tên", "Giới tính", "Chức danh", "Trạng thái", "Email", "Số điện thoại", "Địa chỉ", "Ngày vào làm", "Ngày nghỉ việc"]
            table.setColumnCount(len(headers))
            table.setHorizontalHeaderLabels(headers)
            # Giả sử bảng của bạn tên là 'employee_table'
            self.employee_tableWidget.setRowCount(len(data))
            for row_index, row_data in enumerate(data):
                print(f"DEBUG HÀNG {row_index}: {list(row_data)}")
                for col_index, cell_data in enumerate(row_data):
                    display_text = ""
                    if col_index in capitalize_columns:
                        display_text = str(cell_data).capitalize()
                    else:
                        display_text = str(cell_data)
                    item = QTableWidgetItem(display_text)
                    table.setItem(row_index, col_index, item)
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
            table.setSelectionMode(QAbstractItemView.SingleSelection)