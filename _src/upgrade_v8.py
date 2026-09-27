# -*- coding: utf-8 -*-
"""v8：背景纹饰 + 校区重排（南在中间） + 学院标签式排版"""
import re

INDEX = r"E:\壁纸大赛\招生概念站\index.html"
with open(INDEX, encoding="utf-8") as f:
    html = f.read()

# ========== 1. 背景纹饰：body 加极淡中式回纹 SVG pattern ==========
body_old = """  body{
    background:var(--paper);
    color:var(--ink);"""

# 中式回纹 pattern（极淡，仅作底纹）
huiwen_svg = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='80' height='80' viewBox='0 0 80 80'%3E"
    "%3Cg fill='none' stroke='%232F5D46' stroke-width='1'%3E"
    "%3Cpath d='M8 8h28v14H22v14H8z'/%3E"
    "%3Cpath d='M72 72H44V58h14V44h14z'/%3E"
    "%3Cpath d='M8 72h14v-14h14V44H8z' opacity='.5'/%3E"
    "%3Cpath d='M72 8H58v14H44v14h28z' opacity='.5'/%3E"
    "%3C/g%3E%3C/svg%3E"
)

body_new = """  body{
    background:var(--paper);
    background-image:url(""" + huiwen_svg + """);
    background-size:80px 80px;
    background-repeat:repeat;
    color:var(--ink);"""

assert body_old in html, "未找到 body CSS"
html = html.replace(body_old, body_new, 1)
print("背景回纹已添加")

# ========== 2. 校区排序：珠海→北校→南校(中)→东校→深圳 ==========
# 提取 CAMPUS_DATA 数组
m = re.search(r'(var CAMPUS_DATA = \[)(.*?)(\n  \];)', html, re.DOTALL)
assert m, "未找到 CAMPUS_DATA"
array_content = m.group(2)

# 按对象分割（每个对象以 \n    { 开头）
objects = re.findall(r'\n    \{.*?\n    \},?', array_content, re.DOTALL)
assert len(objects) == 5, f"期望5个校区对象，实际{len(objects)}"

# 原顺序：0南 1东 2北 3深圳 4珠海
# 新顺序：4珠海 → 2北 → 0南 → 1东 → 3深圳
new_order = [objects[4], objects[2], objects[0], objects[1], objects[3]]
# 确保最后一个对象没有逗号（如果有的话去掉，然后前四个加逗号）
new_objects = []
for i, obj in enumerate(new_order):
    obj = obj.rstrip()
    if obj.endswith(','):
        obj = obj[:-1]
    if i < 4:
        obj = obj + ','
    new_objects.append(obj)

new_array_content = '\n'.join(new_objects)
html = html[:m.start(2)] + new_array_content + html[m.end(2):]
print("校区顺序已重排：珠海→北校→南校→东校→深圳")

# ========== 3. 学院标签式排版 ==========
# 3a. CSS：替换 .letter-colleges 样式
colleges_css_old = """  .letter-colleges{
    margin-top:14px; padding-top:12px; border-top:1px dashed rgba(139,58,46,.2);
    font-size:11.5px; line-height:1.9; color:#6b7d6f;
  }
  .letter-colleges strong{color:var(--brick); font-weight:700; margin-right:6px}"""

colleges_css_new = """  .letter-colleges{
    margin-top:14px; padding-top:12px; border-top:1px dashed rgba(139,58,46,.2);
  }
  .college-label{
    font-size:10.5px; letter-spacing:.25em; color:var(--brick); font-weight:700;
    margin-bottom:9px; display:block;
  }
  .college-tags{display:flex; flex-wrap:wrap; gap:6px 8px}
  .college-tag{
    font-size:10.5px; font-family:'Noto Serif SC',serif;
    padding:3px 10px; border:1px solid rgba(47,93,70,.25); border-radius:2px;
    color:var(--green); background:rgba(255,254,248,.6);
    transition:all .3s ease; line-height:1.5;
  }
  .college-tag:hover{
    border-color:var(--brick); color:var(--brick);
    background:rgba(139,58,46,.06);
  }"""

assert colleges_css_old in html, "未找到学院CSS"
html = html.replace(colleges_css_old, colleges_css_new, 1)

# 3b. HTML：替换学院容器结构
colleges_html_old = """        <div class="letter-colleges"><strong>下设院系</strong><span class="colleges-list"></span></div>"""
colleges_html_new = """        <div class="letter-colleges">
          <span class="college-label">下设院系</span>
          <div class="college-tags"></div>
        </div>"""
assert colleges_html_old in html, "未找到学院HTML"
html = html.replace(colleges_html_old, colleges_html_new, 1)

# 3c. JS：把 colleges 字符串分割成标签
colleges_js_old = """      letter.querySelector('.colleges-list').textContent = d.colleges;"""
colleges_js_new = """      var tagsBox = letter.querySelector('.college-tags');
      tagsBox.innerHTML = '';
      d.colleges.split('·').forEach(function(name){
        name = name.trim();
        if(!name) return;
        var tag = document.createElement('span');
        tag.className = 'college-tag';
        tag.textContent = name;
        tagsBox.appendChild(tag);
      });"""
assert colleges_js_old in html, "未找到学院JS"
html = html.replace(colleges_js_old, colleges_js_new, 1)

print("学院标签式排版已完成")

# 保存
with open(INDEX, "w", encoding="utf-8") as f:
    f.write(html)
print(f"v8 改进完成，index.html 大小: {len(html.encode('utf-8'))} bytes")
