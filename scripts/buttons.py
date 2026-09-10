# Gera os botoes de contato do README (rode a partir da raiz do repo: python scripts/buttons.py)
import re
from PIL import Image, ImageDraw, ImageFont

ARC = "M29.109 341.155C58.1032 255.74 107.715 178.794 173.549 117.133C227.189 66.8938 290.25 28.0647 358.897 2.77636C384.809 -6.76916 412.332 9.27651 419.479 35.9499L468.274 218.057C475.38 244.579 459.453 271.452 434.825 283.591C389.848 305.757 350.72 341.03 323.767 387.715C251.279 513.266 294.297 673.809 419.848 746.296C532.893 811.563 674.303 783.189 754.266 685.244C768.399 667.933 792.973 661.238 812.236 672.566L979.52 766.903C1003.75 780.564 1012.35 811.527 996.284 834.232C954.134 893.815 900.411 944.532 838.145 983.251C761.546 1030.88 674.382 1058.89 584.373 1064.79C494.365 1070.69 404.291 1054.3 322.13 1017.07C239.969 979.846 168.257 922.931 113.346 851.369C58.4349 779.808 22.0195 695.808 7.32609 606.812C-7.36722 517.815 0.114864 426.569 29.109 341.155Z"
SQ  = "M690.474 216.067C690.474 188.453 712.86 166.067 740.474 166.067L920.474 166.067C948.089 166.067 970.474 188.453 970.474 216.067V396.067C970.474 423.682 948.089 446.067 920.474 446.067H740.474C712.86 446.067 690.474 423.682 690.474 396.067V216.067Z"

def parse_path(d):
    toks = re.findall(r'[MCLVHZmclvhz]|-?\d*\.?\d+(?:[eE][-+]?\d+)?', d)
    subs, cur, pt, start, i, cmd = [], [], (0.0, 0.0), (0.0, 0.0), 0, None
    def num():
        nonlocal i
        v = float(toks[i]); i += 1; return v
    while i < len(toks):
        t = toks[i]
        if t.isalpha():
            cmd = t; i += 1
            if cmd in 'Zz':
                if cur: subs.append(cur); cur = []
                pt = start; continue
        if cmd == 'M':
            x, y = num(), num(); pt = start = (x, y); cur = [pt]
        elif cmd == 'L':
            x, y = num(), num(); pt = (x, y); cur.append(pt)
        elif cmd == 'H':
            x = num(); pt = (x, pt[1]); cur.append(pt)
        elif cmd == 'V':
            y = num(); pt = (pt[0], y); cur.append(pt)
        elif cmd == 'C':
            x1,y1,x2,y2,x,y = (num() for _ in range(6)); p0 = pt
            for s in range(1, 49):
                u = s/48; m = 1-u
                cur.append((m*m*m*p0[0]+3*m*m*u*x1+3*m*u*u*x2+u*u*u*x,
                            m*m*m*p0[1]+3*m*m*u*y1+3*m*u*u*y2+u*u*u*y))
            pt = (x, y)
        if cmd in 'Zz': pass
    if cur: subs.append(cur)
    return subs

SS = 3
W, H, R = 700, 92, 18
DARK  = (10, 10, 10, 255)
LIGHT = (245, 245, 245, 255)
LIME  = (174, 250, 14, 255)
HAIRLINE = (255, 255, 255, 46)

# tema corrente do botao sendo desenhado (as funcoes de icone leem daqui)
FG = LIGHT
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

def text_width(d, txt):
    return sum(d.textlength(c, font=FONT) for c in txt) + LS*(len(txt)-1)

def build(name, icon_fn, icon_size, label, fg=LIGHT, bg=DARK, border=HAIRLINE):
    global FG
    FG = fg
    im = Image.new('RGBA', (W*SS, H*SS), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    PAD = 10*SS  # respiro lateral dentro do proprio PNG: os 3 encostam em 33.33% e o gap fica visual
    d.rounded_rectangle([PAD, 0, W*SS-1-PAD, H*SS-1], radius=R*SS, fill=bg,
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
