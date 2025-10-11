import sqlite3
import os

class QueryUserName:
    def __init__(self):
        self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
        self.db_path = os.path.join(self.project_root, "database", "database.db")

    def _get_connection(self):
        """Hàm tiện ích để tạo một kết nối mới."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_employee_by_employee_id(self, employee_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT employee_name FROM employees WHERE employee_id = ?", (employee_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Database error in get_employee_by_employee_id: {e}")
            return None

    def get_employee_role_by_employee_id(self, employee_id):
        conn = self._get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT role FROM employees WHERE employee_id = ?", (employee_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
        except sqlite3.Error as e:
            print(f"Database error in get_employee_role_by_employee_id: {e}")
            return None