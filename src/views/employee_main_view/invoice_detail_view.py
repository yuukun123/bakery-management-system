from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog

from src.controllers.employee_main_controller.invoice_detail_controller import InvoiceDetailController
from src.views.moveable_window import MoveableWindow
from resources import resources_rc

class InvoiceDetailView(QDialog, MoveableWindow):
    def __init__(self, invoice_code):
        super().__init__()
        uic.loadUi("UI/forms/employee/invoice_detail.ui", self)
        MoveableWindow.__init__(self)
        self.invoice_code = invoice_code

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1.0)

        self.cancel_btn.clicked.connect(self.accept)

        self.invoice_controller = InvoiceDetailController(self, self.invoice_code)
        self.invoice_controller.setup_dialog()
