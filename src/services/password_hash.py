import os
import sqlite3
from werkzeug.security import generate_password_hash

def migrate_plain_passwords_to_hash():
    db_path = "D:/CODE/bakery-management-system/src/database/database.db"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Lấy tất cả nhân viên có mật khẩu chưa hash (ví dụ không bắt đầu bằng "pbkdf2:")
    cursor.execute("SELECT employee_id, password_hash FROM employees")
    employees = cursor.fetchall()

    for emp_id, plain_pass in employees:
        if not plain_pass.startswith("pbkdf2:"):  # chỉ hash những mật khẩu thô
            hashed = generate_password_hash(plain_pass)
            cursor.execute(
                "UPDATE employees SET password_hash = ? WHERE employee_id = ?",
                (hashed, emp_id),
            )
            print(f"🔐 Hashed password for employee {emp_id}")

    conn.commit()
    conn.close()
    print("✅ Migration completed. All passwords are now hashed.")

if __name__ == "__main__":
    migrate_plain_passwords_to_hash()