import sqlite3
import os
from datetime import datetime
import random

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

    # hàm gen ra mã nhân viên
    def _generate_new_employee_id(self, cursor):
        """
        Tạo mã nhân viên mới theo định dạng YYMMNNNNN.
        Hàm này cần được gọi bên trong một transaction.
        """
        now = datetime.now()
        prefix = now.strftime('%y%m')

        query = "SELECT MAX(employee_id) FROM employees WHERE CAST(employee_id AS TEXT) LIKE ?"
        cursor.execute(query, (f'{prefix}%',))

        # fetchone() trả về một tuple, ví dụ (None,) hoặc (231000001,)
        result = cursor.fetchone()
        last_id = result[0] if result else None

        if last_id is None:
            next_seq_number = 1
        else:
            last_seq_str = str(last_id)[-5:]
            next_seq_number = int(last_seq_str) + 1

        new_id = int(f"{prefix}{next_seq_number:05d}")
        return new_id

    # SỬA LỖI 2: Thêm 'self' và bỏ tham số 'db_path'
    def add_new_employee(self,data):
        """
        Hàm an toàn để thêm một nhân viên mới với ID tự tạo (định dạng YYMMNNNNN).
        """
        conn = None
        try:
            # SỬA LỖI 3: Sử dụng hàm tiện ích _get_connection
            conn = self._get_connection()
            cursor = conn.cursor()

            # Bắt đầu transaction (mặc định trong sqlite3)

            # SỬA LỖI 4: Gọi phương thức tạo ID qua 'self'
            new_employee_id = self._generate_new_employee_id(cursor)
            print(f"Generated new employee ID: {new_employee_id}")

            # Insert nhân viên mới
            insert_query = """
                INSERT INTO employees (employee_id, employee_name, password_hash, email, phone, address, role, starting_date, end_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            employee_data = (new_employee_id, data["name"], data["password"], data["email"], data["phoneNumber"], data["address"], data["role"], data["startDate"], data["endDate"])
            cursor.execute(insert_query, employee_data)

            # Commit transaction
            conn.commit()
            print(f"Successfully added employee {data["name"]} with ID {new_employee_id}.")
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
            cursor.execute("SELECT employee_id, employee_name, sex, role, status, email, phone, address, starting_date, end_date FROM employees")
            rows = cursor.fetchall()
            return rows
        except sqlite3.Error as e:
            print(f"Database error in get_data_manager: {e}")
            return None

    def get_data_product(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT product_id, product_name, selling_price, import_price, stock, status, image_path FROM products")
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
