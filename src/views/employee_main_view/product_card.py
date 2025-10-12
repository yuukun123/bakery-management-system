from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic

class ProductCard(QWidget):
    product_clicked = pyqtSignal(dict)

    def __init__(self, product_data, parent=None):
        super().__init__(parent)
        uic.loadUi("UI/forms/employee/product_card.ui", self)

        self.product_data = product_data
        self.set_data(product_data)

    def set_data(self, data):
        # Điền dữ liệu vào các label
        self.name_label.setText(data.get('product_name'))
        # ... set ảnh và giá

    def mousePressEvent(self, event):
        """
        Hàm này sẽ tự động được Qt gọi khi người dùng click chuột vào widget này.
        """
        self.product_clicked.emit(self.product_data)
        # Gọi lại hàm gốc để đảm bảo các sự kiện khác vẫn hoạt động
        super().mousePressEvent(event)