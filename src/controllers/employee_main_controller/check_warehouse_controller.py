from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtWidgets import (QMessageBox, QTableWidgetItem,
                             QAbstractItemView)

from src.services.query_data_employee.employee_query_data import EmployeeQueryData
from src.constants.table_header import PRODUCT_HEADER

class WarehouseController():
    def __init__(self, parent):
        self.customer_info = {}
        self.parent = parent
        self._initialized = False  # Cờ để chắc rằng chúng ta chỉ setup 1 lần
        self.query_data = EmployeeQueryData()

        self.filter_CB = self.parent.filter_CB_2
        self.search_product = self.parent.search_product_2
        self.search_product_btn = self.parent.search_product_btn_2

        self.table = self.parent.table_warehouse

    def setup_page(self):
        """
        Hàm này sẽ được gọi từ MainWindow để thiết lập toàn bộ trang.
        """
        if not self._initialized:
            print("DEBUG: ProductController setup is running for the first time.")
            # self.setup_ui_connections()
            self._setup_table_header_and_properties()
            # self._install_event_filter()
            self.load_product_data()
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

    # def _install_event_filter(self):
    #     """Cài đặt bộ lọc sự kiện cho cửa sổ chính để xử lý click ngoài bảng."""
    #     # Dòng này bây giờ sẽ hoạt động
    #     self.parent.installEventFilter(self)
    #     print("DEBUG: [CustomerController] Event filter installed on MainWindow.")
    #
    # def clear_table_selection(self):
    #     """Phương thức công khai để xóa lựa chọn trên bảng."""
    #     if self.table:
    #         self.table.clearSelection()
    #         print("DEBUG: [CustomerController] Table selection cleared.")
    #
    # # --- BƯỚC 4: THÊM HÀM eventFilter VÀO ---
    # def eventFilter(self, source, event):
    #     """
    #     Bộ lọc sự kiện, sẽ được gọi cho mọi sự kiện trên self.parent (MainWindow).
    #     """
    #     # Chỉ quan tâm đến sự kiện click chuột trái
    #     if event.type() == QEvent.MouseButtonPress and event.button() == Qt.LeftButton:
    #         # Kiểm tra xem con trỏ chuột có đang nằm trên bảng không
    #         if not self.table.underMouse():
    #             # Nếu không, và nếu bảng đang có lựa chọn
    #             if self.table.selectionModel().hasSelection():
    #                 # Xóa lựa chọn
    #                 self.clear_table_selection()
    #
    #     # Rất quan trọng: Trả về False để các sự kiện được xử lý bình thường
    #     return super().eventFilter(source, event)

    def load_product_data(self):
        """
        Tải danh sách tất cả sản phẩm, định dạng dữ liệu,
        và hiển thị chúng lên QTableWidget.
        """
        # 1. GỌI ĐÚNG HÀM ĐỂ LẤY TẤT CẢ SẢN PHẨM
        # Giả định bạn đã có hàm get_all_products_for_display()
        all_products = self.query_data.get_product_stock()

        if not all_products:
            self.table.setRowCount(0)
            return

        self.table.setRowCount(len(all_products))

        # 2. ĐỊNH NGHĨA THỨ TỰ CÁC CỘT CẦN HIỂN THỊ
        column_order = [
            'product_id',
            'product_name',
            'type_name', # <-- Bạn cần đảm bảo hàm query có JOIN để lấy cột này
            'stock',
            'selling_price',
        ]

        # Thiết lập header (chỉ cần chạy 1 lần trong _setup_table_header_and_properties)
        # self.table.setColumnCount(len(column_order))
        # self.table.setHorizontalHeaderLabels(["ID", "Tên Sản phẩm", "Loại", "Tồn kho", "Giá bán", "Giá nhập"])

        # 3. LẶP QUA DỮ LIỆU VÀ ĐIỀN VÀO BẢNG
        for row_index, product_dict in enumerate(all_products):
            for col_index, key in enumerate(column_order):

                # --- LOGIC ĐÃ ĐƯỢC SỬA LẠI HOÀN TOÀN ---

                # a. Lấy đúng giá trị tương ứng với key hiện tại
                value = product_dict.get(key)

                # b. Chuyển đổi giá trị thành chuỗi để hiển thị
                if value is None:
                    display_text = ""
                elif key is 'selling_price':
                    # Nếu là cột tiền tệ, áp dụng format
                    try:
                        display_text = f"{float(value):,.0f}"
                    except (ValueError, TypeError):
                        display_text = "0"
                else:
                    # Với các cột khác, chỉ cần chuyển thành chuỗi
                    display_text = str(value)

                # c. Tạo item và đặt vào bảng
                item = QTableWidgetItem(display_text)
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