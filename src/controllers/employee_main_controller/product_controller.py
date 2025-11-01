import time
from logging import disable

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem, QStackedWidget, QToolButton, QWidget, QGridLayout, QLabel, QMessageBox, QComboBox, QLineEdit

from src.views.employee_main_view.product_card import ProductCard
from src.views.employee_main_view.item_card import ItemCard
from src.services.query_data_employee.employee_query_data import EmployeeQueryData

class ProductController:
    def __init__(self, ui_page, main_window, order_service):
        self.order_service = order_service
        self.item_card_widgets = {}
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
        self.plus_btn = self.page.findChild(QToolButton, 'plus_btn')
        self.minus_btn = self.page.findChild(QToolButton, 'minus_btn')
        self.total_bill_label = self.page.findChild(QLabel, 'total_bill_label')
        self.total_bill_label.setText("0")

        self.filter_CB = self.page.findChild(QComboBox, 'filter_CB')
        self.search_product = self.page.findChild(QLineEdit, 'search_product')
        self.search_product_btn = self.page.findChild(QToolButton, 'search_product_btn')

        self.contain_customer = self.page.findChild(QWidget, 'contain_customer')
        self.contain_customer.hide()

        self.reset_timer = QTimer(self.page)
        self.reset_timer.setSingleShot(True)  # Rất quan trọng, chỉ chạy 1 lần
        self.reset_timer.timeout.connect(self.apply_product_filters)

        # --- Setup UI ---
        self.product_container = self.main_window.container_list
        print(f"DEBUG: Container được chọn là: {self.product_container.objectName()}")

        # Tạo và áp dụng layout cho container
        if self.product_container.layout() is None:
            self.product_layout = QGridLayout(self.product_container)
        else:
            self.product_layout = self.product_container.layout()

        self.product_layout.setColumnStretch(99, 1)
        self.product_layout.setRowStretch(99, 1)

        self.product_layout.setHorizontalSpacing(5)
        self.product_layout.setVerticalSpacing(5)
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
            self.update_checkout_button_state()
            self.load_product_types_into_combobox()
            self.apply_product_filters()
            self.product_stackedWidget.setCurrentIndex(0)  # Đặt trang mặc định
            self._initialized = True

    def setup_ui_connections(self):
        """Kết nối tất cả các signal và slot cho trang này."""
        self.checkout_btn.clicked.connect(self.show_checkout_page)
        print("DEBUG: Checkout button connected to show_checkout_page.")
        self.cancel_btn.clicked.connect(self.show_product_selection_page)
        print("DEBUG: Cancel button connected to show_product_selection_page.")
        self.filter_CB.currentIndexChanged.connect(self.apply_product_filters)
        print("DEBUG: Filter combo box connected to apply_product_filters.")
        self.search_product_btn.clicked.connect(self.apply_product_filters)
        print("DEBUG: Search button connected to apply_product_filters.")
        self.search_product.textChanged.connect(self.on_search_text_changed)

    def show_checkout_page(self):
        """Chuyển sang trang thanh toán."""
        if not bool(self.order_service.items):
            QMessageBox.warning(self.main_window, "Thông báo", "Giỏ hàng đang trống. Vui lòng thêm sản phẩm trước khi thanh toán.")
            # Ngăn không cho chuyển trang
            return
        print("DEBUG: [ProductController] Switching to checkout page.")
        self.product_stackedWidget.setCurrentIndex(1)

    def show_product_selection_page(self):
        """Chuyển sang trang chọn sản phẩm."""
        print("DEBUG: [ProductController] Switching to product selection page.")
        self.product_stackedWidget.setCurrentIndex(0)

    def load_product_types_into_combobox(self):
        """
        Tải danh sách các loại sản phẩm từ CSDL và điền vào ComboBox.
        """
        print("DEBUG: Loading product types into ComboBox...")

        self.filter_CB.blockSignals(True)

        try:
            # --- BƯỚC 2: THỰC HIỆN THAY ĐỔI ---
            self.filter_CB.clear()
            self.filter_CB.addItem("Tất cả các loại", 0)

            product_types = self.query_data.get_all_product_types()

            if product_types:
                for p_type in product_types:
                    type_name = p_type.get('type_name')
                    type_id = p_type.get('type_id')
                    self.filter_CB.addItem(type_name, type_id)

        finally:
            # --- BƯỚC 3: MỞ LẠI TÍN HIỆU (RẤT QUAN TRỌNG!) ---
            # Dùng finally để đảm bảo tín hiệu luôn được mở lại, kể cả khi có lỗi
            self.filter_CB.blockSignals(False)

        print(f"DEBUG: ComboBox loaded with {self.filter_CB.count()} items. Signals unblocked.")

    def apply_product_filters(self):
        """
        Thu thập các bộ lọc từ UI và gọi hàm truy vấn.
        """
        # === LẤY ID TỪ COMBOBOX ===
        # .currentData() sẽ trả về userData của mục hiện tại
        # (0 cho "Tất cả", 1 cho "Croissant", 2 cho "Mousse", ...)
        selected_type_id = self.filter_CB.currentData()

        # Lấy từ khóa tìm kiếm từ QLineEdit
        keyword = self.search_product.text().strip()

        print(f"DEBUG: Applying filters -> Type ID: {selected_type_id}, Keyword: '{keyword}'")

        # Gọi hàm lọc với các giá trị đã lấy
        products = self.query_data.filter_products(
            type_id=selected_type_id,
            keyword=keyword
        )

        if products is None:
            # Trường hợp 1: Có lỗi CSDL
            QMessageBox.critical(self.main_window, "Lỗi", "Có lỗi xảy ra khi lọc sản phẩm.")
            return
        if products:
            print(f"DEBUG: Found {len(products)} products. Updating display.")
            self.display_product_cards(products)
        else:
            print("INFO: No products found for the current filters. Display remains unchanged.")
            QMessageBox.information(self.main_window, "Không tìm thấy",
                                    "Không tìm thấy sản phẩm nào phù hợp với tiêu chí của bạn.")

    def on_search_text_changed(self, text):
        self.reset_timer.stop()

        if not text.strip():
            # Nếu text là rỗng, khởi động timer với một độ trễ nhỏ (ví dụ 500ms)
            print("DEBUG: Search input is empty. Starting reset timer (500ms)...")
            self.reset_timer.start(50)

    def update_checkout_button_state(self):
        """
        Kiểm tra giỏ hàng và bật/tắt nút thanh toán tương ứng.
        Hàm này nên được gọi mỗi khi giỏ hàng thay đổi.
        """
        is_order_empty = not bool(self.order_service.items)

        print(f"DEBUG: [Controller] Updating checkout button state. Is order empty? {is_order_empty}")

        if is_order_empty:
            # Vô hiệu hóa nút khi giỏ hàng trống
            self.checkout_btn.setEnabled(False)
            self.checkout_btn.setToolTip("Vui lòng thêm sản phẩm vào giỏ hàng để thanh toán.")
            self.checkout_btn.setProperty("disabled", True)

        else:
            # Bật nút khi có ít nhất 1 sản phẩm
            self.checkout_btn.setEnabled(True)
            self.checkout_btn.setToolTip("Đi đến trang thanh toán.")
            self.checkout_btn.setProperty("disabled", False)

        # Yêu cầu cập nhật lại style của nút
        self.checkout_btn.style().polish(self.checkout_btn)

    def display_product_cards(self, products_data):
        """Tải dữ liệu sản phẩm."""
        employee_role = self.main_window._employee_role.get('role')
        print(f"DEBUG: Loading product page for user with role: {employee_role}")

        # Xóa layout cũ
        while self.product_layout.count():
            item = self.product_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
            # Cần xóa cả spacer/stretch item
            elif item.spacerItem():
                self.product_layout.removeItem(item)

        if not products_data:
            print("INFO: No products to display based on current filters.")
            QMessageBox.information(self.main_window, "Thông báo", "Không tìm thấy sản phẩm")
            return

        num_columns = 5
        for index, product_data in enumerate(products_data):
            product_card = ProductCard(product_data, parent=self.product_container)
            product_card.product_clicked.connect(self.handle_click_product)
            row = index // num_columns
            col = index % num_columns
            self.product_layout.addWidget(product_card, row, col)

        self.product_layout.setColumnStretch(num_columns, 1)  # Cột ngay sau cột cuối cùng
        self.product_layout.setRowStretch(len(products_data) // num_columns + 1, 1)  # Hàng ngay sau hàng cuối cùng
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
        if product_id in self.order_service.items:
            # Nếu đã có, chỉ cần tăng số lượng
            print(f"DEBUG: [Controller] Product ID {product_id} already in order. Increasing quantity.")
            # 1. Cập nhật dữ liệu trong Service
            self.order_service.increase_item_quantity(product_id)  # Bạn cần thêm hàm này vào OrderService

            # 2. Lấy widget tương ứng và yêu cầu nó cập nhật giao diện
            if product_id in self.item_card_widgets:
                card_widget = self.item_card_widgets[product_id]
                new_quantity = self.order_service.items[product_id]['quantity']
                card_widget.set_quantity(new_quantity)  # Cập nhật UI
        else:
            # Nếu chưa có, tạo card mới và thêm vào
            print(f"DEBUG: [Controller] Product ID {product_id} not in order. Creating new card.")
            if self.order_list_layout is None:
                print("ERROR: [Controller] order_list_layout is None! Cannot add item card.")
                return
            self.order_service.add_item(product_data)
            new_card = ItemCard(product_data)

            new_card.quantity_updated.connect(
                lambda new_qty, pid=product_id: self.on_item_quantity_change(pid, new_qty)
            )
            new_card.delete_requested.connect(self.remove_item_from_order)

            # Thêm card vào layout
            insert_position = self.order_list_layout.count() - 1  # -1 vì cái stretch cũng được tính là 1 item
            self.order_list_layout.insertWidget(insert_position, new_card)

            # LƯU card mới vào dictionary để theo dõi
            self.item_card_widgets[product_id] = new_card

        self.update_checkout_button_state()
        self.update_total_bill()

        if product_id in self.item_card_widgets:
            print(f"Debug quantity for product {product_id}: {self.item_card_widgets[product_id].quantity}")

    def on_item_quantity_change(self, product_id, new_quantity):
        self.order_service.update_quantity(product_id, new_quantity)
        self.update_total_bill()

    def update_total_bill(self):
        """Tính lại tổng tiền của toàn bộ hóa đơn."""

        total = self.order_service.get_total_amount()
        # Cập nhật tổng tiền lên một QLabel trên giao diện
        formatted_amount = f"{total:,.0f}"
        self.total_bill_label.setText(f"{formatted_amount}")
        print(f"DEBUG: [Controller] Total bill updated to: {formatted_amount}")

    def remove_item_from_order(self, product_data):
        """Xóa một item khỏi hóa đơn."""
        product_id = product_data.get('product_id')
        self.order_service.remove_item(product_id)

        if product_id in self.item_card_widgets:
            card_to_remove = self.item_card_widgets.pop(product_id)  # Xóa khỏi dictionary
            card_to_remove.deleteLater()  # Xóa widget khỏi giao diện

        self.update_total_bill()  # Tính lại tổng tiền
        print(f"DEBUG: [Controller] Removed item '{product_data.get('product_name')}'")
        self.update_checkout_button_state()

    def clear_order_display(self):
        """
        Xóa tất cả các widget ItemCard khỏi giao diện và reset lại bản đồ ánh xạ.
        Hàm này được gọi từ CheckoutController sau khi thanh toán thành công.
        """
        print("DEBUG: [ProductController] Clearing order display...")

        # Xóa tất cả các widget khỏi bản đồ ánh xạ
        # Lặp qua một bản copy của các keys để có thể xóa item trong dictionary gốc
        for product_id in list(self.item_card_widgets.keys()):
            card_to_remove = self.item_card_widgets.pop(product_id)
            if card_to_remove:
                # Xóa widget khỏi layout và bộ nhớ
                self.order_list_layout.removeWidget(card_to_remove)
                card_to_remove.deleteLater()
                self.update_total_bill()

        # Đảm bảo dictionary rỗng sau khi xóa
        self.item_card_widgets.clear()
        print("DEBUG: [ProductController] Order display cleared.")