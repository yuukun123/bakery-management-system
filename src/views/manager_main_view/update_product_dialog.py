import os
import re
import shutil

from PyQt5 import uic
from PyQt5.QtGui import QColor, QRegExpValidator, QIntValidator, QPixmap
from PyQt5.QtWidgets import QDialog, QGraphicsDropShadowEffect, QWidget, QMessageBox, QLineEdit, QFileDialog
from src.services.query_data_manager.manager_query_data import QueryData
from PyQt5.QtCore import Qt, QPoint, QDateTime, QDate, QRegExp
from src.utils.validators import is_valid_phone_number
from src.views.moveable_window import MoveableWindow

class updateProduct(QDialog,MoveableWindow):
    def __init__(self, data=None, parent=None):
        MoveableWindow.__init__(self)
        super(updateProduct, self).__init__(parent)
        uic.loadUi("UI/forms/manager/update_product.ui", self)
        self.text_error.hide()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.new_image_path = None

        self.Update_product_btn.clicked.connect(self.check_data)
        self.query_data = QueryData()
        self.cancel_btn.clicked.connect(self.reject)
        self.upload_btn.clicked.connect(self.select_image)

        self.data = data
        print("----DEBUG: DATA BAN ĐẦU----")
        print(self.data)
        if self.data is None:
             QMessageBox.critical(self, "Lỗi", "Không tìm thấy dữ liệu nhân viên để cập nhật.")
             self.reject()
             return
        # Lưu dữ liệu GỐC
        self.product_id = self.data["product_id"]
        self.original_image_path = self.data["image_path"]
        self.original_status = self.data["status"]
        self.original_type = self.data["type"]

        self.new_image_path = None
        self.new_source_path = None

        self.load_product_types()
        self.set_data(self.data)

        int_validator = QIntValidator()
        int_validator.setRange(0, 999999)
        self.stock_input.setValidator(int_validator)

        self.name_input.textChanged.connect(self.hide_error_frame)
        self.stock_input.textChanged.connect(self.hide_error_frame)
        self.import_input.textChanged.connect(self.hide_error_frame)
        self.import_input.textChanged.connect(lambda: self.format_number(self.import_input))
        self.selling_input.textChanged.connect(self.hide_error_frame)
        self.selling_input.textChanged.connect(lambda: self.format_number(self.selling_input))
        self.type_comboBox.currentIndexChanged.connect(self.hide_error_frame)
        self.type_comboBox.currentIndexChanged.connect(self.on_type_or_image_changed)

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
    def set_data(self, data):
        print("----DEBUG: DATA TRONG HÀM SET----")
        print(data)
        name = data["product_name"]
        stock = data["stock"]
        selling_price = data["selling_price"]
        import_price = data["import_price"]
        type = data["type"]
        image_path = data["image_path"]
        self.name_input.setText(name)
        self.stock_input.setText(stock)
        self.import_input.setText(import_price)
        self.format_number(self.import_input)
        self.selling_input.setText(selling_price)
        self.format_number(self.selling_input)
        self.type_comboBox.setCurrentText(type)
        self.link_product.setText(image_path)
        if image_path:
            pixmap = QPixmap(image_path)
            scaled_pixmap = pixmap.scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setAlignment(Qt.AlignCenter)

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
        print("DEBUG: DỮ LIỆU HỢP LỆ BẮT ĐẦU UPDATE")
        final_relative_path = self.original_image_path
        try:
            if self.new_image_path:
                final_relative_path = os.path.join("UI/images", type_name, self.new_image_path).replace("\\", "/")
                final_absolute_path = os.path.abspath(final_relative_path)
                os.makedirs(os.path.dirname(final_absolute_path), exist_ok=True)
                shutil.copy(self.new_source_path, final_absolute_path)
                print(f"Đã copy ảnh MỚI từ {self.new_source_path} TỚI {final_absolute_path}")
            elif type_name != self.original_type:
                print("Đang di chuyển ảnh sang loại mới...")
                new_filename = os.path.basename(self.original_image_path)
                final_relative_path = os.path.join("UI/images", type_name, new_filename).replace("\\", "/")
                original_absolute_path = os.path.abspath(self.original_image_path)
                final_absolute_path = os.path.abspath(final_relative_path)
                if os.path.exists(original_absolute_path):
                    os.makedirs(os.path.dirname(final_absolute_path), exist_ok=True)
                    # Di chuyển file CŨ
                    shutil.move(original_absolute_path, final_absolute_path)
                    print(f"Đã di chuyển ảnh CŨ từ {original_absolute_path} TỚI {final_absolute_path}")
                else:
                    print(f"Cảnh báo: Không tìm thấy ảnh gốc để di chuyển: {original_absolute_path}")

        except Exception as e:
            print(f"LỖI copy file: {e}")
            return
        data = {
            "product_id": self.product_id,
            "name": name,
            "import_price": import_price,
            "stock": stock,
            "selling_price": selling,
            "type_id": type_id,
            "status": self.original_status,
            "image_path":final_relative_path
        }
        print("DEBUG: DỮ LIỆU CHUẨN BỊ SỬA:", data)
        result = self.query_data.update_product(data)
        if result:
            self.accept()
        else:
            print("sửa product thất bại!")

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

    def load_product_types(self):
        try:
            self.type_comboBox.addItem("--- Chọn loại sản phẩm ---", 0)
            types = self.query_data.get_all_type()
            for type_id, type_name in types:
                self.type_comboBox.addItem(type_name,type_id)
        except Exception as e:
            print(f"Lỗi khi nạp loại sản phẩm: {e}")

    def select_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Chọn ảnh sản phẩm",
            "",
            "Image Files (*.png *.jpg *.jpeg)"
        )
        if file_name:
            file_base_name = os.path.basename(file_name)
            self.new_image_path = file_base_name  # Dùng biến MỚI
            self.new_source_path = file_name
            print(f"Đã lưu tên file: {self.new_image_path}")
            print(f"Đường dẫn gốc: {self.new_source_path}")

            pixmap = QPixmap(file_name)
            scaled_pixmap = pixmap.scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setAlignment(Qt.AlignCenter)
            self.on_type_or_image_changed()

    def on_type_or_image_changed(self):
        self.hide_error_frame()
        type = self.type_comboBox.currentText()
        type_index = self.type_comboBox.currentIndex()
        file_name = self.new_image_path if self.new_image_path else os.path.basename(self.original_image_path)
        if file_name and type_index != 0:
            final_relative_path = os.path.join("UI/images", type, file_name).replace("\\", "/")
            self.link_product.setText(final_relative_path)
        elif file_name:
            self.link_product.setText(file_name)

