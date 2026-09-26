#!/usr/bin/env python3
"""
生成隶书版本的campus-ink-demo
直接基于 campus-ink-demo.html 修改，用PNG图片替换SVG笔画
"""
import os
import base64
import re

# 仓库根目录 = 本文件的上两级
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PNG_DIR = os.path.join(PROJECT_DIR, '_src', 'ligen', 'processed')
INPUT = os.path.join(PROJECT_DIR, 'campus-ink-demo.html')
OUTPUT = os.path.join(PROJECT_DIR, 'campus-ink-ligen-demo.html')

def png_to_base64(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode('utf-8')
    return f'data:image/png;base64,{b64}'


def main():
    print("生成隶书版demo...")
    
    # 读取原demo
    with open(INPUT, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 读取所有PNG
    chars = ['南', '东', '北', '深', '圳', '珠', '海', '校', '园', '区']
    glyph_images = {}
    for char in chars:
        png_path = os.path.join(PNG_DIR, f'{char}.png')
        if os.path.exists(png_path):
            glyph_images[char] = png_to_base64(png_path)
            print(f"  加载 {char}.png")
    
    # 1. 替换 GLYPHS 变量定义
    # 找到 var GLYPHS = {...}; 这一行，替换成 GLYPH_IMAGES
    pattern = r'var GLYPHS = \{.*?\};'
    replacement = 'var GLYPH_IMAGES = ' + repr(glyph_images) + ';'
    # repr 会带引号，我们需要JSON格式
    import json
    replacement = 'var GLYPH_IMAGES = ' + json.dumps(glyph_images, ensure_ascii=False) + ';'
    html = re.sub(pattern, replacement, html, count=1, flags=re.DOTALL)
    
    # 2. 替换 glyphSVG 函数
    old_func_pattern = r'''function glyphSVG\(ch\)\{.*?\n  \}'''
    new_func = '''function glyphSVG(ch){
    var svg = document.createElementNS(NS,'svg');
    svg.setAttribute('viewBox','170 20 660 960');
    svg.setAttribute('aria-hidden','true');
    var g = document.createElementNS(NS,'g');
    g.setAttribute('filter','url(#sealInk)');
    var href = GLYPH_IMAGES[ch];
    if(href){
      var img = document.createElementNS(NS,'image');
      img.setAttribute('x', '170');
      img.setAttribute('y', '20');
      img.setAttribute('width', '660');
      img.setAttribute('height', '960');
      img.setAttribute('preserveAspectRatio','xMidYMid meet');
      img.setAttributeNS('http://www.w3.org/1999/xlink','href', href);
      g.appendChild(img);
    }
    svg.appendChild(g);
    return svg;
  }'''
    
    html = re.sub(old_func_pattern, new_func, html, count=1, flags=re.DOTALL)
    
    # 保存
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(html)
    
    size_kb = os.path.getsize(OUTPUT) // 1024
    print(f"\n完成！输出: {OUTPUT}")
    print(f"文件大小: {size_kb} KB")


if __name__ == '__main__':
    main()
