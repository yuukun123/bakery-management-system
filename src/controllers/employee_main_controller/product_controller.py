from logging import disable

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QHeaderView, QTableWidgetItem, QStackedWidget, QToolButton, QWidget, QGridLayout, QLabel, QMessageBox

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

        self.contain_customer = self.page.findChild(QWidget, 'contain_customer')
        self.contain_customer.hide()

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
            self.update_checkout_button_state()
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

            # <<< XÓA DÒNG QMESSAGEBOX Ở ĐÂY >>>
            # Người dùng đã có đủ thông tin qua việc nút bị mờ và tooltip.
        else:
            # Bật nút khi có ít nhất 1 sản phẩm
            self.checkout_btn.setEnabled(True)
            self.checkout_btn.setToolTip("Đi đến trang thanh toán.")
            self.checkout_btn.setProperty("disabled", False)

        # Yêu cầu cập nhật lại style của nút
        self.checkout_btn.style().polish(self.checkout_btn)

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