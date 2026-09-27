# -*- coding: utf-8 -*-
"""v5：照片hover只提层级 + 印章改长方形横排"""
import re

INDEX = r"E:\壁纸大赛\招生概念站\index.html"
with open(INDEX, encoding="utf-8") as f:
    html = f.read()

# ========== 1. CSS：照片hover只提升z-index，不加transform和阴影 ==========
hover_old = """  /* 单张照片hover时拎到最前（优先级高于散开时的z-index） */
  .letter-photos .polaroid:hover{
    z-index:20;
    transform:translateY(-18px) rotate(0deg) scale(1.08);
    box-shadow:0 18px 44px rgba(0,0,0,.3);
  }"""

hover_new = """  /* 单张照片hover时移到最前面，方便看清 */
  .letter-photos .polaroid:hover{
    z-index:20;
  }"""

assert hover_old in html, "未找到旧 hover 规则"
html = html.replace(hover_old, hover_new, 1)

# ========== 2. JS：替换 sealSVG 函数，改成长方形横排隶书印章 ==========
seal_old = """    // 生成印章 SVG（隶书字 + 磨损纹理 + 装饰边框）
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

seal_new = """    // 生成印章 SVG（长方形横排隶书字 + 磨损纹理 + 装饰边框）
    function sealSVG(text){
      var chars = text.split('');
      var n = chars.length;
      // 长方形 viewBox：宽随字数调整，高固定 64
      var W = 40 + n * 34;  // 左右各20padding，每字34宽
      var H = 64;
      // 文字均匀横排
      var areaW = W - 40;  // 左右各留20
      var step = areaW / n;
      var startX = 20 + step / 2;
      var glyphSize = n <= 3 ? 32 : 27;
      var glyphs = chars.map(function(c, i){
        var src = (typeof GLYPH_IMAGES !== 'undefined' && GLYPH_IMAGES[c]) ? GLYPH_IMAGES[c] : '';
        if(!src) return '';
        var cx = startX + i * step;
        var x = cx - glyphSize / 2;
        var y = (H - glyphSize) / 2;
        return '<image x="' + x + '" y="' + y + '" width="' + glyphSize + '" height="' + glyphSize + '" href="' + src + '" preserveAspectRatio="xMidYMid meet" filter="url(#sealGlyphRed)"/>';
      }).join('');
      return '<svg viewBox="0 0 ' + W + ' ' + H + '" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" filter="url(#sealWear)">'
        + '<rect x="3" y="3" width="' + (W-6) + '" height="' + (H-6) + '" fill="none" stroke="#7A2E24" stroke-width="5" rx="2"/>'
        + '<rect x="9" y="9" width="' + (W-18) + '" height="' + (H-18) + '" fill="none" stroke="#7A2E24" stroke-width="1.2"/>'
        + '<line x1="3" y1="' + (H/2) + '" x2="11" y2="' + (H/2) + '" stroke="#7A2E24" stroke-width="3.5"/>'
        + '<line x1="' + (W-11) + '" y1="' + (H/2) + '" x2="' + (W-3) + '" y2="' + (H/2) + '" stroke="#7A2E24" stroke-width="3.5"/>'
        + glyphs + '</svg>';
    }"""

assert seal_old in html, "未找到旧 sealSVG 函数"
html = html.replace(seal_old, seal_new, 1)

# ========== 3. CSS：印章容器适配长方形（去掉固定宽高比限制） ==========
seal_css_old = """  .letter-seal{
    position:absolute; right:30px; bottom:26px; width:66px; height:66px;
    transform:rotate(-5deg); opacity:.92;
    filter:drop-shadow(0 2px 4px rgba(139,58,46,.25));
  }
  .letter-seal svg{width:100%; height:100%}"""

seal_css_new = """  .letter-seal{
    position:absolute; right:30px; bottom:26px; height:42px;
    transform:rotate(-3deg); opacity:.92;
    filter:drop-shadow(0 2px 4px rgba(139,58,46,.25));
  }
  .letter-seal svg{height:100%; width:auto; display:block}"""

assert seal_css_old in html, "未找到旧印章 CSS"
html = html.replace(seal_css_old, seal_css_new, 1)

# 移动端印章也适配长方形
mobile_seal_old = """    .letter-seal{width:52px; height:52px; right:16px; bottom:16px}"""
mobile_seal_new = """    .letter-seal{height:34px; right:16px; bottom:16px}"""
if mobile_seal_old in html:
    html = html.replace(mobile_seal_old, mobile_seal_new, 1)
    print("移动端印章已适配")

# 保存
with open(INDEX, "w", encoding="utf-8") as f:
    f.write(html)
print(f"v5 改进完成，index.html 大小: {len(html.encode('utf-8'))} bytes")
