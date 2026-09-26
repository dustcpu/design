# -*- coding: utf-8 -*-
"""放大个别字做细节核对：4 列 = 宋体 / 仿篆 / 米字格上的仿篆 / 镜像叠加"""
import os, sys, importlib.util
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("sg", os.path.join(HERE, "seal_glyphs.py"))
sg = importlib.util.module_from_spec(spec); sys.modules["sg"] = sg
spec.loader.exec_module(sg)

want = sys.argv[1:] if len(sys.argv) > 1 else ['南', '校', '深', '珠']
C = 430
PAD = 16
ref = ImageFont.truetype("C:/Windows/Fonts/simsun.ttc", int(C * 0.86))
ink = (31, 77, 56)
img = Image.new('RGB', (PAD + 4 * (C + PAD), PAD + len(want) * (C + PAD)), (255, 255, 255))
dr = ImageDraw.Draw(img)

for i, c in enumerate(want):
    y = PAD + i * (C + PAD)
    xs = [PAD + j * (C + PAD) for j in range(4)]
    for x in xs:
        dr.rectangle([x, y, x + C, y + C], outline=(220, 220, 220))
    dr.text((xs[0] + C / 2, y + C / 2), c, font=ref, fill=(160, 160, 160), anchor='mm')
    sg.draw_glyph(dr, sg.CHARS[c], xs[1], y, C, sg.STROKE_W)
    # 米字格
    g = sg.GX * C / 1000.0 + xs[2]
    gy0 = sg.GY * C / 1000.0 + y
    gy1 = (sg.GY + sg.GH) * C / 1000.0 + y
    gx0 = sg.GX * C / 1000.0 + xs[2]
    gx1 = (sg.GX + sg.GW) * C / 1000.0 + xs[2]
    dr.rectangle([gx0, gy0, gx1, gy1], outline=(235, 200, 210))
    dr.line([gx0, (gy0 + gy1) / 2, gx1, (gy0 + gy1) / 2], fill=(240, 214, 220))
    dr.line([(gx0 + gx1) / 2, gy0, (gx0 + gx1) / 2, gy1], fill=(240, 214, 220))
    sg.draw_glyph(dr, sg.CHARS[c], xs[2], y, C, sg.STROKE_W)
    # 镜像叠加
    m2 = Image.new('RGB', (C, C), (255, 255, 255))
    sg.draw_glyph(ImageDraw.Draw(m2), sg.CHARS[c], 0, 0, C, sg.STROKE_W)
    mm = Image.new('L', (C, C), 0)
    sg.draw_glyph(ImageDraw.Draw(mm), sg.CHARS[c], 0, 0, C, sg.STROKE_W, fill=255)
    mm = mm.transpose(Image.FLIP_LEFT_RIGHT)
    red = Image.new('RGB', (C, C), (255, 255, 255))
    red.paste(Image.new('RGB', (C, C), (240, 90, 80)), (0, 0),
              mm.point(lambda v: 110 if v > 128 else 0))
    img.paste(Image.blend(m2, red, 0.5), (xs[3], y))

img.save(os.path.join(HERE, 'zoom_check.png'))
print('saved', img.size)
