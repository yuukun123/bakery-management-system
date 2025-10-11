from src.controllers.login_controllers.login_controller import LoginController
from src.views.login_view.login_view import Login_Window

def open_login_window():
    window = Login_Window()
    controller = LoginController(window)
    window.controller = controller
    window.show()
    return window