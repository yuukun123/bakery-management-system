from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem, QStackedWidget, QToolButton, QWidget, QGridLayout

from src.views.employee_main_view.product_card import ProductCard
from src.views.employee_main_view.item_card import ItemCard
from src.services.query_data_employee.employee_query_data import EmployeeQueryData

class ProductController:
    def __init__(self, ui_page, main_window):
        self.current_order = {}
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
        self.product_layout.setContentsMargins(0, 0, 0, 0)
        self.product_layout.setAlignment(Qt.AlignTop)

        # --- Setup UI item  ---
        self.order_list_container = self.main_window.order_list_container

        if self.order_list_container is None:
            raise RuntimeError("Không tìm thấy QWidget 'order_list_container' trên trang thanh toán.")

        # Tạo layout cho container này nếu chưa có
        if self.order_list_container.layout() is None:
            self.order_list_layout = QVBoxLayout(self.order_list_container)
            self.order_list_layout.setAlignment(Qt.AlignTop)
        else:
            self.order_list_layout = self.order_list_container.layout()

        self.order_list_layout.addStretch()

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

            product_card.product_clicked.connect(self.handle_click_product)

            row = index // num_columns
            col = index % num_columns
            self.product_layout.addWidget(product_card, row, col)

        print("DEBUG: [ProductController] Finished creating product cards.")

    def handle_click_product(self, product_data):
        """
        Xử lý khi click vào một sản phẩm.
        Kiểm tra xem sản phẩm đã có trong hóa đơn chưa,
        nếu có thì tăng số lượng, nếu chưa thì thêm mới.
        """
        product_id = product_data.get('product_id')
        if product_id is None:
            print("ERROR: Sản phẩm không có ID.")
            return

        print(f"DEBUG: [Controller] Clicked on product ID: {product_id}")

        # KIỂM TRA XEM SẢN PHẨM ĐÃ CÓ TRONG HÓA ĐƠN CHƯA
        if product_id in self.current_order:
            # Nếu đã có, chỉ cần tăng số lượng
            print(f"DEBUG: [Controller] Product ID {product_id} already in order. Increasing quantity.")
            existing_card = self.current_order[product_id]
            existing_card.increase_quantity()  # Bạn sẽ cần tạo hàm này trong ItemCard
        else:
            # Nếu chưa có, tạo card mới và thêm vào
            print(f"DEBUG: [Controller] Product ID {product_id} not in order. Creating new card.")
            if self.order_list_layout is None:
                print("ERROR: [Controller] order_list_layout is None! Cannot add item card.")
                return

            new_card = ItemCard(product_data)

            # Thêm card vào layout
            # self.order_list_layout.addWidget(new_card)
            insert_position = self.order_list_layout.count() - 1  # -1 vì cái stretch cũng được tính là 1 item
            self.order_list_layout.insertWidget(insert_position, new_card)

            # LƯU card mới vào dictionary để theo dõi
            self.current_order[product_id] = new_card
