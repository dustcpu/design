# -*- coding: utf-8 -*-
"""v4：修复照片hover层级 + 印章改用隶书字"""
import re

INDEX = r"E:\壁纸大赛\招生概念站\index.html"
with open(INDEX, encoding="utf-8") as f:
    html = f.read()

# ========== 1. CSS：在散开规则后添加单张hover拎出（高优先级） ==========
css_anchor = """  .polaroid .ph-cap{
    font-size:9.5px; color:#A89B80; text-align:center; margin-top:6px;
    font-family:'Noto Serif SC',serif; letter-spacing:.08em;
  }"""

css_add = css_anchor + """
  /* 单张照片hover时拎到最前（优先级高于散开时的z-index） */
  .letter-photos .polaroid:hover{
    z-index:20;
    transform:translateY(-18px) rotate(0deg) scale(1.08);
    box-shadow:0 18px 44px rgba(0,0,0,.3);
  }"""

assert css_anchor in html, "未找到 .ph-cap 锚点"
html = html.replace(css_anchor, css_add, 1)

# ========== 2. SVG defs：添加隶书字变红 filter ==========
filter_anchor = """    <filter id="sealWear" x="-10%" y="-10%" width="120%" height="120%">
      <feTurbulence type="fractalNoise" baseFrequency="0.06" numOctaves="3" seed="7" result="noise"/>
      <feColorMatrix in="noise" type="matrix" values="0 0 0 0 0.55  0 0 0 0 0.23  0 0 0 0 0.18  0 0 0 -0.7 0.85" result="wearMask"/>
      <feComposite in="SourceGraphic" in2="wearMask" operator="out" result="worn"/>
      <feComposite in="worn" in2="SourceGraphic" operator="over"/>
    </filter>"""

filter_add = filter_anchor + """
    <!-- 把隶书黑字变成印章红 -->
    <filter id="sealGlyphRed" x="-10%" y="-10%" width="120%" height="120%">
      <feColorMatrix type="matrix" values="0 0 0 0 0.48  0 0 0 0 0.18  0 0 0 0 0.14  0 0 0 1 0"/>
    </filter>"""

assert filter_anchor in html, "未找到 sealWear filter"
html = html.replace(filter_anchor, filter_add, 1)

# ========== 3. JS：替换 sealSVG 函数，用隶书字PNG拼印章 ==========
seal_old = """    // 生成精致印章 SVG（磨损纹理 + 粗笔画 + 装饰边框）
    function sealSVG(text){
      var lines;
      if(text.length <= 2){ lines = [text]; }
      else if(text.length === 3){ lines = [text[0], text.slice(1)]; }
      else { lines = [text.slice(0,2), text.slice(2)]; }
      var fontSize = lines.length === 1 ? 34 : (text.length <= 3 ? 26 : 23);
      var yStart = lines.length === 1 ? 62 : 48;
      var tspans = lines.map(function(l, i){
        return '<text x="50" y="' + (yStart + i*30) + '" text-anchor="middle" fill="#7A2E24" font-family="Noto Serif SC,serif" font-size="' + fontSize + '" font-weight="900" letter-spacing="1.5">' + l + '</text>';
      }).join('');
      return '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" filter="url(#sealWear)">'
        + '<rect x="5" y="5" width="90" height="90" fill="none" stroke="#7A2E24" stroke-width="7" rx="2"/>'
        + '<rect x="12" y="12" width="76" height="76" fill="none" stroke="#7A2E24" stroke-width="1.5"/>'
        + '<line x1="5" y1="50" x2="15" y2="50" stroke="#7A2E24" stroke-width="4"/>'
        + '<line x1="85" y1="50" x2="95" y2="50" stroke="#7A2E24" stroke-width="4"/>'
        + '<line x1="50" y1="5" x2="50" y2="15" stroke="#7A2E24" stroke-width="4"/>'
        + '<line x1="50" y1="85" x2="50" y2="95" stroke="#7A2E24" stroke-width="4"/>'
        + tspans + '</svg>';
    }"""

seal_new = """    // 生成印章 SVG（隶书字 + 磨损纹理 + 装饰边框）
    function sealSVG(text){
      var chars = text.split('');
      // 根据字数排版：3字上1下2，4字上2下2，2字竖排，1字居中
      var layout = [];
      if(chars.length === 3){
        layout = [
          {c:chars[0], x:50, y:30, s:30},
          {c:chars[1], x:33, y:64, s:27},
          {c:chars[2], x:67, y:64, s:27}
        ];
      } else if(chars.length === 4){
        layout = [
          {c:chars[0], x:32, y:30, s:26},
          {c:chars[1], x:68, y:30, s:26},
          {c:chars[2], x:32, y:66, s:26},
          {c:chars[3], x:68, y:66, s:26}
        ];
      } else if(chars.length === 2){
        layout = [
          {c:chars[0], x:50, y:34, s:30},
          {c:chars[1], x:50, y:66, s:30}
        ];
      } else {
        layout = [{c:chars[0], x:50, y:50, s:40}];
      }
      // 用隶书字PNG拼出印章文字，filter变红
      var glyphs = layout.map(function(item){
        var src = (typeof GLYPH_IMAGES !== 'undefined' && GLYPH_IMAGES[item.c]) ? GLYPH_IMAGES[item.c] : '';
        if(!src) return '';
        var x = item.x - item.s/2;
        var y = item.y - item.s/2;
        return '<image x="' + x + '" y="' + y + '" width="' + item.s + '" height="' + item.s + '" href="' + src + '" preserveAspectRatio="xMidYMid meet" filter="url(#sealGlyphRed)"/>';
      }).join('');
      return '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" filter="url(#sealWear)">'
        + '<rect x="5" y="5" width="90" height="90" fill="none" stroke="#7A2E24" stroke-width="7" rx="2"/>'
        + '<rect x="12" y="12" width="76" height="76" fill="none" stroke="#7A2E24" stroke-width="1.5"/>'
        + '<line x1="5" y1="50" x2="15" y2="50" stroke="#7A2E24" stroke-width="4"/>'
        + '<line x1="85" y1="50" x2="95" y2="50" stroke="#7A2E24" stroke-width="4"/>'
        + '<line x1="50" y1="5" x2="50" y2="15" stroke="#7A2E24" stroke-width="4"/>'
        + '<line x1="50" y1="85" x2="50" y2="95" stroke="#7A2E24" stroke-width="4"/>'
        + glyphs + '</svg>';
    }"""

assert seal_old in html, "未找到旧 sealSVG 函数"
html = html.replace(seal_old, seal_new, 1)

# 保存
with open(INDEX, "w", encoding="utf-8") as f:
    f.write(html)
print(f"v4 改进完成，index.html 大小: {len(html.encode('utf-8'))} bytes")
