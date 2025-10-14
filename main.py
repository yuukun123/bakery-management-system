import sys
from PyQt5 import QtWidgets, QtCore

from src.windows.login_window import open_login_window

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from src.views.employee_main_view.product_card import ProductCard  # nếu bạn lưu class trên vào file product_card.py

if __name__ == "__main__":
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    # app = QtWidgets.QApplication(sys.argv)
    # open_login_window()
    # # window = open_employee_main_window()
    # sys.exit(app.exec_())



    if __name__ == "__main__":
        app = QApplication(sys.argv)

        # Dữ liệu test
        product_data = {
            "product_id": 1,
            "product_name": "Avocado Croissant",
            "selling_price": 100000,
            "image_path": "UI/images/Croissant/Avocado_Croissant.jpg"
        }

        window = QMainWindow()
        card = ProductCard(product_data)
        window.setCentralWidget(card)
        # window.resize(300, 300)
        window.show()

        sys.exit(app.exec_())