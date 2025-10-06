from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication

# from src.services.query_data.query_data import QueryData
from src.controllers.buttonController import buttonController
# from src.utils.username_ui import set_user_info
from src.views.moveable_window import MoveableWindow
from resources import resources_rc

class EmployeeMainWindow(QMainWindow, MoveableWindow):
    def __init__(self):
        # self.username = username
        super().__init__()
        uic.loadUi("UI/forms/employee/employee_main_screen.ui", self)
        MoveableWindow.__init__(self)

        # self.go_back.hide()

        # Thêm frameless + trong suốt
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1.0)

        # self.query_data = QueryData()
        # self._user_context = None
        # self.load_user_context(username)
        #
        # if not self._user_context:
        #     QMessageBox.critical(self, "Lỗi nghiêm trọng", f"Không thể tìm thấy dữ liệu cho người dùng '{username}'.")
        #     return
        #
        # set_user_info(self.username_label, username)

        self.buttonController = buttonController(self)
        self.closeBtn.clicked.connect(buttonController.handle_close)
        self.hideBtn.clicked.connect(self.buttonController.handle_hidden)
        # self.logout.clicked.connect(self.buttonController.handle_logout)
        #
        # self.vocab.clicked.connect(self.handle_topic_window_click)
        # self.practice.clicked.connect(self.handle_practice_window_click)
        # print("DEBUG: vocab button connected")

    # def load_user_context(self, username):
    #     print(f"DEBUG: Đang tải user context cho username: {username}")
    #     self._user_context = self.query_data.get_user_by_username(username)
    #     print(f"DEBUG: User context đã tải: {self._user_context}")