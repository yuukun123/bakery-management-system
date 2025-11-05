from PyQt5.QtCore import Qt, QEvent, QTimer
from PyQt5.QtWidgets import (QMessageBox, QTableWidgetItem,
                             QAbstractItemView)

from src.services.query_data_employee.employee_query_data import EmployeeQueryData
from src.constants.table_header import PRODUCT_HEADER

class WarehouseController():
    def __init__(self, parent):
        self.customer_info = {}
        self.parent = parent
        self._initialized = False
        self.query_data = EmployeeQueryData()

        self.filter_CB = self.parent.filter_CB_2
        self.search_product = self.parent.search_product_2
        self.search_product_btn = self.parent.search_product_btn_2
        self.table = self.parent.table_warehouse

        # Timer này chỉ dùng để tự động reset bảng khi ô tìm kiếm rỗng
        self.reset_timer = QTimer(self.parent)
        self.reset_timer.setSingleShot(True)
        self.reset_timer.timeout.connect(self.apply_product_filters)

    def setup_page(self):
        if not self._initialized:
            print("DEBUG: WarehouseController setup is running for the first time.")
            self.setup_ui_connections()
            self._setup_table_header_and_properties()
            self.load_product_types_into_combobox()
            self.apply_product_filters()
            self._initialized = True

    def setup_ui_connections(self):
        """Kết nối tất cả các signal và slot cho trang này."""
        self.filter_CB.currentIndexChanged.connect(self.apply_product_filters)
        self.search_product_btn.clicked.connect(self.apply_product_filters)
        # Kết nối này để theo dõi khi nào ô tìm kiếm bị xóa rỗng
        self.search_product.textChanged.connect(self.on_search_text_changed)

    def _setup_table_header_and_properties(self):
        if not self.table:
            print("WARNING: Không tìm thấy QTableWidget.")
            return

        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.table.setColumnCount(len(PRODUCT_HEADER))
        self.table.setHorizontalHeaderLabels(PRODUCT_HEADER)

    def load_product_types_into_combobox(self):
        print("DEBUG: Loading product types into ComboBox...")
        self.filter_CB.blockSignals(True)
        try:
            self.filter_CB.clear()
            self.filter_CB.addItem("Tất cả các loại", 0)
            product_types = self.query_data.get_all_product_types()
            if product_types:
                for p_type in product_types:
                    type_name = p_type.get('type_name')
                    type_id = p_type.get('type_id')
                    self.filter_CB.addItem(type_name, type_id)
        finally:
            self.filter_CB.blockSignals(False)

    def apply_product_filters(self):
        selected_type_id = self.filter_CB.currentData()
        keyword = self.search_product.text().strip()
        print(f"DEBUG: Applying filters -> Type ID: {selected_type_id}, Keyword: '{keyword}'")

        products = self.query_data.filter_products_for_warehouse(
            type_id=selected_type_id,
            keyword=keyword
        )

        if products is None:
            QMessageBox.critical(self.parent, "Lỗi", "Có lỗi xảy ra khi truy vấn dữ liệu sản phẩm.")
            self.load_product_data([])
            return

        self.load_product_data(products)

    def on_search_text_changed(self, text):
        """
        Chỉ kích hoạt bộ lọc tự động KHI VÀ CHỈ KHI ô tìm kiếm trở nên rỗng.
        """
        self.reset_timer.stop()
        if not text.strip():
            # Nếu ô rỗng, khởi động timer để tự động reset lại bảng
            print("DEBUG: Search input is empty. Starting auto-reset timer...")
            self.reset_timer.start(500)
        # Nếu có chữ, không làm gì cả, chờ người dùng nhấn nút.

    def load_product_data(self, products_to_display):
        all_products = products_to_display
        if not all_products:
            self.table.setRowCount(0)
            return

        self.table.setRowCount(len(all_products))
        column_order = [
            'product_id',
            'product_name',
            'type_name',
            'stock',
            'selling_price',
        ]

        for row_index, product_dict in enumerate(all_products):
            for col_index, key in enumerate(column_order):
                value = product_dict.get(key)
                display_text = ""
                if value is not None:
                    if key == 'selling_price':
                        try:
                            display_text = f"{int(value):,}"
                        except (ValueError, TypeError):
                            display_text = "0"
                    else:
                        display_text = str(value)
                item = QTableWidgetItem(display_text)
                item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_index, col_index, item)