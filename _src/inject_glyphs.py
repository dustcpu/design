# -*- coding: utf-8 -*-
"""由模板 + seal_glyphs.json 生成最终的样例页面（把字形数据注入占位符）。

以仓库根目录（本文件的上一级）为基准，全部使用相对路径。
"""
import json, io, os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(BASE, "seal-glyphs.json")
TPL  = os.path.join(BASE, "_src", "campus-ink-demo.src.html")
DST  = os.path.join(BASE, "campus-ink-demo.html")

data = json.load(open(SRC, encoding="utf-8"))
js = json.dumps(data, ensure_ascii=False, separators=(',', ':'))

html = io.open(TPL, encoding="utf-8").read()
token = "/*__GLYPHS__*/{}"
if token not in html:
    raise SystemExit("模板里找不到占位符")
io.open(DST, "w", encoding="utf-8", newline="").write(html.replace(token, js))
print("ok ->", DST, os.path.getsize(DST), "bytes;  glyphs:", "".join(data.keys()))
