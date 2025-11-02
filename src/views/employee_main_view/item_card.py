from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QSpinBox
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5 import uic

class ItemCard(QWidget):
    # Gửi đi ID sản phẩm và số lượng MỚI mà người dùng đã nhập
    quantity_set_requested = pyqtSignal(int, int)
    quantity_change_requested = pyqtSignal(int, int)
    # Tín hiệu để yêu cầu xóa item này khỏi hóa đơn
    delete_requested = pyqtSignal(dict)

    def __init__(self, product_data, parent=None):
        super().__init__(parent)
        uic.loadUi("UI/forms/employee/item_card.ui", self)
        self.item_quantity = self.findChild(QSpinBox, 'item_quantity')
        if self.item_quantity is None:
            raise RuntimeError("Không tìm thấy QSpinBox 'item_quantity_spinbox'")

        self.product_data = product_data
        self.unit_price = product_data.get('selling_price', 0)
        self.product_id = product_data.get('product_id')

        self.set_data()
        self.quantity = 1
        self.set_quantity(1)

        # Kết nối các nút với các hàm xử lý (slot)
        self.item_quantity.editingFinished.connect(self.on_quantity_edited)

        self.plus_btn.clicked.connect(self.request_increase)
        self.minus_btn.clicked.connect(self.request_decrease)
        self.delete_btn.clicked.connect(self.request_delete)

    def set_data(self):
        # Điền dữ liệu vào các label
        item_name = self.product_data.get('product_name', 'Unknown Item')
        self.item_name_label.setText(item_name)

    def set_quantity(self, quantity):
        """
        Một phương thức công khai để Controller ra lệnh cho ItemCard cập nhật số lượng.
        Hàm này chỉ cập nhật UI, không chứa logic.
        """
        try:
            self.item_quantity.editingFinished.disconnect(self.on_quantity_edited)
        except TypeError:
            # Bỏ qua lỗi nếu nó chưa bao giờ được kết nối
            pass

        try:
            # Cập nhật giá trị nội bộ và giao diện
            self.quantity = quantity
            self.item_quantity.setValue(self.quantity)
        finally:
            # --- KẾT NỐI LẠI TÍN HIỆU ---
            self.item_quantity.editingFinished.connect(self.on_quantity_edited)

        print(f"DEBUG: [ItemCard] UI quantity set to {self.quantity} for pid={self.product_id}")

    def request_increase(self):
        """Phát tín hiệu yêu cầu tăng số lượng lên 1."""
        print(f"DEBUG: [ItemCard] Requesting to increase quantity for product {self.product_id}.")
        self.quantity_change_requested.emit(self.product_id, 1)  # Gửi đi +1

    def request_decrease(self):
        """Phát tín hiệu yêu cầu giảm số lượng đi 1."""
        print(f"DEBUG: [ItemCard] Requesting to decrease quantity for product {self.product_id}.")
        self.quantity_change_requested.emit(self.product_id, -1)  # Gửi đi -1

    def request_delete(self):
        """Phát tín hiệu yêu cầu xóa chính nó."""
        self.delete_requested.emit(self.product_data)

    def get_subtotal(self):
        """Trả về tổng tiền cho item này (giá * số lượng)."""
        return self.unit_price * self.quantity

    def on_quantity_edited(self):
        """
        Được gọi khi người dùng nhập xong số lượng.
        Phát tín hiệu yêu cầu đặt số lượng mới.
        """
        new_quantity = self.item_quantity.value()

        # Chỉ phát tín hiệu nếu giá trị thực sự thay đổi
        if new_quantity != self.quantity:
            print(f"DEBUG: [ItemCard] User edited quantity for pid={self.product_id} to {new_quantity}.")
            self.quantity_set_requested.emit(self.product_id, new_quantity)