
from PyQt5.QtCore import QObject, pyqtSignal

class GlobalSignals(QObject):
    product_data_changed = pyqtSignal()

app_signals = GlobalSignals()