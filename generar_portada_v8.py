import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
GOLD = (201, 154, 44)
CREAM = (238, 232, 216)
NAVY_TOP = (14, 24, 48)
NAVY_BOTTOM = (30, 48, 92)
GEORGIA = "C:/Windows/Fonts/georgia.ttf"
GEORGIAB = "C:/Windows/Fonts/georgiab.ttf"

grad_top = Image.new("RGB", (1, H))
for y in range(H):
    t = y / (H - 1)
    r = int(NAVY_TOP[0] + (NAVY_BOTTOM[0] - NAVY_TOP[0]) * t)
    g = int(NAVY_TOP[1] + (NAVY_BOTTOM[1] - NAVY_TOP[1]) * t)
    b = int(NAVY_TOP[2] + (NAVY_BOTTOM[2] - NAVY_TOP[2]) * t)
    grad_top.putpixel((0, y), (r, g, b))
im = grad_top.resize((W, H))

d = ImageDraw.Draw(im)

GOLD_RULE = (196, 151, 45)

def rule(x1, y, x2):
    d.rectangle([x1, y, x2, y + 2], fill=GOLD_RULE)

def text_w(font, s):
    bb = d.textbbox((0, 0), s, font=font)
    return bb[2] - bb[0]

TITLE = "MARATONAIDE"
TAGLINE = "La ayuda que convierte una marat\u00f3n en un viaje por la mente, el cuerpo y el esp\u00edritu."
AUTHOR = "ALEJANDRO OCHOA P\u00c9REZ"

fs_title = 94
f_title = ImageFont.truetype(GEORGIAB, fs_title)
while text_w(f_title, TITLE) > 792 and fs_title > 40:
    fs_title -= 1
    f_title = ImageFont.truetype(GEORGIAB, fs_title)

t_w = text_w(f_title, TITLE)
x_title = (W - t_w) // 2
y_title = 60
d.text((x_title, y_title), TITLE, font=f_title, fill=GOLD)

rule_x1 = (W - 560) // 2
rule_y = y_title + 150
rule(rule_x1, rule_y, rule_x1 + 560)

f_tag = ImageFont.truetype(GEORGIA, 25)
fs_tag = 25
while text_w(f_tag, TAGLINE) > 720 and fs_tag > 14:
    fs_tag -= 1
    f_tag = ImageFont.truetype(GEORGIA, fs_tag)
tag_w = text_w(f_tag, TAGLINE)
d.text(((W - tag_w) // 2, rule_y + 26), TAGLINE, font=f_tag, fill=CREAM)

synopsis_lines = [
    "Un hombre de cincuenta y dos a\u00f1os hereda de su padre siete tarjetas",
    "cifradas con el cuerpo: respiraciones por rengl\u00f3n, pasos por frase.",
    "Para descifrarlas corre la marat\u00f3n de Medell\u00edn \u2014la misma que su",
    "padre corri\u00f3 con el dorsal 2038\u2014 y en cada kil\u00f3metro descubre que",
    "las verdades m\u00e1s hondas no se piensan: se encarnan. Un viaje de",
    "42.195 metros por la mente, el cuerpo y el esp\u00edritu, hasta la \u00faltima",
    "tarjeta que solo se lee a ritmo de carrera.",
]
f_syn = ImageFont.truetype(GEORGIA, 24)
y = rule_y + 150
for line in synopsis_lines:
    lw = text_w(f_syn, line)
    d.text(((W - lw) // 2, y), line, font=f_syn, fill=CREAM)
    y += 40

rule2_y = y + 6
rule(rule_x1, rule2_y, rule_x1 + 560)

f_author = ImageFont.truetype(GEORGIAB, 30)
a_w = text_w(f_author, AUTHOR)
d.text(((W - a_w) // 2, rule2_y + 26), AUTHOR, font=f_author, fill=GOLD)

im.save("maratonaide_cover_v8.png")
print("saved", im.size)
print("title font size:", fs_title, "title width:", t_w)