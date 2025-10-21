import sqlite3
import os

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

    def get_all_products(self):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT product_id, product_name, selling_price, image_path FROM products")
            products = [dict(row) for row in cursor.fetchall()]
            return products
        except sqlite3.Error as e:
            print(f"Database error in get product:  {e}")
            return None
        finally:
            conn.close()

    def save_order(self, order):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO orders (invoice_id, invoice_date, customer_id, employee_id, total_amount) VALUES (?, ?, ?, ?, ?)", (order['order_id'], order['customer_id'], order['employee_id'], order['total_amount'], order['order_date']))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in save order:  {e}")
            return False
        finally:
            conn.close()

    def save_order_items(self, order_items):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            for order_item in order_items:
                cursor.execute("INSERT INTO order_items (invoice_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)", (order_item['order_id'], order_item['product_id'], order_item['quantity'], order_item['price']))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error in save order items:  {e}")
            return False
        finally:
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
            cursor.execute("select customer_id, customer_name, customer_phone from customers where customer_phone = ?", (phone,))
            customers = [dict(row) for row in cursor.fetchall()]
            return customers
        except sqlite3.Error as e:
            print(f"Database error in get customer with phone:  {e}")
            return None
        finally:
            conn.close()