import os
import sqlite3
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

class Login:
    def __init__(self):
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

        self.connection = sqlite3.connect(db_path)
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()
        print(f"connect database '{db_path}' successful")

    def check_login(self, employee_id, password_login):
        """
        Checks user credentials against the database correctly.
        Returns user info dictionary on success, None on failure.
        """
        cursor = self.cursor
        # Bước 1: Lấy thông tin người dùng bằng username
        # Chúng ta chỉ cần lấy password_hash để kiểm tra
        cursor.execute("""
            SELECT
                employee_id AS id,
                role
                password AS password_hash
                status
            FROM
                users
            WHERE
                LOWER(user_name) = LOWER(?)
        """, (employee_id,))
        user_data = cursor.fetchone()

        if not user_data:
            print(f"❌ Login failed: User '{employee_id}' not found.")
            return {"success": False, "error": "invalid_credentials"}

        # Bước 2: Dùng check_password_hash để so sánh mật khẩu người dùng nhập
        # với chuỗi hash đã lưu trong DB.
        stored_password_hash = user_data['password_hash']

        if check_password_hash(stored_password_hash, password_login):
            print(f"✅ Login success for user '{employee_id}'")
            # Trả về một dictionary chứa thông tin người dùng, rất hữu ích cho ứng dụng
            return {"success": True, "user": dict(user_data)}  # luôn có success
        elif not check_password_hash(stored_password_hash, password_login):
            print(f"❌ Login failed for user '{employee_id}': Incorrect password.")
            return {"success": False, "error": "incorrect_password"}
        elif user_data['status'] == 'inactive':
            print(f"❌ Login failed for user '{employee_id}': Account is inactive.")
            return {"success": False, "error": "account_inactive"}
        else:
            print(f"❌ Login failed for user '{employee_id}': Unknown error.")
            return {"success": False, "error": "unknown_error"}

    def close(self):
        self.connection.close()