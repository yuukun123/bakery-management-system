import sys
from PyQt5 import QtWidgets, QtCore

from src.controllers.login_controllers.login_controller import LoginController
from src.views.login_view.login_view import Login_Window
# from src.windows.employee_window.employee_window_manage import open_employee_main_window

def open_login_window():
    window = Login_Window()
    controller = LoginController(window)
    window.controller = controller
    window.show()
    return window

if __name__ == "__main__":
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication(sys.argv)
    open_login_window()
    # window = open_employee_main_window()
    sys.exit(app.exec_())