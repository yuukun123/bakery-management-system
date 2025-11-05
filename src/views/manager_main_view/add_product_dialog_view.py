import os
import re
import shutil

from werkzeug.security import generate_password_hash
from PyQt5 import uic
from PyQt5.QtGui import QColor, QRegExpValidator, QPixmap, QIntValidator
from PyQt5.QtWidgets import QDialog, QGraphicsDropShadowEffect, QWidget, QMessageBox, QLineEdit, QFileDialog
from src.services.query_data_manager.manager_query_data import QueryData
from PyQt5.QtCore import Qt, QPoint, QDateTime, QDate, QRegExp
from src.views.moveable_window import MoveableWindow

class addProduct(QDialog,MoveableWindow):
    def __init__(self, parent=None):
        MoveableWindow.__init__(self)
        super(addProduct, self).__init__(parent)
        uic.loadUi("UI/forms/manager/add_product.ui", self)
        self.text_error.hide()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        int_validator = QIntValidator()
        int_validator.setRange(0, 999999)
        self.stock_input.setValidator(int_validator)

        self.addproduct_btn.clicked.connect(self.check_data)
        self.query_data = QueryData()
        self.cancel_btn.clicked.connect(self.reject)
        self.image_path = None
        self.source_image_path = None
        self.type_comboBox.currentIndexChanged.connect(self.on_type_or_image_changed)
        self.upload_btn.clicked.connect(self.select_image)
        self.load_product_types()

        self.name_input.textChanged.connect(self.hide_error_frame)
        self.stock_input.textChanged.connect(self.hide_error_frame)
        self.import_input.textChanged.connect(self.hide_error_frame)
        self.import_input.textChanged.connect(lambda: self.format_number(self.import_input))
        self.selling_input.textChanged.connect(self.hide_error_frame)
        self.selling_input.textChanged.connect(lambda: self.format_number(self.selling_input))
        self.type_comboBox.currentIndexChanged.connect(self.hide_error_frame)


        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 150))
        self.findChild(QWidget, "mainFrame").setGraphicsEffect(shadow)

    def show_message(self, text):
        if hasattr(self,"text_error"):
            self.text_error.setText(f"{text}")
            self.text_error.show()
    def hide_error_frame(self):
        if hasattr(self, 'text_error'):
            self.text_error.hide()

    def check_data(self):
        name = self.name_input.text()
        import_price_str = self.import_input.text().replace(",", "")
        stock_str = self.stock_input.text()
        selling_str = self.selling_input.text().replace(",", "")
        type_name = self.type_comboBox.currentText()  # Lấy tên (nếu cần)
        type_id = self.type_comboBox.currentData()

        print("DEBUG: BẮT ĐẦU KIỂM TRA DỮ LIỆU")
        if not name or not import_price_str or not stock_str or not selling_str:
            self.show_message("Vui lòng nhập đầy đủ thông tin")
            return
        if type_id == 0:
            self.show_message("Vui lòng chọn loại sản phẩm")
            return
        try:
            stock = int(stock_str)
            import_price = float(import_price_str)
            selling = float(selling_str)
        except ValueError:
            self.show_message("Giá và tồn kho phải là số hợp lệ")
            return
        if stock < 0:
            self.show_message("Tồn kho phải lớn hơn hoặc bằng 0")
            return
        if import_price <= 0:
            self.show_message("Giá nhập phải lớn hơn 0")
            return
        if selling <= 0:
            self.show_message("Giá bán phải lớn hơn 0")
            return
        if selling <= import_price:
            self.show_message("Giá bán phải cao hơn giá nhập")
            return
        if not self.image_path:
            self.show_message("Vui lòng tải lên ảnh sản phẩm")
            return
        print("DEBUG: DỮ LIỆU HỢP LỆ BẮT ĐẦU UPDATE")
        final_relative_path = os.path.join("UI/images", type_name, self.image_path).replace("\\", "/")
        try:
            source_absolute_path = os.path.abspath(self.source_image_path)
            final_absolute_path = os.path.abspath(final_relative_path)
            # Tạo thư mục đích nếu nó chưa tồn tại (ví dụ: "UI/images/Tart")
            os.makedirs(os.path.dirname(final_relative_path), exist_ok=True)
            if source_absolute_path != final_absolute_path:
                shutil.copy(source_absolute_path, final_absolute_path)
                print(f"Đã copy ảnh từ {source_absolute_path} TỚI {final_absolute_path}")
            else:
                print("Ảnh đã ở đúng vị trí, không cần copy.")

        except Exception as e:
            print(f"LỖI copy file: {e}")
            return
        data = {
            "name": name,
            "import_price": import_price,
            "stock_price": stock,
            "selling": selling,
            "type_id": type_id,
            "status": "đang kinh doanh",
            "image_path":final_relative_path
        }
        print("DEBUG: DỮ LIỆU CHUẨN BỊ THÊM:", data)
        result = self.query_data.add_new_product(data)
        if result:
            self.accept()
        else:
            print("Thêm product thất bại!")

    def select_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Chọn ảnh sản phẩm",
            "",
            "Image Files (*.png *.jpg *.jpeg)"
        )
        if file_name:
            file_base_name = os.path.basename(file_name)
            self.image_path = file_base_name
            self.source_image_path = file_name
            print(f"Đã lưu tên file: {self.image_path}")
            print(f"Đường dẫn gốc: {self.source_image_path}")
            self.link_product.setText(self.source_image_path)
            pixmap = QPixmap(file_name)
            scaled_pixmap = pixmap.scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setAlignment(Qt.AlignCenter)
            self.on_type_or_image_changed()

    def format_number(self, line_edit):
        text = line_edit.text()
        digits_only = "".join(filter(str.isdigit, text))
        if digits_only:
            formatted = "{:,}".format(int(digits_only))
        else:
            formatted = ""
        if text != formatted:
            line_edit.blockSignals(True)
            line_edit.setText(formatted)
            line_edit.blockSignals(False)
            line_edit.setCursorPosition(len(formatted))

    def on_type_or_image_changed(self):
        self.hide_error_frame()
        type = self.type_comboBox.currentText()
        type_index = self.type_comboBox.currentIndex()
        file_name = self.image_path

        if file_name and type_index != 0:
            final_relative_path = os.path.join("UI/images", type, file_name).replace("\\", "/")
            self.link_product.setText(final_relative_path)
        elif file_name:
            self.link_product.setText(file_name)

    def load_product_types(self):
        try:
            self.type_comboBox.addItem("--- Chọn loại sản phẩm ---", 0)
            types = self.query_data.get_all_type()
            for type_id, type_name in types:
                self.type_comboBox.addItem(type_name,type_id)
        except Exception as e:
            print(f"Lỗi khi nạp loại sản phẩm: {e}")