import os

from PyQt5.QtCore import QDateTime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT

class PDFService:
    def __init__(self):
        self.register_font()

    def register_font(self):
        try:
            font_path = os.path.join("resources", "fonts", "arial.ttf")
            if not os.path.exists(font_path):
                 font_path = "arial.ttf"

            pdfmetrics.registerFont(TTFont('Arial', font_path))
            pdfmetrics.registerFont(TTFont('Arial-Bold', font_path))
            self.font_name = 'Arial'
            self.font_name_bold = 'Arial-Bold'
        except Exception as e:
            print(f"Cảnh báo: Không tải được font tiếng Việt. Sử dụng font mặc định (có thể lỗi font). {e}")
            self.font_name = 'Helvetica'
            self.font_name_bold = 'Helvetica-Bold'

    def format_currency(self, value):
        try:
            return "{:,.0f}đ".format(float(value)).replace(",", ".")
        except (ValueError, TypeError):
            return str(value)

    import os
from PyQt5.QtCore import QDateTime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT

class PDFService:
    def __init__(self):
        self.register_font()

    def register_font(self):
        try:
            # Đường dẫn font, ưu tiên tìm trong thư mục resources/fonts/
            font_path = os.path.join("resources", "fonts", "arial.ttf")
            if not os.path.exists(font_path):
                 font_path = "arial.ttf" # Fallback tìm ở thư mục gốc

            pdfmetrics.registerFont(TTFont('Arial', font_path))
            # Nếu có file arialbd.ttf riêng thì tốt hơn, tạm dùng arial.ttf cho cả 2 nếu không có
            pdfmetrics.registerFont(TTFont('Arial-Bold', font_path))
            self.font_name = 'Arial'
            self.font_name_bold = 'Arial-Bold'
        except Exception as e:
            print(f"Cảnh báo font: {e}")
            self.font_name = 'Helvetica'
            self.font_name_bold = 'Helvetica-Bold'

    def format_currency(self, value):
        try:
            return "{:,.0f}đ".format(float(value)).replace(",", ".")
        except (ValueError, TypeError):
            return str(value)

    def export_import_invoice(self, file_path, invoice_info, invoice_details):
        doc = SimpleDocTemplate(file_path, pagesize=A4, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=18)
        elements = []

        # --- 1. XÁC ĐỊNH LOẠI PHIẾU ---
        invoice_type_str = invoice_info.get('invoice_type', 'Phiếu nhập').strip()
        is_cancellation = invoice_type_str.lower() == 'phiếu hủy'

        if is_cancellation:
            title_text = "THÔNG TIN PHIẾU HỦY"
            date_label = "Thời gian hủy:"
            employee_label = "Nhân viên hủy"
        else:
             title_text = "THÔNG TIN PHIẾU NHẬP"
             date_label = "Thời gian nhập:"
             employee_label = "Nhân viên nhận"

        # --- 2. ĐỊNH NGHĨA STYLES ---
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='HeaderLeft', fontName=self.font_name, fontSize=11, alignment=TA_LEFT))
        styles.add(ParagraphStyle(name='HeaderRight', fontName=self.font_name, fontSize=10, alignment=TA_RIGHT))
        styles.add(ParagraphStyle(name='TitleBoldCenter', fontName=self.font_name_bold, fontSize=18, alignment=TA_CENTER, spaceAfter=15))
        styles.add(ParagraphStyle(name='NormalLeft', fontName=self.font_name, fontSize=11, alignment=TA_LEFT, leading=14))
        styles.add(ParagraphStyle(name='NormalRight', fontName=self.font_name, fontSize=11, alignment=TA_RIGHT))
        styles.add(ParagraphStyle(name='TableDataCenter', fontName=self.font_name, fontSize=10, alignment=TA_CENTER, leading=12))
        styles.add(ParagraphStyle(name='TableDataLeft', fontName=self.font_name, fontSize=10, alignment=TA_LEFT, leading=12))
        styles.add(ParagraphStyle(name='TotalAmount', fontName=self.font_name_bold, fontSize=12, alignment=TA_RIGHT, spaceBefore=10, spaceAfter=10))
        styles.add(ParagraphStyle(name='SignatureRole', fontName=self.font_name_bold, fontSize=11, alignment=TA_CENTER, spaceAfter=5))
        styles.add(ParagraphStyle(name='SignatureName', fontName=self.font_name, fontSize=10, alignment=TA_CENTER))

        # --- 3. HEADER & TIÊU ĐỀ ---
        now = QDateTime.currentDateTime().toString("dd/MM/yyyy hh:mm")
        header_table = Table([
            [Paragraph("Hệ thống quản lý bán bánh", styles['HeaderLeft']), Paragraph(f"Thời gian in phiếu: {now}", styles['HeaderRight'])]
        ], colWidths=[doc.width/2, doc.width/2])
        header_table.setStyle(TableStyle([('BOTTOMPADDING', (0,0), (-1,-1), 0), ('TOPPADDING', (0,0), (-1,-1), 0)]))
        elements.append(header_table)
        elements.append(Spacer(1, 15))

        elements.append(Paragraph(title_text, styles['TitleBoldCenter']))
        elements.append(Spacer(1, 10))

        # --- 4. THÔNG TIN CHUNG ---
        elements.append(Paragraph(f"<b>Mã phiếu:</b> {invoice_info.get('import_code', '')}", styles['NormalLeft']))
        emp_id = invoice_info.get('employee_id', '')
        emp_info = f"{invoice_info.get('employee_name', '')} - Mã NV: {emp_id}" if emp_id else invoice_info.get('employee_name', '')
        elements.append(Paragraph(f"<b>Người thực hiện:</b> {emp_info}", styles['NormalLeft']))
        elements.append(Paragraph(f"<b>{date_label}</b> {invoice_info.get('import_date', '')}", styles['NormalLeft']))
        elements.append(Spacer(1, 15))

        # --- 5. CẤU HÌNH BẢNG CHI TIẾT ---
        if is_cancellation:
            # Phiếu hủy: 3 cột (Tên, Phiên bản, Số lượng)
            table_headers = ["Tên sản phẩm", "Phiên bản", "Số lượng"]
            col_widths = [doc.width * 0.50, doc.width * 0.30, doc.width * 0.20]
        else:
            # Phiếu nhập: 5 cột (Tên, Phiên bản, Giá, SL, Tổng tiền)
            table_headers = ["Tên sản phẩm", "Phiên bản", "Giá", "Số lượng", "Tổng tiền"]
            col_widths = [doc.width * 0.35, doc.width * 0.25, doc.width * 0.15, doc.width * 0.1, doc.width * 0.15]

        table_data = [table_headers]
        total_amount_all_products = 0

        for item in invoice_details:
            quantity = item.get('quantity', 0)
            # Lấy 'product_type' từ Controller truyền sang (đã map từ 'type_name' DB)
            product_type = item.get('product_type', '')

            if is_cancellation:
                row = [
                    Paragraph(item.get('product_name', ''), styles['TableDataLeft']),
                    Paragraph(product_type, styles['TableDataCenter']),
                    Paragraph(str(quantity), styles['TableDataCenter']),
                ]
            else:
                price = item.get('unit_price', 0)
                subtotal = quantity * price
                total_amount_all_products += subtotal
                row = [
                    Paragraph(item.get('product_name', ''), styles['TableDataLeft']),
                    Paragraph(product_type, styles['TableDataCenter']),
                    Paragraph(self.format_currency(price), styles['NormalRight']),
                    Paragraph(str(quantity), styles['TableDataCenter']),
                    Paragraph(self.format_currency(subtotal), styles['NormalRight'])
                ]
            table_data.append(row)

        detail_table = Table(table_data, colWidths=col_widths)

        # Style chung
        common_style = [
            ('FONTNAME', (0, 0), (-1, -1), self.font_name),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E0E0E0')), # Màu header
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('FONTNAME', (0, 0), (-1, 0), self.font_name_bold), # Header in đậm
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]

        if is_cancellation:
             common_style.extend([
                ('ALIGN', (0, 1), (0, -1), 'LEFT'),   # Tên SP căn trái
             ])
        else:
             common_style.extend([
                ('ALIGN', (0, 1), (0, -1), 'LEFT'),   # Tên SP căn trái
                ('ALIGN', (2, 1), (2, -1), 'RIGHT'),  # Giá căn phải
                ('ALIGN', (4, 1), (4, -1), 'RIGHT'),  # Tổng tiền căn phải
                ('RIGHTPADDING', (2,1), (2,-1), 5),
                ('RIGHTPADDING', (4,1), (4,-1), 5),
             ])

        detail_table.setStyle(TableStyle(common_style))
        elements.append(detail_table)
        elements.append(Spacer(1, 15))

        # --- 6. TỔNG TIỀN (Chỉ cho phiếu nhập) ---
        if not is_cancellation:
            elements.append(Paragraph(f"<b>Tổng thành tiền: {self.format_currency(total_amount_all_products)}</b>", styles['TotalAmount']))
            elements.append(Spacer(1, 40))
        else:
            elements.append(Spacer(1, 40))

        # --- 7. CHỮ KÝ (2 cột) ---
        signature_table = Table([
            [Paragraph(employee_label, styles['SignatureRole']),
             Paragraph(employee_label, styles['SignatureRole'])],
            [Paragraph("(Ký và ghi rõ họ tên)", styles['SignatureName']),
             Paragraph("(Ký và ghi rõ họ tên)", styles['SignatureName'])]
        ], colWidths=[doc.width/2, doc.width/2])

        signature_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
        ]))
        elements.append(signature_table)

        # --- 8. XUẤT FILE ---
        try:
            doc.build(elements)
            print(f"Đã xuất PDF thành công tại: {file_path}")
            return True
        except Exception as e:
            print(f"Lỗi khi xây dựng PDF: {e}")
            return False