from PyQt5 import uic, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QLineEdit

from src.controllers.login_controllers.login_controller import LoginController
from src.views.moveable_window import MoveableWindow
from src.controllers.buttonController import buttonController
from resources import resources_rc

class Login_Window(QMainWindow , MoveableWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/forms/login.ui", self)
        MoveableWindow.__init__(self)
        # bên login_query đặt mặc định ẩn khi mở vì login_query luôn mở lên đầu tiên
        QtGui.QFontDatabase.addApplicationFont(":/UI/fonts/LuckiestGuy-Regular.ttf")
        font = QtGui.QFont("Luckiest Guy", 50)
        self.label.setFont(font)
        self.label.setStyleSheet("color: #1A5276;")

        font = QtGui.QFont("Luckiest Guy", 50)
        self.label_7.setFont(font)

        self.errors_5.hide()
        self.errors_6.hide()
        # Thêm frameless + trong suốt
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1.0)
        # Tạo controller, truyền self vào
        self.buttonController = buttonController(self)
        self.login_controller = LoginController(self)
        # Gắn nút
        self.LoginBtn.clicked.connect(
            lambda: self.login_controller.handle_login(
                self.employee_id_login.text(), self.password_login.text()
            )
        )
        self.closeBtn.clicked.connect(buttonController.handle_close)
        self.hideBtn.clicked.connect(self.buttonController.handle_hidden)

        # show and hide password
        self.show_pass.clicked.connect(self.toggle_new_password)
        self.hide_pass.clicked.connect(self.toggle_new_password)
        self.hide_pass.hide()  # ẩn icon hide ban đầu

    def toggle_new_password(self):
        if self.password_login.echoMode() == QLineEdit.Password:
            # Hiện mật khẩu
            self.password_login.setEchoMode(QLineEdit.Normal)
            self.show_pass.hide()
            self.hide_pass.show()
        else:
            # Ẩn mật khẩu
            self.password_login.setEchoMode(QLineEdit.Password)
            self.hide_pass.hide()
            self.show_pass.show()