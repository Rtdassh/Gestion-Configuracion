MIN_FONT_SIZE = 8
MAX_FONT_SIZE = 24
DEFAULT_FONT_SIZE = 14


def parse_font_size(value):
    try:
        size = int(str(value).strip())
    except Exception:
        return DEFAULT_FONT_SIZE
    if size < MIN_FONT_SIZE or size > MAX_FONT_SIZE:
        return DEFAULT_FONT_SIZE
    return size


