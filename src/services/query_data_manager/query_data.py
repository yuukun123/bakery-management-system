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
    def generate_new_employee_id(cursor):
        """
        Tạo mã nhân viên mới theo định dạng YYMMNNNNN.
        Hàm này cần được gọi bên trong một transaction.
        """
        # 1. Lấy tiền tố năm (2 số cuối) và tháng hiện tại
        now = datetime.now()
        # THAY ĐỔI DUY NHẤT LÀ Ở ĐÂY: từ %Y sang %y
        prefix = now.strftime('%y%m')  # Ví dụ: '2310'

        # 2. Tìm ID lớn nhất trong tháng hiện tại
        # Logic còn lại giữ nguyên
        query = """
            SELECT MAX(employee_id) 
            FROM employees 
            WHERE CAST(employee_id AS TEXT) LIKE ?
        """
        cursor.execute(query, (f'{prefix}%',))
        last_id = cursor.fetchone()[0]

        # 3. Xác định số thứ tự tiếp theo
        if last_id is None:
            # Chưa có nhân viên nào trong tháng này, bắt đầu từ 1
            next_seq_number = 1
        else:
            # Đã có nhân viên, lấy 5 số cuối và cộng thêm 1
            # Độ dài tiền tố là 4 (YYMM), nên chuỗi ID sẽ là 9 ký tự
            last_seq_str = str(last_id)[-5:]  # Vẫn lấy 5 ký tự cuối
            next_seq_number = int(last_seq_str) + 1

        # 4. Tạo mã nhân viên hoàn chỉnh
        # Ghép tiền tố '2310' với số thứ tự '00001'
        new_id = int(f"{prefix}{next_seq_number:05d}")

        return new_id