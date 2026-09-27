# -*- coding: utf-8 -*-
"""方案一：信笺展开式交互 — 注入 CSS / HTML / JS"""
import re

INDEX = r"E:\壁纸大赛\招生概念站\index.html"
with open(INDEX, encoding="utf-8") as f:
    html = f.read()

# ========== 1. CSS：在 .campus-place 后注入信笺样式 ==========
css_anchor = "  .campus-place{margin-top:calc(var(--cs)*.24);font-size:11px;letter-spacing:.28em;color:#96A096}"
css_new = css_anchor + """

  /* ===== 信笺展开 ===== */
  .campus-letter{
    max-height:0; overflow:hidden; opacity:0;
    transition:max-height .7s cubic-bezier(.4,0,.2,1), opacity .5s ease, margin .5s ease;
  }
  .campus-letter.open{max-height:640px; opacity:1; margin-top:28px}
  .letter-paper{
    position:relative; background:var(--paper);
    border:1px solid var(--brick); padding:28px 32px;
    display:grid; grid-template-columns:260px 1fr; gap:28px;
    box-shadow:0 8px 32px -12px rgba(31,77,56,.18);
  }
  .letter-paper::before, .letter-paper::after{
    content:''; position:absolute; width:14px; height:14px; border:1px solid var(--brick);
  }
  .letter-paper::before{top:-1px;left:-1px;border-right:0;border-bottom:0}
  .letter-paper::after{bottom:-1px;right:-1px;border-left:0;border-top:0}
  .letter-img-wrap{border:1px solid var(--line); padding:6px; background:#fff}
  .letter-img-wrap img{width:100%; aspect-ratio:4/3; object-fit:cover; display:block}
  .letter-city{font-size:11px; letter-spacing:.3em; color:var(--brick); font-weight:700}
  .letter-name{font-family:'Noto Serif SC',serif; font-size:26px; font-weight:700; color:var(--green); margin-top:6px}
  .letter-desc{margin-top:14px; font-size:14px; line-height:1.9; color:#3a4f3e; font-weight:300}
  .letter-meta{margin-top:16px; display:flex; gap:24px; font-size:12px; color:#8a968b; flex-wrap:wrap}
  .letter-seal{
    position:absolute; right:28px; bottom:24px; width:58px; height:58px;
    background:var(--brick); color:var(--paper);
    display:flex; align-items:center; justify-content:center;
    font-family:'Noto Serif SC',serif; font-size:13px; font-weight:700;
    line-height:1.25; text-align:center; border-radius:3px;
    transform:rotate(-4deg); box-shadow:0 2px 8px rgba(139,58,46,.3); padding:4px;
  }
  .campus-word.active .campus-ch{color:#0D2818}
  .campus-word.active::before{transform:scale(1.8); opacity:1; background:var(--brick)}
  .campus-word.dim{opacity:.35; transition:opacity .4s ease}
  .campus-word.dim:hover{opacity:.6}
  @media (max-width:760px){
    .letter-paper{grid-template-columns:1fr; padding:20px}
    .letter-seal{width:48px; height:48px; font-size:11px; right:16px; bottom:16px}
  }"""
assert css_anchor in html, "未找到 .campus-place CSS"
html = html.replace(css_anchor, css_new, 1)

# ========== 2. HTML：在 #campusRow 后注入信笺容器 ==========
html_anchor = '  <div class="campus-ink-row" id="campusRow"></div>'
html_new = html_anchor + """
  <div class="campus-letter" id="campusLetter">
    <div class="letter-paper">
      <div class="letter-img-wrap"><img class="letter-img" src="" alt=""></div>
      <div class="letter-body">
        <div class="letter-city"></div>
        <h3 class="letter-name"></h3>
        <p class="letter-desc"></p>
        <div class="letter-meta">
          <span class="letter-address"></span>
          <span class="letter-area"></span>
        </div>
      </div>
      <div class="letter-seal"></div>
    </div>
  </div>"""
assert html_anchor in html, "未找到 #campusRow"
html = html.replace(html_anchor, html_new, 1)

# ========== 3. JS：替换五校园渲染块（364-401行） ==========
js_old = """  /* ===== 五校园隶书字形渲染（静态，交互待做） ===== */
  var CAMPUS_INK = [
    {name:'南校园', short:'广州'},
    {name:'东校园', short:'广州'},
    {name:'北校园', short:'广州'},
    {name:'深圳校区', short:'深圳'},
    {name:'珠海校区', short:'珠海'}
  ];
  (function(){
    var row = document.getElementById('campusRow');
    if(!row) return;
    var NS = 'http://www.w3.org/2000/svg';
    CAMPUS_INK.forEach(function(c){
      var btn = document.createElement('button');
      btn.type='button'; btn.className='campus-word'; btn.setAttribute('aria-label',c.name);
      var stack = document.createElement('span'); stack.className='campus-stack';
      c.name.split('').forEach(function(ch){
        var sp = document.createElement('span'); sp.className='campus-ch';
        var svg = document.createElementNS(NS,'svg');
        svg.setAttribute('viewBox','170 20 660 960'); svg.setAttribute('aria-hidden','true');
        var g = document.createElementNS(NS,'g'); g.setAttribute('filter','url(#sealInk)');
        var href = GLYPH_IMAGES[ch];
        if(href){
          var img = document.createElementNS(NS,'image');
          img.setAttribute('x','170'); img.setAttribute('y','20');
          img.setAttribute('width','660'); img.setAttribute('height','960');
          img.setAttribute('preserveAspectRatio','xMidYMid meet');
          img.setAttributeNS('http://www.w3.org/1999/xlink','href',href);
          g.appendChild(img);
        }
        svg.appendChild(g); sp.appendChild(svg); stack.appendChild(sp);
      });
      btn.appendChild(stack);
      var pl = document.createElement('span'); pl.className='campus-place'; pl.textContent=c.short;
      btn.appendChild(pl);
      row.appendChild(btn);
    });
  })();"""

js_new = """  /* ===== 五校园隶书字形 + 信笺展开交互 ===== */
  var CAMPUS_DATA = [
    {name:'南校园', short:'广州', img:'assets/campus-nan.png',
     city:'广州 · 海珠',
     desc:'珠江之畔的康乐园，中大文脉的起点。红砖绿瓦的怀士堂见证百年春秋，所有大一新生在此开启大学生活，体味百年中大的精神底蕴。',
     address:'广州市海珠区新港西路135号', area:'1.239 km²'},
    {name:'东校园', short:'广州', img:'assets/campus-dong.png',
     city:'广州 · 大学城',
     desc:'广州大学城的知识之门，工科与信息科学的创新沃土。现代化图书馆矗立其间，年轻学子在此探索前沿，与城市共生长。',
     address:'广州市番禺区大学城外环东路132号', area:'0.989 km²'},
    {name:'北校园', short:'广州', img:'assets/campus-bei.png',
     city:'广州 · 越秀',
     desc:'珠江之滨的医学殿堂，中山医学院所在地。红楼掩映间，"救人救国救世"的誓言回响百年，是中大医科传统优势的根基所在。',
     address:'广州市越秀区中山二路74号', area:'0.209 km²'},
    {name:'深圳校区', short:'深圳', img:'assets/campus-shenzhen.png',
     city:'深圳 · 光明',
     desc:'山海之间的红砖新章，着力发展医科与新型工科。6.8万平方米的图书馆藏书五百万册，是深圳校区的知识心脏，与特区同频共振。',
     address:'深圳市光明区公常路66号', area:'3.143 km²'},
    {name:'珠海校区', short:'珠海', img:'assets/campus-zhuhai.png',
     city:'珠海 · 唐家湾',
     desc:'南海之滨、凤凰山下，三面环山一面向海。天琴中心在此聆听宇宙的引力波，"深海、深空、深地"学科群扎根于此，仰望星空，脚踏实地。',
     address:'珠海市唐家湾镇大学路2号', area:'3.571 km²'}
  ];
  (function(){
    var row = document.getElementById('campusRow');
    var letter = document.getElementById('campusLetter');
    if(!row) return;
    var NS = 'http://www.w3.org/2000/svg';
    var activeIdx = -1;
    var words = [];

    function glyphSVG(ch){
      var svg = document.createElementNS(NS,'svg');
      svg.setAttribute('viewBox','170 20 660 960'); svg.setAttribute('aria-hidden','true');
      var g = document.createElementNS(NS,'g'); g.setAttribute('filter','url(#sealInk)');
      var href = GLYPH_IMAGES[ch];
      if(href){
        var img = document.createElementNS(NS,'image');
        img.setAttribute('x','170'); img.setAttribute('y','20');
        img.setAttribute('width','660'); img.setAttribute('height','960');
        img.setAttribute('preserveAspectRatio','xMidYMid meet');
        img.setAttributeNS('http://www.w3.org/1999/xlink','href',href);
        g.appendChild(img);
      }
      svg.appendChild(g); return svg;
    }

    function openLetter(idx){
      activeIdx = idx;
      var d = CAMPUS_DATA[idx];
      letter.querySelector('.letter-img').src = d.img;
      letter.querySelector('.letter-img').alt = d.name;
      letter.querySelector('.letter-city').textContent = d.city;
      letter.querySelector('.letter-name').textContent = d.name;
      letter.querySelector('.letter-desc').textContent = d.desc;
      letter.querySelector('.letter-address').textContent = d.address;
      letter.querySelector('.letter-area').textContent = d.area;
      letter.querySelector('.letter-seal').textContent = d.name;
      letter.classList.add('open');
      words.forEach(function(w,i){
        w.classList.toggle('active', i===idx);
        w.classList.toggle('dim', i!==idx);
      });
    }
    function closeLetter(){
      activeIdx = -1;
      letter.classList.remove('open');
      words.forEach(function(w){ w.classList.remove('active','dim'); });
    }

    CAMPUS_DATA.forEach(function(c, i){
      var btn = document.createElement('button');
      btn.type='button'; btn.className='campus-word'; btn.setAttribute('aria-label',c.name);
      var stack = document.createElement('span'); stack.className='campus-stack';
      c.name.split('').forEach(function(ch){
        var sp = document.createElement('span'); sp.className='campus-ch';
        sp.appendChild(glyphSVG(ch)); stack.appendChild(sp);
      });
      btn.appendChild(stack);
      var pl = document.createElement('span'); pl.className='campus-place'; pl.textContent=c.short;
      btn.appendChild(pl);
      btn.addEventListener('click', function(){
        if(activeIdx === i){ closeLetter(); } else { openLetter(i); }
      });
      words.push(btn);
      row.appendChild(btn);
    });

    // 点空白处关闭
    document.addEventListener('click', function(e){
      if(activeIdx < 0) return;
      if(!e.target.closest('.campus-word') && !e.target.closest('.campus-letter')){
        closeLetter();
      }
    });
    // ESC 关闭
    document.addEventListener('keydown', function(e){
      if(e.key === 'Escape' && activeIdx >= 0){ closeLetter(); }
    });
  })();"""

assert js_old in html, "未找到旧五校园 JS 块"
html = html.replace(js_old, js_new, 1)

# 保存
with open(INDEX, "w", encoding="utf-8") as f:
    f.write(html)
print(f"方案一注入完成，index.html 大小: {len(html.encode('utf-8'))} bytes")
