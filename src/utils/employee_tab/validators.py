import re

def is_valid_phone_number(phone_number: str) -> bool:
    """
    Kiểm tra xem một chuỗi có phải là số điện thoại hợp lệ của Việt Nam hay không.
    Chấp nhận các SĐT 10 số, bắt đầu bằng đầu số 0.

    Args:
        phone_number (str): Chuỗi số điện thoại cần kiểm tra.

    Returns:
        bool: True nếu hợp lệ, False nếu không hợp lệ.
    """
    if not phone_number or not isinstance(phone_number, str):
        return False

    # Regex cho SĐT Việt Nam 10 số (bắt đầu bằng 0, theo sau là 9 chữ số)
    # Ví dụ: 0912345678, 0398765432, ...
    pattern = r'^0\d{9}$'

    if re.match(pattern, phone_number):
        return True
    else:
        return False