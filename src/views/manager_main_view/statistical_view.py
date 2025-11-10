from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QDate, QTimer
from src.views.manager_main_view.revenue_stats_view import RevenueStatsView
from src.views.manager_main_view.product_stats_view import ProductStatsView
from src.views.manager_main_view.destroy_stats_view import DestroyStatsView

class statisticalView(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.ui = parent

        self.revenue_view = RevenueStatsView(parent=self.ui)
        self.product_view = ProductStatsView(parent = self.ui)
        self.destroy_view = DestroyStatsView(parent = self.ui)

        self.ui.dateOption.hide()
        self.ui.dateOption.setDate(QDate.currentDate())
        self.ui.date_option_product.hide()
        self.ui.date_option_product.setDate(QDate.currentDate())
        self.ui.date_option_destroy.hide()
        self.ui.date_option_destroy.setDate(QDate.currentDate())

        self.ui.statistical_invenue_btn.clicked.connect(self.handle_statistical_btn)
        self.ui.statistical_product_btn.clicked.connect(self.handle_statistical_product)
        self.ui.statistical_destroy_btn.clicked.connect(self.handle_statistical_destroy)

        self.ui.time_statiscal_comboBox.currentIndexChanged.connect(self.on_combobox_revenue_changed)
        self.ui.time_statiscal_product.currentIndexChanged.connect(self.on_comboBox_product_changed)
        self.ui.time_statiscal_destroy.currentIndexChanged.connect(self.on_comboBox_destroy_changed)

        self.ui.statistical_invenue_tab.clicked.connect(self.show_revenue_view)
        self.revenue_view.update_charts()
        self.product_view.update_best_seller_table()
        self.product_view.update_low_product_table()
        self.destroy_view.update_stats()

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(50, self.handle_statistical_btn)

    def on_combobox_revenue_changed(self):
        selection = self.ui.time_statiscal_comboBox.currentText()
        if selection == 'Tùy chỉnh':
            self.ui.dateOption.show()
        else:
            self.ui.dateOption.hide()

    def on_comboBox_product_changed(self):
        selection = self.ui.time_statiscal_product.currentText()
        if selection == 'Tùy chỉnh':
            self.ui.date_option_product.show()
        else:
            self.ui.date_option_product.hide()

    def on_comboBox_destroy_changed(self):
        selection = self.ui.time_statiscal_destroy.currentText()
        if selection == 'Tùy chỉnh':
            self.ui.date_option_destroy.show()
        else:
            self.ui.date_option_destroy.hide()

    def handle_statistical_btn(self):
        self.revenue_view.update_charts()

    def handle_statistical_product(self):
        self.product_view.update_best_seller_table()
        self.product_view.update_low_product_table()

    def handle_statistical_destroy(self):
        self.destroy_view.update_stats()

    def show_revenue_view(self):
        self.revenue_view.update_charts()