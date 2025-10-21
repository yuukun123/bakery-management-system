from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5 import uic

class ItemCard(QWidget):
    quantity_updated = pyqtSignal(int)
    # Tín hiệu để yêu cầu xóa item này khỏi hóa đơn
    delete_requested = pyqtSignal(dict)

    def __init__(self, product_data, parent=None):
        super().__init__(parent)
        uic.loadUi("UI/forms/employee/item_card.ui", self)
        self.quantity = 1
        self.item_quantity.setValue(self.quantity)
        self.unit_price = product_data.get('selling_price', 0)

        self.product_data = product_data
        self.set_data(self.product_data)

        # Kết nối các nút với các hàm xử lý (slot)
        self.plus_btn.clicked.connect(self.increase_quantity)
        self.minus_btn.clicked.connect(self.decrease_quantity)
        # Giả sử bạn có một nút xóa tên là 'delete_btn'
        self.delete_btn.clicked.connect(self.request_delete)

    def set_data(self, data):
        # Điền dữ liệu vào các label
        item_name = data.get('product_name', 'Unknown Item')
        self.item_name_label.setText(item_name)

    def set_quantity(self, quantity):
        self.quantity = quantity
        # Bây giờ ItemCard tự biết phải làm gì với widget của nó
        self.item_quantity.setValue(self.quantity)

    def increase_quantity(self):
        """Tăng số lượng của item này lên 1."""
        self.quantity += 1
        self.update_ui()

    def decrease_quantity(self):
        if self.quantity > 1:
            self.quantity -= 1
            self.update_ui()

    def request_delete(self):
        """Phát tín hiệu yêu cầu xóa chính nó."""
        self.delete_requested.emit(self.product_data)

    def get_subtotal(self):
        """Trả về tổng tiền cho item này (giá * số lượng)."""
        return self.unit_price * self.quantity

    def update_ui(self):
        self.item_quantity.setValue(self.quantity)
        self.quantity_updated.emit(self.quantity)
        print(f"DEBUG: [ItemCard] '{self.product_data.get('product_name')}' quantity changed to {self.quantity}")