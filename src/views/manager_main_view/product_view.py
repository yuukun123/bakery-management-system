from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QAbstractScrollArea, QLabel
from src.services.query_data_manager.manager_query_data import QueryData

class ProductViewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Lấy các widget cần thiết từ cửa sổ cha (ManagerMainWindow)
        self.product_tableWidget = parent.product_tableWidget
        self.delete_product_btn = parent.delete_product_btn
        self.update_product_btn = parent.update_product_btn

        # Khởi tạo các service cần thiết
        self.query_data = QueryData()

        # Tải dữ liệu
        self.load_product_data()

        # Kết nối tín hiệu (signals) với các hành động (slots)
        self.product_tableWidget.itemSelectionChanged.connect(self.handle_selection_change)

    def load_product_data(self):
        data = self.query_data.get_data_product()
        print(f"DEBUG (EmployeeView): data product: {data}")
        if not data:
            print("Không có dữ liệu sản phẩm")
            self.product_tableWidget.setRowCount(0) # Xóa dữ liệu cũ nếu không có dữ liệu mới
            return

        table = self.product_tableWidget
        headers = ["Mã sản phẩm", "Tên sản phẩm", "Giá bán", "Giá nhập", "Tồn kho", "Trạng thái", "Hình ảnh"]
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setRowCount(len(data))
        image_col_index = headers.index("Hình ảnh")
        for row_index, row_data in enumerate(data):
            for col_index, cell_data in enumerate(row_data):
                if col_index == image_col_index:
                    image_path = str(cell_data)
                    if image_path:
                        image_label = QLabel()
                        image_label.setAlignment(Qt.AlignCenter)
                        pixmap = QPixmap(image_path)
                        scaled_pixmap = pixmap.scaledToHeight(60, Qt.SmoothTransformation)
                        image_label.setPixmap(scaled_pixmap)
                        table.setCellWidget(row_index, col_index, image_label)
                else:
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

        for i in range(table.columnCount()):
            if i == image_col_index:
                # Đặt chiều rộng tối thiểu cho cột hình ảnh hoặc co giãn theo nội dung
                table.setColumnWidth(i, 80)
            else:
                table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch) 
        table.resizeRowsToContents()

    def handle_selection_change(self):
        """Kích hoạt/Vô hiệu hóa các nút dựa trên lựa chọn trong bảng."""
        selected_rows = self.product_tableWidget.selectionModel().selectedRows()
        is_selection_non_empty = bool(selected_rows)
        self.delete_product_btn.setEnabled(is_selection_non_empty)
        self.update_product_btn.setEnabled(is_selection_non_empty)