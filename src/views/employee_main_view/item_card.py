from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5 import uic

class ItemCard(QWidget):
    product_clicked = pyqtSignal(dict)

    def __init__(self, product_data, parent=None):
        super().__init__(parent)
        uic.loadUi("UI/forms/employee/item_card.ui", self)
        self.quantity = 1
        self.item_quantity.setValue(self.quantity)

        self.product_data = product_data
        self.set_data(self.product_data)

    def set_data(self, data):
        # Điền dữ liệu vào các label
        item_name = data.get('product_name', 'Unknown Item')
        self.item_name_label.setText(item_name)

    def increase_quantity(self):
        """Tăng số lượng của item này lên 1."""
        self.quantity += 1
        self.item_quantity.setValue(self.quantity)
