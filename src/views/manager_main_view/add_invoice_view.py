from PyQt5.QtWidgets import QWidget


class addInvoiceViewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.view = parent
        self.view.type_invoice_comboBox.currentIndexChanged.connect(self.check_invoice)

    def check_invoice(self):
        frame_import_price = self.view.frame_import_price
        type_invoice_comboBox = self.view.type_invoice_comboBox
        if type_invoice_comboBox.currentIndex() != 1:
            frame_import_price.show()
        else:
            frame_import_price.hide()