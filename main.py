import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets, QtCore, QtGui

from src.views.employee_main_view.invoice_detail_view import InvoiceDetailView
from src.views.employee_main_view.item_card import ItemCard
from src.views.login_view.login_view import Login_Window
# from src.windows.login_window import open_login_window
from src.views.employee_main_view.product_card import ProductCard  # nếu bạn lưu class trên vào file product_card.py

def load_stylesheet(file_path):
    """Đọc và trả về nội dung của một file stylesheet."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"WARNING: Stylesheet file not found at '{file_path}'")
        return ""

if __name__ == "__main__":
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    # Load font từ resource (đường dẫn trong .qrc)
    # QtGui.QFontDatabase.addApplicationFont(":/UI/fonts/LuckiestGuy-Regular.ttf")

    app = QtWidgets.QApplication(sys.argv)
    # open_login_window()

    stylesheet_path = "UI/styles/container.css"

    # Đọc file
    stylesheet = load_stylesheet(stylesheet_path)

    # Áp dụng cho toàn bộ ứng dụng
    if stylesheet:
        app.setStyleSheet(stylesheet)
        print("Stylesheet loaded successfully.")

    # auto fill login for testing
    login_window = Login_Window()
    if login_window.login_controller:
        login_window.login_controller.auto_fill_login("251000002")
    login_window.show()

    # invoice_detail = InvoiceDetailView()
    # invoice_detail.show()

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