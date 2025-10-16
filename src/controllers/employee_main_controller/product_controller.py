# In src/controllers/product_controller.py

from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem


class ProductController:
    def __init__(self, ui_page, main_window):
        """
        Khởi tạo controller cho trang sản phẩm.
        :param ui_page: Widget của trang sản phẩm (self.prodcut_page từ MainWindow).
        :param main_window: Instance của EmployeeMainWindow.
        """
        self.page = ui_page
        self.main_window = main_window
        self._initialized = False  # Cờ để chắc rằng chúng ta chỉ setup 1 lần

        # Lấy các widget con từ trang sản phẩm để tiện truy cập
        # Tên widget phải khớp với tên bạn đặt trong Qt Designer
        self.product_stackedWidget = self.page.findChild(QStackedWidget, 'product_stackedWidget')
        self.checkout_button = self.page.findChild(QPushButton, 'checkout_button')
        # ... và các widget khác

    def setup_page(self):
        """
        Hàm này sẽ được gọi từ MainWindow để thiết lập toàn bộ trang.
        """
        if not self._initialized:
            print("DEBUG: ProductController setup is running for the first time.")
            self.setup_ui_connections()
            self.load_initial_data()
            self.product_stackedWidget.setCurrentIndex(0)  # Đặt trang mặc định
            self._initialized = True

    def setup_ui_connections(self):
        """Kết nối tất cả các signal và slot cho trang này."""
        self.checkout_button.clicked.connect(self.show_checkout_page)
        # self.back_to_selection_button.clicked.connect(self.show_product_selection_page)
        # ... các kết nối khác

    def load_initial_data(self):
        """Tải dữ liệu ban đầu, ví dụ: danh sách sản phẩm."""
        # Đây là nơi bạn sẽ đặt logic render các ProductCard
        # Bạn có thể truy cập QueryData thông qua self.main_window.query_username
        all_products = self.main_window.query_username.get_all_products()
        # for product in all_products:
        #     card = ProductCard(product)
        #     self.product_list_layout.addWidget(card)

        # Ví dụ truy cập context của nhân viên đang đăng nhập
        employee_role = self.main_window._employee_context.get('role')
        print(f"DEBUG: Loading product page for user with role: {employee_role}")

    def show_checkout_page(self):
        """Chuyển sang trang thanh toán."""
        print("DEBUG: [ProductController] Switching to checkout page.")
        self.product_stackedWidget.setCurrentIndex(1)

    # ... các hàm logic khác cho trang sản phẩm