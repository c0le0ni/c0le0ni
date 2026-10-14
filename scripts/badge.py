# Gera a tag "open source" da tabela de projetos (rode a partir da raiz do repo: python scripts/badge.py)
from PIL import Image, ImageDraw, ImageFont

SS = 4            # o PNG sai 4x maior que a exibicao (height="18" no README)
H = 18*SS
PAD = 7*SS
TEXT = 'open source'
DARK = (10, 10, 10, 255)
LIME = (174, 250, 14, 255)
FONT = ImageFont.truetype('C:/Windows/Fonts/seguisb.ttf', 11*SS)

l, t, r, b = FONT.getbbox(TEXT)
W = (r - l) + 2*PAD
img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
d.rounded_rectangle((0, 0, W-1, H-1), radius=5*SS, fill=LIME)
# centraliza pela caixa real das letras, nao pela linha de base
d.text((PAD - l, (H - (b - t))/2 - t), TEXT, font=FONT, fill=DARK)
img.save('assets/projects/open-source.png')
print(W//SS, 'x', H//SS)
