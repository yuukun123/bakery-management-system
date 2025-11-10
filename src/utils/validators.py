import re

def is_valid_phone_number(phone_number: str) -> bool:
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
