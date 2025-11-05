from PyQt5 import uic
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QTableWidgetItem, QAbstractItemView, QHeaderView, QAbstractScrollArea, QLabel
from src.services.query_data_manager.manager_query_data import QueryData
from src.controllers.manager_main_controller.product_controller import productController

class ProductViewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Lấy các widget cần thiết từ cửa sổ cha (ManagerMainWindow)
        self.product_tableWidget = parent.product_tableWidget
        self.stop_product_btn = parent.stop_product_btn
        self.update_product_btn = parent.update_product_btn
        self.add_product_btn = parent.add_product_btn

        viewport = self.product_tableWidget.viewport()
        self.placeholder_label = QLabel("Không tìm thấy dữ liệu phù hợp", viewport)
        self.placeholder_label.setStyleSheet("border-radius: none; background: #ffffff;")
        self.placeholder_label.setAlignment(Qt.AlignCenter)
        self.placeholder_label.setStyleSheet("color: grey; font-size: 14px;")
        self.placeholder_label.setWordWrap(True)
        self.placeholder_label.hide()

        self.parent().installEventFilter(self)
        self.product_tableWidget.installEventFilter(self)
        self.product_controller = productController(parent,self)

        self.add_product_btn.clicked.connect(self.product_controller.open_add_product_dialog)
        self.stop_product_btn.clicked.connect(self.product_controller.handle_stop_selling)
        self.update_product_btn.clicked.connect(self.product_controller.open_update_product_dialog)

        self.query_data = self.product_controller.query_data

        # Kết nối tín hiệu (signals) với các hành động (slots)
        self.product_tableWidget.itemSelectionChanged.connect(self.handle_selection_change)

    def populate_table(self,data):
        print(f"DEBUG (ProductView): data product: {data}")
        if not data:
            print("Không có dữ liệu sản phẩm")
            self.product_tableWidget.setRowCount(0) # Xóa bảng
            self.placeholder_label.resize(self.product_tableWidget.viewport().size())
            self.placeholder_label.show()           # Hiện label
            return # Dừng lại
        else:
            # Nếu có data, ẩn label đi
            self.placeholder_label.hide()
        table = self.product_tableWidget
        headers = ["Mã sản phẩm", "Tên sản phẩm", "Loại", "Giá bán", "Giá nhập", "Tồn kho", "Trạng thái", "Hình ảnh"]
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setRowCount(len(data))

        image_col_index = headers.index("Hình ảnh")     # 7
        price_col_index = headers.index("Giá bán")    # 3
        cost_col_index = headers.index("Giá nhập")      # 4
        stock_col_index = headers.index("Tồn kho")      # 5

        for row_index, row_data in enumerate(data):
            image_path_to_store = str(row_data[image_col_index])
            for col_index, cell_data in enumerate(row_data):
                item = None # Khởi tạo item
                if col_index == image_col_index:
                    # Cột hình ảnh: Dùng setCellWidget, không tạo item
                    if image_path_to_store:
                        image_label = QLabel()
                        image_label.setAlignment(Qt.AlignCenter)
                        image_label.setStyleSheet("background-color: transparent;")
                        pixmap = QPixmap(image_path_to_store)
                        scaled_pixmap = pixmap.scaledToHeight(60, Qt.SmoothTransformation)
                        image_label.setPixmap(scaled_pixmap)
                        table.setCellWidget(row_index, col_index, image_label)

                elif col_index == price_col_index or col_index == cost_col_index:
                    # Cột giá: Format tiền
                    try:
                        numeric_value = int(float(cell_data))
                        display_text = f"{numeric_value:,}đ".replace(",", ".")
                    except (ValueError, TypeError):
                        display_text = str(cell_data) if cell_data is not None else ""
                    item = QTableWidgetItem(display_text)
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

                elif col_index == stock_col_index:
                    # Cột tồn kho
                    display_text = str(cell_data)
                    item = QTableWidgetItem(display_text)
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

                else:
                    # Các cột text bình thường
                    item = QTableWidgetItem(str(cell_data))
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

                # Nếu có item được tạo (tức là không phải cột hình ảnh)
                if item is not None:
                    table.setItem(row_index, col_index, item)

                    # 2. KIỂM TRA: Nếu đây là cột 0, GẮN DỮ LIỆU
                    if col_index == 0:
                        # 3. "Giấu" image_path vào UserRole của ô "Mã sản phẩm"
                        item.setData(Qt.UserRole, image_path_to_store)

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

        for i in range(table.columnCount()):
            if i == image_col_index:
                # Đặt chiều rộng tối thiểu cho cột hình ảnh hoặc co giãn theo nội dung
                table.setColumnWidth(i, 80)
            else:
                table.horizontalHeader().setSectionResizeMode(i, QHeaderView.Stretch)
        table.resizeRowsToContents()

    def load_product_data(self):
        if not self.query_data:
            print("LỖI (ProductView): QueryData chưa được set.")
            return
        data = self.query_data.get_data_product()
        self.populate_table(data)

    def handle_selection_change(self):
        """Kích hoạt/Vô hiệu hóa các nút dựa trên lựa chọn trong bảng."""
        selected_rows = self.product_tableWidget.selectionModel().selectedRows()
        is_selection_non_empty = bool(selected_rows)
        self.stop_product_btn.setEnabled(is_selection_non_empty)
        self.update_product_btn.setEnabled(is_selection_non_empty)

    def eventFilter(self, obj, event):
        table = self.product_tableWidget
        if obj == self.parent() and event.type() == QEvent.MouseButtonPress:
            mapped_pos = self.mapFromParent(event.pos())
            table_rect = table.geometry()

            # Nếu click ngoài bảng -> bỏ chọn
            if not table_rect.contains(mapped_pos):
                table.clearSelection()

        return super().eventFilter(obj, event)

    def get_selected_product_data(self):
            selected_rows = self.product_tableWidget.selectionModel().selectedRows()
            if not selected_rows:
                return None

            row_index = selected_rows[0].row()
            table = self.product_tableWidget

            product_data = {
                "product_id": table.item(row_index, 0).text(),
                "product_name": table.item(row_index, 1).text(),
                "type": table.item(row_index, 2).text(),
                # Khi đọc giá, phải xóa 'đ' và '.' đi để lấy số thô
                "selling_price": table.item(row_index, 3).text().replace(".", "").replace("đ", ""),
                "import_price": table.item(row_index, 4).text().replace(".", "").replace("đ", ""),
                "stock": table.item(row_index, 5).text(),
                "status": table.item(row_index, 6).text()
            }

            # 2. Lấy item của cột "Mã sản phẩm" (cột 0)
            id_item = table.item(row_index, 0)
            if id_item:
                # 3. Lấy image_path đã "giấu" từ UserRole
                image_path = id_item.data(Qt.UserRole)

                # 4. Thêm key 'image_path' vào dictionary
                product_data["image_path"] = image_path
            else:
                # Dự phòng trường hợp không lấy được
                product_data["image_path"] = None

            print(f"DEBUG: Đã lấy data để update: {product_data}")
            return product_data