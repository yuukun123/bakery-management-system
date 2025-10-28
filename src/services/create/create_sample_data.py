import os
import sqlite3

class CreateSampleData:
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

        # # Kết nối CSDL
        # self.connection = sqlite3.connect(db_path)
        # self.connection.row_factory = sqlite3.Row  # trả về dạng dict-like thay vì tuple
        # self.cursor = self.connection.cursor()
        # print(f"connect database '{db_path}' successful")

    def _get_connection(self):
        """Hàm tiện ích để tạo một kết nối mới."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create_sample_data(self):
        self.cursor.executescript("""
                INSERT INTO products (product_id, product_name, selling_price, stock, import_price, created_at, updated_at, status, type_id, image_path)
                VALUES 
                    ('1', 'Avocado_Croissant', 100000, 10, 90000, datetime('now'), datetime('now'), 'active', 1, 'UI/images/Croissant/Avocado_Croissant.jpg'),
                    ('2', 'Choco_Mallow_Croissant', 110000, 10, 100000, datetime('now'), datetime('now'), 'active', 1, 'UI/images/Croissant/Choco_Mallow_Croissant.png'),
                    ('3', 'Dinosaur_Almond_Croissant', 120000, 10, 110000, datetime('now'), datetime('now'), 'active', 1, 'UI/images/Croissant/Dinosaur_Almond_Croissant.png'),
                    ('4', 'Honey_Almond_Croissant', 130000, 10, 120000, datetime('now'), datetime('now'), 'active', 1, 'UI/images/Croissant/Honey_Almond_Croissant.png'),
                    ('5', 'Matcha_Croissant', 140000, 10, 130000, datetime('now'), datetime('now'), 'active', 1, 'UI/images/Croissant/Matcha_Croissant.jpg'),
                    ('6', 'Avocado_Mousse', 200000, 10, 190000, datetime('now'), datetime('now'), 'active', 2, 'UI/images/Mousse/Avocado_Mousse.jpg'),
                    ('7', 'Blueberry_Mousse', 210000, 10, 200000, datetime('now'), datetime('now'), 'active', 2, 'UI/images/Mousse/Blueberry_Mousse.jpg'),
                    ('8', 'Corn_Mousse', 220000, 10, 210000, datetime('now'), datetime('now'), 'active', 2, 'UI/images/Mousse/Corn_Mousse.jpg'),
                    ('9', 'Longan_Mousse', 230000, 10, 220000, datetime('now'), datetime('now'), 'active', 2, 'UI/images/Mousse/Longan_Mousse.jpg'),
                    ('10', 'Mango_Mousse', 240000, 10, 230000, datetime('now'), datetime('now'), 'active', 2, 'UI/images/Mousse/Mango_Mousse.jpg'),
                    ('11', 'Coffee_Tart', 50000, 10, 40000, datetime('now'), datetime('now'), 'active', 3, 'UI/images/Tart/Coffee_Tart.jpg'),
                    ('12', 'Cherry_Tart', 550000, 10, 45000, datetime('now'), datetime('now'), 'active', 3, 'UI/images/Tart/Cherry_Tart.jpg'),
                    ('13', 'Matcha_Tart', 600000, 10, 50000, datetime('now'), datetime('now'), 'active', 3, 'UI/images/Tart/Matcha_Tart.jpg'),
                    ('14', 'Strawberry_Tart', 650000, 10, 55000, datetime('now'), datetime('now'), 'active', 3, 'UI/images/Tart/Strawberry_Tart.jpg'),
                    ('15', 'Tiramisu_Tart', 70000, 10, 60000, datetime('now'), datetime('now'), 'active', 3, 'UI/images/Tart/Tiramisu_Tart.jpg');
                
                INSERT INTO import_invoice (import_id, employee_id, import_date, total_amount)
                VALUES     
                    (1, 1, datetime('now'), 18500000);
                    
                INSERT INTO import_invoice_details (import_id, product_id, quantity, unit_price)
                VALUES
                    (1, 1, 10, 90000),
                    (1, 2, 10, 100000),
                    (1, 3, 10, 110000),
                    (1, 4, 10, 120000),
                    (1, 5, 10, 130000),
                    (1, 6, 10, 190000),
                    (1, 7, 10, 200000),
                    (1, 8, 10, 210000),
                    (1, 9, 10, 220000),
                    (1, 10, 10, 230000),
                    (1, 11, 10, 40000),
                    (1, 12, 10, 45000),
                    (1, 13, 10, 50000),
                    (1, 14, 10, 55000),
                    (1, 15, 10, 60000);
            """)
        self.connection.commit()
        print("Sample data inserted successfully.")

    def update_element(self):
        # employees_gender = [
        #     ("2025-10-14", "251000001"),
        #     ("2025-10-10", "251000002"),
        #     ("2025-10-9", "251000003"),
        #     ("2025-10-12", "251000004"),
        # ]
        #
        # for starting_date, emp_id in employees_gender:
        #     self.cursor.execute("""
        #         UPDATE employees
        #         SET starting_date = ?
        #         WHERE employee_id = ?
        #     """, (starting_date, emp_id))
        conn = self._get_connection()
        cursor = conn.cursor()

        # cursor.execute("ALTER TABLE customers RENAME TO customers_old;")
        # cursor.execute("""
        # CREATE TABLE customers (
        #     customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
        #     customer_name TEXT NOT NULL,
        #     customer_phone TEXT UNIQUE NOT NULL
        # );
        # """)
        # cursor.execute("""
        # INSERT INTO customers (customer_id, customer_name, customer_phone)
        # SELECT customer_id, customer_name, customer_phone FROM customers_old;
        # """)
        # cursor.execute("DROP TABLE customers_old;")

        # try:
        #     print("Đã kết nối tới database.")
        #     print("Bắt đầu quá trình sửa lại bảng 'invoices' để thêm DEFAULT cho invoice_date...")
        #
        #     cursor.execute("BEGIN TRANSACTION;")
        #     cursor.execute("PRAGMA foreign_keys=OFF;")
        #
        #     # TẠO BẢNG MỚI VỚI CẤU TRÚC ĐÚNG
        #     print(" -> Bước 1: Tạo bảng mới 'invoices_new'...")
        #     cursor.execute("""
        #             CREATE TABLE invoices_new (
        #                 invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
        #                 invoice_code TEXT NOT NULL UNIQUE,
        #                 invoice_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        #                 total_amount DOUBLE NOT NULL CHECK(total_amount >= 0),
        #                 employee_id INTEGER NOT NULL,
        #                 customer_id INTEGER NOT NULL,
        #                 payment_method TEXT NOT NULL CHECK(payment_method IN ('Tiền mặt', 'Chuyển khoản')),
        #                 cash_received TEXT not null,
        #                 change_given TEXT not null,
        #                 FOREIGN KEY(employee_id) REFERENCES employees(employee_id),
        #                 FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
        #             )
        #         """)
        #
        #     # SAO CHÉP DỮ LIỆU TỪ BẢNG CŨ SANG BẢNG MỚI
        #     print(" -> Bước 2: Sao chép dữ liệu từ 'invoices' sang 'invoices_new'...")
        #     # Lấy tất cả các cột từ bảng cũ
        #     cursor.execute("""
        #             INSERT INTO invoices_new (
        #                 invoice_id, invoice_code, invoice_date, total_amount, payment_method,
        #                 cash_received, change_given, employee_id, customer_id
        #             )
        #             SELECT
        #                 invoice_id, invoice_code, invoice_date, total_amount, payment_method,
        #                 cash_received, change_given, employee_id, customer_id
        #             FROM invoices;
        #         """)
        #
        #     # XÓA BẢNG CŨ VÀ ĐỔI TÊN BẢNG MỚI
        #     print(" -> Bước 3: Xóa bảng cũ 'invoices' và đổi tên bảng mới...")
        #     cursor.execute("DROP TABLE invoices;")
        #     cursor.execute("ALTER TABLE invoices_new RENAME TO invoices;")
        #
        #     conn.commit()
        #     print("\nGiao dịch thành công! Bảng 'invoices' đã được cập nhật với cấu trúc đúng.")
        #
        # except sqlite3.Error as e:
        #     print(f"\nCó lỗi xảy ra: {e}")
        #     if conn:
        #         conn.rollback()
        # finally:
        #     if conn:
        #         cursor.execute("PRAGMA foreign_keys=ON;")
        #         conn.close()
        #         print("Đã đóng kết nối database.")

        # cursor.execute("ALTER TABLE invoices add column cash_received TEXT")
        # cursor.execute("ALTER TABLE invoices add column change_given TEXT")
        # cursor.execute("ALTER TABLE invoices add column payment_method TEXT NOT NULL CHECK(payment_method IN ('Tiền mặt', 'Chuyển khoản'))")

        # cursor.execute(
        #    """INSERT OR REPLACE INTO customers (customer_id, customer_name, customer_phone)
        #     VALUES (1, 'Khách vãng lai', 'N/A')
        # """)

        conn.commit()
        conn.close()

if __name__ == "__main__":
    sample = CreateSampleData()  # phải khởi tạo object
    # sample.create_sample_data()  # gọi hàm instance
    sample.update_element()