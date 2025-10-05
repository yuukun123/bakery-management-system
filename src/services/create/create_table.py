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
        CREATE TABLE IF NOT EXISTS positions (
            position_name TEXT PRIMARY KEY
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_name TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            address TEXT NOT NULL,
            position_name TEXT NOT NULL,
            created_at DATETIME,
            update_at DATETIME,
            FOREIGN KEY(position_name) REFERENCES positions(position_name)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS type_product (
            type_id INTEGER PRIMARY KEY AUTOINCREMENT,
            type_name TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            price DOUBLE NOT NULL,
            type_id INTEGER NOT NULL,
            FOREIGN KEY(type_id) REFERENCES type_product(type_id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT NOT NULL,
            customer_phone TEXT NOT NULL,
            customer_address TEXT NOT NULL,
            customer_email TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            invoice_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_buy DATETIME NOT NULL,
            total_amount DOUBLE NOT NULL,
            employee_id INTEGER NOT NULL,
            customer_id INTEGER NOT NULL,
            FOREIGN KEY(employee_id) REFERENCES employees(employee_id),
            FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
        )
    """)

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS invoice_details (
                invoice_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL CHECK(quantity > 0),
                unit_price DOUBLE NOT NULL,
                subtotal_amount DOUBLE NOT NULL,
                product_id INTEGER NOT NULL,
                PRIMARY KEY (invoice_id, product_id),
                FOREIGN KEY(invoice_id) REFERENCES invoice(invoice_id) ON DELETE CASCADE,
                FOREIGN KEY(product_id) REFERENCES products(product_id)
            )
    """)

    conn.commit()
    conn.close()

    print("Tables created successfully.")

if __name__ == "__main__":
    create_table()