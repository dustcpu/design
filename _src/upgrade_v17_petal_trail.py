# -*- coding: utf-8 -*-
"""v17：移植Geometric Islands春主题桃花瓣鼠标拖尾到招生概念站
- 独立overlay canvas，position:fixed，z-index:50，pointer-events:none
- 只保留春主题（粉色桃花瓣，1/8概率五瓣小桃花）
- 帧率无关的粒子系统，出生淡入+消亡淡出
"""
import re

INDEX = r"E:\壁纸大赛\招生概念站\index.html"

with open(INDEX, encoding='utf-8') as f:
    html = f.read()

# ===== 1. 插入CSS（在</style>前）=====
css = """  /* 鼠标花瓣拖尾 canvas */
  .mouse-trail-canvas{
    position:fixed;inset:0;width:100vw;height:100vh;
    z-index:50;pointer-events:none;
  }
"""

if '.mouse-trail-canvas' not in html:
    html = html.replace('</style>', css + '</style>', 1)
    print("CSS已插入")
else:
    print("CSS已存在，跳过")

# ===== 2. 插入JavaScript（在</body>前）=====
js = """  <!-- 春主题桃花瓣鼠标拖尾（移植自Geometric Islands） -->
  <script>
  (function(){
    var MAX_PARTICLES = 60;
    var IDLE_MS = 100;
    function rand(a,b){return a+Math.random()*(b-a);}

    var CFG = {
      rate:[20,28], life:[45,62], size:[2.4,4.4],
      color:'#f8c8d8',
      vx:[-16,16], vy:[-14,7], gravity:14, drag:0.955,
      rotSpeed:[-3.4,3.4], sway:6, swayFreq:[1.2,2.2]
    };

    var overlay = document.createElement('canvas');
    overlay.className = 'mouse-trail-canvas';
    overlay.setAttribute('aria-hidden','true');
    document.body.appendChild(overlay);
    var ctx = overlay.getContext('2d');
    var W=0,H=0,DPR=1;

    function resize(){
      DPR = Math.min(window.devicePixelRatio||1, 2);
      W = window.innerWidth; H = window.innerHeight;
      overlay.width = Math.round(W*DPR);
      overlay.height = Math.round(H*DPR);
      overlay.style.width = W+'px';
      overlay.style.height = H+'px';
      ctx.setTransform(DPR,0,0,DPR,0,0);
    }
    resize();
    window.addEventListener('resize', resize);

    var particles = [];
    var curRate = 10, emitAcc = 0, wasEmpty = false;
    var mouse = {x:0,y:0,moving:false,has:false,lastMove:0};
    var reduced = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    window.addEventListener('mousemove', function(e){
      mouse.x = e.clientX; mouse.y = e.clientY;
      mouse.moving = true; mouse.has = true;
      mouse.lastMove = performance.now();
    }, {passive:true});
    document.addEventListener('mouseleave', function(){ mouse.moving = false; });

    function sampleRate(){ return rand(CFG.rate[0], CFG.rate[1]); }

    function evictIfFull(){
      if(particles.length < MAX_PARTICLES) return;
      var worst=0, worstLife=Infinity;
      for(var i=0;i<particles.length;i++){
        if(particles[i].life < worstLife){ worstLife=particles[i].life; worst=i; }
      }
      particles.splice(worst,1);
    }

    function spawn(x,y){
      var p = {
        x:x, y:y, vx:0, vy:0,
        size: rand(CFG.size[0], CFG.size[1]),
        rotation: Math.random()*Math.PI*2,
        rotSpeed: rand(CFG.rotSpeed[0], CFG.rotSpeed[1]),
        swayPhase: Math.random()*Math.PI*2,
        swayFreq: rand(CFG.swayFreq[0], CFG.swayFreq[1]),
        maxLife: rand(CFG.life[0], CFG.life[1])/60,
        life:0, alpha:0,
        floret: Math.random() < 0.125
      };
      p.life = p.maxLife;
      p.vx = rand(CFG.vx[0], CFG.vx[1]);
      p.vy = rand(CFG.vy[0], CFG.vy[1]);
      return p;
    }

    function update(dt){
      if(mouse.moving && performance.now()-mouse.lastMove > IDLE_MS) mouse.moving = false;

      if(!reduced && mouse.moving && mouse.has){
        emitAcc += curRate * dt;
        while(emitAcc >= 1){
          emitAcc -= 1;
          evictIfFull();
          particles.push(spawn(mouse.x, mouse.y));
          curRate = sampleRate();
        }
      } else { emitAcc = 0; }

      for(var i=particles.length-1;i>=0;i--){
        var p = particles[i];
        var dragF = Math.pow(CFG.drag, dt*60);
        p.life -= dt;
        if(p.life <= 0){ particles.splice(i,1); continue; }
        p.vy += CFG.gravity * dt;
        p.vx *= dragF; p.vy *= dragF;
        p.swayPhase += p.swayFreq * dt;
        p.x += (p.vx + Math.sin(p.swayPhase)*CFG.sway) * dt;
        p.y += p.vy * dt;
        p.rotation += p.rotSpeed * dt;
        var k = p.life / p.maxLife;
        p.alpha = Math.max(0, Math.min(1, (1-k)/0.2, k/0.35));
      }
    }

    function petalPath(s){
      ctx.beginPath();
      ctx.moveTo(0, s*1.3);
      ctx.bezierCurveTo(-s*1.15, s*0.85, -s*1.2, -s*0.55, -s*0.3, -s*1.35);
      ctx.lineTo(0, -s*1.02);
      ctx.lineTo(s*0.3, -s*1.35);
      ctx.bezierCurveTo(s*1.2, -s*0.55, s*1.15, s*0.85, 0, s*1.3);
      ctx.closePath();
    }

    function drawPetal(p){
      var s = p.size;
      ctx.save();
      ctx.translate(p.x, p.y);
      ctx.rotate(p.rotation);
      ctx.globalAlpha = p.alpha;
      var grad = ctx.createLinearGradient(0, s*1.3, 0, -s*1.35);
      grad.addColorStop(0, '#fdeef4');
      grad.addColorStop(1, CFG.color);
      ctx.fillStyle = grad;
      petalPath(s);
      ctx.fill();
      ctx.restore();
    }

    function drawFloret(p){
      var s = p.size * 0.55;
      ctx.save();
      ctx.translate(p.x, p.y);
      ctx.rotate(p.rotation);
      ctx.globalAlpha = p.alpha;
      var grad = ctx.createLinearGradient(0, s*1.3, 0, -s*1.35);
      grad.addColorStop(0, '#fdeef4');
      grad.addColorStop(1, CFG.color);
      ctx.fillStyle = grad;
      for(var i=0;i<5;i++){
        ctx.rotate(Math.PI*2/5);
        petalPath(s);
        ctx.fill();
      }
      ctx.fillStyle = '#f5d76e';
      for(var j=0;j<5;j++){
        var ang = j*Math.PI*2/5 + 0.3;
        ctx.beginPath();
        ctx.arc(Math.cos(ang)*s*0.5, Math.sin(ang)*s*0.5, s*0.18, 0, Math.PI*2);
        ctx.fill();
      }
      ctx.restore();
    }

    function draw(){
      if(!particles.length){
        if(!wasEmpty){ ctx.clearRect(0,0,W,H); wasEmpty=true; }
        return;
      }
      wasEmpty = false;
      ctx.clearRect(0,0,W,H);
      for(var i=0;i<particles.length;i++){
        var p = particles[i];
        if(p.floret) drawFloret(p); else drawPetal(p);
      }
    }

    var last = performance.now();
    function frame(now){
      requestAnimationFrame(frame);
      if(document.hidden){ last=now; return; }
      var dt = Math.min((now-last)/1000, 0.05);
      last = now;
      update(dt);
      draw();
    }
    requestAnimationFrame(frame);
  })();
  </script>
"""

if 'mouse-trail-canvas' not in html.split('</body>')[0] or '春主题桃花瓣鼠标拖尾' not in html:
    html = html.replace('</body>', js + '\n</body>', 1)
    print("JavaScript已插入")
else:
    print("JavaScript已存在，跳过")

# 保存
with open(INDEX, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nv17 完成，index.html 大小: {len(html.encode('utf-8'))} bytes")
