from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHeaderView, QAbstractItemView, QWidget

from src.constants.table_header import INVOICE_DETAIL_HEADER
from src.services.query_data_employee.employee_query_data import EmployeeQueryData
from src.views.moveable_window import MoveableWindow
from resources import resources_rc

class InvoiceDetailView(QWidget, MoveableWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/forms/employee/invoice_detail.ui", self)
        MoveableWindow.__init__(self)

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1.0)

        # self.parent = parent
        self._initialized = False  # Cờ để chắc rằng chúng ta chỉ setup 1 lần
        self.query_data = EmployeeQueryData()
        # self.invoice_id = invoice_id

        self.summary_table = self.summary_table

    def setup_page(self):
        """
        Hàm này sẽ được gọi từ MainWindow để thiết lập toàn bộ trang.
        """
        if not self._initialized:
            print("DEBUG: ProductController setup is running for the first time.")
            self.setup_ui_connections()
            self._setup_table_header_and_properties()
            self.load_all_invoices()
            self._initialized = True

    def setup_ui_connections(self):
        """Kết nối tất cả các signal và slot cho trang này."""
        self.filter_btn.clicked.connect(self.apply_filters)
        self.search_invoice_btn.clicked.connect(self.apply_filters)
        self.clear_btn.clicked.connect(self.clear_search_input)

    def _setup_table_header_and_properties(self):
        if not self.summary_table:
            print("WARNING: Không tìm thấy QTableWidget.")
            return

        # === BƯỚC 1: THIẾT LẬP CẤU TRÚC CƠ BẢN CỦA BẢNG ===

        # Đặt số lượng cột và tên header TRƯỚC TIÊN
        self.summary_table.setColumnCount(len(INVOICE_DETAIL_HEADER))
        self.summary_table.setHorizontalHeaderLabels(INVOICE_DETAIL_HEADER)

        # === BƯỚC 2: TÙY CHỈNH CHI TIẾT CÁC CỘT ===

        # Lấy đối tượng header sau khi các cột đã được tạo
        header = self.summary_table.horizontalHeader()

        # Giả sử INVOICE_DETAIL_HEADER có thứ tự:
        # ['Tên sản phẩm', 'Số lượng', 'Đơn giá', 'Thành tiền']
        # Cột 0: Tên sản phẩm
        # Cột 1: Số lượng
        # Cột 2: Đơn giá
        # Cột 3: Thành tiền

        # Đặt chế độ co giãn mặc định cho tất cả các cột là Interactive
        # (cho phép người dùng tự kéo)
        header.setSectionResizeMode(QHeaderView.Interactive)

        # Sau đó, ghi đè cho các cột cụ thể

        # Cột 'Tên sản phẩm' (cột 0) sẽ co giãn để lấp đầy không gian
        header.setSectionResizeMode(0, QHeaderView.Stretch)

        # Cột 'Số lượng' (cột 1) nên có độ rộng cố định
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        self.summary_table.setColumnWidth(1, 80)  # Ví dụ 80px

        # Cột 'Đơn giá' và 'Thành tiền' (2, 3) có thể tự vừa với nội dung
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)

        # === BƯỚC 3: CÁC THUỘC TÍNH CHUNG KHÁC ===
        self.summary_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.summary_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.summary_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.summary_table.verticalHeader().setVisible(False)  # Ẩn cột số thứ tự

        # Thiết lập word wrap
        self.summary_table.setWordWrap(True)
        # Kết nối để tự động thay đổi chiều cao hàng khi kéo cột
        header.sectionResized.connect(self.summary_table.resizeRowsToContents)

