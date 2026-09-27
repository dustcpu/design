# -*- coding: utf-8 -*-
"""方案一 v2：信纸质感 + 照片堆叠 + 精致印章 + 扩充简介"""
import re

INDEX = r"E:\壁纸大赛\招生概念站\index.html"
with open(INDEX, encoding="utf-8") as f:
    html = f.read()

# ========== 1. CSS：替换信笺样式 ==========
css_old_start = "  /* ===== 信笺展开 ===== */"
css_old_end = "  @media (max-width:760px){\n    .letter-paper{grid-template-columns:1fr; padding:20px}\n    .letter-seal{width:48px; height:48px; font-size:11px; right:16px; bottom:16px}\n  }"
css_old = html[html.index(css_old_start):html.index(css_old_end)+len(css_old_end)]

css_new = """  /* ===== 信笺展开 ===== */
  .campus-letter{
    max-height:0; overflow:hidden; opacity:0;
    transition:max-height .8s cubic-bezier(.4,0,.2,1), opacity .5s ease, margin .6s ease;
  }
  .campus-letter.open{max-height:900px; opacity:1; margin-top:32px}
  .letter-paper{
    position:relative;
    background:
      repeating-linear-gradient(90deg, transparent, transparent 30px, rgba(139,58,46,.035) 30px, rgba(139,58,46,.035) 31px),
      radial-gradient(ellipse at 25% 15%, rgba(255,252,240,.7), transparent 55%),
      radial-gradient(ellipse at 80% 90%, rgba(200,180,140,.12), transparent 50%),
      linear-gradient(160deg, #F8F3E8 0%, #F2ECDA 50%, #EFE7D2 100%);
    border:1px solid rgba(139,58,46,.35);
    padding:32px 36px 28px;
    display:grid; grid-template-columns:280px 1fr; gap:32px;
    box-shadow:0 10px 40px -14px rgba(31,77,56,.22), inset 0 0 60px rgba(200,180,140,.08);
  }
  /* 信笺四角装饰 */
  .letter-paper::before, .letter-paper::after{
    content:''; position:absolute; width:18px; height:18px; border:1.5px solid var(--brick);
  }
  .letter-paper::before{top:-1px;left:-1px;border-right:0;border-bottom:0}
  .letter-paper::after{bottom:-1px;right:-1px;border-left:0;border-top:0}
  /* 左侧装订线 */
  .letter-paper .letter-body{position:relative; padding-left:20px}
  .letter-paper .letter-body::before{
    content:''; position:absolute; left:0; top:4px; bottom:4px; width:1px;
    background:linear-gradient(to bottom, transparent, rgba(139,58,46,.25) 10%, rgba(139,58,46,.25) 90%, transparent);
  }

  /* ===== 照片堆叠（拍立得） ===== */
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
  }

  /* ===== 信笺文字 ===== */
  .letter-city{font-size:11px; letter-spacing:.35em; color:var(--brick); font-weight:700}
  .letter-name{
    font-family:'Noto Serif SC',serif; font-size:28px; font-weight:700;
    color:var(--green); margin-top:8px; letter-spacing:.06em;
  }
  .letter-desc{
    margin-top:16px; font-size:13.5px; line-height:2; color:#3a4f3e; font-weight:300;
    text-align:justify;
  }
  .letter-colleges{
    margin-top:14px; padding-top:12px; border-top:1px dashed rgba(139,58,46,.2);
    font-size:11.5px; line-height:1.9; color:#6b7d6f;
  }
  .letter-colleges strong{color:var(--brick); font-weight:700; margin-right:6px}
  .letter-meta{
    margin-top:14px; display:flex; gap:24px; font-size:11.5px; color:#8a968b; flex-wrap:wrap;
  }

  /* ===== 印章（SVG） ===== */
  .letter-seal{
    position:absolute; right:30px; bottom:26px; width:66px; height:66px;
    transform:rotate(-5deg); opacity:.92;
    filter:drop-shadow(0 2px 4px rgba(139,58,46,.25));
  }
  .letter-seal svg{width:100%; height:100%}

  /* 字形状态 */
  .campus-word.active .campus-ch{color:#0D2818}
  .campus-word.active::before{transform:scale(1.8); opacity:1; background:var(--brick)}
  .campus-word.dim{opacity:.35; transition:opacity .4s ease}
  .campus-word.dim:hover{opacity:.6}

  /* ===== Lightbox 照片放大 ===== */
  .lightbox{
    position:fixed; inset:0; background:rgba(20,30,25,.85);
    display:flex; align-items:center; justify-content:center;
    z-index:500; opacity:0; pointer-events:none; transition:opacity .3s ease;
    backdrop-filter:blur(4px);
  }
  .lightbox.show{opacity:1; pointer-events:auto}
  .lightbox img{
    max-width:85vw; max-height:85vh; object-fit:contain;
    box-shadow:0 20px 60px rgba(0,0,0,.5);
    background:#FFFEF8; padding:12px;
  }
  .lightbox .lb-close{
    position:absolute; top:24px; right:32px; color:#fff; font-size:28px;
    cursor:pointer; background:none; border:0; opacity:.7; transition:opacity .2s;
  }
  .lightbox .lb-close:hover{opacity:1}
  .lightbox .lb-cap{
    position:absolute; bottom:24px; left:50%; transform:translateX(-50%);
    color:#ddd; font-size:13px; font-family:serif; letter-spacing:.1em;
  }

  @media (max-width:860px){
    .letter-paper{grid-template-columns:1fr; padding:24px 20px}
    .letter-photos{height:200px}
    .polaroid{width:140px}
    .polaroid:nth-child(2){left:70px}
    .polaroid:nth-child(3){left:140px}
    .letter-seal{width:52px; height:52px; right:16px; bottom:16px}
  }"""

html = html.replace(css_old, css_new, 1)

# ========== 2. HTML：替换信笺容器结构 ==========
html_old_letter = """  <div class="campus-letter" id="campusLetter">
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

html_new_letter = """  <div class="campus-letter" id="campusLetter">
    <div class="letter-paper">
      <div class="letter-photos" id="letterPhotos"></div>
      <div class="letter-body">
        <div class="letter-city"></div>
        <h3 class="letter-name"></h3>
        <p class="letter-desc"></p>
        <div class="letter-colleges"><strong>下设院系</strong><span class="colleges-list"></span></div>
        <div class="letter-meta">
          <span class="letter-address"></span>
          <span class="letter-area"></span>
        </div>
      </div>
      <div class="letter-seal" id="letterSeal"></div>
    </div>
  </div>
  <!-- 照片放大 lightbox -->
  <div class="lightbox" id="lightbox">
    <button class="lb-close" aria-label="关闭">&times;</button>
    <img src="" alt="">
    <div class="lb-cap"></div>
  </div>"""

assert html_old_letter in html, "未找到旧信笺 HTML"
html = html.replace(html_old_letter, html_new_letter, 1)

# ========== 3. JS：替换 CAMPUS_DATA 和渲染逻辑 ==========
js_old_start = "  /* ===== 五校园隶书字形 + 信笺展开交互 ===== */"
js_old_end_marker = "  var fadeEls = document.querySelectorAll('.scene, .bldg, .stat');"
js_old = html[html.index(js_old_start):html.index(js_old_end_marker)]

js_new = """  /* ===== 五校园隶书字形 + 信笺展开交互 v2 ===== */
  var CAMPUS_DATA = [
    {
      name:'南校园', short:'广州', city:'广州 · 海珠',
      photos:[
        {src:'', cap:'康乐园 · 怀士堂'},
        {src:'', cap:'中大北门'},
        {src:'', cap:'马丁堂'}
      ],
      desc:'珠江之畔的康乐园，是中大文脉的起点，也是所有大一新生开启大学生活的地方。红砖绿瓦的怀士堂见证百年春秋，沿中轴线分布的近代建筑群掩映在榕树浓荫之中。这里汇聚了人文社科与基础理学的传统优势学科，漫步其间，处处是百年学府的沉静与厚重。',
      colleges:'中国语言文学系 · 历史学系 · 哲学系 · 社会学与人类学学院 · 博雅学院 · 岭南学院 · 外国语学院 · 马克思主义学院 · 心理学系 · 传播与设计学院 · 艺术学院 · 数学学院 · 物理学院 · 化学学院 · 生命科学学院 · 地理科学与规划学院 等',
      address:'广州市海珠区新港西路135号', area:'1.239 km²'
    },
    {
      name:'东校园', short:'广州', city:'广州 · 大学城',
      photos:[
        {src:'', cap:'图书馆'},
        {src:'', cap:'中心花坛'},
        {src:'', cap:'教学楼群'}
      ],
      desc:'广州大学城的知识之门，工科与信息科学的创新沃土。现代化图书馆矗立其间，年轻学子在此探索前沿科技，与城市共生长。这里汇聚了工学、信息科学与部分社科学科，是中大新工科人才培养的核心阵地。',
      colleges:'法学院 · 政治与公共事务管理学院 · 管理学院 · 信息管理学院 · 工学院 · 材料科学与工程学院 · 电子与信息工程学院 · 计算机学院 · 环境科学与工程学院 · 国家保密学院 · 网络安全学院 · 系统科学与工程学院 等',
      address:'广州市番禺区大学城外环东路132号', area:'0.989 km²'
    },
    {
      name:'北校园', short:'广州', city:'广州 · 越秀',
      photos:[
        {src:'', cap:'中山医红楼'},
        {src:'', cap:'医学图书馆'},
        {src:'', cap:'校园全景'}
      ],
      desc:'珠江之滨的医学殿堂，中山医学院所在地。红楼掩映间，"救人救国救世"的誓言回响百年。作为中大医科传统优势的根基所在，这里汇聚了临床医学、口腔医学、公共卫生、药学与护理学等完整医学学科体系，培养了一代又一代医者。',
      colleges:'中山医学院 · 光华口腔医学院 · 公共卫生学院 · 药学院 · 护理学院',
      address:'广州市越秀区中山二路74号', area:'0.209 km²'
    },
    {
      name:'深圳校区', short:'深圳', city:'深圳 · 光明',
      photos:[
        {src:'', cap:'图书馆'},
        {src:'', cap:'红砖建筑群'},
        {src:'', cap:'校园全景'}
      ],
      desc:'山海之间的红砖新章，紧密契合深圳未来产业发展与创新驱动战略。6.8万平方米的图书馆藏书五百万册，是校区的知识心脏。这里着力发展医科与新型工科，与特区同频共振，是中大服务粤港澳大湾区建设的前沿阵地。',
      colleges:'医学院 · 公共卫生学院（深圳） · 药学院（深圳） · 材料学院 · 生物医学工程学院 · 电子与通信工程学院 · 智能工程学院 · 航空航天学院 · 农学院 · 生态学院 · 集成电路学院 · 先进制造学院 · 先进能源学院 · 网络空间安全学院 · 商学院 · 理学院',
      address:'深圳市光明区公常路66号', area:'3.143 km²'
    },
    {
      name:'珠海校区', short:'珠海', city:'珠海 · 唐家湾',
      photos:[
        {src:'', cap:'天琴中心'},
        {src:'', cap:'图书馆'},
        {src:'', cap:'若海'}
      ],
      desc:'南海之滨、凤凰山下，三面环山一面向海。天琴中心在此聆听宇宙的引力波，"深海、深空、深地、深蓝"四大学科群扎根于此。这里拥有天琴计划、南海研究院、"中山大学"号科考船等重大平台，仰望星空，脚踏实地，观天测地探海。',
      colleges:'中国语言文学系（珠海） · 历史学系（珠海） · 哲学系（珠海） · 国际金融学院 · 国际翻译学院 · 国际关系学院 · 旅游学院 · 数学学院（珠海） · 物理与天文学院 · 大气科学学院 · 海洋科学学院 · 地球科学与工程学院 · 化学工程与技术学院 · 海洋工程与技术学院 · 中法核工程与技术学院 · 土木工程学院 · 测绘科学与技术学院 · 微电子科学与技术学院 · 人工智能学院 · 软件工程学院',
      address:'珠海市唐家湾镇大学路2号', area:'3.571 km²'
    }
  ];

  (function(){
    var row = document.getElementById('campusRow');
    var letter = document.getElementById('campusLetter');
    var photosWrap = document.getElementById('letterPhotos');
    var sealBox = document.getElementById('letterSeal');
    var lightbox = document.getElementById('lightbox');
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

    // 生成精致印章 SVG
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
    }

    function renderPhotos(photos){
      photosWrap.innerHTML = '';
      photos.forEach(function(p){
        var div = document.createElement('div');
        div.className = 'polaroid';
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
    }

    function openLightbox(src, cap){
      if(!src) return;
      lightbox.querySelector('img').src = src;
      lightbox.querySelector('.lb-cap').textContent = cap || '';
      lightbox.classList.add('show');
    }
    function closeLightbox(){ lightbox.classList.remove('show'); }
    lightbox.querySelector('.lb-close').addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', function(e){ if(e.target === lightbox) closeLightbox(); });

    function openLetter(idx){
      activeIdx = idx;
      var d = CAMPUS_DATA[idx];
      renderPhotos(d.photos);
      letter.querySelector('.letter-city').textContent = d.city;
      letter.querySelector('.letter-name').textContent = d.name;
      letter.querySelector('.letter-desc').textContent = d.desc;
      letter.querySelector('.colleges-list').textContent = d.colleges;
      letter.querySelector('.letter-address').textContent = d.address;
      letter.querySelector('.letter-area').textContent = d.area;
      sealBox.innerHTML = sealSVG(d.name);
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

    document.addEventListener('click', function(e){
      if(activeIdx < 0) return;
      if(!e.target.closest('.campus-word') && !e.target.closest('.campus-letter') && !e.target.closest('.lightbox')){
        closeLetter();
      }
    });
    document.addEventListener('keydown', function(e){
      if(e.key === 'Escape'){
        if(lightbox.classList.contains('show')){ closeLightbox(); }
        else if(activeIdx >= 0){ closeLetter(); }
      }
    });
  })();

"""

html = html.replace(js_old, js_new, 1)

# 保存
with open(INDEX, "w", encoding="utf-8") as f:
    f.write(html)
print(f"v2 改进完成，index.html 大小: {len(html.encode('utf-8'))} bytes")
