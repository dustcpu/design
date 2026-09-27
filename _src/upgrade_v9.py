# -*- coding: utf-8 -*-
"""v9：背景回纹调浓 + 学院鱼骨枝条设计（生长动画）"""
import re

INDEX = r"E:\壁纸大赛\招生概念站\index.html"
with open(INDEX, encoding="utf-8") as f:
    html = f.read()

# ========== 1. 背景回纹调浓：减小pattern尺寸+加粗线条+全不透明 ==========
huiwen_old = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='80' height='80' viewBox='0 0 80 80'%3E"
    "%3Cg fill='none' stroke='%232F5D46' stroke-width='1'%3E"
    "%3Cpath d='M8 8h28v14H22v14H8z'/%3E"
    "%3Cpath d='M72 72H44V58h14V44h14z'/%3E"
    "%3Cpath d='M8 72h14v-14h14V44H8z' opacity='.5'/%3E"
    "%3Cpath d='M72 8H58v14H44v14h28z' opacity='.5'/%3E"
    "%3C/g%3E%3C/svg%3E"
)

# 更浓的回纹：60x60，stroke-width 1.5，全不透明
huiwen_new = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='64' height='64' viewBox='0 0 64 64'%3E"
    "%3Cg fill='none' stroke='%232F5D46' stroke-width='1.4'%3E"
    "%3Cpath d='M6 6h24v12H18v12H6z'/%3E"
    "%3Cpath d='M58 58H34V46h12V34h12z'/%3E"
    "%3Cpath d='M6 58h12v-12h12V34H6z'/%3E"
    "%3Cpath d='M58 6H46v12H34v12h24z'/%3E"
    "%3C/g%3E%3C/svg%3E"
)

assert huiwen_old in html, "未找到旧回纹SVG"
html = html.replace(huiwen_old, huiwen_new, 1)
html = html.replace("background-size:80px 80px;", "background-size:64px 64px;", 1)
print("背景回纹已调浓")

# ========== 2. CSS：替换学院标签样式为鱼骨枝条样式 ==========
colleges_css_old = """  .letter-colleges{
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

colleges_css_new = """  .letter-colleges{
    margin-top:14px; padding-top:12px; border-top:1px dashed rgba(139,58,46,.2);
  }
  .college-label{
    font-size:10.5px; letter-spacing:.3em; color:var(--brick); font-weight:700;
    margin-bottom:14px; display:block; text-align:center;
  }
  /* 鱼骨枝条容器 */
  .college-branch{position:relative;}
  .branch-svg{
    position:absolute; left:50%; top:0; width:28px; height:100%;
    transform:translateX(-50%); z-index:0; pointer-events:none;
    overflow:visible;
  }
  .branch-main{
    stroke:var(--green); stroke-width:1.8; fill:none; stroke-linecap:round;
    stroke-dasharray:1200; stroke-dashoffset:1200;
    animation:branchGrow 1.8s cubic-bezier(.4,0,.2,1) forwards;
  }
  .branch-node{
    fill:var(--paper); stroke:var(--green); stroke-width:1.5;
    opacity:0; animation:nodePop .35s ease forwards;
  }
  .branch-items{position:relative; z-index:1;}
  .branch-pair{
    display:grid; grid-template-columns:1fr 28px 1fr; align-items:center;
    padding:7px 0; opacity:0; transform:translateY(6px);
    animation:pairIn .5s ease forwards;
  }
  .branch-left{text-align:right; padding-right:8px;}
  .branch-right{text-align:left; padding-left:8px;}
  .branch-left, .branch-right{
    font-size:11px; font-family:'Noto Serif SC',serif; color:var(--green);
    line-height:1.5;
  }
  .branch-pair:hover .branch-left,
  .branch-pair:hover .branch-right{color:var(--brick);}
  @keyframes branchGrow{to{stroke-dashoffset:0;}}
  @keyframes nodePop{to{opacity:1;}}
  @keyframes pairIn{to{opacity:1; transform:none;}}"""

assert colleges_css_old in html, "未找到旧学院CSS"
html = html.replace(colleges_css_old, colleges_css_new, 1)
print("学院鱼骨枝条CSS已替换")

# ========== 3. HTML：替换学院容器 ==========
colleges_html_old = """        <div class="letter-colleges">
          <span class="college-label">下设院系</span>
          <div class="college-tags"></div>
        </div>"""
colleges_html_new = """        <div class="letter-colleges">
          <span class="college-label">下设院系</span>
          <div class="college-branch"></div>
        </div>"""
assert colleges_html_old in html, "未找到旧学院HTML"
html = html.replace(colleges_html_old, colleges_html_new, 1)
print("学院HTML容器已替换")

# ========== 4. JS：替换学院渲染为鱼骨枝条 ==========
colleges_js_old = """      var tagsBox = letter.querySelector('.college-tags');
      tagsBox.innerHTML = '';
      d.colleges.split('·').forEach(function(name){
        name = name.trim();
        if(!name) return;
        var tag = document.createElement('span');
        tag.className = 'college-tag';
        tag.textContent = name;
        tagsBox.appendChild(tag);
      });"""

colleges_js_new = """      renderCollegeBranch(letter.querySelector('.college-branch'), d.colleges);"""

assert colleges_js_old in html, "未找到旧学院JS"
html = html.replace(colleges_js_old, colleges_js_new, 1)

# 在 renderPhotos 函数后添加 renderCollegeBranch 函数
render_anchor = """    function renderPhotos(photos){
      photosWrap.innerHTML = '';
      photosWrap.dataset.photoIdx = '1';
      photos.forEach(function(p, i){
        var div = document.createElement('div');
        div.className = 'polaroid' + (i === 1 ? ' active' : '');
        var inner = document.createElement('div');
        inner.className = 'ph-img';
        if(p.src){
          var im = document.createElement('img');
          im.src = p.src; im.alt = p.cap;
          im.addEventListener('click', function(){ openLightbox(p.src, p.cap); });
          inner.appendChild(im);
        } else {
          inner.textContent = '照片待替换';
        }
        var cap = document.createElement('div');
        cap.className = 'ph-cap'; cap.textContent = p.cap;
        div.appendChild(inner); div.appendChild(cap);
        photosWrap.appendChild(div);
      });
    }"""

branch_fn = render_anchor + """

    // 鱼骨枝条学院列表
    function renderCollegeBranch(box, collegesStr){
      box.innerHTML = '';
      var names = collegesStr.split('·').map(function(s){return s.trim();}).filter(Boolean);
      if(!names.length) return;
      var pairCount = Math.ceil(names.length / 2);
      var rowH = 36;
      var svgH = pairCount * rowH + 16;

      // SVG 枝条
      var SVG_NS = 'http://www.w3.org/2000/svg';
      var svg = document.createElementNS(SVG_NS, 'svg');
      svg.setAttribute('class', 'branch-svg');
      svg.setAttribute('viewBox', '0 0 28 ' + svgH);
      svg.setAttribute('preserveAspectRatio', 'none');

      // 主枝：自然弯曲的路径
      var d = 'M14 6';
      for(var i = 0; i < pairCount; i++){
        var y = 16 + i * rowH;
        var cpy = y - rowH/2;
        var cpx = 14 + ((i % 2 === 0) ? 3.5 : -3.5);
        d += ' Q' + cpx + ' ' + cpy + ' 14 ' + y;
      }
      var path = document.createElementNS(SVG_NS, 'path');
      path.setAttribute('d', d);
      path.setAttribute('class', 'branch-main');
      svg.appendChild(path);

      // 节点圆点
      for(var j = 0; j < pairCount; j++){
        var cy = 16 + j * rowH;
        var c = document.createElementNS(SVG_NS, 'circle');
        c.setAttribute('cx', '14');
        c.setAttribute('cy', cy);
        c.setAttribute('r', '3.5');
        c.setAttribute('class', 'branch-node');
        c.style.animationDelay = (0.4 + j * 0.14) + 's';
        svg.appendChild(c);
      }
      box.appendChild(svg);

      // 学院名称（左右成对）
      var items = document.createElement('div');
      items.className = 'branch-items';
      for(var k = 0; k < names.length; k += 2){
        var pair = document.createElement('div');
        pair.className = 'branch-pair';
        pair.style.animationDelay = (0.5 + (k/2) * 0.14) + 's';

        var left = document.createElement('span');
        left.className = 'branch-left';
        left.textContent = names[k];
        pair.appendChild(left);

        var mid = document.createElement('span');
        pair.appendChild(mid);

        var right = document.createElement('span');
        right.className = 'branch-right';
        right.textContent = names[k+1] || '';
        pair.appendChild(right);

        items.appendChild(pair);
      }
      box.appendChild(items);
    }"""

assert render_anchor in html, "未找到 renderPhotos 锚点"
html = html.replace(render_anchor, branch_fn, 1)
print("鱼骨枝条JS函数已添加")

# 保存
with open(INDEX, "w", encoding="utf-8") as f:
    f.write(html)
print(f"v9 改进完成，index.html 大小: {len(html.encode('utf-8'))} bytes")
