from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem, QStackedWidget, QToolButton, QWidget, QGridLayout

from src.views.employee_main_view.product_card import ProductCard
from src.services.query_data_employee.employee_query_data import EmployeeQueryData

class ProductController:
    def __init__(self, ui_page, main_window):
        self.page = ui_page
        self.main_window = main_window
        self._initialized = False  # Cờ để chắc rằng chúng ta chỉ setup 1 lần
        self.query_data = EmployeeQueryData()
        self.product_list_layout = self.page.findChild(QWidget, 'container_product')

        # Lấy các widget con từ trang sản phẩm để tiện truy cập
        # Tên widget phải khớp với tên bạn đặt trong Qt Designer
        self.product_stackedWidget = self.page.findChild(QStackedWidget, 'product_stackedWidget')
        self.checkout_btn = self.page.findChild(QToolButton, 'checkout_btn')
        self.cancel_btn = self.page.findChild(QToolButton, 'cancel_btn')

        # --- Setup UI ---
        self.product_container = self.main_window.container_list
        print(f"DEBUG: Container được chọn là: {self.product_container.objectName()}")

        # Tạo và áp dụng layout cho container
        if self.product_container.layout() is None:
            self.product_layout = QGridLayout(self.product_container)
        else:
            self.product_layout = self.product_container.layout()

        self.product_layout.setHorizontalSpacing(15)
        self.product_layout.setVerticalSpacing(15)
        self.product_layout.setAlignment(Qt.AlignTop)

        self.items_layout = self.product_layout

    def setup_page(self):
        """
        Hàm này sẽ được gọi từ MainWindow để thiết lập toàn bộ trang.
        """
        if not self._initialized:
            print("DEBUG: ProductController setup is running for the first time.")
            self.setup_ui_connections()
            # self.load_initial_data()
            self.load_product_data()
            self.product_stackedWidget.setCurrentIndex(0)  # Đặt trang mặc định
            self._initialized = True

    def setup_ui_connections(self):
        """Kết nối tất cả các signal và slot cho trang này."""
        self.checkout_btn.clicked.connect(self.show_checkout_page)
        print("DEBUG: Checkout button connected to show_checkout_page.")
        self.cancel_btn.clicked.connect(self.show_product_selection_page)
        print("DEBUG: Cancel button connected to show_product_selection_page.")
        # self.back_to_selection_button.clicked.connect(self.show_product_selection_page)
        # ... các kết nối khác

    def show_checkout_page(self):
        """Chuyển sang trang thanh toán."""
        print("DEBUG: [ProductController] Switching to checkout page.")
        self.product_stackedWidget.setCurrentIndex(1)

    def show_product_selection_page(self):
        """Chuyển sang trang chọn sản phẩm."""
        print("DEBUG: [ProductController] Switching to product selection page.")
        self.product_stackedWidget.setCurrentIndex(0)

    def load_product_data(self):
        """Tải dữ liệu sản phẩm."""
        employee_role = self.main_window._employee_role.get('role')
        print(f"DEBUG: Loading product page for user with role: {employee_role}")

        # Xóa layout cũ
        while self.product_layout.count():
            child = self.product_layout.takeAt(0)
            if child.widget(): child.widget().deleteLater()

        print("DEBUG: [ProductController] Querying all products from database...")
        all_products = self.query_data.get_all_products()

        if not all_products:
            print("WARNING: Không có sản phẩm nào trong cơ sở dữ liệu.")
            return

        print(f"DEBUG: [ProductController] Found {len(all_products)} products. Now creating cards...")
        # Tạo và thêm card (thao tác GUI)
        num_columns = 4
        for index, product_data in enumerate(all_products):
            # topic_card = TopicCardWidget(topic_data, parent=self.topic_container)
            product_card = ProductCard(product_data, parent=self.product_container)

            # topic_card.details_requested.connect(self.handle_details_requested)
            row = index // num_columns
            col = index % num_columns
            self.product_layout.addWidget(product_card, row, col)

        print("DEBUG: [ProductController] Finished creating product cards.")
        #
        # for product in all_products:
        #     self.product_list_layout.addWidget(card)
