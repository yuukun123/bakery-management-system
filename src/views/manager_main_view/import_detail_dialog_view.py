import os
import re
import shutil
from PyQt5 import uic
from PyQt5.QtGui import QColor, QRegExpValidator, QPixmap, QIntValidator
from PyQt5.QtWidgets import QDialog, QGraphicsDropShadowEffect, QWidget, QMessageBox, QLineEdit, QFileDialog
from src.services.query_data_manager.manager_query_data import QueryData
from PyQt5.QtCore import Qt, QPoint, QDateTime, QDate, QRegExp
from src.views.moveable_window import MoveableWindow

class importDetail(QDialog,MoveableWindow):
    def __init__(self, parent=None):
        MoveableWindow.__init__(self)
        super(importDetail, self).__init__(parent)
        uic.loadUi("UI/forms/manager/import_invoice_detail.ui", self)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.query_data = QueryData()
        self.cancel_btn.clicked.connect(self.reject)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0, 0, 0, 150))
        self.findChild(QWidget, "mainFrame").setGraphicsEffect(shadow)

    # def load_table(self, data):



