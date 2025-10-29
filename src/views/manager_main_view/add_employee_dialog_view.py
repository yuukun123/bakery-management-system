import os
from datetime import datetime
from PyQt5 import uic
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QDialog, QGraphicsDropShadowEffect, QWidget, QMessageBox, QLineEdit
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QPoint, QDateTime

class addEmployee(QDialog):
    def __init__(self, parent=None):
        super(addEmployee, self).__init__(parent)
        uic.loadUi("UI/forms/login.ui", self)
        self.text_error.hide()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.adduser_btn.clicked.connect(self.check_data)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 150))
        self.findChild(QWidget, "mainFrame").setGraphicsEffect(shadow)

    def show_message(self, text):
        if hasattr(self,"text_error"):
            self.text_error.setText(f"{text}")
            self.frame_check.show()
    def hide_error_frame(self):
        if hasattr(self, 'text_error'):
            self.frame_check.hide()

    def check_data(self):
        name = self.name_input.text()
        email = self.email_input.text()
        address = self.address_input.text()
        phoneNumber = self.phonenumber_input.text()
        sex = self.sex_comboBox.currentText()
        sex_index = self.sex_comboBox.currentIndex()
        role = self.role_comboBox.currentText()
        role_index = self.role_comboBox.currentIndex()
        status = self.status_comboBox.currentText()
        date = self.dateEdit.currentDate()

        if not name or not email or not address or not phoneNumber:
            self.show_message("Please fill in all information")
            return
        if


