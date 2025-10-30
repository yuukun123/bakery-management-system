import sqlite3
import os

def create_table():
    # lấy đường dẫn đến thư mục chứ file hiện tại
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # lùi 1 bước về thư muc services
    models_dir = os.path.dirname(script_dir)
    # chốt lại thư mục gốc để chứa folder database
    project_root = os.path.dirname(models_dir)
    # đường dẫn đầy đủ đến thư mục database
    db_folder = os.path.join(project_root, "database")
    # Và cuối cùng, đường dẫn đầy đủ đến file CSDL
    db_path = os.path.join(db_folder, "database.db")

    print(f"Thư mục script hiện tại: {script_dir}")
    print(f"Thư mục gốc của dự án: {project_root}")
    print(f"Đường dẫn CSDL sẽ được tạo tại: {db_path}")

    # Tạo thư mục 'database' trong thư mục gốc nếu nó chưa tồn tại
    os.makedirs(db_folder, exist_ok=True)
    print(f"Thư mục '{db_folder}' đã sẵn sàng.")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    print(f"connect database '{db_path}' successful")
    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            employee_id BIGINT PRIMARY KEY,
            employee_name TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('Quản lý', 'Nhân viên')),
            sex TEXT NOT NULL CHECK(sex IN ('Name', 'Nữ')),
            -- hỗ trợ xóa nhân viên nhưng chỉ là xóa mềm
            status TEXT NOT NULL DEFAULT 'đang làm' CHECK(status IN ('đang làm', 'đã nghỉ')),
            starting_date DATE NOT NULL,
            end_date DATE,
            created_at DATE DEFAULT CURRENT_TIMESTAMP,
            updated_at DATE
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS type_product (
            type_id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_name TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            selling_price REAL NOT NULL CHECK(selling_price >= 0),
            stock INTEGER NOT NULL CHECK(stock >= 0),
            import_price REAL NOT NULL CHECK(import_price >= 0),
            image_path TEXT NOT NULL, -- nếu bạn lưu đường dẫn tương đối (ví dụ: "images/cake1.jpg")
            created_at DATE DEFAULT CURRENT_TIMESTAMP,
            updated_at DATE,
            -- hỗ trợ xóa sản phẩm nhưng chỉ là xóa mềm
            status TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'discontinued')),
            type_id INTEGER NOT NULL,
            FOREIGN KEY(type_id) REFERENCES type_product(type_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            customer_phone TEXT NOT NULL UNIQUE,
            created_at DATE DEFAULT CURRENT_TIMESTAMP, -- Vẫn OK ở đây
            updated_at DATE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_code TEXT NOT NULL UNIQUE,
            invoice_date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            total_amount DOUBLE NOT NULL CHECK(total_amount >= 0),
            employee_id INTEGER NOT NULL,
            customer_id INTEGER NOT NULL,
            payment_method TEXT NOT NULL CHECK(payment_method IN ('Tiền mặt', 'Chuyển khoản')),
            cash_received TEXT not null,
            change_given TEXT not null,
            FOREIGN KEY(employee_id) REFERENCES employees(employee_id),
            FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoice_details (
            invoice_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            unit_price REAL NOT NULL,
            subtotal_amount_invoice REAL GENERATED ALWAYS AS (quantity * unit_price) STORED,
            PRIMARY KEY (invoice_id, product_id),
            FOREIGN KEY(invoice_id) REFERENCES invoices(invoice_id) ON DELETE CASCADE,
            FOREIGN KEY(product_id) REFERENCES products(product_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS import_invoice (
            import_id INTEGER PRIMARY KEY AUTOINCREMENT,
            invoice_date TEXT NOT NULL UNIQUE,
            employee_id INTEGER NOT NULL,
            import_date DATE NOT NULL DEFAULT CURRENT_TIMESTAMP,
            total_amount DOUBLE NOT NULL CHECK(total_amount >= 0),
            FOREIGN KEY(employee_id) REFERENCES employees(employee_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS import_invoice_details (
            import_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            unit_price DOUBLE NOT NULL,
            subtotal_amount_import_invoice REAL GENERATED ALWAYS AS (quantity * unit_price) STORED,
            PRIMARY KEY (import_id, product_id),
            FOREIGN KEY(import_id) REFERENCES import_invoice(import_id) ON DELETE CASCADE,
            FOREIGN KEY(product_id) REFERENCES products(product_id)
        )
    """)

    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS trg_decrease_stock_on_sale
        AFTER INSERT ON invoice_details
        BEGIN
            UPDATE products
            SET stock = stock - NEW.quantity
            WHERE product_id = NEW.product_id;
        END;
    """)

    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS trg_increase_stock_on_import
        AFTER INSERT ON import_invoice_details
        BEGIN
            UPDATE products
            SET stock = stock + NEW.quantity
            WHERE product_id = NEW.product_id;
        END;
    """)

    # Trigger tự động cập nhật `updated_at` cho bảng employees
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS trg_employees_updated_at
        AFTER UPDATE ON employees
        FOR EACH ROW
        BEGIN
            UPDATE employees
            SET updated_at = CURRENT_TIMESTAMP
            WHERE employee_id = OLD.employee_id;
        END;
    """)

    # Trigger tự động cập nhật `updated_at` cho bảng products
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS trg_products_updated_at
        AFTER UPDATE ON products
        FOR EACH ROW
        BEGIN
            UPDATE products
            SET updated_at = CURRENT_TIMESTAMP
            WHERE product_id = OLD.product_id;
        END;
    """)

    print("Tables and Triggers created successfully.")

    conn.commit()
    conn.close()

    print("Tables created successfully.")

if __name__ == "__main__":
    create_table()