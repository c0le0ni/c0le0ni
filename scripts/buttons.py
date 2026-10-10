# Gera os botoes de contato do README (rode a partir da raiz do repo: python scripts/buttons.py)
import re
from PIL import Image, ImageDraw, ImageFont

ARC = "M29.109 341.155C58.1032 255.74 107.715 178.794 173.549 117.133C227.189 66.8938 290.25 28.0647 358.897 2.77636C384.809 -6.76916 412.332 9.27651 419.479 35.9499L468.274 218.057C475.38 244.579 459.453 271.452 434.825 283.591C389.848 305.757 350.72 341.03 323.767 387.715C251.279 513.266 294.297 673.809 419.848 746.296C532.893 811.563 674.303 783.189 754.266 685.244C768.399 667.933 792.973 661.238 812.236 672.566L979.52 766.903C1003.75 780.564 1012.35 811.527 996.284 834.232C954.134 893.815 900.411 944.532 838.145 983.251C761.546 1030.88 674.382 1058.89 584.373 1064.79C494.365 1070.69 404.291 1054.3 322.13 1017.07C239.969 979.846 168.257 922.931 113.346 851.369C58.4349 779.808 22.0195 695.808 7.32609 606.812C-7.36722 517.815 0.114864 426.569 29.109 341.155Z"
SQ  = "M690.474 216.067C690.474 188.453 712.86 166.067 740.474 166.067L920.474 166.067C948.089 166.067 970.474 188.453 970.474 216.067V396.067C970.474 423.682 948.089 446.067 920.474 446.067H740.474C712.86 446.067 690.474 423.682 690.474 396.067V216.067Z"

# Discord do simple-icons (viewBox 24x24): o contorno e os dois olhos
DISCORD = open(__file__.replace('buttons.py', 'discord.path')).read().strip()

NUM = re.compile(r'-?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?')

def parse_path(d):
    # M L H V C Z, absolutos e relativos. Arco vira reta ate o ponto final: nos
    # icones daqui os arcos sao cantos minusculos, e a diferenca nao chega a um pixel.
    subs, cur, i, n, cmd = [], [], 0, len(d), None
    x = y = sx = sy = 0.0
    def skip():
        nonlocal i
        while i < n and d[i] in ' ,\t\r\n': i += 1
    def num():
        nonlocal i
        skip(); m = NUM.match(d, i); i = m.end(); return float(m.group())
    def flag():
        nonlocal i
        skip(); i += 1; return d[i-1] == '1'
    def add(p):
        if not cur: cur.append((sx, sy))
        cur.append(p)
    while True:
        skip()
        if i >= n: break
        if d[i].isalpha():
            cmd = d[i]; i += 1
        C = cmd.upper()
        ox, oy = (x, y) if cmd.islower() else (0.0, 0.0)
        if C == 'Z':
            if cur: subs.append(cur); cur = []
            x, y = sx, sy
        elif C == 'M':
            if cur: subs.append(cur)
            x, y = ox + num(), oy + num(); sx, sy = x, y; cur = [(x, y)]
            cmd = 'l' if cmd == 'm' else 'L'
        elif C == 'L':
            x, y = ox + num(), oy + num(); add((x, y))
        elif C == 'H':
            x = ox + num(); add((x, y))
        elif C == 'V':
            y = oy + num(); add((x, y))
        elif C == 'A':
            num(); num(); num(); flag(); flag()
            x, y = ox + num(), oy + num(); add((x, y))
        elif C == 'C':
            x1, y1, x2, y2 = ox + num(), oy + num(), ox + num(), oy + num()
            ex, ey = ox + num(), oy + num(); p0 = (x, y)
            for s in range(1, 49):
                u = s/48; m = 1-u
                add((m*m*m*p0[0]+3*m*m*u*x1+3*m*u*u*x2+u*u*u*ex,
                     m*m*m*p0[1]+3*m*m*u*y1+3*m*u*u*y2+u*u*u*ey))
            x, y = ex, ey
    if cur: subs.append(cur)
    return subs

SS = 3
W, H, R = 700, 112, 18
PAD, VPAD = 10, 10  # respiro dentro do PNG: os botoes encostam (dois por linha, em 50%) e o vao aparece
DARK  = (10, 10, 10, 255)
LIGHT = (245, 245, 245, 255)
LIME  = (174, 250, 14, 255)
HAIRLINE = (255, 255, 255, 46)

# tema corrente do botao sendo desenhado (as funcoes de icone leem daqui)
FG, BG = LIGHT, DARK
FONT = ImageFont.truetype('C:/Windows/Fonts/seguisb.ttf', 27*SS)
LS = 2.4*SS

def logo_coleoni(d, cx, cy, s):
    # simbolo oficial, monocromatico branco (arco + quadrado)
    sc = s/1066.0
    ox, oy = cx - (1005*sc)/2, cy - s/2
    for path in (ARC, SQ):
        for sub in parse_path(path):
            d.polygon([(ox + x*sc, oy + y*sc) for x, y in sub], fill=FG)

def icon_mail(d, cx, cy, s):
    lw = max(2, int(0.075*s)); w, h = s, s*0.74
    d.rounded_rectangle([cx-w/2, cy-h/2, cx+w/2, cy+h/2], radius=s*0.13, outline=FG, width=lw)
    d.line([(cx-w/2+lw*1.4, cy-h/2+lw*1.4), (cx, cy+h*0.11), (cx+w/2-lw*1.4, cy-h/2+lw*1.4)],
           fill=FG, width=lw, joint='curve')

def icon_instagram(d, cx, cy, s):
    lw = max(2, int(0.082*s))
    d.rounded_rectangle([cx-s/2, cy-s/2, cx+s/2, cy+s/2], radius=s*0.29, outline=FG, width=lw)
    r = s*0.215
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=FG, width=lw)
    dr = s*0.055; dx, dy = cx+s*0.265, cy-s*0.265
    d.ellipse([dx-dr, dy-dr, dx+dr, dy+dr], fill=FG)

def icon_discord(d, cx, cy, s):
    # o contorno no FG; os olhos sao furos, pintados com o fundo
    sc = s/24.0
    subs = parse_path(DISCORD)
    ys = [y for x, y in subs[0]]
    oy = cy - (min(ys) + max(ys))/2*sc
    for k, sub in enumerate(subs):
        d.polygon([(cx - 12*sc + x*sc, oy + y*sc) for x, y in sub], fill=FG if k == 0 else BG)

def text_width(d, txt):
    return sum(d.textlength(c, font=FONT) for c in txt) + LS*(len(txt)-1)

def build(name, icon_fn, icon_size, label, fg=LIGHT, bg=DARK, border=HAIRLINE):
    global FG, BG
    FG, BG = fg, bg
    im = Image.new('RGBA', (W*SS, H*SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    px, py = PAD*SS, VPAD*SS
    d.rounded_rectangle([px, py, W*SS-1-px, H*SS-1-py], radius=R*SS, fill=bg,
                        outline=border, width=max(1, int(1.5*SS)))
    isz = icon_size*SS
    gap = 17*SS
    tw = text_width(d, label)
    total = isz + gap + tw
    x = (W*SS - total)/2
    cy = H*SS/2
    icon_fn(d, x + isz/2, cy, isz)
    tx = x + isz + gap
    for ch in label:
        d.text((tx, cy), ch, font=FONT, fill=fg, anchor='lm')
        tx += d.textlength(ch, font=FONT) + LS
    im = im.resize((W, H), Image.LANCZOS)
    p = 'assets/buttons/%s.png' % name
    im.save(p, 'PNG', optimize=True)
    print('%-11s %sx%s  %s bytes' % (name, W, H, im.size and __import__('os').path.getsize(p)))

build('website',   logo_coleoni,    40, 'COLEONI.COM', fg=DARK, bg=LIME, border=LIME)
build('email',     icon_mail,       38, 'MICHEL@COLEONI.COM')
build('instagram', icon_instagram,  38, '@COLEONI.DEV')
build('discord',   icon_discord,    40, 'DISCORD')
