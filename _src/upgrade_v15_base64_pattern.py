# -*- coding: utf-8 -*-
"""v15：用base64编码的SVG回纹替换，彻底解决data URI编码问题
回纹设计：经典回字纹，四角各一个，深绿色，线条加粗，pattern适中
"""
import base64

INDEX = r"E:\壁纸大赛\招生概念站\index.html"

# 生成回纹SVG：经典"回"字纹，四角各一个
# 48x48 viewBox，每个回纹占角落约22x22
svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 48 48">
  <g fill="none" stroke="#2F5D46" stroke-width="2.4" stroke-opacity="0.45" stroke-linejoin="miter">
    <!-- 左上角回纹 -->
    <path d="M3 3h18v9H12v9H3z"/>
    <!-- 右下角回纹 -->
    <path d="M45 45H27V36h9V27h18z"/>
    <!-- 左下角回纹 -->
    <path d="M3 45h9v-9h9V27H3z"/>
    <!-- 右上角回纹 -->
    <path d="M45 3H36v9H27v9h18z"/>
  </g>
</svg>'''

# base64编码
svg_b64 = base64.b64encode(svg.encode('utf-8')).decode('ascii')
data_uri = f"url(data:image/svg+xml;base64,{svg_b64})"

print(f"SVG base64长度: {len(svg_b64)}")
print(f"data URI前60字: {data_uri[:60]}...")

# 读取文件
with open(INDEX, encoding='utf-8') as f:
    html = f.read()

# 替换body的background-image和background-size
import re

# 替换background-image（匹配当前的红色渐变）
html = re.sub(
    r"background-image:linear-gradient\([^)]*\);",
    f"background-image:{data_uri};",
    html,
    count=1
)

# 替换background-size为48px
html = re.sub(
    r"background-size:\d+px \d+px;",
    "background-size:48px 48px;",
    html,
    count=1
)

# 保存
with open(INDEX, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nv15 完成，index.html 大小: {len(html.encode('utf-8'))} bytes")
print("回纹参数：48x48 pattern, 2.4px线条, 0.45透明度, 深绿色#2F5D46")
