def hex_to_rgb(hex_color: str):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def relative_luminance(rgb):
    def srgb_to_linear(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = rgb
    r_lin, g_lin, b_lin = srgb_to_linear(r), srgb_to_linear(g), srgb_to_linear(b)
    return 0.2126 * r_lin + 0.7152 * g_lin + 0.0722 * b_lin


def contrast_ratio(hex1: str, hex2: str) -> float:
    l1 = relative_luminance(hex_to_rgb(hex1))
    l2 = relative_luminance(hex_to_rgb(hex2))
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


# Opciones de color por nombre para los comboboxes
COLOR_OPTIONS = [
    ("Blanco", "#ffffff"),
    ("Negro", "#000000"),
    ("Rojo", "#ff0000"),
    ("Verde", "#007f5f"),
    ("Azul", "#184E77"),
    ("Amarillo", "#ffd449"),
    ("Magenta", "#8367c7"),
    ("Cian", "#34A0A4"),
]

COLOR_NAME_TO_HEX = {name: hexv for name, hexv in COLOR_OPTIONS}
HEX_TO_COLOR_NAME = {hexv.lower(): name for name, hexv in COLOR_OPTIONS}
DEFAULT_COLOR_NAME = "Blanco"


