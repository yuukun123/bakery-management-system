# from src.views.login_view.login_regis import Login_and_Register_Window
from src.views.employee_main_view.employee_main_view import EmployeeMainWindow
# from src.views.main_view.topic_view import TopicWindow
# from src.views.main_view.vocab_view import VocabWindow
# from src.controllers.login_controllers.login_controller import LoginController

def open_employee_main_window(employee_id):
    window = EmployeeMainWindow(employee_id)
    window.setFixedSize(1920, 1080)
    window.show()
    return window

# def open_topic_window(username_login, parent=None):
#     window = TopicWindow(username_login, parent=parent)
#     window.show()
#     return window
#
# def open_vocab_window(username_login, topic_id, pre_window, parent=None):
#     window = VocabWindow(username_login, topic_id, pre_window, parent=parent)
#     window.show()
#     return window