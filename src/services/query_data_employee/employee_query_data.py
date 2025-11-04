import sqlite3
import os
from datetime import datetime, time


class EmployeeQueryData:
    def __init__(self):
        # lấy đường dẫn đến thư mục chứ file hiện tại
        script_dir = os.path.dirname(os.path.abspath(__file__))
        # lùi 1 bước về thư muc services
        models_dir = os.path.dirname(script_dir)
        # chốt lại thư mục gốc để chứa folder database
        project_root = os.path.dirname(models_dir)
        # đường dẫn đầy đủ đến thư mục database
        db_folder = os.path.join(project_root, "database")
        os.makedirs(db_folder, exist_ok=True)
        # Và cuối cùng, đường dẫn đầy đủ đến file CSDL
        self.db_path = os.path.join(db_folder, "database.db")
        print(f"DEBUG: QueryData initialized. DB path is '{self.db_path}'")

    def _get_connection(self):
        """Hàm tiện ích để tạo một kết nối mới."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    # def get_all_products(self):
    #     conn = self._get_connection()
    #     cursor = conn.cursor()
    #     try:
    #         cursor.execute("SELECT product_id, product_name, selling_price, image_path FROM products")
    #         products = [dict(row) for row in cursor.fetchall()]
    #         return products
    #     except sqlite3.Error as e:
    #         print(f"Database error in get product:  {e}")
    #         return None
    #     finally:
    #         conn.close()

    def get_guest_customer_info(self):
        """
        Lấy thông tin của khách hàng mặc định "Khách vãng lai".
        Chúng ta quy ước khách hàng này luôn có customer_id = 1.

        Returns:
            dict: Một dictionary chứa thông tin của "Khách vãng lai" nếu tìm thấy.
            None: Nếu không tìm thấy (trường hợp CSDL bị lỗi cấu hình).
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            # Tìm chính xác khách hàng có ID là 1
            sql = "SELECT * FROM customers WHERE customer_id = 1"
            cursor.execute(sql)

            guest_customer_row = cursor.fetchone()

            if guest_customer_row:
                return dict(guest_customer_row)  # Trả về dictionary thông tin
            else:
                # Đây là một tình huống lỗi nghiêm trọng, cho thấy CSDL chưa được thiết lập đúng
                print("CRITICAL ERROR: 'Khách vãng lai' record (customer_id = 1) not found in the database.")
                return None

        except sqlite3.Error as e:
            print(f"Database error in get_guest_customer_info: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def get_all_product_types(self):
        """Lấy danh sách tất cả các loại sản phẩm."""
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            sql = "SELECT type_id, type_name FROM type_product ORDER BY type_name"
            cursor.execute(sql)

            rows = cursor.fetchall()
            return [dict(row) for row in rows] if rows else []
        except sqlite3.Error as e:
            print(f"❌ Database error in get_all_product_types: {e}")
            return []  # Trả về list rỗng nếu có lỗi
        finally:
            if conn:
                conn.close()

    def get_check_stock_product(self, product_id):
        """
        Lấy số lượng tồn kho (stock) của một sản phẩm để kiểm tra

        Args:
            product_id (int): ID của sản phẩm.

        Returns:
            int: Số lượng tồn kho nếu tìm thấy sản phẩm.
            None: Nếu sản phẩm không tồn tại hoặc có lỗi xảy ra.
        """
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            # Chỉ cần SELECT cột 'stock'
            sql = "SELECT stock FROM products WHERE product_id = ?"

            cursor.execute(sql, (product_id,))

            result = cursor.fetchone()

            # fetchone() sẽ trả về một tuple, ví dụ: (10,)
            # Nếu tìm thấy, trả về phần tử đầu tiên của tuple. Nếu không, trả về None.
            return result[0] if result is not None else None

        except sqlite3.Error as e:
            print(f"❌ Database error in get_product_stock: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def get_product_stock(self):
        """lấy tồn kho sản phẩm"""
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            sql = """SELECT p.product_id, p.product_name, tp.type_name, p.stock, p.selling_price 
                        FROM products p
                        LEFT JOIN type_product tp ON tp.type_id = p.type_id
                        ORDER BY product_id """
            cursor.execute(sql)

            # Dùng fetchall() để lấy TẤT CẢ các dòng kết quả
            product_rows = cursor.fetchall()

            # Dùng list comprehension để chuyển đổi mỗi sqlite3.Row trong danh sách thành dict
            return [dict(row) for row in product_rows] if product_rows else []

        except sqlite3.Error as e:
            print(f"❌ Database error in get_all_products_for_display: {e}")
            # Trả về list rỗng khi có lỗi để Controller dễ xử lý
            return []
        finally:
            if conn:
                conn.close()

    def filter_products(self, type_id=None, keyword=None):
        """
        Lọc danh sách các sản phẩm đang kinh doanh và còn hàng.
        """
        conn = None
        try:
            conn = self._get_connection()
            conn.row_factory = sqlite3.Row  # Rất quan trọng để trả về dict-like
            cursor = conn.cursor()

            base_sql = "SELECT * FROM products"

            # --- THÊM CÁC ĐIỀU KIỆN CỐ ĐỊNH Ở ĐÂY ---
            # Luôn luôn chỉ lấy sản phẩm 'đang kinh doanh' và 'còn hàng'
            conditions = [
                "status = 'đang kinh doanh'",
                "stock > 0"
            ]
            params = []

            # --- CÁC ĐIỀU KIỆN ĐỘNG (TỪ BỘ LỌC) ---
            # 1. Lọc theo Loại sản phẩm
            if type_id is not None and type_id > 0:
                conditions.append("type_id = ?")
                params.append(type_id)

            # 2. Lọc theo Từ khóa
            if keyword:
                conditions.append("product_name LIKE ?")
                params.append(f"%{keyword}%")

            # Ghép tất cả các điều kiện lại bằng "AND"
            if conditions:
                final_sql = base_sql + " WHERE " + " AND ".join(conditions)
            else:
                final_sql = base_sql

            final_sql += " ORDER BY product_name;"

            print(f"DEBUG: Executing SQL: {final_sql}")
            print(f"DEBUG: With params: {params}")

            cursor.execute(final_sql, tuple(params))
            rows = cursor.fetchall()

            return [dict(row) for row in rows] if rows else []

        except sqlite3.Error as e:
            print(f"❌ Database error in filter_products: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def add_customer(self, customer_name, customer_phone):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO customers (customer_name, customer_phone) VALUES (?, ?)", (customer_name, customer_phone))
            conn.commit()

            # Lấy ID của bản ghi vừa được chèn
            last_id = cursor.lastrowid
            print(f"Successfully added customer '{customer_name}' with ID: {last_id}")
            return last_id
        except sqlite3.IntegrityError as e:
            print(f"Error: Could not add customer. Phone number may already exist. Details: {e}")
            return None
        except sqlite3.Error as e:
            print(f"Database error in add_customer: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def get_customer_with_phone(self, phone):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            sql = "SELECT customer_id, customer_name, customer_phone FROM customers WHERE customer_phone = ?"
            cursor.execute(sql, (phone,))

            # DÙNG fetchone() ĐỂ CHỈ LẤY MỘT KẾT QUẢ
            customer_row = cursor.fetchone()

            if customer_row:
                # Nếu tìm thấy, chuyển đối tượng sqlite3.Row thành một dictionary Python thực sự
                return dict(customer_row)
            else:
                # Nếu không tìm thấy, trả về None
                return None

        except sqlite3.Error as e:
            print(f"Database error in get_customer_by_phone: {e}")
            return None  # Trả về None nếu có lỗi CSDL
        finally:
            if conn:
                conn.close()

    def generate_invoice_code(self, cursor):
        """Tạo mã hóa đơn mới theo định dạng HD-YYMM-NNNNNN."""
        now = datetime.now()
        year_month_prefix = f"HD-{now.strftime('%y%m')}"
        sql = "SELECT invoice_code FROM invoices WHERE invoice_code LIKE ? ORDER BY invoice_code DESC LIMIT 1"
        cursor.execute(sql, (f"{year_month_prefix}-%",))
        last_invoice = cursor.fetchone()

        if last_invoice:
            next_sequence = int(last_invoice[0].split('-')[-1]) + 1
        else:
            next_sequence = 1

        return f"{year_month_prefix}-{next_sequence:06d}"

    def save_invoice(self, employee_id, customer_id, total_amount, payment_method,
                     cash_received, change_given, items):
        """
        Lưu toàn bộ thông tin hóa đơn vào CSDL một cách an toàn.
        Bao gồm:
        1. Tạo mã hóa đơn.
        2. Lưu thông tin hóa đơn chính.
        3. Lưu các chi tiết hóa đơn (sản phẩm đã bán).
        Tất cả các bước được thực hiện trong một TRANSACTION.

        Args:
            employee_id (int): ID của nhân viên bán hàng.
            customer_id (int): ID của khách hàng.
            total_amount (float): Tổng tiền của hóa đơn.
            payment_method (str): Phương thức thanh toán ('Tiền mặt' hoặc 'Chuyển khoản').
            cash_received (float): Tiền mặt khách đưa.
            change_given (float): Tiền thối lại.
            items (dict): Dictionary từ OrderService, ví dụ: {product_id: {'data': ..., 'quantity': ...}}

        Returns:
            str: Mã hóa đơn mới (invoice_code) nếu thành công, None nếu thất bại.
        """
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            # --- BẮT ĐẦU TRANSACTION: Đảm bảo tất cả hoặc không có gì được lưu ---
            cursor.execute("BEGIN TRANSACTION;")

            # === Bước 1: Tạo mã hóa đơn mới ===
            new_invoice_code = self.generate_invoice_code(cursor)

            # === Bước 2: Lưu thông tin chính vào bảng `invoices` ===
            sql_invoice = """
                INSERT INTO invoices (
                    invoice_code, total_amount, payment_method, 
                    cash_received, change_given, employee_id, customer_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            cursor.execute(sql_invoice, (
                new_invoice_code, total_amount, payment_method,
                cash_received, change_given, employee_id, customer_id
            ))

            last_invoice_id = cursor.lastrowid

            # === Bước 3: Lưu các sản phẩm vào bảng `invoice_details` ===
            sql_details = """
                INSERT INTO invoice_details (invoice_id, product_id, quantity, unit_price)
                VALUES (?, ?, ?, ?)
            """
            for product_id, item_info in items.items():
                quantity = item_info['quantity']
                unit_price = item_info['data'].get('selling_price', 0)
                cursor.execute(sql_details, (last_invoice_id, product_id, quantity, unit_price))

            # === Bước 4: Cập nhật điểm tích lũy ĐÃ ĐƯỢC XÓA BỎ ===

            # --- KẾT THÚC TRANSACTION ---
            conn.commit()

            print(f"SUCCESS: Hóa đơn {new_invoice_code} và các chi tiết đã được lưu thành công.")
            return new_invoice_code

        except sqlite3.Error as e:
            print(f"DATABASE ERROR in save_invoice: {e}")
            if conn:
                print("ROLLING BACK transaction...")
                conn.rollback()
            return None
        finally:
            if conn:
                conn.close()

    def get_all_customer(self):
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM customers")
            rows = cursor.fetchall()
            return rows

        except sqlite3.Error as e:
            print(f"DATABASE ERROR in save_invoice: {e}")
            if conn:
                print("ROLLING BACK transaction...")
                conn.rollback()
            return None
        finally:
            if conn:
                conn.close()

    def update_customer(self, customer_id, new_customer_name, new_customer_phone):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE customers
                SET customer_name = ?, customer_phone = ?
                WHERE customer_id = ?
            """, (new_customer_name, new_customer_phone, customer_id))
            conn.commit()

            if cursor.rowcount > 0:
                print(f"✅ Successfully updated customer ID {customer_id} to '{new_customer_name}', phone '{new_customer_phone}'.")
                return True
            else:
                print(f"⚠️ No customer found with ID {customer_id}.")
                return False

        except sqlite3.IntegrityError as e:
            print(f"⚠️ Error: Could not update customer. Phone number may already exist. Details: {e}")
            return None

        except sqlite3.Error as e:
            print(f"❌ Database error in update_customer: {e}")
            return None

        finally:
            if conn:
                conn.close()

    def get_customer_phone(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""select customer_id, customer_phone from customers""")
            conn.commit()

            rows = cursor.fetchall()
            return rows

        except sqlite3.IntegrityError as e:
            print(f"⚠️ Error: Could not get any customer phone. Details: {e}")
            return None

        except sqlite3.Error as e:
            print(f"❌ Database error in get customer phone: {e}")
            return None

        finally:
            if conn:
                conn.close()

    def get_all_invoices(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            sql = """
                SELECT i.invoice_code, i.invoice_date, 
                e.employee_name, c.customer_name, 
                i.payment_method, i.total_amount 
                FROM 'invoices' i, 'employees' e, 'customers' c 
                where i.employee_id = e.employee_id 
                and i.customer_id = c.customer_id 
            """
            cursor.execute(sql)
            rows = cursor.fetchall()  # rows là một list của sqlite3.Row

            # <<< THÊM BƯỚC CHUYỂN ĐỔI QUAN TRỌNG NÀY VÀO >>>
            return [dict(row) for row in rows] if rows else []

        except sqlite3.IntegrityError as e:
            print(f"⚠️ Error: Could not get any invoice. Details: {e}")
            return None

        except sqlite3.Error as e:
            print(f"❌ Database error in get all invoice: {e}")
            return None

        finally:
            if conn:
                conn.close()

    def filter_invoices (self, start_date=None, end_date=None, invoice_code=None,
                        customer_name=None, customer_phone=None):
        """
        Lọc và lấy danh sách hóa đơn trong một khoảng thời gian.

        Args:
            start_date (datetime.date or QDate): Ngày bắt đầu.
            end_date (datetime.date or QDate): Ngày kết thúc.

        Returns:
            list: Một danh sách các dictionary, mỗi dictionary là một hóa đơn.
            None: Nếu có lỗi xảy ra.
        """
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            base_sql = """
                            SELECT 
                                i.invoice_code, i.invoice_date, e.employee_name, 
                                c.customer_name, i.payment_method, i.total_amount
                            FROM invoices AS i
                            LEFT JOIN employees AS e ON i.employee_id = e.employee_id
                            LEFT JOIN customers AS c ON i.customer_id = c.customer_id
                        """

            conditions = []
            params = []

            # 1. Thêm điều kiện lọc theo ngày
            if start_date and end_date:
                start_datetime = datetime.combine(start_date, time.min)
                end_datetime = datetime.combine(end_date, time.max)
                conditions.append("i.invoice_date BETWEEN ? AND ?")
                params.extend([
                    start_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                    end_datetime.strftime('%Y-%m-%d %H:%M:%S')
                ])

            # 2. Thêm điều kiện lọc theo Mã hóa đơn
            if invoice_code:
                conditions.append("i.invoice_code LIKE ?")
                params.append(f"%{invoice_code}%")  # Dùng LIKE để tìm kiếm gần đúng

            # 3. Thêm điều kiện lọc theo Tên khách hàng
            if customer_name:
                conditions.append("c.customer_name LIKE ?")
                params.append(f"%{customer_name}%")

            # 4. Thêm điều kiện lọc theo SĐT khách hàng
            if customer_phone:
                conditions.append("c.customer_phone LIKE ?")
                params.append(f"%{customer_phone}%")

            # Ghép các điều kiện lại với nhau
            if conditions:
                final_sql = base_sql + " WHERE " + " AND ".join(conditions)
            else:
                final_sql = base_sql

            final_sql += " ORDER BY i.invoice_date DESC;"

            print(f"DEBUG: Executing SQL: {final_sql}")
            print(f"DEBUG: With params: {params}")

            cursor.execute(final_sql, tuple(params))
            rows = cursor.fetchall()

            return [dict(row) for row in rows] if rows else []

        except sqlite3.Error as e:
            print(f"❌ Database error in filter_invoices: {e}")
            return None
        finally:
            if conn:
                conn.close()

    def get_invoice_detail_by_code(self, invoice_code):
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            sql_info = """
                            SELECT 
                                i.invoice_id, i.invoice_code, i.invoice_date, i.total_amount, i.payment_method,
                                e.employee_name, c.customer_name, i.cash_received, i.change_given, sum(id.quantity) as total_quantity
                            FROM invoices AS i
                            LEFT JOIN employees AS e ON i.employee_id = e.employee_id
                            LEFT JOIN customers AS c ON i.customer_id = c.customer_id
                            LEFT JOIN invoice_details id on id.invoice_id = i.invoice_id
                            WHERE i.invoice_code = ?
                        """
            cursor.execute(sql_info, (invoice_code,))
            info_row = cursor.fetchone()

            if not info_row:
                print(f"INFO: Không tìm thấy hóa đơn với mã: {invoice_code}")
                return None

            invoice_info_dict = dict(info_row)
            # Lấy invoice_id để dùng cho truy vấn tiếp theo
            invoice_id = invoice_info_dict['invoice_id']

            # --- BƯỚC 2: LẤY DANH SÁCH SẢN PHẨM TRONG HÓA ĐƠN ĐÓ ---
            sql_products = """
                            SELECT 
                                p.product_name,
                                id.quantity,
                                id.unit_price,
                                id.subtotal_amount_invoice
                            FROM invoice_details AS id
                            JOIN products AS p ON id.product_id = p.product_id
                            WHERE id.invoice_id = ?
                        """
            cursor.execute(sql_products, (invoice_id,))
            product_rows = cursor.fetchall()

            # --- BƯỚC 3: GỘP KẾT QUẢ VÀ TRẢ VỀ ---
            result = {
                'info': invoice_info_dict,
                'products': product_rows
            }
            return result

        except sqlite3.Error as e:
            print(f"❌ Database error in get_full_invoice_details_by_code: {e}")
            return None
        finally:
            if conn:
                conn.close()