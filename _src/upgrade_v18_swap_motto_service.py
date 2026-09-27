# -*- coding: utf-8 -*-
"""v18：校训模块与走进中大（招生服务）模块位置互换
校训移到数字里的中大之后、结尾之前
"""
import re

INDEX = r"E:\壁纸大赛\招生概念站\index.html"

with open(INDEX, encoding='utf-8') as f:
    html = f.read()

# 提取校训模块（含注释和前后空行）
motto_start = html.index('<!-- ===== 校训：滚动书写 ===== -->')
motto_end = html.index('</section>', motto_start) + len('</section>')
motto_block = html[motto_start:motto_end]
print(f"校训模块: {len(motto_block)} chars, 位置 {motto_start}-{motto_end}")

# 提取走进中大（招生服务）模块
service_start = html.index('<!-- ===== 招生服务入口 ===== -->')
service_end = html.index('</section>', service_start) + len('</section>')
service_block = html[service_start:service_end]
print(f"走进中大模块: {len(service_block)} chars, 位置 {service_start}-{service_end}")

# 用占位符替换，避免冲突
PLACEHOLDER_MOTTO = '___MOTTO_BLOCK_PLACEHOLDER___'
PLACEHOLDER_SERVICE = '___SERVICE_BLOCK_PLACEHOLDER___'

html = html.replace(motto_block, PLACEHOLDER_MOTTO, 1)
html = html.replace(service_block, PLACEHOLDER_SERVICE, 1)

# 互换
html = html.replace(PLACEHOLDER_MOTTO, service_block, 1)
html = html.replace(PLACEHOLDER_SERVICE, motto_block, 1)

with open(INDEX, 'w', encoding='utf-8') as f:
    f.write(html)

# 验证新顺序
sections = re.findall(r'<!-- ===== (.+?) ===== -->', html)
print("\n新模块顺序:")
for i, s in enumerate(sections):
    print(f"  {i+1}. {s}")

print(f"\nv18 完成")
