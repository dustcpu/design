# -*- coding: utf-8 -*-
"""v11：严格按用户参考图修正学院列表（去掉工学院/马院/系统学院等）"""
import re

INDEX = r"E:\壁纸大赛\招生概念站\index.html"
with open(INDEX, encoding="utf-8") as f:
    html = f.read()

# 南校园（13个，人文社科+基础理科）
old_nan = "colleges:'中国语言文学系 · 历史学系 · 哲学系 · 社会学与人类学学院 · 博雅学院 · 岭南学院 · 外国语学院 · 马克思主义学院 · 数学学院 · 物理学院 · 化学学院 · 地理科学与规划学院 · 生命科学学院 · 艺术学院'"
new_nan = "colleges:'中国语言文学系 · 历史学系 · 哲学系 · 社会学与人类学学院 · 岭南学院 · 外国语学院 · 数学学院 · 物理学院 · 化学学院 · 地理科学与规划学院 · 生命科学学院 · 艺术学院 · 博雅学院(通识教育部)'"

# 东校园（10个，社科+工科，去掉工学院和系统学院，电信加微电子学院）
old_dong = "colleges:'法学院 · 政治与公共事务管理学院 · 管理学院 · 心理学系 · 新闻传播学院 · 信息管理学院 · 工学院 · 材料科学与工程学院 · 电子与信息工程学院 · 计算机学院 · 环境科学与工程学院 · 系统科学与工程学院'"
new_dong = "colleges:'法学院 · 政治与公共事务管理学院 · 管理学院 · 心理学系 · 新闻传播学院 · 信息管理学院 · 材料科学与工程学院 · 电子与信息工程学院（微电子学院） · 计算机学院 · 环境科学与工程学院'"

for name, old, new in [("南校园", old_nan, new_nan), ("东校园", old_dong, new_dong)]:
    if old in html:
        html = html.replace(old, new, 1)
        print(f"已替换 {name}")
    else:
        print(f"未找到 {name} 的旧字符串")

with open(INDEX, "w", encoding="utf-8") as f:
    f.write(html)
print(f"\nv11 完成，index.html 大小: {len(html.encode('utf-8'))} bytes")
