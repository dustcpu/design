# -*- coding: utf-8 -*-
"""校形工具：① 宋体参照 ② 仿篆 ③ 镜像叠加（看对称）+ 打印对称度分数。"""
import os, importlib.util, sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("sg", os.path.join(HERE, "seal_glyphs.py"))
sg = importlib.util.module_from_spec(spec); sys.modules["sg"] = sg
spec.loader.exec_module(sg)

CELL, PAD = 260, 18
seq = sg.SEQ
ref = ImageFont.truetype("C:/Windows/Fonts/simsun.ttc", int(CELL * 0.82))

img = Image.new('RGB', (PAD + 3 * (CELL + PAD), PAD + len(seq) * (CELL + PAD)), (255, 255, 255))
dr = ImageDraw.Draw(img)
report = []

for i, c in enumerate(seq):
    y = PAD + i * (CELL + PAD)
    xs = [PAD, PAD + (CELL + PAD), PAD + 2 * (CELL + PAD)]
    for x in xs:
        dr.rectangle([x, y, x + CELL, y + CELL], outline=(222, 222, 222))
    dr.text((xs[0] + CELL / 2, y + CELL / 2), c, font=ref, fill=(158, 158, 158), anchor='mm')

    img.paste(sg.glyph_image(sg.CHARS[c], CELL), (xs[1], y))

    m = sg.glyph_mask(sg.CHARS[c], CELL)
    base = sg.glyph_image(sg.CHARS[c], CELL).convert('RGB')
    red = Image.new('RGB', (CELL, CELL), (255, 255, 255))
    red.paste(Image.new('RGB', (CELL, CELL), (242, 96, 86)), (0, 0),
              m.transpose(Image.FLIP_LEFT_RIGHT).point(lambda v: 105 if v > 128 else 0))
    img.paste(Image.blend(base, red, 0.5), (xs[2], y))

    px = list(m.getdata())
    def at(a, b): return px[a * CELL + b] > 128
    inter = union = 0
    for a in range(CELL):
        for b in range(CELL):
            p, q = at(a, b), at(a, CELL - 1 - b)
            if p and q: inter += 1
            if p or q: union += 1
    lr = inter / union if union else 0
    inter = union = 0
    for a in range(CELL):
        for b in range(CELL):
            p, q = at(a, b), at(CELL - 1 - a, b)
            if p and q: inter += 1
            if p or q: union += 1
    ud = inter / union if union else 0
    ink = sum(1 for v in px if v > 128) / float(CELL * CELL)

    # 满格度：字形实际外接框 / 字格
    rows = [a for a in range(CELL) if any(at(a, b) for b in range(CELL))]
    cols = [b for b in range(CELL) if any(at(a, b) for a in range(CELL))]
    gx0 = sg.GX * CELL / 1000; gw = sg.GW * CELL / 1000
    gy0 = sg.GY * CELL / 1000; gh = sg.GH * CELL / 1000
    fillX = (cols[-1] - cols[0]) / gw
    fillY = (rows[-1] - rows[0]) / gh
    offX = (cols[0] + cols[-1]) / 2.0 - (gx0 + gw / 2)
    offY = (rows[0] + rows[-1]) / 2.0 - (gy0 + gh / 2)
    report.append((c, lr, ud, ink, fillX, fillY, offX, offY))

img.save(os.path.join(HERE, 'seal_check.png'))
print('%-3s %7s %7s %7s %7s %7s %7s %7s' % ('字', '左右IoU', '上下IoU', '墨占比', '横向满', '纵向满', '横偏心', '纵偏心'))
for r in report:
    print('%-3s %7.3f %7.3f %7.3f %7.3f %7.3f %7.1f %7.1f' % r)
