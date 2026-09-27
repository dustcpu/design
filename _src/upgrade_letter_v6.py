# -*- coding: utf-8 -*-
"""v6：照片区域鼠标位置控制哪张在最前（扇面效果）"""
import re

INDEX = r"E:\壁纸大赛\招生概念站\index.html"
with open(INDEX, encoding="utf-8") as f:
    html = f.read()

# ========== 1. CSS：去掉单张hover提层级，改为.front class；散开时中间不强制z-index ==========

# 1a. 散开时中间那张去掉 z-index:10（改为默认层级，由.front控制）
css_mid_old = """  .letter-photos:hover .polaroid:nth-child(2){
    transform:translateY(-14px) rotate(0deg) scale(1.08); z-index:10;
    box-shadow:0 14px 36px rgba(0,0,0,.25);
  }"""
css_mid_new = """  .letter-photos:hover .polaroid:nth-child(2){
    transform:translateY(-14px) rotate(0deg) scale(1.08);
    box-shadow:0 14px 36px rgba(0,0,0,.25);
  }"""
assert css_mid_old in html, "未找到散开中间张CSS"
html = html.replace(css_mid_old, css_mid_new, 1)

# 1b. 去掉旧的单张hover规则，替换为 .front class
css_hover_old = """  /* 单张照片hover时移到最前面，方便看清 */
  .letter-photos .polaroid:hover{
    z-index:20;
  }"""
css_hover_new = """  /* 鼠标指向的照片浮到最前（JS控制.front） */
  .polaroid.front{ z-index:20; }"""
assert css_hover_old in html, "未找到旧hover规则"
html = html.replace(css_hover_old, css_hover_new, 1)

# ========== 2. JS：添加照片区域mousemove事件委托（动态渲染的信笺也能生效） ==========
js_anchor = """  })();"""

js_add = """
    // ===== 照片区域：鼠标左右移动时，对应位置的照片浮到最前（扇面效果） =====
    document.addEventListener('mousemove', function(e){
      var box = e.target.closest('.letter-photos');
      if(!box) return;
      var imgs = box.querySelectorAll('.polaroid');
      if(imgs.length < 2) return;
      var r = box.getBoundingClientRect();
      var ratio = (e.clientX - r.left) / r.width;
      var idx = ratio < 0.33 ? 0 : (ratio < 0.66 ? 1 : 2);
      imgs.forEach(function(el, i){ el.classList.toggle('front', i === idx); });
    });
    document.addEventListener('mouseout', function(e){
      var box = e.target.closest('.letter-photos');
      if(box && e.relatedTarget && !box.contains(e.relatedTarget)){
        box.querySelectorAll('.polaroid').forEach(function(el){ el.classList.remove('front'); });
      }
    });
  })();"""

assert js_anchor in html, "未找到 IIFE 结束锚点"
html = html.replace(js_anchor, js_add, 1)

# 保存
with open(INDEX, "w", encoding="utf-8") as f:
    f.write(html)
print(f"v6 改进完成，index.html 大小: {len(html.encode('utf-8'))} bytes")
