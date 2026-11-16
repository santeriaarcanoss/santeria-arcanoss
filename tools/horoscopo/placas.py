"""Genera las placas del horóscopo (tapa + 12 signos + cierre) y el texto del posteo.
Uso: python3 placas.py datos.json ../../public/horoscopo
Crea public/horoscopo/AAAA-MM-DD/NN-nombre.jpg y publicacion.json
"""
import json, math, os, random, sys, datetime
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

AQUI = os.path.dirname(os.path.abspath(__file__)); FU = os.path.join(AQUI, "fuentes")
SITIO = "https://santeriaarcanoss.com.ar"
S = 2; W, H = 1080 * S, 1350 * S
GOLD = (214, 178, 110); CREAM = (240, 232, 214); DIM = (160, 150, 175); SOFT = (215, 205, 225)
_F = {"t": "texgyrepagella-regular.otf", "ti": "texgyrepagella-italic.otf", "b": "Inter-Light.otf",
      "bm": "Inter-Medium.otf", "bs": "Inter-SemiBold.otf", "g": "DejaVuSans.ttf"}
def F(k, size): return ImageFont.truetype(os.path.join(FU, _F[k]), int(size * S))
DIAS = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
FASES = [" Con la Luna creciendo, empujá lo que querés que crezca.", " Con la Luna menguando, aprovechá para soltar y limpiar."]

def fondo(seed):
    rnd = random.Random(seed); im = Image.new("RGB", (W, H)); d = ImageDraw.Draw(im)
    top, bot = (16, 10, 34), (4, 3, 10)
    for y in range(H):
        t = y / H; d.line([(0, y), (W, y)], fill=tuple(int(top[i] * (1 - t) + bot[i] * t) for i in range(3)))
    glow = Image.new("RGB", (W, H)); g = ImageDraw.Draw(glow); cx, cy, r = W // 2, int(H * .30), int(W * .55)
    g.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(46, 26, 84)); glow = glow.filter(ImageFilter.GaussianBlur(220 * S))
    im = ImageChops.add(im, glow); d = ImageDraw.Draw(im)
    for _ in range(140):
        x, y = rnd.randint(0, W), rnd.randint(0, H); rr = rnd.choice([1, 1, 1, 2, 2, 3]); a = rnd.randint(70, 200)
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=(a, a, int(a * .9)))
    for _ in range(7):
        x, y = rnd.randint(80 * S, W - 80 * S), rnd.randint(80 * S, H - 80 * S); l = rnd.randint(7, 12) * S
        d.line([(x - l, y), (x + l, y)], fill=GOLD, width=S); d.line([(x, y - l), (x, y + l)], fill=GOLD, width=S)
    d.rectangle([38 * S, 38 * S, W - 38 * S, H - 38 * S], outline=GOLD, width=2 * S)
    d.rectangle([50 * S, 50 * S, W - 50 * S, H - 50 * S], outline=(110, 90, 60), width=S)
    return im, d

def wrap(d, text, font, maxw):
    out = []
    for para in text.split("\n"):
        line = ""
        for w in para.split():
            t = (line + " " + w).strip()
            if d.textlength(t, font=font) <= maxw: line = t
            else: out.append(line); line = w
        out.append(line)
    return out

def bloque(d, text, font, y, fill, maxw=None, lh=1.25, x=None, dibujar=True):
    maxw = maxw or W - 220 * S; h = int(font.size * lh)
    for l in wrap(d, text, font, maxw):
        if dibujar:
            if x is None: d.text((W // 2, y), l, font=font, fill=fill, anchor="ma")
            else: d.text((x, y), l, font=font, fill=fill, anchor="la")
        y += h
    return y

def volanta(d, text, y):
    f = F("bs", 26); sp = 7 * S; tw = sum(d.textlength(c, font=f) for c in text) + sp * (len(text) - 1); x = (W - tw) / 2
    for c in text: d.text((x, y), c, font=f, fill=GOLD); x += d.textlength(c, font=f) + sp

def fases(d, cy):
    for i, k in enumerate((-2, -1, 0, 1, 2)):
        x = W // 2 + k * 70 * S; r = (22 if i == 2 else 15) * S
        d.ellipse([x - r, cy - r, x + r, cy + r], fill=GOLD)
        if i != 2:
            o = int(r * (.9 if i in (0, 4) else .5)) * (1 if i < 2 else -1)
            d.ellipse([x - r + o, cy - r, x + r + o, cy + r], fill=(13, 8, 28))

def linea(d, y, w=120):
    d.line([(W // 2 - w * S, y), (W // 2 + w * S, y)], fill=GOLD, width=2 * S); d.regular_polygon((W // 2, y, 9 * S), 4, fill=GOLD)

def pie(d, extra=None):
    if extra: d.text((W // 2, H - 160 * S), extra, font=F("bm", 26), fill=GOLD, anchor="ma")
    d.text((W // 2, H - 118 * S), "@santiagojara.tarot", font=F("bm", 26), fill=DIM, anchor="ma")

def guardar(im, path): im.resize((1080, 1350), Image.LANCZOS).save(path, quality=88, optimize=True)

def tapa(dia, seed, path):
    im, d = fondo(seed); fases(d, 240 * S); volanta(d, "HORÓSCOPO DEL DÍA", 400 * S)
    y = bloque(d, dia["titulo"], F("t", 96), 480 * S, CREAM, maxw=W - 240 * S, lh=1.08); linea(d, y + 40 * S)
    y = bloque(d, "Luna en " + dia["luna"], F("ti", 52), y + 88 * S, SOFT)
    y = bloque(d, dia["tip"], F("b", 36), y + 40 * S, CREAM, maxw=W - 300 * S, lh=1.35)
    bloque(d, "Color del día: " + dia["color"], F("bm", 32), y + 26 * S, GOLD)
    d.text((W // 2, H - 230 * S), "Buscá tu signo  →", font=F("bm", 30), fill=GOLD, anchor="ma"); pie(d); guardar(im, path)

def signo(dia, s, seed, path):
    im, d = fondo(seed); volanta(d, dia["titulo"].upper(), 92 * S)
    cx, cy, r = W // 2, 222 * S, 80 * S
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=GOLD, width=3 * S)
    d.ellipse([cx - r - 13 * S, cy - r - 13 * S, cx + r + 13 * S, cy + r + 13 * S], outline=(110, 90, 60), width=S)
    d.text((cx, cy + 3 * S), s["glifo"] + "\ufe0e", font=F("g", 92), fill=GOLD, anchor="mm")
    d.text((cx, 330 * S), s["nombre"], font=F("t", 80), fill=CREAM, anchor="ma")
    d.text((cx, 426 * S), s["fechas"], font=F("b", 27), fill=DIM, anchor="ma")
    st = F("g", 34); step = 54 * S
    for q in range(5): d.text((cx - step * 2 + q * step, 486 * S), "✦", font=st, fill=GOLD if q < s["energia"] else (86, 70, 60), anchor="mm")
    d.text((cx, 516 * S), s["etiqueta"].upper(), font=F("bs", 22), fill=GOLD, anchor="ma")
    plan = " ".join(s["plan"]); etiq = ("PORQUE SOS " + s["nombre"]).upper()
    def dibujar(k, ok):
        y = bloque(d, s["lead"], F("ti", 38 * k), 572 * S, CREAM, maxw=W - 220 * S, lh=1.26, dibujar=ok)
        y = bloque(d, s["intimo"], F("b", 29 * k), y + 20 * S, SOFT, maxw=W - 230 * S, lh=1.42, dibujar=ok)
        y += 30 * S
        if ok: d.line([(W // 2 - 60 * S, y), (W // 2 + 60 * S, y)], fill=(140, 112, 66), width=S)
        y += 22 * S
        if ok: d.text((W // 2, y), etiq, font=F("bs", 21 * k), fill=GOLD, anchor="ma")
        y = bloque(d, s["alma"], F("ti", 31 * k), y + 36 * S * k, CREAM, maxw=W - 250 * S, lh=1.3, dibujar=ok)
        if plan: y = bloque(d, plan, F("b", 25 * k), y + 22 * S, GOLD, maxw=W - 270 * S, lh=1.34, dibujar=ok)
        return y
    for k in (1.0, .95, .9, .85, .8, .75, .7):  # achica si no entra
        if dibujar(k, False) < H - 196 * S: break
    dibujar(k, True)
    pie(d, "¿Te sentiste identificado? Compartilo y etiquetame"); guardar(im, path)

def cierre(seed, path):
    im, d = fondo(seed); fases(d, 250 * S)
    y = bloque(d, "¿Coincide con tu día?", F("t", 86), 390 * S, CREAM, maxw=W - 240 * S, lh=1.1); linea(d, y + 40 * S); y += 110 * S
    for t in ["Compartí la placa de tu signo en tu historia y etiquetame.", "Mandásela a ese signo que la necesita leer.", "Comentá tu signo y contame cómo arrancó tu día."]:
        d.regular_polygon((150 * S, y + 26 * S, 10 * S), 4, fill=GOLD)
        y = bloque(d, t, F("b", 40), y, CREAM, maxw=W - 330 * S, lh=1.34, x=195 * S) + 40 * S
    bloque(d, "El horóscopo de cada día está en", F("b", 32), y + 30 * S, DIM)
    bloque(d, "santeriaarcanoss.com.ar", F("bs", 38), y + 80 * S, GOLD); pie(d); guardar(im, path)

def slug(t): return t.lower().translate(str.maketrans("áéíóú", "aeiou"))

def main(datos_path, salida):
    for dia in json.load(open(datos_path, encoding="utf-8")):
        f = datetime.date.fromisoformat(dia["fecha"])
        dia["titulo"] = f"{DIAS[f.weekday()].capitalize()} {f.day} de {MESES[f.month - 1]}"
        carpeta = os.path.join(salida, dia["fecha"]); os.makedirs(carpeta, exist_ok=True)
        seed = int(f.strftime("%Y%m%d")); nombres = ["01-tapa.jpg"]
        tapa(dia, seed, os.path.join(carpeta, nombres[0]))
        for i, s in enumerate(dia["signos"]):
            n = f"{i + 2:02d}-{slug(s['nombre'])}.jpg"; nombres.append(n); signo(dia, s, seed + i + 1, os.path.join(carpeta, n))
        nombres.append("14-cierre.jpg"); cierre(seed + 20, os.path.join(carpeta, nombres[-1]))
        texto = [f"Horóscopo del {dia['titulo'][0].lower() + dia['titulo'][1:]} ✨ Luna en {dia['luna']}", dia["tip"],
                 "Deslizá hasta tu signo y fijate cómo viene tu día. Si tenés ascendente, leé también ese.", "¿Te sentiste identificado? Mandásela a esa persona de tu signo que tiene que leerla. 💌",
                 "📲 Compartí la placa de tu signo en tu historia y etiquetame.", "💬 Comentá tu signo y contame si coincide.",
                 "El horóscopo de cada día está en santeriaarcanoss.com.ar",
                 "#horoscopo #horoscopodehoy #signos #astrologia #zodiaco"]
        pub = {"fecha": dia["fecha"], "hora_local": "08:00", "zona": "America/Buenos_Aires",
               "texto_html": "".join(f"<p>{t}</p>" for t in texto),
               "imagenes": [f"{SITIO}/horoscopo/{dia['fecha']}/{n}" for n in nombres]}
        json.dump(pub, open(os.path.join(carpeta, "publicacion.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(carpeta)

if __name__ == "__main__": main(sys.argv[1], sys.argv[2])
