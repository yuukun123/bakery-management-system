import sys
from PyQt5 import QtWidgets, QtCore

from src.windows.employee_window.employee_window_manage import open_employee_main_window

# from src.views.login_view.login_regis import Login_and_Register_Window

if __name__ == "__main__":
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication(sys.argv)
    # open_login_window()
    window = open_employee_main_window()
    sys.exit(app.exec_())