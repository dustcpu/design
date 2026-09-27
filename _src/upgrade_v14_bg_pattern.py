# -*- coding: utf-8 -*-
"""v14：修复背景回纹不可见问题
1. background简写改为background-color，避免覆盖background-image
2. 回纹线条加粗 1.4→2.5
3. pattern缩小 64→52，更密集
4. 回纹路径放大，更饱满
5. 颜色用稍深的墨绿，带轻微透明度
"""
import re

INDEX = r"E:\壁纸大赛\招生概念站\index.html"
with open(INDEX, encoding="utf-8") as f:
    html = f.read()

# 旧的body背景规则
old_body = """  body{
    background:var(--paper);
    background-image:url(data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='64' height='64' viewBox='0 0 64 64'%3E%3Cg fill='none' stroke='%232F5D46' stroke-width='1.4'%3E%3Cpath d='M6 6h24v12H18v12H6z'/%3E%3Cpath d='M58 58H34V46h12V34h12z'/%3E%3Cpath d='M6 58h12v-12h12V34H6z'/%3E%3Cpath d='M58 6H46v12H34v12h24z'/%3E%3C/g%3E%3C/svg%3E);
    background-size:64px 64px;
    background-repeat:repeat;"""

# 新的body背景规则：更粗、更密、更饱满的回纹
# 回纹用经典的"回"字纹，四角各一个，线条加粗到2.5，pattern 52x52
new_body = """  body{
    background-color:var(--paper);
    background-image:url(data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='52' height='52' viewBox='0 0 52 52'%3E%3Cg fill='none' stroke='%232F5D46' stroke-width='2.2' stroke-opacity='0.35'%3E%3Cpath d='M4 4h20v10H14v10H4z'/%3E%3Cpath d='M48 48H28V38h10V28h10z'/%3E%3Cpath d='M4 48h10v-10h10V28H4z'/%3E%3Cpath d='M48 4H38v10H28v10h20z'/%3E%3C/g%3E%3C/svg%3E);
    background-size:52px 52px;
    background-repeat:repeat;"""

if old_body in html:
    html = html.replace(old_body, new_body, 1)
    print("已修复背景回纹")
else:
    print("未找到旧的body背景规则，尝试用正则替换...")
    # 用正则替换
    pattern = r"  body\{[^}]*background-image:url\(data:image/svg\+xml[^)]*\);[^}]*\}"
    match = re.search(pattern, html, re.DOTALL)
    if match:
        html = html[:match.start()] + new_body + html[match.end():]
        print("正则替换成功")
    else:
        print("正则也没找到，需要手动检查")

with open(INDEX, "w", encoding="utf-8") as f:
    f.write(html)
print(f"v14 完成，index.html 大小: {len(html.encode('utf-8'))} bytes")
