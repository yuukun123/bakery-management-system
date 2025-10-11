# from src.views.login_view.login_regis import Login_and_Register_Window
from src.views.manager_main_view.manager_main_view import ManagerMainWindow
# from src.views.main_view.topic_view import TopicWindow
# from src.views.main_view.vocab_view import VocabWindow
# from src.controllers.login_regis_controllers.login_controller import LoginController
#
# def open_login_window():
#     window = Login_and_Register_Window()
#     controller = LoginController(window)
#     window.controller = controller
#     window.show()
#     return window

def open_main_window():
    window = ManagerMainWindow()
    window.setFixedSize(1920, 1080)
    window.show()
    return window