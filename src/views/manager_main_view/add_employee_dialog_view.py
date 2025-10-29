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

class addEmployee(QDialog,MoveableWindow):
    def __init__(self, parent=None):
        MoveableWindow.__init__(self)
        super(addEmployee, self).__init__(parent)
        uic.loadUi("UI/forms/manager/add_employee.ui", self)
        self.text_error.hide()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.adduser_btn.clicked.connect(self.check_data)
        self.query_data = QueryData()
        self.cancel_btn.clicked.connect(self.reject)
        now = QDate.currentDate()
        self.dateEdit.setDate(now)
        self.status_comboBox.setEnabled(False)
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

    def check_data(self):
        name = self.name_input.text().lower()
        email = self.email_input.text().lower()
        address = self.address_input.text()
        phoneNumber = self.phonenumber_input.text()
        sex = self.sex_comboBox.currentText()
        sex_index = self.sex_comboBox.currentIndex()
        role = self.role_comboBox.currentText()
        role_index = self.role_comboBox.currentIndex()
        status = self.status_comboBox.currentText()
        date = self.dateEdit.date()
        password_hash = generate_password_hash("1")
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
        if self.query_data.check_mail_exists(email):
            self.show_message("Email already exists!")
            return
        if not is_valid_phone_number(phoneNumber):
            self.show_message("Invalid Phone Number!")
            return
        if self.query_data.check_phone_exists(phoneNumber):
            self.show_message("Phone number already exists")
            return
        print("DEBUG: DỮ LIỆU HỢP LỆ BẮT ĐẦU UPDATE")
        data = {
            "name": name,
            "password": password_hash,
            "email": email,
            "address": address,
            "phoneNumber": phoneNumber,
            "sex": sex,
            "role": role,
            "status": status,
            "startDate": date.toString("yyyy-MM-dd"),
            "endDate": ""
        }
        result = self.query_data.add_new_employee(data)
        if result:
            self.accept()






