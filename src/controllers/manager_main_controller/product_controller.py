from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QDialog, QMessageBox
from src.services.query_data_manager.manager_query_data import QueryData
from src.views.manager_main_view.add_product_dialog_view import addProduct
from src.views.manager_main_view.update_product_dialog import updateProduct


class productController:
        def __init__(self, mainview, tableview):
            self.query_data = QueryData()
            self.view = mainview
            self.table = tableview
            self.connect_filter_signal()
            self.load_product_filter_data()

        def open_add_product_dialog(self):
            print("DEBUG: BẮT ĐẦU MỞ ADD DIALOG")
            dialog = addProduct(self.view)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                QMessageBox.information(self.view,"Thành công", "Đã thêm sản phẩm thành công!")
                self.table.load_product_data()

        def handle_stop_selling(self):
            product_data =  self.table.get_selected_product_data()
            reply = QMessageBox.question( self.view, 'Xác nhận ngừng bán',
                    f"Bạn có chắc chắn muốn bán sản phẩm này?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.set_product_stop_selling(product_data)

        def set_product_stop_selling(self, data):
            print(f"DEBUG: CHO SẢN PHẨM NGỪNG BÁN")
            product_id = data["product_id"]
            success = self.query_data.update_status_product(product_id)
            if success:
                QMessageBox.information(
                         self.view,
                        "Thành công",
                        f"Đã cho sản phẩm {data['product_name']} (ID: {data['product_id']}) ngừng bán thành công."
                    )
                self.table.load_product_data()
            else:
                QMessageBox.critical(
                     self.view,
                    "Lỗi",
                    f"Không thể cập nhật trạng thái ngừng bán cho sản phẩm {data['product_name']}."
                )
        def open_update_product_dialog(self):
            print("DEBUG: BẮT ĐẦU MỞ UPDATE DIALOG")
            product_data = self.table.get_selected_product_data()
            if not product_data:
                print("lỗi không lấy được product data")
            if product_data["status"].lower() == "ngừng kinh doanh":
                QMessageBox.warning(self.view, "Không thể sửa", "Không thể sửa thông tin của sản phẩm đã ngừng kinh doanh.")
                return
            dialog = updateProduct(data=product_data)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                QMessageBox.information( self.view,"Thành công", "Đã sửa thông tin sản phẩm thành công!")
                self.table.load_product_data()

        def connect_filter_signal(self):
            try:
                self.view.comboBox_category.currentIndexChanged.connect(self.load_product_filter_data)
                self.view.status_comboBox.currentIndexChanged.connect(self.load_product_filter_data)
                self.view.comboBox_display.currentIndexChanged.connect(self.load_product_filter_data)
                self.view.search_product_btn.clicked.connect(self.load_product_filter_data)
            except AttributeError as e:
                print(f"LỖI: Không tìm thấy widget filter trong View. Tên widget có đúng không? {e}")

        def load_product_filter_data(self):
            try:
                category = self.view.comboBox_category.currentText()
                status = self.view.status_comboBox.currentText().lower()
                display = self.view.comboBox_display.currentText()
                search_term = self.view.search_product.text().strip()

                if not category:
                    category = "Tất cả"
                if not status:
                    status = "Tất cả"
                if not display:
                    display = "Tất cả"

                filtered_data = self.query_data.search_products(category,status,display,search_term)
                self.table.populate_table(filtered_data)

            except Exception as e:
                print(f"Lỗi khi tải/filter dữ liệu nhân viên: {e}")