import numpy as np
from PyQt5.QtCore import QDate
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from matplotlib.ticker import FuncFormatter
from src.services.query_data_manager.manager_query_data import QueryData
from src.utils.draw_chart import MplCanvas


class RevenueStatsView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = parent
        self.query_data = QueryData()
        self.init_ui()
        self.current_time_option = "Hôm nay"

    def init_ui(self):
        if not self.ui.Frame_chart_revenue.layout():
             self.chart_layout = QVBoxLayout(self.ui.Frame_chart_revenue)
             self.chart_layout.setContentsMargins(0, 10, 0, 0)
        else:
             self.chart_layout = self.ui.Frame_chart_revenue.layout()

        self.canvas = MplCanvas(self.ui.Frame_chart_revenue, dpi=100)
        self.canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.chart_layout.addWidget(self.canvas)

        # Setup Canvas cho Biểu đồ tròn
        if not self.ui.Frame_piechart_revenue.layout():
             self.pie_layout = QVBoxLayout(self.ui.Frame_piechart_revenue)
        else:
             self.pie_layout = self.ui.Frame_piechart_revenue.layout()

        self.pie_canvas = MplCanvas(self.ui.Frame_piechart_revenue, dpi=100)
        self.pie_canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.pie_layout.addWidget(self.pie_canvas)

    def update_charts(self):
        time_option = self.ui.time_statiscal_comboBox.currentText()
        self.plot_revenue_chart(time_option)
        self.plot_product_pie_chart(time_option)

    def plot_revenue_chart(self, time_option):
        self.current_time_option = time_option
        print(f"plot_revenue_chart: {time_option}, Canvas size =", self.canvas.size())
        today = QDate.currentDate()
        # Khởi tạo biến chứa dữ liệu vẽ
        categories = []
        values = []
        title_suffix = ""

        # --- TRƯỜNG HỢP 1: HÔM NAY (Theo giờ) ---
        if time_option == "Hôm nay":
            date_str = today.toString("yyyy-MM-dd")
            title_suffix = f"Hôm nay ({date_str})"
            categories = [f"{h}h" for h in range(24)]
            values = self.query_data.get_revenue_by_hour(date_str)

        # --- TRƯỜNG HỢP 2: TUẦN NÀY (Theo thứ) ---
        elif time_option == "Tuần này":
            # Tìm thứ 2 đầu tuần và CN cuối tuần
            start_week = today.addDays(-(today.dayOfWeek() - 1))
            end_week = start_week.addDays(6)
            title_suffix = f"Tuần này ({start_week.toString('dd/MM')} - {end_week.toString('dd/MM')})"

            categories = ["T2", "T3", "T4", "T5", "T6", "T7", "CN"]
            # Khởi tạo doanh thu cả tuần bằng 0
            week_data = {day: 0 for day in range(1, 8)} # 1=T2, 7=CN theo chuẩn Qt

            # Lấy dữ liệu từ DB
            rows = self.query_data.get_revenue_by_day_of_week(
                start_week.toString("yyyy-MM-dd"),
                end_week.toString("yyyy-MM-dd")
            )

            # Map dữ liệu DB vào đúng thứ
            for row in rows:
                # row[0] là chuỗi ngày 'YYYY-MM-DD'
                date_obj = QDate.fromString(row[0], "yyyy-MM-dd")
                day_of_week = date_obj.dayOfWeek() # Trả về 1 (T2) -> 7 (CN)
                week_data[day_of_week] = row[1]

            values = [week_data[d] for d in range(1, 8)]

        # --- TRƯỜNG HỢP 3: THÁNG NÀY (Theo tuần) ---
        elif time_option == "Tháng này":
            current_month = today.month()
            current_year = today.year()
            title_suffix = f"Tháng {current_month}/{current_year}"

            # Lấy dữ liệu thô các tuần có doanh thu
            raw_weeks = self.query_data.get_revenue_by_week_in_month(current_year, current_month)

            # Tạo nhãn tự động dựa trên số tuần có dữ liệu (thường là 4-6 tuần)
            num_weeks = len(raw_weeks)
            if num_weeks == 0:
                 categories = ["Không có dữ liệu"]
                 values = [0]
            else:
                 categories = [f"Tuần {i+1}" for i in range(num_weeks)]
                 values = raw_weeks

        # --- TRƯỜNG HỢP 4: NĂM NÀY (Theo tháng) ---
        elif time_option == "Năm này":
            current_year = today.year()
            title_suffix = f"Năm {current_year}"
            categories = [f"T{m}" for m in range(1, 13)] # Nhãn: T1, T2... T12
            values = self.query_data.get_revenue_by_month_in_year(current_year)

        # --- TRƯỜNG HỢP 5: TÙY CHỈNH (Xử lý đơn giản: nếu chọn 1 ngày -> xem theo giờ) ---
        elif time_option == "Tùy chỉnh":
             selected_date = self.ui.dateOption.date()
             date_str = selected_date.toString("yyyy-MM-dd")
             title_suffix = f"Ngày {date_str}"
             categories = [f"{h}h" for h in range(0, 24, 2)] # Hiển thị nhãn cách quãng cho đỡ rối nếu cần: 0h, 2h, 4h...
             categories = [f"{h}h" for h in range(24)]
             values = self.query_data.get_revenue_by_hour(date_str)
        self.canvas.axes.clear()
        bars = self.canvas.axes.bar(categories, values, color='#658C58', width=0.6)

        def format_vnd(x, pos):
            return f"{int(x):,}"
        self.canvas.axes.yaxis.set_major_formatter(FuncFormatter(format_vnd))
        # Trang trí
        self.canvas.axes.set_title(f'Biểu đồ Doanh thu - {title_suffix}', fontsize=12, fontweight='bold')
        self.canvas.axes.set_ylabel('Doanh thu (VNĐ)')
        self.canvas.axes.grid(axis='y', linestyle='--', alpha=0.5)
        self.canvas.axes.margins(y=0.2)

        for bar, value in zip(bars, values):
            if value > 0:
                height = bar.get_height()
                self.canvas.axes.annotate(f"{value:,.0f}",
                                          xy=(bar.get_x() + bar.get_width() / 2, height),
                                          xytext=(0, 3), textcoords="offset points",
                                          ha='center', va='bottom', fontsize=9)

        self.canvas.fig.tight_layout(rect=[0, 0, 1, 0.95])
        self.canvas.fig.subplots_adjust(left=0.1, right=0.95, top=0.9, bottom=0.15)
        self.canvas.draw()

    def plot_product_pie_chart(self, time_option):
        today = QDate.currentDate()
        labels = ['Croissant', 'Tart', 'Mousse']
        values = [0, 0, 0]
        title_suffix = ""

        if time_option == "Hôm nay":
            date_str = today.toString("yyyy-MM-dd")
            title_suffix = f"Hôm nay ({date_str})"
            values = self.query_data.get_product_revenue_by_type(date_str, date_str)
        elif time_option == "Tuần này":
            start_week = today.addDays(-(today.dayOfWeek() - 1))
            end_week = start_week.addDays(6)
            start_str = start_week.toString("yyyy-MM-dd")
            end_str = end_week.toString("yyyy-MM-dd")
            title_suffix = f"Tuần này ({start_week.toString('dd/MM')} - {end_week.toString('dd/MM')})"
            values = self.query_data.get_product_revenue_by_type(start_str, end_str)
        elif time_option == "Tháng này":
            year, month = today.year(), today.month()
            start_str = f"{year}-{month:02d}-01"
            end_date = today.addMonths(1).addDays(-today.day())
            end_str = end_date.toString("yyyy-MM-dd")
            title_suffix = f"Tháng {month}/{year}"
            values = self.query_data.get_product_revenue_by_type(start_str, end_str)
        elif time_option == "Năm này":
            year = today.year()
            start_str = f"{year}-01-01"
            end_str = f"{year}-12-31"
            title_suffix = f"Năm {year}"
            values = self.query_data.get_product_revenue_by_type(start_str, end_str)
        elif time_option == "Tùy chỉnh":
            selected_date = self.ui.dateOption.date()
            date_str = selected_date.toString("yyyy-MM-dd")
            title_suffix = f"Ngày {date_str}"
            values = self.query_data.get_product_revenue_by_type(date_str, date_str)

        print(f"DEBUG: VALUES FOR PIE CHART: {values}")

        total = sum(values)
        if total == 0:
            self.pie_canvas.axes.clear()
            self.pie_canvas.axes.pie([1], colors=['#e0e0e0'], startangle=90, wedgeprops={'edgecolor': 'white', 'linewidth': 1})
            self.pie_canvas.axes.text(0, 0, 'Không có\ndữ liệu', ha='center', va='center', fontsize=12, color='#757575', fontweight='bold')
            self.pie_canvas.axes.set_title(f'Doanh thu theo loại sản phẩm - {title_suffix}', fontsize=12, fontweight='bold', pad=20)
            self.pie_canvas.axes.axis('equal')
            self.pie_canvas.fig.tight_layout(rect=[0, 0, 1, 0.92])
            self.pie_canvas.draw()
            return

        self.pie_canvas.axes.clear()
        colors = ['#F4A261', '#E76F51', '#2A9D8F']
        wedges, texts = self.pie_canvas.axes.pie(
            values,
            colors=colors,
            startangle=90,
            wedgeprops={'linewidth': 1.5, 'edgecolor': 'white'}
        )

        bbox_props = dict(boxstyle="square,pad=0.3", fc="w", ec="k", lw=0.72)
        kw = dict(arrowprops=dict(arrowstyle="-"), bbox=bbox_props, zorder=0, va="center")

        for i, p in enumerate(wedges):
            ang = (p.theta2 - p.theta1)/2. + p.theta1
            y = np.sin(np.deg2rad(ang))
            x = np.cos(np.deg2rad(ang))
            horizontalalignment = {-1: "right", 1: "left"}[int(np.sign(x))]
            connectionstyle = f"angle,angleA=0,angleB={ang}"
            kw["arrowprops"].update({"connectionstyle": connectionstyle})
            pct = values[i] / total * 100
            label_text = f"{labels[i]}: {pct:.1f}%\n({int(values[i]):,}đ)"
            self.pie_canvas.axes.annotate(label_text, xy=(x, y), xytext=(1.35*np.sign(x), 1.4*y),
                        horizontalalignment=horizontalalignment, color='black', **kw) # Thêm color='black'

        self.pie_canvas.axes.set_title(f'Doanh thu theo loại sản phẩm - {title_suffix}', fontsize=12, fontweight='bold', pad=20)
        self.pie_canvas.fig.tight_layout(rect=[0, 0, 1, 0.92])
        self.pie_canvas.fig.subplots_adjust(left=0.1, right=0.9, top=0.85, bottom=0.15)
        self.pie_canvas.draw()

    def _format_pie_label(self, pct, all_values):
        absolute = int(round(pct * sum(all_values) / 100))
        return f"{pct:.1f}%\n{absolute:,}đ"