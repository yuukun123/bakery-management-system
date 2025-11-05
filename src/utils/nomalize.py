import unicodedata

def _normalize_search_sqlite(input_str):
    if input_str is None:
        return None
    nfkd_form = unicodedata.normalize('NFD', str(input_str))
    only_ascii = u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
    return only_ascii.lower()