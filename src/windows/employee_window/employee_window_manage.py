from src.views.employee_main_view.employee_main_view import EmployeeMainWindow

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