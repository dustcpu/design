# -*- coding: utf-8 -*-
"""v16：回纹调淡 - 降低透明度、变细线条、放大pattern"""
import base64, re

INDEX = r"E:\壁纸大赛\招生概念站\index.html"

# 淡雅回纹：56x56 pattern, 1.6px线条, 0.15透明度
svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="56" height="56" viewBox="0 0 56 56">
  <g fill="none" stroke="#2F5D46" stroke-width="1.6" stroke-opacity="0.15" stroke-linejoin="miter">
    <path d="M4 4h20v10H14v10H4z"/>
    <path d="M52 52H32V42h10V32h20z"/>
    <path d="M4 52h10v-10h10V32H4z"/>
    <path d="M52 4H42v10H32v10h20z"/>
  </g>
</svg>'''

svg_b64 = base64.b64encode(svg.encode('utf-8')).decode('ascii')
data_uri = f"url(data:image/svg+xml;base64,{svg_b64})"

with open(INDEX, encoding='utf-8') as f:
    html = f.read()

html = re.sub(r"background-image:url\(data:image/svg\+xml;base64,[^)]*\);", f"background-image:{data_uri};", html, count=1)
html = re.sub(r"background-size:\d+px \d+px;", "background-size:56px 56px;", html, count=1)

with open(INDEX, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"v16 完成，回纹调淡：56px pattern, 1.6px线条, 0.15透明度")
