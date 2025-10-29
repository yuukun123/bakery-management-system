import re

def is_valid_phone_number(phone_number: str) -> bool:
    """
    Kiểm tra số điện thoại VN 10 chữ số hợp lệ.
    - Bắt đầu bằng 0 và có 10 chữ số tổng cộng.
    - Bắt đầu bằng một trong các đầu số phổ biến: 03,05,07,08,09.
    - Loại trừ chuỗi toàn '0' như '0000000000'.
    """
    if not phone_number or not isinstance(phone_number, str):
        return False

    phone = phone_number.strip()

    # Loại trừ chuỗi toàn 0
    if phone == "0" * 10:
        return False

    if len(phone) != 10:
        return False

    if not phone.startswith("0"):
        return False

    # Regex: bắt đầu bằng 03|05|07|08|09 + 8 chữ số nữa (tổng 10 chữ số)
    pattern = r'^(03|05|07|08|09)\d{8}$'
    return bool(re.match(pattern, phone))
