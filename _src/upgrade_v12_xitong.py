# -*- coding: utf-8 -*-
"""v12：系统科学与工程学院加回南校园（2023年已搬迁至南校园）"""
INDEX = r"E:\壁纸大赛\招生概念站\index.html"
with open(INDEX, encoding="utf-8") as f:
    html = f.read()

old = "colleges:'中国语言文学系 · 历史学系 · 哲学系 · 社会学与人类学学院 · 岭南学院 · 外国语学院 · 数学学院 · 物理学院 · 化学学院 · 地理科学与规划学院 · 生命科学学院 · 艺术学院 · 博雅学院(通识教育部)'"
new = "colleges:'中国语言文学系 · 历史学系 · 哲学系 · 社会学与人类学学院 · 岭南学院 · 外国语学院 · 数学学院 · 物理学院 · 化学学院 · 地理科学与规划学院 · 生命科学学院 · 艺术学院 · 系统科学与工程学院 · 博雅学院(通识教育部)'"

if old in html:
    html = html.replace(old, new, 1)
    print("已将系统科学与工程学院加回南校园")
else:
    print("未找到旧字符串")

with open(INDEX, "w", encoding="utf-8") as f:
    f.write(html)
print(f"v12 完成，index.html 大小: {len(html.encode('utf-8'))} bytes")
