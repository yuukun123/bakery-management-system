from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication

from src.controllers.buttonController import buttonController
from src.services.query_user_name import QueryUserName
from src.utils.username_ui import set_employee_info, set_employee_role
from src.views.moveable_window import MoveableWindow
from resources import resources_rc

class ManagerMainWindow(QMainWindow, MoveableWindow):
    def __init__(self, employee_id):
        # self.username = username
        super().__init__()
        uic.loadUi("UI/forms/manager/manager_main_screen.ui", self)
        MoveableWindow.__init__(self)

        # Thêm frameless + trong suốt
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowOpacity(1.0)

        self.query_username = QueryUserName()
        self._employee_context = None
        self._employee_role = None
        self.employee_id = employee_id
        self.load_employee_context(self.employee_id)

        if not self._employee_context:
            QMessageBox.critical(self, "Lỗi nghiêm trọng", f"Không thể tìm thấy dữ liệu cho người dùng '{self.employee_id}'.")
            return
        employee_name = self._employee_context.get('employee_name', 'Unknown')
        employee_role = self._employee_role.get('role', 'Unknown')

        set_employee_info(self.username_label, employee_name)
        set_employee_role(self.role_label, employee_role)
    #
        self.buttonController = buttonController(self)
        self.closeBtn.clicked.connect(buttonController.handle_close)
        self.hideBtn.clicked.connect(self.buttonController.handle_hidden)
        self.logout.clicked.connect(self.buttonController.handle_logout)

    def load_employee_context(self, employee_id):
        print(f"DEBUG: Đang tải user context cho employee id: {employee_id}")
        self._employee_context = self.query_username.get_employee_by_employee_id(employee_id)
        self._employee_role = self.query_username.get_employee_role_by_employee_id(employee_id)
        print(f"DEBUG: User context đã tải: {self._employee_context}")
    #
    # def handle_topic_window_click(self):
    #     print("DEBUG: start open_topic_window")
    #     if not self._user_context:
    #         # Sử dụng self._user_context để lấy username cho thông báo lỗi
    #         user_name_for_msg = self.username # Hoặc một giá trị mặc định
    #         QMessageBox.critical(self, "Lỗi nghiêm trọng", f"Không thể tìm thấy dữ liệu cho người dùng '{user_name_for_msg}'.")
    #         return
    #     try:
    #         self.hide()  # ẩn ngay lập tức
    #         current_username = self._user_context.get('user_name')
    #         self.topic_window = TopicWindow(parent=self, username=current_username, main_window=self)
    #         self.topic_window.topic_controller.setup_for_user(self._user_context)
    #         print("DEBUG: topic_window created", self.topic_window)
    #         self.topic_window.show()
    #         print("DEBUG: vocab_window show called")
    #     except Exception as e:
    #         print("ERROR while opening topic window:", e)
    #         self.show()
    #
    # def handle_practice_window_click(self):
    #     print("DEBUG: start open dialog topic_for_practice")
    #     dialog = topic_practice(self._user_context, self)
    #     dialog.open()


