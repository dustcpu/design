# -*- coding: utf-8 -*-
"""v3：照片悬停散开 + 印章精致化"""
import re

INDEX = r"E:\壁纸大赛\招生概念站\index.html"
with open(INDEX, encoding="utf-8") as f:
    html = f.read()

# ========== 1. CSS：替换照片堆叠样式 ==========
css_old = """  /* ===== 照片堆叠（拍立得） ===== */
  .letter-photos{position:relative; height:230px; margin-bottom:4px}
  .polaroid{
    position:absolute; width:165px; background:#FFFEF8;
    padding:7px 7px 30px;
    box-shadow:0 3px 14px rgba(0,0,0,.18), 0 1px 3px rgba(0,0,0,.1);
    transition:transform .4s cubic-bezier(.34,1.56,.64,1), box-shadow .4s, z-index 0s;
    cursor:zoom-in;
  }
  .polaroid:nth-child(1){left:0; top:14px; transform:rotate(-6deg); z-index:1}
  .polaroid:nth-child(2){left:88px; top:0; transform:rotate(2.5deg); z-index:2}
  .polaroid:nth-child(3){left:176px; top:18px; transform:rotate(-3deg); z-index:3}
  .polaroid:hover{
    transform:translateY(-16px) rotate(0deg) scale(1.06);
    z-index:20; box-shadow:0 16px 40px rgba(0,0,0,.28);
  }
  .polaroid .ph-img{
    width:100%; aspect-ratio:1; display:block;
    background:linear-gradient(135deg, #E8E0D0, #D8CFBC);
    display:flex; align-items:center; justify-content:center;
    color:#A89B80; font-size:11px; font-family:serif; letter-spacing:.1em;
  }
  .polaroid .ph-img img{width:100%; height:100%; object-fit:cover; display:block}
  .polaroid .ph-cap{
    font-size:10px; color:#A89B80; text-align:center; margin-top:7px;
    font-family:'Noto Serif SC',serif; letter-spacing:.08em;
  }"""

css_new = """  /* ===== 照片堆叠（拍立得） ===== */
  .letter-photos{position:relative; height:210px; margin-bottom:4px}
  .polaroid{
    position:absolute; width:128px; background:#FFFEF8;
    padding:6px 6px 24px;
    box-shadow:0 3px 12px rgba(0,0,0,.18), 0 1px 3px rgba(0,0,0,.1);
    transition:transform .5s cubic-bezier(.34,1.56,.64,1), box-shadow .5s, z-index 0s;
    cursor:zoom-in;
  }
  /* 平时紧凑堆叠，控制在列宽内不遮挡文字 */
  .polaroid:nth-child(1){left:0; top:14px; transform:rotate(-6deg); z-index:1}
  .polaroid:nth-child(2){left:42px; top:0; transform:rotate(2deg); z-index:2}
  .polaroid:nth-child(3){left:84px; top:18px; transform:rotate(-3deg); z-index:3}
  /* 悬停时三张散开 */
  .letter-photos:hover .polaroid:nth-child(1){
    transform:translateX(-22px) translateY(4px) rotate(-11deg); z-index:1;
  }
  .letter-photos:hover .polaroid:nth-child(2){
    transform:translateY(-14px) rotate(0deg) scale(1.08); z-index:10;
    box-shadow:0 14px 36px rgba(0,0,0,.25);
  }
  .letter-photos:hover .polaroid:nth-child(3){
    transform:translateX(22px) translateY(4px) rotate(7deg); z-index:3;
  }
  .polaroid .ph-img{
    width:100%; aspect-ratio:1; display:block;
    background:linear-gradient(135deg, #E8E0D0, #D8CFBC);
    display:flex; align-items:center; justify-content:center;
    color:#A89B80; font-size:10px; font-family:serif; letter-spacing:.1em;
  }
  .polaroid .ph-img img{width:100%; height:100%; object-fit:cover; display:block}
  .polaroid .ph-cap{
    font-size:9.5px; color:#A89B80; text-align:center; margin-top:6px;
    font-family:'Noto Serif SC',serif; letter-spacing:.08em;
  }"""

assert css_old in html, "未找到旧照片堆叠 CSS"
html = html.replace(css_old, css_new, 1)

# ========== 2. SVG defs：添加印章磨损 filter ==========
svg_old = """    <filter id="sealInk" x="-14%" y="-14%" width="128%" height="128%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.020" numOctaves="2" seed="9" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="4.5" xChannelSelector="R" yChannelSelector="G"/>
    </filter>"""

svg_new = svg_old + """
    <filter id="sealWear" x="-10%" y="-10%" width="120%" height="120%">
      <feTurbulence type="fractalNoise" baseFrequency="0.06" numOctaves="3" seed="7" result="noise"/>
      <feColorMatrix in="noise" type="matrix" values="0 0 0 0 0.55  0 0 0 0 0.23  0 0 0 0 0.18  0 0 0 -0.7 0.85" result="wearMask"/>
      <feComposite in="SourceGraphic" in2="wearMask" operator="out" result="worn"/>
      <feComposite in="worn" in2="SourceGraphic" operator="over"/>
    </filter>"""

assert svg_old in html, "未找到 sealInk filter"
html = html.replace(svg_old, svg_new, 1)

# ========== 3. JS：替换 sealSVG 函数，印章更精致 ==========
seal_old = """    // 生成精致印章 SVG
    function sealSVG(text){
      var lines;
      if(text.length <= 2){ lines = [text]; }
      else if(text.length === 3){ lines = [text[0], text.slice(1)]; }
      else { lines = [text.slice(0,2), text.slice(2)]; }
      var fontSize = lines.length === 1 ? 30 : (text.length <= 3 ? 22 : 19);
      var yStart = lines.length === 1 ? 58 : 44;
      var tspans = lines.map(function(l, i){
        return '<text x="50" y="' + (yStart + i*28) + '" text-anchor="middle" fill="#8B3A2E" font-family="Noto Serif SC,serif" font-size="' + fontSize + '" font-weight="700" letter-spacing="3">' + l + '</text>';
      }).join('');
      return '<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">'
        + '<rect x="7" y="7" width="86" height="86" fill="none" stroke="#8B3A2E" stroke-width="5" rx="2"/>'
        + '<rect x="14" y="14" width="72" height="72" fill="none" stroke="#8B3A2E" stroke-width="1"/>'
        + tspans + '</svg>';
    }"""

seal_new = """    // 生成精致印章 SVG（磨损纹理 + 粗笔画 + 装饰边框）
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

assert seal_old in html, "未找到旧 sealSVG 函数"
html = html.replace(seal_old, seal_new, 1)

# 保存
with open(INDEX, "w", encoding="utf-8") as f:
    f.write(html)
print(f"v3 改进完成，index.html 大小: {len(html.encode('utf-8'))} bytes")
