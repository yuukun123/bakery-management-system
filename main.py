import sys
from PyQt5 import QtWidgets, QtCore

from src.windows.login_window import open_login_window

if __name__ == "__main__":
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication(sys.argv)
    open_login_window()
    # window = open_employee_main_window()
    sys.exit(app.exec_())