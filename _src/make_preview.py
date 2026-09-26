# -*- coding: utf-8 -*-
"""生成「五校园」仿篆书字形预览图：五列竖排，浅棕宣纸底 + 墨绿笔画。"""
import os, sys, importlib.util
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("sg", os.path.join(HERE, "seal_glyphs.py"))
sg = importlib.util.module_from_spec(spec); sys.modules["sg"] = sg
spec.loader.exec_module(sg)

PAPER = (245, 241, 232)
INK = (31, 77, 56)
CS = 112                            # 字径
CH = int(CS * 1.4545)               # 单字高（与字形 viewBox 同比）
GAP = 4                             # 字距
PAD_X, PAD_TOP = 46, 54
LABEL_H = 86

COLS = [('南校园', '广州 · 海珠'), ('东校园', '广州 · 大学城'), ('北校园', '广州 · 中山医'),
        ('深圳校区', '深圳 · 光明'), ('珠海校区', '珠海 · 唐家湾')]

maxlen = max(len(c[0]) for c in COLS)
W = PAD_X * 2 + len(COLS) * CS + (len(COLS) - 1) * 30
H = PAD_TOP + maxlen * (CH + GAP) + LABEL_H
im = Image.new('RGB', (W, H), PAPER)
dr = ImageDraw.Draw(im)

lab = ImageFont.truetype("C:/Windows/Fonts/simsun.ttc", 19)
cap = ImageFont.truetype("C:/Windows/Fonts/simsun.ttc", 15)

for i, (name, place) in enumerate(COLS):
    ox = PAD_X + i * (CS + 30)
    for j, ch in enumerate(name):
        gi = sg.glyph_image(sg.CHARS[ch], CS, ss=4, fill=INK, bg=PAPER)
        # glyph_image 输出的是 1000 画布（字格在中间），裁出字格再贴
        gx = int(sg.GX * CS / 1000.0)
        gy = int(sg.GY * CS / 1000.0)
        gw = int(sg.GW * CS / 1000.0)
        gh = int(sg.GH * CS / 1000.0)
        pad = int(sg.STROKE_W * CS / 1000.0)
        x0 = max(0, gx - pad); y0 = max(0, gy - pad)
        cell = gi.crop((x0, y0, gx + gw + pad, gy + gh + pad))
        im.paste(cell, (ox - pad + (x0 - (gx - pad)), PAD_TOP + j * (CH + GAP) - pad + (y0 - (gy - pad))))
    dr.text((ox + CS / 2, PAD_TOP + maxlen * (CH + GAP) + 26), place,
            font=lab, fill=(107, 86, 60), anchor='ma')

im.save(os.path.join(HERE, 'seal-glyphs-preview.png'))
print('saved', im.size)
