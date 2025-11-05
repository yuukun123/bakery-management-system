from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QDialog, QMessageBox
from src.views.manager_main_view.add_employee_dialog_view import addEmployee
from src.services.query_data_manager.manager_query_data import QueryData
from src.views.manager_main_view.update_employee_dialog_view import updateEmployee

class employeeController:
        def __init__(self, mainview, tableview):
            self.query_data = QueryData()
            self.view = mainview
            self.table = tableview
            self.connect_filter_signal()
            self.load_employee_data()

        def open_add_employee_dialog(self):
            print("DEBUG: BẮT ĐẦU MỞ ADD DIALOG")
            dialog = addEmployee()
            result = dialog.exec_()
            if result == QDialog.Accepted:
                QMessageBox.information(self.view,"Thành công", "Đã thêm nhân viên thành công!")
                self.load_employee_data()

        def handle_quit_employee(self):
            employee_data =  self.table.get_selected_employee_data()
            reply = QMessageBox.question( self.view, 'Xác nhận Nghỉ việc',
                    f"Bạn có chắc chắn muốn cho nhân viên này nghỉ việc?",
                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.set_employee_inactive(employee_data)

        def set_employee_inactive(self, data):
            print(f"DEBUG: CHO NHÂN VIÊN NGHỈ VIỆC")
            now = QDate.currentDate()
            update_data = {
                "employee_id": data["employee_id"],
                "end_date": now.toString("yyyy-MM-dd")
            }
            success = self.query_data.update_inactive_employee(update_data)
            if success:
                QMessageBox.information(
                         self.view,
                        "Thành công",
                        f"Đã cho nhân viên {data['name']} (ID: {data['employee_id']}) nghỉ việc thành công."
                    )
                self.load_employee_data()
            else:
                QMessageBox.critical(
                     self.view,
                    "Lỗi",
                    f"Không thể cập nhật trạng thái nghỉ việc cho nhân viên {data['name']}."
                )
        def open_update_employee_dialog(self):
            print("DEBUG: BẮT ĐẦU MỞ UPDATE DIALOG")
            employee_data = self.table.get_selected_employee_data()
            if not employee_data:
                print("lỗi không lấy được employee data")
            # if employee_data["status"].lower() == "đã nghỉ":
            #     QMessageBox.warning(self.view, "Không thể sửa", "Không thể sửa thông tin của nhân viên đã nghỉ việc.")
            #     return
            dialog = updateEmployee(data=employee_data)
            result = dialog.exec_()
            if result == QDialog.Accepted:
                QMessageBox.information( self.view,"Thành công", "Đã sửa thông tin nhân viên thành công!")
                self.load_employee_data()

        def connect_filter_signal(self):
            try:
                self.view.filter_employee.currentIndexChanged.connect(self.load_employee_data)
                self.view.display_filter.currentIndexChanged.connect(self.load_employee_data)
                self.view.status_filter.currentIndexChanged.connect(self.load_employee_data)
                self.view.search_employee_btn.clicked.connect(self.load_employee_data)
                self.view.search_input.textChanged.connect(self.reset_search)
            except AttributeError as e:
                print(f"LỖI: Không tìm thấy widget filter trong View. Tên widget có đúng không? {e}")

        def reset_search(self):
            if self.view.search_input.text() == "":
                self.load_employee_data()

        def load_employee_data(self):
            try:
                role = self.view.filter_employee.currentText().lower()
                status = self.view.status_filter.currentText().lower()
                display = self.view.display_filter.currentText()
                search_term = self.view.search_input.text().strip()

                if not role:
                    role = "Tất cả"
                if not status:
                    status = "Tất cả"
                if not display:
                    display = "Tất cả"

                filtered_data = self.query_data.search_employees(role,status,display,search_term)
                self.table.populate_employee_table(filtered_data)
            except Exception as e:
                print(f"Lỗi khi tải/filter dữ liệu nhân viên: {e}")