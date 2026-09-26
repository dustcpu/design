# -*- coding: utf-8 -*-
"""构建 campus-ink-ligen-demo.html（仓库版，全部相对路径）。

流程：从 _src/campus-ink-ligen-demo.v3-anim.bak.html 提取超长的
GLYPH_IMAGES base64 行（约 98,070 字符，无法直接手工编辑），
注入 _src/ligen-lite.src.html 模板的占位行 __GLYPH_IMAGES_LINE__，
输出到仓库根目录的 campus-ink-ligen-demo.html。

用法：python build_lite.py
"""
import io
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
BAK = os.path.join(BASE, "_src", "campus-ink-ligen-demo.v3-anim.bak.html")
TPL = os.path.join(BASE, "_src", "ligen-lite.src.html")
DST = os.path.join(BASE, "demos", "campus-ink-ligen-demo.html")

html = io.open(BAK, encoding="utf-8").read()
m = re.search(r"^\s*var GLYPH_IMAGES = .*$", html, re.M)
if not m:
    raise SystemExit("备份文件里找不到 GLYPH_IMAGES 行")
line = m.group(0).strip()

tpl = io.open(TPL, encoding="utf-8").read()
if "__GLYPH_IMAGES_LINE__" not in tpl:
    raise SystemExit("模板里找不到占位行")
out = tpl.replace("__GLYPH_IMAGES_LINE__", line)

io.open(DST, "w", encoding="utf-8", newline="").write(out)
print("glyph line:", len(line), "chars")
print("ok ->", os.path.relpath(DST, BASE), os.path.getsize(DST), "bytes")
