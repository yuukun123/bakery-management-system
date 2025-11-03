from PyQt5.QtCore import Qt, QEvent, QObject
from PyQt5.QtWidgets import (QMessageBox, QTableWidgetItem,
                             QAbstractItemView)

from src.services.query_data_employee.employee_query_data import EmployeeQueryData
from src.constants.table_header import PRODUCT_HEADER
from src.utils.validators import is_valid_phone_number

class WarehouseController(QObject):
    def __init__(self, parent):
        super().__init__(parent)
        self.customer_info = {}
        self.parent = parent
        self._initialized = False  # Cờ để chắc rằng chúng ta chỉ setup 1 lần
        self.query_data = EmployeeQueryData()

        self.filter_CB = self.parent.filter_CB_2
        self.search_product = self.search_product_2
        self.search_product_btn = self.search_product_btn_2

        self.table = self.parent.table_warehouse

    def setup_page(self):
        """
        Hàm này sẽ được gọi từ MainWindow để thiết lập toàn bộ trang.
        """
        if not self._initialized:
            print("DEBUG: ProductController setup is running for the first time.")
            self.setup_ui_connections()
            self._setup_table_header_and_properties()
            self._install_event_filter()
            self.load_customer_data()
            self._initialized = True

    def setup_ui_connections(self):
        """Kết nối tất cả các signal và slot cho trang này."""
        # self.search_customer_btn_2.clicked.connect(self.search_customer_with_phone)
        # print("DEBUG: Checkout button connected to show_checkout_page.")
        # self.show_update_customer_btn.clicked.connect(self.toggle_show_add_customer)
        # print("DEBUG: Cancel button connected to show_product_selection_page.")
        # self.update_customer_btn.clicked.connect(self.handle_update_customer_infor)
        # print("DEBUG: Cancel button connected to show_product_selection_page.")
        # self.table.selectionModel().selectionChanged.connect(self.handle_selection_change)

    def _setup_table_header_and_properties(self):
        if not self.table:
            print("WARNING: Không tìm thấy QTableWidget.")
            return

            # YÊU CẦU 1: CHỌN CẢ DÒNG KHI CLICK
            # --------------------------------------------------
            # setSelectionBehavior sẽ quyết định đơn vị lựa chọn là Ô (Item), Dòng (Row), hay Cột (Column)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        print("DEBUG: Table selection behavior set to SelectRows.")
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)

        self.table.setColumnCount(len(PRODUCT_HEADER))
        self.table.setHorizontalHeaderLabels(PRODUCT_HEADER)

    def _install_event_filter(self):
        """Cài đặt bộ lọc sự kiện cho cửa sổ chính để xử lý click ngoài bảng."""
        # Dòng này bây giờ sẽ hoạt động
        self.parent.installEventFilter(self)
        print("DEBUG: [CustomerController] Event filter installed on MainWindow.")

    def clear_table_selection(self):
        """Phương thức công khai để xóa lựa chọn trên bảng."""
        if self.table:
            self.table.clearSelection()
            print("DEBUG: [CustomerController] Table selection cleared.")

    # --- BƯỚC 4: THÊM HÀM eventFilter VÀO ---
    def eventFilter(self, source, event):
        """
        Bộ lọc sự kiện, sẽ được gọi cho mọi sự kiện trên self.parent (MainWindow).
        """
        # Chỉ quan tâm đến sự kiện click chuột trái
        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
            # Kiểm tra xem con trỏ chuột có đang nằm trên bảng không
            if not self.table.underMouse():
                # Nếu không, và nếu bảng đang có lựa chọn
                if self.table.selectionModel().hasSelection():
                    # Xóa lựa chọn
                    self.clear_table_selection()

        # Rất quan trọng: Trả về False để các sự kiện được xử lý bình thường
        return super().eventFilter(source, event)

    def load_customer_data(self):
        product_data = self.query_data.get_product_stock()
        print(f"DEBUG (EmployeeView): data manager: {product_data}")
        if not product_data:
            print("Không có dữ liệu nhân viên")
            self.table.setRowCount(0) # Xóa dữ liệu cũ nếu không có dữ liệu mới
            return

        self.table.setRowCount(len(product_data))

        for row_index, row_data in enumerate(product_data):
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                if item:
                    item.setTextAlignment(Qt.AlignCenter)
                self.table.setItem(row_index, col_index, item)

    def clear_search_input(self):
        """
        Xóa nội dung trong ô tìm kiếm.
        """
        # if self.search_customer_2:
        #     self.search_customer_2.clear()
        #     print("DEBUG: Search input cleared.")