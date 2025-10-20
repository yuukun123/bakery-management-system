import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets, QtCore

from src.views.employee_main_view.item_card import ItemCard
from src.views.login_view.login_view import Login_Window
# from src.windows.login_window import open_login_window
from src.views.employee_main_view.product_card import ProductCard  # nếu bạn lưu class trên vào file product_card.py

if __name__ == "__main__":
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QtWidgets.QApplication(sys.argv)
    # open_login_window()

    # auto fill login for testing
    login_window = Login_Window()
    if login_window.login_controller:
        login_window.login_controller.auto_fill_login("251000003")
    login_window.show()

    sys.exit(app.exec_())

    # Dữ liệu test
    # product_data = {
    #     "product_id": 1,
    #     "product_name": "Strawberry Dream Croissant",
    #     "selling_price": 100000,
    #     "image_path": "UI/images/Mousse/Avocado_Mousse.jpg"
    # }
    #
    # window = QMainWindow()
    # card = ItemCard(product_data)
    # window.setCentralWidget(card)
    # # window.resize(300, 300)
    # window.show()
    #
    # sys.exit(app.exec_())