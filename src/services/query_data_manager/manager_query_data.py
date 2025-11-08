import sqlite3
import os
from datetime import datetime
import random

from src.utils.nomalize import _normalize_search_sqlite


class QueryData:
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

    def get_user_by_username(self, username):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT user_id, user_name FROM users WHERE LOWER(user_name) = LOWER(?)", (username,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Database error in get_user_by_username: {e}")
            return None

    def get_employee_name_by_id(self, employee_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT employee_name FROM employees WHERE employee_id = ?", (employee_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Database error in get_employee_name_by_id: {e}")
            return None

    def _generate_new_employee_id(self, cursor):
        now = datetime.now()
        prefix = now.strftime('%y%m')

        query = "SELECT MAX(employee_id) FROM employees WHERE CAST(employee_id AS TEXT) LIKE ?"
        cursor.execute(query, (f'{prefix}%',))
        result = cursor.fetchone()
        last_id = result[0] if result else None

        if last_id is None:
            next_seq_number = 1
        else:
            last_seq_str = str(last_id)[-5:]
            next_seq_number = int(last_seq_str) + 1

        new_id = int(f"{prefix}{next_seq_number:05d}")
        return new_id

    def add_new_employee(self,data):
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            new_employee_id = self._generate_new_employee_id(cursor)
            print(f"Generated new employee ID: {new_employee_id}")

            # Insert nhân viên mới
            insert_query = """
                INSERT INTO employees (employee_id, employee_name, password_hash, email, gender, phone, address, role, starting_date, end_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            employee_data = (new_employee_id, data["name"], data["password"], data["email"],data["gender"], data["phoneNumber"], data["address"], data["role"], data["startDate"], data["endDate"])
            cursor.execute(insert_query, employee_data)

            # Commit transaction
            conn.commit()
            print(f"Successfully added employee {data['name']} with ID {new_employee_id}.")
            return True # Trả về cả ID để có thể dùng sau này

        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            print(f"Database error in add_new_employee: {e}")
            return False, None
        finally:
            if conn:
                conn.close()

    def get_data_manager(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT employee_id, employee_name, gender, role, status, email, phone, address, starting_date, end_date FROM employees")
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Database error in get_data_manager: {e}")
            return None

    def get_data_product(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""SELECT p.product_id, p.product_name, tp.type_name, p.selling_price, p.import_price, p.stock, p.status, p.image_path 
                              FROM products as p
                              JOIN type_product as tp ON p.type_id = tp.type_id
                              """)
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Database error in get_data_product: {e}")
            return None
    def check_mail_exists(self, email):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("select count(*) from employees where email = ?",(email,))
            result = cursor.fetchone()
            if result and result[0] > 0:
                return True
            else:
                return False
        except sqlite3.Error as e:
            print(f"Database error in check_email_exists: {e}")
            return None

    def check_phone_exists(self, phone):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("select count(*) from employees where phone = ?",(phone,))
            result = cursor.fetchone()
            if result and result[0] > 0:
                return True
            else:
                return False
        except sqlite3.Error as e:
            print(f"Database error in check_phone_exists: {e}")
            return None
    def update_inactive_employee(self, update_data):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("update employees set status = ?, end_date = ? where employee_id = ?",("đã nghỉ", update_data["end_date"], update_data["employee_id"]))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in update_inactive_employee: {e}")
            return None
    def update_employee(self, data):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                update employees
                set employee_id = ?, employee_name = ?, password_hash = ?, email = ?, gender = ?, phone = ?, address = ?, role = ?, starting_date = ?, end_date = ?
                where employee_id = ?
            """,(data["employee_id"],
                            data["name"],
                            data["password"],
                            data["email"],
                            data["gender"],
                            data["phoneNumber"],
                            data["address"],
                            data["role"],
                            data["startDate"],
                            data["endDate"],
                            data["employee_id"]))
            if cursor.rowcount == 0:
                print(f"CẢNH BÁO: Lệnh UPDATE đã chạy nhưng không tìm thấy employee_id = {data['employee_id']} để cập nhật.")
                conn.rollback()
                return False
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in update_inactive_employee: {e}")
            return None

    def search_employees(self, role, status,display,search_term):
        conn = self._get_connection()
        conn.create_function("normalize_search", 1, _normalize_search_sqlite)
        cursor = conn.cursor()
        try:
            base_query = """
                SELECT 
                    employee_id, employee_name, gender, role, status, 
                    email, phone, address, starting_date, end_date 
                FROM employees
            """
            conditions = []
            parameters = []
            if role.lower() != "tất cả":
                conditions.append("role = ?")
                parameters.append(role)
            if status.lower() != "tất cả":
                conditions.append("status = ?")
                parameters.append(status)
            if search_term:
                search_like = f"%{search_term}%"
                search_like_normalized = _normalize_search_sqlite(search_like)
                conditions.append("(LOWER(employee_id) LIKE ? OR normalize_search(employee_name) LIKE ?)")
                parameters.append(search_like.lower())
                parameters.append(search_like_normalized)
            if conditions:
                base_query += " WHERE " + " AND ".join(conditions)
            base_query += " ORDER BY employee_name"
            if display.isdigit():
                try:
                    limit_value = int(display)
                    base_query += " LIMIT ?"
                    parameters.append(limit_value)
                except ValueError:
                    # Bỏ qua nếu không phải số hợp lệ
                    pass
            cursor.execute(base_query, tuple(parameters))
            results = cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"Database error in get_data_product: {e}")
            conn.rollback()
            return None

    def get_all_type(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM type_product")
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Database error in get_type_product: {e}")
            return None

    def add_new_product(self, data):
        conn = None
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            insert_query = """
                INSERT INTO products ( product_name, selling_price, stock, import_price, image_path, status, type_id)
                VALUES ( ?, ?, ?, ?, ?, ?, ?)
            """
            product_data = (data["name"], data["selling"], data["stock_price"],data["import_price"], data["image_path"], data["status"], data["type_id"])
            cursor.execute(insert_query, product_data)
            conn.commit()
            return True
        except sqlite3.Error as e:
            if conn:
                conn.rollback()
            print(f"Database error in add_new_product: {e}")
            return False
        finally:
            if conn:
                conn.close()

    def update_status_product(self,product_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("update products set status = ? where product_id = ?",("ngừng kinh doanh", product_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in update_status_product: {e}")
            return None

    def update_product(self,data):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE products
                SET product_name = ?, selling_price = ?, stock = ?, import_price = ?, image_path = ?, status = ?, type_id = ?
                WHERE product_id = ?
            """,(data["name"],data["selling_price"],data["stock"],data["import_price"],data["image_path"],data["status"],data["type_id"],data["product_id"]))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in update_status_product: {e}")
            return None

    def search_products(self, category,status,display,search_term):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            base_query = """
                SELECT 
                    p.product_id, p.product_name, tp.type_name, p.selling_price, 
                    p.import_price, p.stock, p.status, p.image_path
                FROM products as p
                JOIN type_product as tp ON p.type_id = tp.type_id
            """
            conditions = []
            parameters = []
            if category.lower() != "tất cả":
                conditions.append("tp.type_name = ?")
                parameters.append(category)
            if status.lower() != "tất cả":
                conditions.append("p.status = ?")
                parameters.append(status)
            if search_term:
                search_like = f"%{search_term}%"
                conditions.append("(LOWER(p.product_id) LIKE LOWER(?) OR LOWER(p.product_name) LIKE LOWER(?))")
                parameters.append(search_like)
                parameters.append(search_like)
            if conditions:
                base_query += " WHERE " + " AND ".join(conditions)
            base_query += " ORDER BY p.product_name"
            if display.isdigit():
                try:
                    limit_value = int(display)
                    base_query += " LIMIT ?"
                    parameters.append(limit_value)
                except ValueError:
                    # Bỏ qua nếu không phải số hợp lệ
                    pass
            cursor.execute(base_query, tuple(parameters))
            results = cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"Database error in search_products: {e}")
            conn.rollback()
            return None

    def search_import(self, employee,from_date,to_date, type_invoice, display, search_term):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            base_query = """
                SELECT 
                    i.import_code, i.invoice_type, e.employee_name, i.import_date, i.total_amount
                FROM import_invoice as i
                LEFT JOIN import_invoice_details as id ON i.import_id = id.import_id
                LEFT JOIN employees as e ON e.employee_id = i.employee_id
            """
            conditions = []
            parameters = []
            if employee.lower() != "tất cả":
                conditions.append("e.employee_name = ?")
                parameters.append(employee)
            if type_invoice.lower() != "tất cả":
                conditions.append("i.invoice_type = ?")
                parameters.append(type_invoice)
            if search_term:
                search_like = f"%{search_term}%"
                conditions.append("LOWER(i.import_code) LIKE LOWER(?)")
                parameters.append(search_like)
            if from_date and to_date:
                conditions.append("DATE(i.import_date) BETWEEN DATE(?) AND DATE(?)")
                parameters.append(from_date)
                parameters.append(to_date)
            elif from_date:
                # Nếu chỉ có ngày bắt đầu
                conditions.append("DATE(i.import_date) >= DATE(?)")
                parameters.append(from_date)
            elif to_date:
                # Nếu chỉ có ngày kết thúc
                conditions.append("DATE(i.import_date) <= DATE(?)")
                parameters.append(to_date)
            if conditions:
                base_query += " WHERE " + " AND ".join(conditions)
            base_query += """ GROUP BY i.import_id, i.import_code, i.invoice_type, e.employee_name, i.import_date, i.total_amount
                              ORDER BY i.import_code """
            if display.isdigit():
                try:
                    limit_value = int(display)
                    base_query += " LIMIT ?"
                    parameters.append(limit_value)
                except ValueError:
                    # Bỏ qua nếu không phải số hợp lệ
                    pass
            cursor.execute(base_query, tuple(parameters))
            results = cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"Database error in search_products: {e}")
            conn.rollback()
            return None

    def get_all_name_employee(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT employee_name FROM employees")
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Database error in get_type_product: {e}")
            return None

    def get_date_oldest_import_invoice(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT MIN(import_date) AS oldest_date FROM import_invoice")
            row = cursor.fetchone()
            if row and row["oldest_date"]:
                return row["oldest_date"]
            return None
        except sqlite3.Error as e:
            print(f"Database error in get_date_oldest_import_invoice: {e}")
            return None
        finally:
            conn.close()

    def get_all_product(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""SELECT p.product_id, p.product_name, tp.type_name, p.stock 
                              FROM products as p
                              JOIN type_product as tp ON p.type_id = tp.type_id   
                              WHERE p.status = "đang kinh doanh"
            """)
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Database error in get_type_product: {e}")
            return None

    def _generate_new_import_invoice_id(self, cursor, prefix_type):
        now = datetime.now()
        full_prefix = f"{prefix_type}{now.strftime('%y%m')}"
        query = "SELECT MAX(import_code) FROM import_invoice WHERE import_code LIKE ?"
        cursor.execute(query, (f'{full_prefix}%',))

        result = cursor.fetchone()
        last_id = result[0] if result else None

        if last_id is None:
            next_seq_number = 1
        else:
            last_seq_str = last_id[-5:]
            next_seq_number = int(last_seq_str) + 1
        new_id = f"{full_prefix}{next_seq_number:05d}"
        return new_id

    def get_new_invoice_code(self, prefix_type):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            new_code = self._generate_new_import_invoice_id(cursor, prefix_type)
            return new_code
        except Exception as e:
            print(f"Lỗi khi tạo mã phiếu mới: {e}")
            return None
        finally:
            conn.close()

    def create_import_invoice(self, invoice_data, details_data):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:

            cursor.execute("""
                INSERT INTO import_invoice (import_code, employee_id, import_date, total_amount, invoice_type)
                VALUES (?, ?, DATE('now', 'localtime'), ?, ?)
            """, (
                invoice_data['import_code'],
                invoice_data['employee_id'],
                invoice_data['total_amount'],
                invoice_data['invoice_type']
            ))

            import_id = cursor.lastrowid
            print(f"DEBUG: Loại phiếu đang xử lý: '{invoice_data['invoice_type']}'")
            for item in details_data:
                cursor.execute("""
                    INSERT INTO import_invoice_details (import_id, product_id, quantity, unit_price)
                    VALUES (?, ?, ?, ?)
                """, (import_id, item['product_id'], item['quantity'], item['price']))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error creating import invoice: {e}")
            return False
        finally:
            conn.close()

    def get_product_import_detail(self, import_code):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""SELECT p.product_id, p.product_name, tp.type_name, id.unit_price, id.quantity
                            FROM import_invoice as i
                            JOIN import_invoice_details as id ON i.import_id = id.import_id
                            JOIN products as p ON p.product_id = id.product_id
                            JOIN type_product as tp ON tp.type_id = p.type_id
                            WHERE i.import_code = ?
            """,(import_code,))
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Database error in get_product_import_detail: {e}")
            return None

    def get_invoice_information(self, import_code):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""SELECT i.import_code, i.invoice_type, e.employee_name, i.import_date
                            FROM import_invoice as i
                            JOIN employees as e ON e.employee_id = i.employee_id
                            WHERE i.import_code = ?
            """,(import_code,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Database error in get_invoice_information: {e}")
            return None