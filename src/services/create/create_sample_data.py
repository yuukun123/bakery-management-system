import os
import sqlite3

class CreateSampleData:
    def __init__(self):
        # lấy đường dẫn đến thư mục chứ file hiện tại
        script_dir = os.path.dirname(os.path.abspath(__file__))

        # lùi 1 bước về thư mục services
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

        # Kết nối CSDL
        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row  # trả về dạng dict-like thay vì tuple
        self.cursor = self.connection.cursor()
        print(f"connect database '{db_path}' successful")

    def create_sample_data(self):
        self.cursor.execute("""
                INSERT INTO products (product_id, product_name, selling_price, stock, import_price, created_at, updated_at, status, type_id)
                VALUES 
                    ('1', 'Avocado_Croissant', 50000, 10, 45000, datetime('now'), datetime('now'), 'active', 1),
                    ('1', 'Avocado_Croissant', 50000, 10, 45000, datetime('now'), datetime('now'), 'active', 1),
                    ('1', 'Avocado_Croissant', 50000, 10, 45000, datetime('now'), datetime('now'), 'active', 1),
                    ('1', 'Avocado_Croissant', 50000, 10, 45000, datetime('now'), datetime('now'), 'active', 1),
                    ('1', 'Avocado_Croissant', 50000, 10, 45000, datetime('now'), datetime('now'), 'active', 1),
                    ('1', 'Avocado_Croissant', 50000, 10, 45000, datetime('now'), datetime('now'), 'active', 1),
                    ('2', 'Mousse'),
                    ('3', 'Tart')
            """)
        self.connection.commit()
        print("Sample data inserted successfully.")

    # def update_element(self):
    #     self.cursor.execute("""ALTER TABLE products RENAME COLUMN sellingPrice TO selling_price""")
    #     self.connection.commit()

if __name__ == "__main__":
    sample = CreateSampleData()  # phải khởi tạo object
    sample.create_sample_data()  # gọi hàm instance