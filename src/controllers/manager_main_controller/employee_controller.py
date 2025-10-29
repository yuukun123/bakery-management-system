from PyQt5.QtWidgets import QDialog, QMessageBox
from src.views.manager_main_view.add_employee_dialog_view import addEmployee

def open_add_employee_dialog(self):
    print("DEBUG: BẮT ĐẦU MỞ DIALOG")
    dialog = addEmployee()
    result = dialog.exec_()
    if result == QDialog.Accepted:
        QMessageBox.information(self,"successfully", "Add employee successful")
        self.load_employee_data()