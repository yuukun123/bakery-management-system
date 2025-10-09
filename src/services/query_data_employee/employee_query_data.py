import sqlite3
import os
import time
from datetime import datetime, timedelta
import random


from src.services.API.word_api import generate_audio_from_text


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

# if __name__ == "__main__":
#     query = QueryData()
#     query.remove_word_from_topic(self, )

