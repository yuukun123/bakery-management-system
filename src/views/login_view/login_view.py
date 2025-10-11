
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QLineEdit

from src.controllers.login_controllers.login_controller import LoginController
from src.views.moveable_window import MoveableWindow
from src.controllers.buttonController import buttonController

class Login_Window(QMainWindow , MoveableWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi("UI/forms/login.ui", self)

        MoveableWindow.__init__(self)

        # bên login đặt mặc định ẩn khi mở vì login luôn mở lên đầu tiên
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
                self.username_login.text(), self.password_login.text()
            )
        )

        self.closeBtn.clicked.connect(buttonController.handle_close)
        self.hideBtn.clicked.connect(self.buttonController.handle_hidden)

        # show and hide password
        self.hide_pass.clicked.connect(self.toggle_new_password)

        # #debug
        # self.login_link.clicked.connect(lambda: print("Login clicked"))
        #
        # buttons = [
        #     self.login_link
        # ]
        # index_map = {
        #     self.login_link: self.stackedWidget.indexOf(self.login_page),
        # }
        # self.menu_nav = MenuNavigator(self.stackedWidget, buttons, index_map, default_button=self.login_link)
        #
        # self.stackedWidget.currentChanged.connect(self.on_tab_changed)
        #
        # # Chủ động tải Dashboard lần đầu tiên nếu nó là tab mặc định
        # if self.stackedWidget.currentWidget() == self.login_page:
        #     self.on_tab_changed(self.stackedWidget.currentIndex())

    # def on_tab_changed(self, index):
    #     # clear toàn bộ input ở page trước đó
    #     prev_index = self.stackedWidget.previousIndex if hasattr(self.stackedWidget, "previousIndex") else None
    #     if prev_index is not None:
    #         old_widget = self.stackedWidget.widget(prev_index)
    #         for child in old_widget.findChildren(QLineEdit):
    #             child.clear()
    #
    #     # lưu lại index hiện tại
    #     self.stackedWidget.previousIndex = index
    #
    #     current_widget = self.stackedWidget.widget(index)
    #     if current_widget == self.login_page:
    #         # bên register
    #         self.errors_1.hide()
    #         self.errors_2.hide()
    #         self.errors_3.hide()
    #         self.errors_4.hide()
    #         print()
    #     elif current_widget == self.sign_up_page:
    #         # bên login
    #         self.errors_5.hide()
    #         self.errors_6.hide()
    #         print()
    #     elif current_widget == self.enter_email_page:
    #         self.errors_7.hide()

    def toggle_new_password(self):
        if self.enter_password.echoMode() == QLineEdit.Password:
            self.enter_password.setEchoMode(QLineEdit.Normal)
            path = "UI/icons/eye.svg"
            self.hide_pass.setIcon(QIcon(path))
        else:
            self.enter_password.setEchoMode(QLineEdit.Password)
            path = "UI/icons/eye-off.svg"
            self.hide_pass.setIcon(QIcon(path))