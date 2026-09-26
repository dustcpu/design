#!/usr/bin/env python3
"""
隶书字形提取脚本
从隶书图片中提取纯字形状，生成SVG path数据
保持现有系统的坐标系：viewBox 170 20 660 960
"""
import os
import json
import numpy as np
from PIL import Image, ImageFilter

# 图片和字的对应关系
CHAR_MAP = {
    'nan': '南',
    'dong': '东',
    'bei': '北',
    'xiao': '校',
    'yuan': '园',
    'shen': '深',
    'hai': '海',
    'zhu': '珠',
    'zhen': '圳',
    'qu': '区'
}

# 输出坐标系参数（与现有系统一致）
VIEWBOX_X = 170
VIEWBOX_Y = 20
VIEWBOX_W = 660
VIEWBOX_H = 960

INPUT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_JSON = os.path.join(os.path.dirname(INPUT_DIR), '..', 'seal-glyphs-ligen.json')
OUTPUT_PNG_DIR = os.path.join(INPUT_DIR, 'processed')

os.makedirs(OUTPUT_PNG_DIR, exist_ok=True)


def load_image(filepath):
    """加载图片，返回RGBA numpy数组"""
    img = Image.open(filepath).convert('RGBA')
    return np.array(img)


def extract_character(img_array, key=None):
    """
    从图片中提取字：
    1. 判断背景是浅色还是深色
    2. 二值化
    3. 裁剪到字的边界
    4. 特殊处理：去掉区字左边竖线、园字上面横线
    返回：(字的二值mask, 边界box)
    """
    # 转灰度
    gray = np.mean(img_array[:, :, :3], axis=2)
    
    # 判断背景亮度
    bg_sample = np.concatenate([
        gray[:10, :].flatten(),
        gray[-10:, :].flatten(),
        gray[:, :10].flatten(),
        gray[:, -10:].flatten()
    ])
    bg_brightness = np.median(bg_sample)
    
    # 二值化：背景亮则字暗，背景暗则字亮
    if bg_brightness > 128:
        # 浅色背景，深色字
        mask = gray < (bg_brightness - 40)
    else:
        # 深色背景，浅色字
        mask = gray > (bg_brightness + 40)
    
    # 特殊处理：区字去掉左边的竖线
    if key == 'qu':
        # 区字左边有一条竖虚线，直接从左边裁掉15%
        w = mask.shape[1]
        crop_left = int(w * 0.15)
        mask = mask[:, crop_left:]
        print(f"  去掉左边竖线（裁掉 {crop_left}px）")
    
    # 特殊处理：园字去掉上面的横线
    if key == 'yuan':
        # 园字上面有一条横线，直接从上面裁掉15%
        h = mask.shape[0]
        crop_top = int(h * 0.15)
        mask = mask[crop_top:, :]
        print(f"  去掉上面横线（裁掉 {crop_top}px）")
    
    # 找字的边界
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    
    if not rows.any() or not cols.any():
        return None, None
    
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    
    # 裁剪
    cropped_mask = mask[rmin:rmax+1, cmin:cmax+1]
    
    return cropped_mask, (rmin, rmax, cmin, cmax)


def dilate_mask(mask, iterations=1):
    """
    对二值mask做膨胀操作（加粗笔画）
    用简单的3x3核膨胀
    """
    result = mask.copy()
    h, w = mask.shape
    
    for _ in range(iterations):
        new_result = result.copy()
        # 上下左右四个方向各扩展一格
        new_result[1:, :] |= result[:-1, :]  # 下
        new_result[:-1, :] |= result[1:, :]  # 上
        new_result[:, 1:] |= result[:, :-1]  # 右
        new_result[:, :-1] |= result[:, 1:]  # 左
        result = new_result
    
    return result


def mask_to_svg_path(mask):
    """
    将二值mask转换为SVG path（fill风格）
    使用简单的轮廓追踪
    """
    h, w = mask.shape
    # 转为坐标列表
    ys, xs = np.where(mask)
    if len(xs) == 0:
        return ""
    
    # 简化：用边界矩形的近似路径
    # 更好的方法是轮廓追踪，但先用简单方法
    
    # 找所有行的左右边界
    path_parts = []
    for y in range(h):
        row = mask[y, :]
        if row.any():
            x_coords = np.where(row)[0]
            x_left, x_right = x_coords[0], x_coords[-1]
            path_parts.append((y, x_left, x_right))
    
    if not path_parts:
        return ""
    
    # 构建简单的矩形近似路径（上下边缘）
    top_y = path_parts[0][0]
    bottom_y = path_parts[-1][0]
    
    # 上边缘
    top_edge = []
    bottom_edge = []
    for y, xl, xr in path_parts:
        if y == top_y:
            top_edge.append((xl, xr))
        bottom_edge.append((xl, xr))
    
    # 简化：生成一个大致的轮廓路径
    # 先左边界从上到下，再右边界从下到上
    left_xs = [xl for _, xl, _ in path_parts]
    right_xs = [xr for _, _, xr in path_parts]
    ys_list = [y for y, _, _ in path_parts]
    
    # 简化路径点（每隔几个点取一个）
    step = max(1, len(ys_list) // 50)
    
    d = f"M {left_xs[0]} {ys_list[0]}"
    for i in range(1, len(ys_list), step):
        d += f" L {left_xs[i]} {ys_list[i]}"
    
    # 底部
    d += f" L {right_xs[-1]} {ys_list[-1]}"
    
    # 右边界从下到上
    for i in range(len(ys_list)-2, 0, -step):
        d += f" L {right_xs[i]} {ys_list[i]}"
    
    d += " Z"
    return d


def resize_to_viewbox(mask, target_w=VIEWBOX_W, target_h=VIEWBOX_H, padding=30):
    """
    将mask缩放到目标坐标系大小
    保持宽高比，居中放置
    """
    h, w = mask.shape
    
    # 计算缩放比例（保持宽高比，留出padding）
    avail_w = target_w - 2 * padding
    avail_h = target_h - 2 * padding
    
    scale = min(avail_w / w, avail_h / h)
    new_w = int(w * scale)
    new_h = int(h * scale)
    
    # 居中
    offset_x = (target_w - new_w) / 2
    offset_y = (target_h - new_h) / 2
    
    # 创建目标大小的mask
    result = np.zeros((target_h, target_w), dtype=bool)
    
    # 用PIL缩放mask
    mask_img = Image.fromarray((mask * 255).astype(np.uint8))
    mask_resized = mask_img.resize((new_w, new_h), Image.LANCZOS)
    mask_resized = np.array(mask_resized) > 127
    
    # 放置到目标位置
    y_start = int(offset_y)
    x_start = int(offset_x)
    result[y_start:y_start+new_h, x_start:x_start+new_w] = mask_resized
    
    return result, scale, offset_x, offset_y


def process_character(key, char_name):
    """处理单个字"""
    filepath = os.path.join(INPUT_DIR, f'{key}.jpg')
    if not os.path.exists(filepath):
        print(f"  跳过 {char_name}: 文件不存在")
        return None
    
    print(f"处理 {char_name} ({key})...")
    img = load_image(filepath)
    mask, bbox = extract_character(img, key=key)
    
    if mask is None:
        print(f"  警告: 未能从 {char_name} 提取到字")
        return None
    
    # 圳字加粗笔画
    if key == 'zhen':
        mask = dilate_mask(mask, iterations=2)
        print(f"  加粗笔画")
    
    print(f"  原始尺寸: {mask.shape[1]}x{mask.shape[0]}")
    
    # 缩放到目标坐标系
    resized_mask, scale, off_x, off_y = resize_to_viewbox(mask)
    print(f"  缩放比例: {scale:.3f}, 偏移: ({off_x:.1f}, {off_y:.1f})")
    
    # 保存处理后的PNG（透明背景）
    h, w = resized_mask.shape
    rgba = np.zeros((h, w, 4), dtype=np.uint8)
    rgba[resized_mask, 0] = 47   # R
    rgba[resized_mask, 1] = 93   # G (--green: #2F5D46)
    rgba[resized_mask, 2] = 70   # B
    rgba[resized_mask, 3] = 255  # A
    
    out_img = Image.fromarray(rgba, 'RGBA')
    png_path = os.path.join(OUTPUT_PNG_DIR, f'{char_name}.png')
    out_img.save(png_path)
    print(f"  已保存: {png_path}")
    
    # 生成SVG path
    path = mask_to_svg_path(resized_mask)
    
    return {
        'char': char_name,
        'path': path,
        'scale': scale,
        'offset_x': off_x,
        'offset_y': off_y
    }


def main():
    print("=" * 50)
    print("隶书字形提取")
    print("=" * 50)
    
    results = {}
    for key, char_name in CHAR_MAP.items():
        result = process_character(key, char_name)
        if result:
            results[char_name] = result
    
    # 保存JSON
    output = {}
    for char_name, data in results.items():
        output[char_name] = data['path']
    
    json_path = os.path.abspath(OUTPUT_JSON)
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n完成！共处理 {len(results)} 个字")
    print(f"JSON输出: {json_path}")
    print(f"PNG输出目录: {OUTPUT_PNG_DIR}")


if __name__ == '__main__':
    main()
