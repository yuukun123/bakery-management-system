import os
import sqlite3
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash


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
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.executescript("""
                INSERT INTO type_product (type_id, type_name)
                VALUES 
                    (1, 'Croissant'),
                    (2, 'Mousse'),
                    (3, 'Tart');
                
                INSERT INTO products (product_id, product_name, selling_price, stock, import_price, created_at, updated_at, status, type_id, image_path)
                VALUES 
                    ('1', 'Avocado_Croissant', 100000, 10, 90000, datetime('now'), datetime('now'), 'đang kinh doanh', 1, 'UI/images/Croissant/Avocado_Croissant.jpg'),
                    ('2', 'Choco_Mallow_Croissant', 110000, 10, 100000, datetime('now'), datetime('now'), 'đang kinh doanh', 1, 'UI/images/Croissant/Choco_Mallow_Croissant.png'),
                    ('3', 'Dinosaur_Almond_Croissant', 120000, 10, 110000, datetime('now'), datetime('now'), 'đang kinh doanh', 1, 'UI/images/Croissant/Dinosaur_Almond_Croissant.png'),
                    ('4', 'Honey_Almond_Croissant', 130000, 10, 120000, datetime('now'), datetime('now'), 'đang kinh doanh', 1, 'UI/images/Croissant/Honey_Almond_Croissant.png'),
                    ('5', 'Matcha_Croissant', 140000, 10, 130000, datetime('now'), datetime('now'), 'đang kinh doanh', 1, 'UI/images/Croissant/Matcha_Croissant.jpg'),
                    ('6', 'Avocado_Mousse', 200000, 10, 190000, datetime('now'), datetime('now'), 'đang kinh doanh', 2, 'UI/images/Mousse/Avocado_Mousse.jpg'),
                    ('7', 'Blueberry_Mousse', 210000, 10, 200000, datetime('now'), datetime('now'), 'đang kinh doanh', 2, 'UI/images/Mousse/Blueberry_Mousse.jpg'),
                    ('8', 'Corn_Mousse', 220000, 10, 210000, datetime('now'), datetime('now'), 'đang kinh doanh', 2, 'UI/images/Mousse/Corn_Mousse.jpg'),
                    ('9', 'Longan_Mousse', 230000, 10, 220000, datetime('now'), datetime('now'), 'đang kinh doanh', 2, 'UI/images/Mousse/Longan_Mousse.jpg'),
                    ('10', 'Mango_Mousse', 240000, 10, 230000, datetime('now'), datetime('now'), 'đang kinh doanh', 2, 'UI/images/Mousse/Mango_Mousse.jpg'),
                    ('11', 'Coffee_Tart', 50000, 10, 40000, datetime('now'), datetime('now'), 'đang kinh doanh', 3, 'UI/images/Tart/Coffee_Tart.jpg'),
                    ('12', 'Cherry_Tart', 550000, 10, 45000, datetime('now'), datetime('now'), 'đang kinh doanh', 3, 'UI/images/Tart/Cherry_Tart.jpg'),
                    ('13', 'Matcha_Tart', 600000, 10, 50000, datetime('now'), datetime('now'), 'đang kinh doanh', 3, 'UI/images/Tart/Matcha_Tart.jpg'),
                    ('14', 'Strawberry_Tart', 650000, 10, 55000, datetime('now'), datetime('now'), 'đang kinh doanh', 3, 'UI/images/Tart/Strawberry_Tart.jpg'),
                    ('15', 'Tiramisu_Tart', 70000, 10, 60000, datetime('now'), datetime('now'), 'đang kinh doanh', 3, 'UI/images/Tart/Tiramisu_Tart.jpg');
                
                INSERT INTO import_invoice (import_id, import_code, employee_id, import_date, total_amount)
                VALUES     
                    (1, 'PN251000001' ,1, date('now'), 18500000);
                    
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
                    
                INSERT INTO customers (customer_id, customer_name, customer_phone, created_at)
                VALUES
                    (1, 'Khách vãng lai', '', datetime('now')),
                    (2, 'Jane Smith', '0987654321', datetime('now'));
                    
                INSERT INTO employees (employee_id, employee_name, phone, address, email, password_hash, role, gender, starting_date, status, created_at)
                VALUES
                    (251000001, 'hao', '0808080808', '123 Main St', 'john.doe@example.com', '1', 'quản lý', 'nữ', date('now'), 'đang làm', datetime('now')),
                    (251000002, 'phong', '0987654321', '456 Elm St', 'jane.smith@example.com', '1', 'nhân viên', 'nam', date('now'), 'đang làm', datetime('now'));
            """)
        conn.commit()
        conn.close()
        print("Sample data inserted successfully.")

    def update_element(self):

        conn = self._get_connection()
        cursor = conn.cursor()

        # employees_gender = [
        #     ("2025-10-14", "251000001"),
        #     ("2025-10-10", "251000002"),
        #     ("2025-10-9", "251000003"),
        #     ("2025-10-12", "251000004"),
        # ]
        #
        # for starting_date, emp_id in employees_gender:
        #     cursor.execute("""
        #         UPDATE employees
        #         SET starting_date = ?
        #         WHERE employee_id = ?
        #     """, (starting_date, emp_id))

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

        # try:
        #     conn.execute("BEGIN TRANSACTION;")  # Bắt đầu giao dịch
        #
        #     # --- KIỂM TRA VÀ THÊM CỘT ---
        #     cursor.execute("PRAGMA table_info(customers)")
        #     columns = [info[1] for info in cursor.fetchall()]
        #
        #     # 1. Thêm cột 'created_at' nếu chưa tồn tại
        #     if 'created_at' not in columns:
        #         print(" -> Thêm cột 'created_at'...")
        #
        #         # BƯỚC 1: Thêm cột với giá trị mặc định là NULL
        #         cursor.execute("ALTER TABLE customers ADD COLUMN created_at DATETIME")
        #
        #         # BƯỚC 2: Cập nhật giá trị cho các dòng đã có
        #         # Dùng strftime để có định dạng YYYY-MM-DD HH:MM:SS
        #         now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        #         cursor.execute("UPDATE customers SET created_at = ? WHERE created_at IS NULL", (now_str,))
        #         print(" -> Đã cập nhật giá trị mặc định cho 'created_at'.")
        #     else:
        #         print(" -> Cột 'created_at' đã tồn tại.")
        #
        #     # 2. Thêm cột 'updated_at' nếu chưa tồn tại
        #     if 'updated_at' not in columns:
        #         print(" -> Thêm cột 'updated_at'...")
        #
        #         # BƯỚC 1: Thêm cột
        #         cursor.execute("ALTER TABLE customers ADD COLUMN updated_at DATETIME")
        #
        #         # BƯỚC 2: Cập nhật giá trị, sao chép từ created_at
        #         cursor.execute("UPDATE customers SET updated_at = created_at WHERE updated_at IS NULL")
        #         print(" -> Đã cập nhật giá trị mặc định cho 'updated_at'.")
        #     else:
        #         print(" -> Cột 'updated_at' đã tồn tại.")
        #
        #     # --- TẠO TRIGGER ĐỂ TỰ ĐỘNG CẬP NHẬT 'updated_at' ---
        #     print(" -> Tạo/Tạo lại trigger 'trg_customers_updated_at'...")
        #     cursor.execute("""
        #             CREATE TRIGGER IF NOT EXISTS trg_customers_updated_at
        #             AFTER UPDATE ON customers
        #             FOR EACH ROW
        #             BEGIN
        #                 UPDATE customers
        #                 SET updated_at = CURRENT_TIMESTAMP
        #                 WHERE customer_id = OLD.customer_id;
        #             END;
        #         """)
        #
        #     conn.commit()  # Lưu tất cả các thay đổi
        #     print("\nCập nhật bảng 'customers' thành công!")
        #
        # except sqlite3.Error as e:
        #     print(f"\nCó lỗi xảy ra: {e}")
        #     if conn:
        #         conn.rollback()  # Hủy bỏ nếu có lỗi
        # finally:
        #     if conn:
        #         conn.close()
        #         print("Đã đóng kết nối database.")

        # try:
        #     print("Đã kết nối tới database.")
        #
        #     # --- BẮT ĐẦU GIAO DỊCH AN TOÀN ---
        #     cursor.execute("BEGIN TRANSACTION;")
        #     cursor.execute("PRAGMA foreign_keys=OFF;")
        #
        #     # === BƯỚC 1: TẠO BẢNG MỚI VỚI CẤU TRÚC ĐÚNG (BAO GỒM CẢ CỘT MỚI) ===
        #     print(" -> Bước 1: Tạo bảng tạm 'employees_new' với cấu trúc hoàn chỉnh...")
        #     cursor.execute("""
        #             CREATE TABLE employees_new (
        #                 employee_id BIGINT PRIMARY KEY,
        #                 employee_name TEXT NOT NULL,
        #                 password_hash TEXT NOT NULL,
        #                 email TEXT NOT NULL UNIQUE,
        #                 phone TEXT NOT NULL,
        #                 address TEXT NOT NULL,
        #                 role TEXT NOT NULL CHECK(role IN ('Quản lý', 'Nhân viên')),
        #                 sex TEXT NOT NULL CHECK(sex IN ('Nam', 'Nữ')),
        #                 status TEXT NOT NULL DEFAULT 'đang làm' CHECK(status IN ('đang làm', 'đã nghỉ')),
        #
        #                 -- <<< THÊM 2 CỘT MỚI VÀO ĐÂY >>>
        #                 starting_date DATETIME NOT NULL,
        #                 end_date DATETIME,
        #
        #                 created_at DATETIME,
        #                 updated_at DATETIME
        #             )
        #         """)
        #
        #     # === BƯỚC 2: SAO CHÉP, "DỊCH" VÀ ĐIỀN DỮ LIỆU MẶC ĐỊNH ===
        #     print(" -> Bước 2: Chuyển đổi và sao chép dữ liệu sang 'employees_new'...")
        #     cursor.execute("""
        #             INSERT INTO employees_new (
        #                 employee_id, employee_name, password_hash, email, phone, address,
        #                 role, sex, status,
        #                 starting_date, end_date, -- Thêm vào danh sách INSERT
        #                 created_at, updated_at
        #             )
        #             SELECT
        #                 employee_id, employee_name, password_hash, email, phone, address,
        #                 -- "Dịch" các giá trị sang tiếng Việt
        #                 CASE role
        #                     WHEN 'Manager' THEN 'Quản lý'
        #                     WHEN 'Employee' THEN 'Nhân viên'
        #                     ELSE role
        #                 END,
        #                 CASE sex
        #                     WHEN 'Male' THEN 'Nam'
        #                     WHEN 'Female' THEN 'Nữ'
        #                     ELSE sex
        #                 END,
        #                 CASE status
        #                     WHEN 'active' THEN 'đang làm'
        #                     WHEN 'inactive' THEN 'đã nghỉ'
        #                     ELSE status
        #                 END,
        #
        #                 -- <<< CUNG CẤP GIÁ TRỊ CHO 2 CỘT MỚI >>>
        #                 -- Dùng `created_at` làm giá trị mặc định cho `starting_date`
        #                 COALESCE(created_at, CURRENT_TIMESTAMP),
        #                 -- Mặc định `end_date` là NULL cho các nhân viên cũ
        #                 NULL,
        #
        #                 created_at,
        #                 updated_at
        #             FROM employees;
        #         """)
        #
        #     row_count = cursor.rowcount
        #     print(f" -> Đã chuyển đổi thành công {row_count} bản ghi.")
        #
        #     # === BƯỚC 3: XÓA BẢNG CŨ VÀ ĐỔI TÊN BẢNG MỚI ===
        #     print(" -> Bước 3: Xóa bảng cũ 'employees'...")
        #     cursor.execute("DROP TABLE employees;")
        #
        #     print(" -> Bước 4: Đổi tên 'employees_new' thành 'employees'...")
        #     cursor.execute("ALTER TABLE employees_new RENAME TO employees;")
        #
        #     # === BƯỚC 4: TẠO LẠI CÁC TRIGGER LIÊN QUAN ===
        #     print(" -> Bước 5: Tạo lại trigger 'trg_employees_updated_at'...")
        #     cursor.execute("""
        #             CREATE TRIGGER IF NOT EXISTS trg_employees_updated_at
        #             AFTER UPDATE ON employees
        #             FOR EACH ROW
        #             BEGIN
        #                 UPDATE employees
        #                 SET updated_at = CURRENT_TIMESTAMP
        #                 WHERE employee_id = OLD.employee_id;
        #             END;
        #         """)
        #
        #     # --- KẾT THÚC GIAO DỊCH ---
        #     conn.commit()
        #     print("\nCập nhật bảng 'employees' thành công!")
        #
        # except sqlite3.Error as e:
        #     print(f"\nCó lỗi xảy ra: {e}")
        #     if conn:
        #         print("Đang rollback lại các thay đổi...")
        #         conn.rollback()
        # finally:
        #     if conn:
        #         cursor.execute("PRAGMA foreign_keys=ON;")
        #         conn.close()
        #         print("Đã đóng kết nối database.")

        # cursor.execute("ALTER TABLE customers add column create_at DATETIME DEFAULT CURRENT_TIMESTAMP")
        # cursor.execute("ALTER TABLE customers add column update_at DATETIME DEFAULT CURRENT_TIMESTAMP")
        # cursor.execute("ALTER TABLE invoices add column payment_method TEXT NOT NULL CHECK(payment_method IN ('Tiền mặt', 'Chuyển khoản'))")

        # cursor.execute(
        #    """INSERT OR REPLACE INTO customers (customer_id, customer_name, customer_phone)
        #     VALUES (1, 'Khách vãng lai', 'N/A')
        # """)


        # conn.commit()
        # conn.close()

        # try:
        #
        #     print("Đã kết nối tới database.")
        #
        #     # 1. Lấy ID và mật khẩu plain text của tất cả nhân viên
        #     print(" -> Đang đọc thông tin nhân viên...")
        #     cursor.execute("SELECT employee_id, password_hash FROM employees")
        #     all_employees = cursor.fetchall()
        #
        #     if not all_employees:
        #         print("Không có nhân viên nào để cập nhật.")
        #         return
        #
        #     updates_to_perform = []
        #     print(" -> Bắt đầu băm mật khẩu...")
        #
        #     for employee_id, plain_password in all_employees:
        #         # Kiểm tra xem mật khẩu có phải là hash hay không (rất cơ bản)
        #         # Hash của Werkzeug thường bắt đầu bằng một tiền tố như "pbkdf2:sha256:..."
        #         # Nếu mật khẩu không chứa ký tự '$', khả năng cao nó là plain text
        #         if '$' in plain_password and ':' in plain_password:
        #             print(f"    - Bỏ qua Employee ID {employee_id}: Mật khẩu có vẻ đã được băm.")
        #             continue
        #
        #         # 2. Băm mật khẩu bằng hàm của werkzeug
        #         hashed_password = generate_password_hash(plain_password)
        #         updates_to_perform.append((hashed_password, employee_id))
        #         print(f"    - Employee ID {employee_id}: Chuẩn bị cập nhật mật khẩu từ '{plain_password}' sang hash.")
        #
        #     if not updates_to_perform:
        #         print("Tất cả mật khẩu đã được băm. Không có gì để làm.")
        #         return
        #
        #     # 3. Cập nhật lại CSDL với mật khẩu đã băm
        #     print(f" -> Đang cập nhật {len(updates_to_perform)} mật khẩu vào CSDL...")
        #     sql_update = "UPDATE employees SET password_hash = ? WHERE employee_id = ?"
        #     cursor.executemany(sql_update, updates_to_perform)
        #
        #     conn.commit()
        #     print("\nCập nhật mật khẩu thành công!")
        #
        # except sqlite3.Error as e:
        #     print(f"\nCó lỗi xảy ra: {e}")
        #     if conn:
        #         conn.rollback()
        # finally:
        #     if conn:
        #         conn.close()
        #         print("Đã đóng kết nối database.")


if __name__ == "__main__":
    sample = CreateSampleData()  # phải khởi tạo object
    # sample.create_sample_data()  # gọi hàm instance
    sample.update_element()