from PyQt5 import uic
from PyQt5.QtWidgets import QToolButton, QLineEdit, QPushButton

from src.services.query_data_employee.employee_query_data import EmployeeQueryData


class AddCustomerView:
    def __init__(self):
        super().__init__()
        uic.loadUi("UI/forms/employee/customer_infor_view.ui", self)
        self._initialized = False  # Cờ để chắc rằng chúng ta chỉ setup 1 lần
