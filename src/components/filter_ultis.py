def filter_students_by_keyword(data, keyword: str):
    keyword = keyword.strip().lower()
    if not keyword:
        return data
    return [
        s for s in data if keyword in
        str(s.get("employee_id", "")).lower()
        or keyword in str(s.get("employee_name", "")).lower()
        or keyword in str(s.get("customer_name", "")).lower()
        or keyword in str(s.get("customer_phone", "")).lower()
        or keyword in str(s.get("product_id", "")).lower()
        or keyword in str(s.get("product_name", "")).lower()
        or keyword in str(s.get("invoice_code", "")).lower()
        or keyword in str(s.get("import_code", "")).lower()
    ]