"""
Sınıf numarası → sınıf kodu ve çizim rengi.

Model sınıf NUMARASI döndürür (0-3). Sıra eğitimdeki data.yaml ile birebir aynı olmak zorunda
(CLAUDE.md, "Sınıflar"); yanlış sırada her kutu yanlış adla gösterilir.
Okunur adlar (Boyuna çatlak / Longitudinal crack ...) iki dilli olduğu için texts.py'de.
"""

# Eğitimdeki sıra: 0 D00, 1 D10, 2 D20, 3 D40 (data/yolo/data.yaml)
CLASS_CODES = ["D00", "D10", "D20", "D40"]

# Okabe–Ito paleti: renk körlüğünde de birbirinden ayrılan 4 renk (RGB, 0-255).
# Aynı renk kutuda, tabloda ve lejantta kullanılır; sayfa boyunca tek bir renk dili olsun diye.
CLASS_COLORS = {
    "D00": (0, 114, 178),    # #0072B2 mavi
    "D10": (230, 159, 0),    # #E69F00 turuncu
    "D20": (0, 158, 115),    # #009E73 yeşil
    "D40": (204, 121, 167),  # #CC79A7 pembe-mor
}


def hex_color(code):
    """Sınıfın rengini "#RRGGBB" metni olarak döndürür (HTML/CSS'te kullanmak için)."""
    r, g, b = CLASS_COLORS[code]
    return f"#{r:02X}{g:02X}{b:02X}"
