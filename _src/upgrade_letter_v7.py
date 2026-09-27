# -*- coding: utf-8 -*-
"""v7：照片交互改为滚轮翻页（紧凑堆叠 + 滚轮切换 + 弹性过渡）"""
import re

INDEX = r"E:\壁纸大赛\招生概念站\index.html"
with open(INDEX, encoding="utf-8") as f:
    html = f.read()

# ========== 1. CSS：替换整个照片堆叠样式（去掉散开/扇面，改为紧凑堆叠+active） ==========
css_old = """  /* ===== 照片堆叠（拍立得） ===== */
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
    transform:translateY(-14px) rotate(0deg) scale(1.08);
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
  }
  /* 鼠标指向的照片浮到最前（JS控制.front） */
  .polaroid.front{ z-index:20; }"""

css_new = """  /* ===== 照片堆叠（拍立得·滚轮翻页） ===== */
  .letter-photos{position:relative; height:210px; margin-bottom:4px}
  .polaroid{
    position:absolute; width:128px; background:#FFFEF8;
    padding:6px 6px 24px;
    box-shadow:0 3px 12px rgba(0,0,0,.18), 0 1px 3px rgba(0,0,0,.1);
    transition:transform .55s cubic-bezier(.34,1.56,.64,1), box-shadow .5s, z-index 0s, opacity .45s ease;
    cursor:zoom-in;
  }
  /* 紧凑堆叠，三张都居中区域，轻微错开角度和位置 */
  .polaroid:nth-child(1){left:22px; top:16px; transform:rotate(-8deg); z-index:1; opacity:.7}
  .polaroid:nth-child(2){left:42px; top:0; transform:rotate(2deg); z-index:2; opacity:1}
  .polaroid:nth-child(3){left:62px; top:20px; transform:rotate(-5deg); z-index:1; opacity:.7}
  /* 当前翻到的照片：放大上浮到最前 */
  .polaroid.active{
    z-index:20;
    transform:translateY(-14px) rotate(0deg) scale(1.12);
    box-shadow:0 18px 44px rgba(0,0,0,.3);
    opacity:1;
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

assert css_old in html, "未找到旧照片堆叠CSS"
html = html.replace(css_old, css_new, 1)

# ========== 2. JS：去掉扇面mousemove，改为wheel滚轮翻页 ==========
js_old = """    // ===== 照片区域：鼠标左右移动时，对应位置的照片浮到最前（扇面效果） =====
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
    });"""

js_new = """    // ===== 照片区域：滚轮翻页（悬停时滚动鼠标切换哪张在最前） =====
    document.addEventListener('wheel', function(e){
      var box = e.target.closest('.letter-photos');
      if(!box) return;
      e.preventDefault();
      var imgs = box.querySelectorAll('.polaroid');
      if(imgs.length < 2) return;
      var idx = parseInt(box.dataset.photoIdx || '1', 10);
      if(e.deltaY > 0) idx = (idx + 1) % imgs.length;
      else idx = (idx + imgs.length - 1) % imgs.length;
      box.dataset.photoIdx = idx;
      imgs.forEach(function(el, i){ el.classList.toggle('active', i === idx); });
    }, {passive:false});"""

assert js_old in html, "未找到旧扇面JS"
html = html.replace(js_old, js_new, 1)

# ========== 3. 渲染照片时默认给中间那张加active ==========
render_old = """    function renderPhotos(photos){
      photosWrap.innerHTML = '';
      photos.forEach(function(p){
        var div = document.createElement('div');
        div.className = 'polaroid';"""

render_new = """    function renderPhotos(photos){
      photosWrap.innerHTML = '';
      photosWrap.dataset.photoIdx = '1';
      photos.forEach(function(p, i){
        var div = document.createElement('div');
        div.className = 'polaroid' + (i === 1 ? ' active' : '');"""

assert render_old in html, "未找到 renderPhotos 函数"
html = html.replace(render_old, render_new, 1)

# 保存
with open(INDEX, "w", encoding="utf-8") as f:
    f.write(html)
print(f"v7 改进完成，index.html 大小: {len(html.encode('utf-8'))} bytes")
