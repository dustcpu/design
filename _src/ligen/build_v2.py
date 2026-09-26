#!/usr/bin/env python3
"""
生成新版本的隶书demo（信封+信纸堆+照片堆）
"""
import os
import base64
import json

# 仓库根目录 = 本文件的上两级
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PNG_DIR = os.path.join(PROJECT_DIR, '_src', 'ligen', 'processed')
TEMPLATE = os.path.join(PROJECT_DIR, '_src', 'ligen', 'template_v2.html')
OUTPUT = os.path.join(PROJECT_DIR, 'campus-ink-ligen-demo.html')

def png_to_base64(filepath):
    with open(filepath, 'rb') as f:
        data = f.read()
    b64 = base64.b64encode(data).decode('utf-8')
    return f'data:image/png;base64,{b64}'

def main():
    # 读取所有PNG
    chars = ['南', '东', '北', '深', '圳', '珠', '海', '校', '园', '区']
    glyph_images = {}
    for char in chars:
        png_path = os.path.join(PNG_DIR, f'{char}.png')
        if os.path.exists(png_path):
            glyph_images[char] = png_to_base64(png_path)
    
    # 读取模板
    with open(TEMPLATE, 'r', encoding='utf-8') as f:
        html = f.read()
    
    # 注入字形数据
    glyph_js = json.dumps(glyph_images, ensure_ascii=False)
    html = html.replace('/*__GLYPHS__*/{}', glyph_js)
    
    # 保存
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(html)
    
    size_kb = os.path.getsize(OUTPUT) // 1024
    print(f"完成！输出: {OUTPUT}")
    print(f"文件大小: {size_kb} KB")

if __name__ == '__main__':
    main()
