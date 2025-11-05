import os
import re
from werkzeug.security import generate_password_hash
from PyQt5 import uic
from PyQt5.QtGui import QColor, QRegExpValidator
from PyQt5.QtWidgets import QDialog, QGraphicsDropShadowEffect, QWidget, QMessageBox, QLineEdit
from src.services.query_data_manager.manager_query_data import QueryData
from PyQt5.QtCore import Qt, QPoint, QDateTime, QDate, QRegExp
from src.utils.validators import is_valid_phone_number
from src.views.moveable_window import MoveableWindow

class updateEmployee(QDialog,MoveableWindow):
    def __init__(self, data=None, parent=None):
        MoveableWindow.__init__(self)
        super(updateEmployee, self).__init__(parent)
        uic.loadUi("UI/forms/manager/update_employee.ui", self)
        self.text_error.hide()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.updateuser_btn.clicked.connect(self.check_data)
        self.query_data = QueryData()
        self.cancel_btn.clicked.connect(self.reject)
        self.status_comboBox.setEnabled(False)

        self.data = data
        print("----DEBUG: DATA BAN ĐẦU----")
        print(self.data)
        if self.data is None:
             QMessageBox.critical(self, "Lỗi", "Không tìm thấy dữ liệu nhân viên để cập nhật.")
             self.reject()
             return
        self.set_data(self.data)

        regex = QRegExp("^0[0-9]{9}$")
        self.phonenumber_input.setValidator(QRegExpValidator(regex))

        self.name_input.textChanged.connect(self.hide_error_frame)
        self.email_input.textChanged.connect(self.hide_error_frame)
        self.address_input.textChanged.connect(self.hide_error_frame)
        self.phonenumber_input.textChanged.connect(self.hide_error_frame)
        self.sex_comboBox.currentIndexChanged.connect(self.hide_error_frame)
        self.role_comboBox.currentIndexChanged.connect(self.hide_error_frame)
        self.dateEdit.dateChanged.connect(self.hide_error_frame)


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
        name = data["name"]
        email = data["email"]
        address = data["address"]
        sex = data["gender"].capitalize()
        phone_number = data["phone_number"]
        role = data["role"].capitalize()
        status = data["status"].lower()
        start_date_str = data["start_date"]
        self.name_input.setText(name)
        self.email_input.setText(email)
        self.address_input.setText(address)
        self.phonenumber_input.setText(phone_number)
        self.sex_comboBox.setCurrentText(sex)
        self.role_comboBox.setCurrentText(role)
        self.status_comboBox.setCurrentText(status)
        start_date_qdate = QDate.fromString(start_date_str, "yyyy-MM-dd")
        if start_date_qdate.isValid():
            self.dateEdit.setDate(start_date_qdate)
        else:
            # Xử lý nếu chuỗi ngày không hợp lệ (nên thêm log hoặc báo lỗi)
            print(f"ERROR: Invalid date string received: {start_date_str}")
        print(f"----DEBUG: DATA SAU KHI SET----")
        print(name,email,address,sex,phone_number,role,status,start_date_qdate)

    def check_data(self):
        print("BẮT ĐẦU CHECK DATA")
        name = self.name_input.text().lower().strip()
        email = self.email_input.text().lower().strip()
        address = self.address_input.text()
        phoneNumber = self.phonenumber_input.text()
        sex = self.sex_comboBox.currentText().lower()
        sex_index = self.sex_comboBox.currentIndex()
        role = self.role_comboBox.currentText().lower()
        role_index = self.role_comboBox.currentIndex()
        status = self.status_comboBox.currentText().lower()
        date = self.dateEdit.date()
        password_hash = generate_password_hash("1")
        old_email = self.data["email"].lower().strip()
        old_phoneNumber = self.data["phone_number"]
        print("DEBUG: BẮT ĐẦU KIỂM TRA DỮ LIỆU")
        if not name or not email or not address or not phoneNumber:
            self.show_message("Please fill in all information")
            return
        if sex_index == 0 or role_index == 0:
            self.show_message("Please fill in all information")
            return
        if not re.match(r"^[a-zA-Z0-9._%+-]+@gmail\.com$", email):
            self.show_message("Invalid Email!")
            return
        if email != old_email:
            if self.query_data.check_mail_exists(email):
                self.show_message("Email already exists!")
                return
        if not is_valid_phone_number(phoneNumber):
            self.show_message("Invalid Phone Number!")
            return
        if phoneNumber != old_phoneNumber:
            if self.query_data.check_phone_exists(phoneNumber):
                self.show_message("Phone number already exists")
                return
        print("DEBUG: DỮ LIỆU HỢP LỆ BẮT ĐẦU UPDATE")
        update_data = {
            "name": name,
            "password": password_hash,
            "email": email,
            "address": address,
            "phoneNumber": phoneNumber,
            "gender": sex,
            "role": role,
            "status": status,
            "startDate": date.toString("yyyy-MM-dd"),
            "endDate": self.data["end_date"],
            "employee_id": self.data["employee_id"]
        }
        result = self.query_data.update_employee(update_data)
        if result:
            self.accept()






