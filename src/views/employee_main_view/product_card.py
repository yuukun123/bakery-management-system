from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5 import uic

class ProductCard(QWidget):
    product_clicked = pyqtSignal(dict)

    def __init__(self, product_data, parent=None):
        super().__init__(parent)
        uic.loadUi("UI/forms/employee/product_card.ui", self)
        self.setFixedSize(227, 330)
        self.product_data = product_data
        self.set_data(product_data)

    def set_data(self, data):
        # Điền dữ liệu vào các label
        self.product_name_label.setText(data.get('product_name'))
        product_price = data.get('selling_price')
        formatted_price = f"{product_price:,.0f}"
        self.product_price_label.setText(f"{formatted_price}")

        # Set ảnh
        pixmap = QPixmap(data.get('image_path'))
        if not pixmap.isNull():
            target_width = int(self.image_label.width() * 13)  # tăng 30%
            target_height = int(self.image_label.height() * 8)

            scaled_pixmap = pixmap.scaled(
                target_width,
                target_height,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setAlignment(Qt.AlignCenter)

    def mousePressEvent(self, event):
        """Xử lý khi click vào card."""
        print(f"DEBUG: [ProductCard] Clicked on '{self.product_data.get('product_name')}'!")
        self.product_clicked.emit(self.product_data)
        super().mousePressEvent(event)