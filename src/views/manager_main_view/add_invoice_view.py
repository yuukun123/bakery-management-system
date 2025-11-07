from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QLabel, QTableWidgetItem, QAbstractItemView, QHeaderView, QAbstractScrollArea, \
    QMessageBox
from src.services.query_data_manager.manager_query_data import QueryData
from src.controllers.manager_main_controller.add_invoice_controller import addInvoiceController
from src.utils.global_signal import app_signals

class addInvoiceViewWidget(QWidget):
    def __init__(self, parent=None, employee_id = None):
        super().__init__(parent)
        self.view = parent
        self.query_data = QueryData()
        self.employee_id = employee_id
        self.data_import = {}
        self.view.update_product_import.setEnabled(False)
        self.view.delete_product_import.setEnabled(False)
        self.view.type_invoice_comboBox.currentIndexChanged.connect(self.check_invoice)
        self.addInvoiceController = addInvoiceController(self)
        app_signals.product_data_changed.connect(self.load_product)
        self.parent().installEventFilter(self)
        self.view.product_import_tableWidget.installEventFilter(self)
        self.view.list_product_import.installEventFilter(self)
        self.view.product_import_tableWidget.viewport().installEventFilter(self)
        self.view.list_product_import.viewport().installEventFilter(self)

        int_validator = QIntValidator()
        int_validator.setRange(0, 999999)
        self.view.quantity_import.setValidator(int_validator)

        viewport_1 = self.view.product_import_tableWidget.viewport()
        viewport_2 = self.view.list_product_import.viewport()
        self.placeholder_label = QLabel("Không tìm thấy dữ liệu phù hợp", viewport_1)
        self.placeholder_label.setStyleSheet("border-radius: none; background: #ffffff;")
        self.placeholder_label.setAlignment(Qt.AlignCenter)
        self.placeholder_label.setStyleSheet("color: grey; font-size: 14px;")
        self.placeholder_label.setWordWrap(True)
        self.placeholder_label.hide()

        self.placeholder_label_2 = QLabel("Chưa có sản phẩm nào được thêm vào phiếu", viewport_2)
        self.placeholder_label_2.setStyleSheet("border-radius: none; background: #ffffff;")
        self.placeholder_label_2.setAlignment(Qt.AlignCenter)
        self.placeholder_label_2.setStyleSheet("color: grey; font-size: 14px;")
        self.placeholder_label_2.setWordWrap(True)
        self.placeholder_label_2.hide()

        self.view.product_import_tableWidget.cellClicked.connect(self.addInvoiceController.render_product_infor)
        self.view.list_product_import.cellClicked.connect(self.set_enable_btn)
        self.view.list_product_import.cellClicked.connect(self.fill_data_for_edit)
        self.view.import_price.textChanged.connect(lambda: self.format_number(self.view.import_price))
        self.view.add_product_import.clicked.connect(self.add_product_to_invoice)
        self.view.delete_product_import.clicked.connect(self.remove_product_from_invoice)
        self.view.update_product_import.clicked.connect(self.save_product_update)

        self.load_product()
        self.load_product_to_import()
        self.check_invoice()

    def check_invoice(self):
        frame_import_price = self.view.frame_import_price
        type_invoice_comboBox = self.view.type_invoice_comboBox
        employee_data = self.query_data.get_employee_name_by_id(self.employee_id)
        if employee_data and 'employee_name' in employee_data:
            employee_name = employee_data['employee_name']
        else:
            employee_name = "Không xác định"
        if type_invoice_comboBox.currentIndex() != 1:
            frame_import_price.show()
            new_invoice_id = self.query_data.get_new_invoice_code("PN")
        else:
            frame_import_price.hide()
            new_invoice_id = self.query_data.get_new_invoice_code("PH")
        self.view.import_id_output.setText(new_invoice_id)
        self.view.employee_output.setText(employee_name)


    def load_product(self):
        data = self.query_data.get_all_product()
        table = self.view.product_import_tableWidget
        headers = ["Mã sản phẩm", "Tên sản phẩm", "Loại", "Số lượng Tồn"]
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setRowCount(len(data))
        print(f"DEBUG: DATA PRODUCT: {data}")
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        if not data:
            print("Không có dữ liệu sản phẩm")
            self.view.product_import_tableWidget.setRowCount(0)
            self.placeholder_label.resize(self.view.product_tableWidget.viewport().size())
            self.placeholder_label.show()
            return
        else:
            self.placeholder_label.hide()

        for row_index, row_data in enumerate(data):
            for col_index, cell_data in enumerate(row_data):
                item = QTableWidgetItem(str(cell_data))
                table.setItem(row_index, col_index, item)
        table.resizeColumnsToContents()
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setAlternatingRowColors(False)
        table.setSortingEnabled(True)
        table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        table.verticalHeader().setVisible(False)
        table.setFocusPolicy(Qt.NoFocus)
        table.setSelectionMode(QAbstractItemView.SingleSelection)

    def get_selected_product_import_data(self):
        selected_rows = self.view.product_import_tableWidget.selectionModel().selectedRows()
        if not selected_rows:
            return None
        row_index = selected_rows[0].row()
        headers = ["product_id", "product_name", "product_type", "product_quantity"]
        product_data = {}
        table = self.view.product_import_tableWidget
        for col_index in range(table.columnCount()):
            item = table.item(row_index, col_index)
            if item is not None:
                key = headers[col_index]
                value = item.text()
                product_data[key] = value
        return product_data

    def eventFilter(self, obj, event):
        table1 = self.view.product_import_tableWidget
        if (obj == table1 or obj == table1.viewport()) and event.type() == QEvent.Resize:
            self.placeholder_label.setGeometry(table1.viewport().rect())

        table2 = self.view.list_product_import
        if (obj == table2 or obj == table2.viewport()) and event.type() == QEvent.Resize:
            self.placeholder_label_2.setGeometry(table2.viewport().rect())

        # Xử lý click ra ngoài để bỏ chọn
        if obj == self.parent() and event.type() == QEvent.MouseButtonPress:
            mapped_pos = self.mapFromParent(event.pos())
            # Kiểm tra nếu click ngoài CẢ 2 bảng thì mới bỏ chọn và clear input
            if not table1.geometry().contains(mapped_pos) and not table2.geometry().contains(mapped_pos):
                table1.clearSelection()
                table2.clearSelection()
                self.clear_input_fields()

        return super().eventFilter(obj, event)

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

    def set_enable_btn(self):
        self.view.update_product_import.setEnabled(True)
        self.view.delete_product_import.setEnabled(True)

    def set_disable_btn(self):
        self.view.update_product_import.setEnabled(False)
        self.view.delete_product_import.setEnabled(False)

    def clear_input_fields(self):
        if hasattr(self.view, 'product_id_import'): self.view.product_id_import.clear()
        if hasattr(self.view, 'type_import'): self.view.type_import.clear()
        if hasattr(self.view, 'name_import'): self.view.name_import.clear()
        self.view.quantity_import.clear()
        self.view.import_price.clear()
        self.view.update_product_import.setEnabled(False)
        self.view.delete_product_import.setEnabled(False)

    def add_product_to_invoice(self):
        p_id = self.view.product_id_import.text().strip()
        p_name = self.view.name_import.text()
        p_type = self.view.type_import.text()
        price_text = self.view.import_price.text().replace(',', '').strip()
        qty_text = self.view.quantity_import.text().strip()

        if not price_text or not qty_text:
            QMessageBox.warning(self.view, "Thiếu thông tin", "Vui lòng nhập đầy đủ Giá nhập và Số lượng!")
            return

        try:
            price = int(price_text)
            quantity = int(qty_text)
        except ValueError:
             print("Lỗi: Giá hoặc số lượng không hợp lệ.")
             return
        if not p_id:
            QMessageBox.information(self.view,"Thông báo", "Vui lòng chọn sản phẩm trước khi thêm!")
            return
        if quantity <= 0:
            QMessageBox.information(self.view,"Thông báo", "Vui lòng nhập số lượng từ 1 trở lên")
            return
        if p_id in self.data_import:
            QMessageBox.warning(
                self.view,
                "Sản phẩm đã tồn tại",
                f"Sản phẩm có mã '{p_id}' đã có trong phiếu.\n"
                "Vui lòng nhấn nút 'Sửa sản phẩm' nếu muốn thay đổi giá nhập hoặc số lượng."
            )
            return
        else:
            self.data_import[p_id] = {
                'product_id': p_id,
                'product_name': p_name,
                'product_type': p_type,
                'price': price,
                'quantity': quantity
            }
        self.load_product_to_import()
        self.clear_input_fields()


    def load_product_to_import(self):
        data_list = list(self.data_import.values())
        table = self.view.list_product_import
        headers = ["Mã SP", "Tên sản phẩm", "Loại", "Đơn giá", "Số lượng", "Thành tiền"]
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.setRowCount(len(data_list))
        table.horizontalHeader().setDefaultAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        if not data_list:
            print("Không có dữ liệu sản phẩm")
            self.view.list_product_import.setRowCount(0)
            self.placeholder_label_2.resize(self.view.list_product_import.viewport().size())
            self.placeholder_label_2.show()
            return
        else:
            self.placeholder_label_2.hide()

        total_invoice_value = 0
        for row_idx, item_data in enumerate(data_list):
            total = item_data['price'] * item_data['quantity']
            total_invoice_value += total

            row_values = [
                item_data['product_id'],
                item_data['product_name'],
                item_data['product_type'],
                "{:,}".format(item_data['price']),
                str(item_data['quantity']),
                "{:,}".format(total)
            ]

            for col_idx, value in enumerate(row_values):
                item = QTableWidgetItem(value)
                if col_idx >= 3:
                    item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                else:
                    item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                table.setItem(row_idx, col_idx, item)
        self.view.total_price_import.setText(f"{total_invoice_value:,}đ")
        table.resizeColumnsToContents()
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setSelectionBehavior(QAbstractItemView.SelectRows)
        table.setAlternatingRowColors(False)
        table.setSortingEnabled(True)
        table.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        table.verticalHeader().setVisible(False)
        table.setFocusPolicy(Qt.NoFocus)
        table.setSelectionMode(QAbstractItemView.SingleSelection)

    def remove_product_from_invoice(self):
        current_row = self.view.list_product_import.currentRow()
        if current_row == -1:
            QMessageBox.warning(self.view, "Thông báo", "Vui lòng chọn dòng sản phẩm cần xóa trong phiếu!")
            return
        p_id_item = self.view.list_product_import.item(current_row, 0)
        if p_id_item:
             p_id = p_id_item.text()
             reply = QMessageBox.question(
                 self.view,
                 'Xác nhận xóa',
                 f"Bạn có chắc muốn xóa sản phẩm '{p_id}' khỏi phiếu này không?",
                 QMessageBox.Yes | QMessageBox.No,
                 QMessageBox.No
             )

             if reply == QMessageBox.Yes:
                if p_id in self.data_import:
                    del self.data_import[p_id]
                    print(f"DEBUG: Đã xóa {p_id} khỏi phiếu tạm.")
                self.load_product_to_import()

    def fill_data_for_edit(self):
        current_row = self.view.list_product_import.currentRow()
        if current_row < 0:
            return
        p_id = self.view.list_product_import.item(current_row, 0).text()

        if p_id in self.data_import:
            data = self.data_import[p_id]

            self.view.product_id_import.setText(data['product_id'])
            self.view.name_import.setText(data['product_name'])
            self.view.type_import.setText(data['product_type'])
            self.view.import_price.setText(str(data['price']))
            self.view.quantity_import.setText(str(data['quantity']))

    def save_product_update(self):
        p_id = self.view.product_id_import.text().strip()
        price_text = self.view.import_price.text().replace(',', '').strip()
        qty_text = self.view.quantity_import.text().strip()
        if not p_id or not price_text or not qty_text:
             QMessageBox.warning(self.view, "Thiếu thông tin", "Vui lòng chọn sản phẩm và nhập đầy đủ giá, số lượng!")
             return
        try:
            price = int(price_text)
            quantity = int(qty_text)
        except ValueError:
             QMessageBox.warning(self.view, "Lỗi định dạng", "Giá và số lượng phải là số hợp lệ.")
             return

        if quantity <= 0:
             QMessageBox.warning(self.view, "Lỗi số lượng", "Số lượng phải lớn hơn 0.")
             return

        if p_id not in self.data_import:
             QMessageBox.warning(self.view, "Lỗi", "Sản phẩm này không có trong phiếu để sửa!")
             return
        self.data_import[p_id]['price'] = price
        self.data_import[p_id]['quantity'] = quantity

        print(f"DEBUG: Đã cập nhật {p_id} - Giá: {price}, SL: {quantity}")

        self.load_product_to_import()
        self.clear_input_fields()
        QMessageBox.information(self.view, "Thành công", "Đã cập nhật thông tin sản phẩm.")

    def reset_view(self):
        print("DEBUG: LOAD LẠI ADD INVOICE")
        self.data_import.clear()
        self.clear_input_fields()
        self.load_product_to_import()
        self.load_product()
        self.check_invoice()
        self.view.total_price_import.setText("0đ")