# -*- coding: utf-8 -*-
"""将 campus-ink-ligen-demo.html 的五校园隶书字形静态整合进 index.html"""
import re

DEMO = r"E:\壁纸大赛\招生概念站\demos\campus-ink-ligen-demo.html"
INDEX = r"E:\壁纸大赛\招生概念站\index.html"

# 1. 提取 GLYPH_IMAGES 行
with open(DEMO, encoding="utf-8") as f:
    demo = f.read()
m = re.search(r"(var GLYPH_IMAGES = \{.*?\};)", demo, re.DOTALL)
assert m, "未找到 GLYPH_IMAGES"
glyph_line = m.group(1)
print(f"GLYPH_IMAGES 长度: {len(glyph_line)} 字符")

# 2. 读 index.html
with open(INDEX, encoding="utf-8") as f:
    html = f.read()

# 3. 替换 CSS：.campus-row 样式块 -> 隶书字形样式
old_css = """  /* ===== 五校园长廊 ===== */
  .campus-row{display:grid;grid-template-columns:repeat(5,1fr);gap:24px}
  .bldg.pre{opacity:0;transform:translateY(24px);transition:opacity .7s ease,transform .7s ease}
  .bldg.in{opacity:1;transform:none}
  .bldg img{width:100%;aspect-ratio:1;object-fit:contain;border-radius:4px}
  .bldg .place{margin-top:14px;font-size:12px;letter-spacing:.2em;color:var(--brick);font-weight:700}
  .bldg h4{margin-top:3px;font-family:'Noto Serif SC',serif;font-size:17px;font-weight:700}
  .bldg p{margin-top:5px;font-size:13px;color:#4a5f50;font-weight:300}"""

new_css = """  /* ===== 五校园 · 隶书字形 ===== */
  .campus-ink-row{
    display:flex;align-items:flex-start;justify-content:center;
    gap:clamp(20px,4vw,80px);margin-top:48px;
    --cs:clamp(40px,5.5vw,72px);
    --chh:calc(var(--cs) * 1.4545);
  }
  .campus-word{
    appearance:none;background:none;border:0;padding:0;font-family:inherit;
    cursor:pointer;display:flex;flex-direction:column;align-items:center;
  }
  .campus-word::before{
    content:'';width:4px;height:4px;border-radius:50%;background:var(--gold);
    opacity:.75;margin-bottom:calc(var(--cs)*.30);transition:transform .2s,opacity .2s;
  }
  .campus-word:hover::before{transform:scale(1.6);opacity:1}
  .campus-word:hover .campus-ch{color:#14382A}
  .campus-stack{
    display:flex;flex-direction:column;justify-content:center;align-items:center;
    gap:calc(var(--cs)*.06);
  }
  .campus-ch{display:block;width:var(--cs);height:var(--chh);color:var(--green);transition:color .2s}
  .campus-ch svg{display:block;width:100%;height:100%;overflow:visible}
  .campus-place{margin-top:calc(var(--cs)*.24);font-size:11px;letter-spacing:.28em;color:#96A096}"""

assert old_css in html, "未找到旧 .campus-row CSS"
html = html.replace(old_css, new_css)

# 4. 替换响应式里的 .campus-row 引用
html = html.replace("    .campus-row{grid-template-columns:repeat(3,1fr)}",
                    "    .campus-ink-row{--cs:clamp(32px,4.5vw,52px);gap:16px}")
html = html.replace("    .campus-row{grid-template-columns:repeat(2,1fr)}",
                    "    .campus-ink-row{--cs:clamp(26px,8vw,40px);gap:10px;flex-wrap:wrap}")

# 5. 替换 HTML：.campus-row 整块 -> .campus-ink-row
old_html = """  <div class="campus-row">
    <div class="bldg">
      <img src="assets/campus-nan.png" alt="南校园怀士堂">
      <div class="place">广州 · 南校园</div>
      <h4>怀士堂</h4>
      <p>红砖绿瓦，百年礼堂。</p>
    </div>
    <div class="bldg">
      <img src="assets/campus-bei.png" alt="北校园中山医红楼">
      <div class="place">广州 · 北校园</div>
      <h4>中山医红楼</h4>
      <p>救人救国救世。</p>
    </div>
    <div class="bldg">
      <img src="assets/campus-dong.png" alt="东校园图书馆">
      <div class="place">广州 · 东校园</div>
      <h4>图书馆</h4>
      <p>大学城的知识之门。</p>
    </div>
    <div class="bldg">
      <img src="assets/campus-shenzhen.png" alt="深圳校区图书馆">
      <div class="place">深圳校区</div>
      <h4>图书馆</h4>
      <p>山海之间，红砖新章。</p>
    </div>
    <div class="bldg">
      <img src="assets/campus-zhuhai.png" alt="珠海校区天琴中心">
      <div class="place">珠海校区</div>
      <h4>天琴中心</h4>
      <p>仰望星空，聆听引力波。</p>
    </div>
  </div>"""

new_html = """  <div class="campus-ink-row" id="campusRow"></div>"""

assert old_html in html, "未找到旧 .campus-row HTML"
html = html.replace(old_html, new_html)

# 6. 在 body 开头注入 SVG filter（sealInk）
svg_filter = """<svg class="svg-defs" aria-hidden="true" focusable="false" style="position:absolute;width:0;height:0;overflow:hidden">
  <defs>
    <filter id="sealInk" x="-14%" y="-14%" width="128%" height="128%" color-interpolation-filters="sRGB">
      <feTurbulence type="fractalNoise" baseFrequency="0.020" numOctaves="2" seed="9" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="4.5" xChannelSelector="R" yChannelSelector="G"/>
    </filter>
  </defs>
</svg>
"""
html = html.replace("<body>\n", "<body>\n" + svg_filter, 1)

# 7. 在 script 开头注入 GLYPH_IMAGES + 渲染逻辑
campus_js = glyph_line + """

  /* ===== 五校园隶书字形渲染（静态，交互待做） ===== */
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
  })();
"""

# 在 <script>\n(function(){ 之后注入
script_anchor = "<script>\n(function(){"
assert script_anchor in html, "未找到 script 入口"
html = html.replace(script_anchor, script_anchor + "\n" + campus_js, 1)

# 8. 保存
with open(INDEX, "w", encoding="utf-8") as f:
    f.write(html)

print(f"整合完成，index.html 新大小: {len(html)} 字符 ({len(html.encode('utf-8'))} bytes)")
