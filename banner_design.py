#!/usr/bin/env python3
"""
横幅设计：西雅博才小学家长棒棒堂·智慧陪伴·共育花开
尺寸：300cm x 50cm (印刷级 300dpi → 35433 x 5906 px)
风格：温暖治愈、校园亲子主题
主色调：天蓝色、暖黄色、米白色
"""

from PIL import Image, ImageDraw, ImageFont
import math

# ── 画布尺寸 (300cm x 50cm @ 150dpi for manageable file size, still high quality) ──
DPI = 150
W = int(300 / 2.54 * DPI)   # ≈ 17717
H = int(50 / 2.54 * DPI)    # ≈ 2953
# Use moderate resolution for practical handling
W, H = 6000, 1000

# ── 颜色定义 ──
SKY_BLUE       = (108, 185, 240)    # 天蓝色
SKY_BLUE_LIGHT = (168, 215, 255)    # 浅天蓝
WARM_YELLOW    = (255, 200, 60)     # 暖黄色
WARM_YELLOW_L  = (255, 225, 120)    # 浅暖黄
CREAM_WHITE    = (255, 248, 235)    # 米白色
SOFT_GREEN     = (130, 200, 130)    # 柔和绿色
DARK_GREEN     = (80, 160, 80)      # 深绿
SOFT_ORANGE    = (255, 165, 80)     # 柔和橙
BROWN          = (160, 110, 60)     # 棕色
WHITE          = (255, 255, 255)
DARK_TEXT       = (50, 60, 80)      # 深色文字
MID_TEXT        = (80, 100, 130)    # 中间文字色

# ── 字体加载 ──
FONT_DIR = r'D:\Program Files\QClaw\resources\openclaw\config\skills\canvas-design\canvas-fonts'
SYS_FONT_DIR = r'C:\Windows\Fonts'

def load_font(size, bold=False):
    """优先使用微软雅黑（圆润端正），备选黑体"""
    if bold:
        paths = [
            f'{SYS_FONT_DIR}\\msyhbd.ttc',
            f'{SYS_FONT_DIR}\\simhei.ttf',
        ]
    else:
        paths = [
            f'{SYS_FONT_DIR}\\msyh.ttc',
            f'{SYS_FONT_DIR}\\simhei.ttf',
        ]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except:
            continue
    return ImageFont.load_default()

# ── 创建画布 ──
img = Image.new('RGB', (W, H), CREAM_WHITE)
draw = ImageDraw.Draw(img)

# ── 背景渐变 (天蓝到米白) ──
for y in range(H):
    ratio = y / H
    r = int(SKY_BLUE_LIGHT[0] * (1 - ratio) + CREAM_WHITE[0] * ratio)
    g = int(SKY_BLUE_LIGHT[1] * (1 - ratio) + CREAM_WHITE[1] * ratio)
    b = int(SKY_BLUE_LIGHT[2] * (1 - ratio) + CREAM_WHITE[2] * ratio)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# ── 装饰波浪底部 (柔和曲线) ──
wave_h = 80
for x in range(W):
    for dy in range(wave_h):
        y = H - wave_h + dy
        wave_y = math.sin(x / W * 2 * math.pi * 3) * 20 + (H - wave_h + 30)
        if y > wave_y:
            ratio2 = dy / wave_h
            cr = int(WARM_YELLOW_L[0] * (1-ratio2) + CREAM_WHITE[0] * ratio2)
            cg = int(WARM_YELLOW_L[1] * (1-ratio2) + CREAM_WHITE[1] * ratio2)
            cb = int(WARM_YELLOW_L[2] * (1-ratio2) + CREAM_WHITE[2] * ratio2)
            draw.point((x, y), fill=(cr, cg, cb))

# ── 绘制太阳 (右上角) ──
sun_cx, sun_cy = W - 350, 200
sun_r = 100
# 光芒
for i in range(12):
    angle = i * math.pi / 6
    x1 = sun_cx + math.cos(angle) * (sun_r + 20)
    y1 = sun_cy + math.sin(angle) * (sun_r + 20)
    x2 = sun_cx + math.cos(angle) * (sun_r + 65)
    y2 = sun_cy + math.sin(angle) * (sun_r + 65)
    draw.line([(x1, y1), (x2, y2)], fill=WARM_YELLOW, width=8)
# 太阳本体
for r_off in range(sun_r, 0, -1):
    ratio3 = r_off / sun_r
    cr = int(255 * ratio3 + WARM_YELLOW_L[0] * (1 - ratio3))
    cg = int(200 * ratio3 + WARM_YELLOW_L[1] * (1 - ratio3))
    cb = int(60 * ratio3 + WARM_YELLOW_L[2] * (1 - ratio3))
    draw.ellipse([sun_cx-r_off, sun_cy-r_off, sun_cx+r_off, sun_cy+r_off], fill=(cr, cg, cb))

# ── 绘制简约校园建筑 (左侧) ──
bx, by = 180, H - 280
# 主体
draw.rectangle([bx, by, bx+220, H-80], fill=SKY_BLUE, outline=SKY_BLUE_LIGHT)
# 屋顶三角
draw.polygon([(bx-15, by), (bx+110, by-80), (bx+235, by)], fill=SKY_BLUE)
# 门
draw.rectangle([bx+85, by+80, bx+135, H-80], fill=WARM_YELLOW)
# 窗户
for wx in [bx+25, bx+155]:
    for wy in [by+20, by+60]:
        draw.rectangle([wx, wy, wx+40, wy+30], fill=WARM_YELLOW_L, outline=SKY_BLUE_LIGHT, width=2)
# 旗帜
draw.line([(bx+110, by-80), (bx+110, by-160)], fill=DARK_TEXT, width=3)
draw.polygon([(bx+110, by-160), (bx+155, by-145), (bx+110, by-130)], fill=SOFT_ORANGE)

# ── 绘制书本 (左下) ──
book_x, book_y = 460, H - 200
# 左页
draw.polygon([(book_x, book_y), (book_x-50, book_y-15), (book_x-50, book_y+60), (book_x, book_y+50)], fill=WHITE, outline=SKY_BLUE, width=2)
# 右页
draw.polygon([(book_x, book_y), (book_x+50, book_y-15), (book_x+50, book_y+60), (book_x, book_y+50)], fill=WHITE, outline=SKY_BLUE, width=2)
# 书脊
draw.line([(book_x, book_y), (book_x, book_y+50)], fill=SKY_BLUE, width=3)
# 书页线条
for i in range(3):
    ly = book_y + 10 + i * 12
    draw.line([(book_x-42, ly), (book_x-8, ly+2)], fill=SKY_BLUE_LIGHT, width=1)
    draw.line([(book_x+8, ly+2), (book_x+42, ly)], fill=SKY_BLUE_LIGHT, width=1)

# ── 绘制树苗 (书本上方) ──
stem_x, stem_y = book_x, book_y - 10
# 茎
draw.line([(stem_x, stem_y), (stem_x, stem_y-70)], fill=DARK_GREEN, width=4)
# 叶子
for angle_deg in [-40, -15, 15, 40]:
    angle = math.radians(angle_deg)
    lx = stem_x + math.sin(angle) * 35
    ly = stem_y - 50 - math.cos(angle) * 20
    draw.ellipse([lx-18, ly-10, lx+18, ly+10], fill=SOFT_GREEN)

# ── 绘制花朵 (右侧) ──
def draw_flower(cx, cy, petal_r, color, petal_n=5):
    for i in range(petal_n):
        angle = i * 2 * math.pi / petal_n
        px = cx + math.cos(angle) * petal_r * 0.7
        py = cy + math.sin(angle) * petal_r * 0.7
        draw.ellipse([px-petal_r*0.5, py-petal_r*0.5, px+petal_r*0.5, py+petal_r*0.5], fill=color)
    draw.ellipse([cx-petal_r*0.3, cy-petal_r*0.3, cx+petal_r*0.3, cy+petal_r*0.3], fill=WARM_YELLOW)

# 花朵1
draw_flower(W-600, H-220, 30, (255, 160, 180))
# 花茎
draw.line([(W-600, H-190), (W-600, H-80)], fill=DARK_GREEN, width=3)
draw.ellipse([W-615, H-100, W-585, H-80], fill=SOFT_GREEN)
# 花朵2
draw_flower(W-530, H-180, 22, (255, 200, 160))
draw.line([(W-530, H-158), (W-530, H-80)], fill=DARK_GREEN, width=3)
# 花朵3
draw_flower(W-480, H-200, 18, (200, 160, 255))
draw.line([(W-480, H-182), (W-480, H-80)], fill=DARK_GREEN, width=2)

# ── 绘制大手牵小手 (右侧区域) ──
hand_cx, hand_cy = W - 850, H // 2 + 30

def draw_hand(cx, cy, scale, color):
    """绘制简约手掌"""
    s = scale
    # 手掌
    draw.ellipse([cx-s*40, cy-s*20, cx+s*40, cy+s*40], fill=color)
    # 手指 (5根) - (fx, fy_top, fy_bottom) relative to palm center
    fingers = [
        (-30, -90, -20),   # 小指
        (-12, -100, -20),  # 无名指
        (5, -105, -20),    # 中指
        (22, -95, -20),    # 食指
    ]
    for fx, fy_top, fy_bot in fingers:
        x0 = cx + s*fx - s*8
        y0 = cy + s*fy_top
        x1 = cx + s*fx + s*8
        y1 = cy + s*fy_bot
        if y1 < y0:
            y0, y1 = y1, y0
        draw.rounded_rectangle([x0, y0, x1, y1], radius=int(s*6), fill=color)
    # 拇指
    tx0 = cx + s*30
    ty0 = cy + s*(-45)
    tx1 = cx + s*58
    ty1 = cy + s*(-15)
    if ty1 < ty0:
        ty0, ty1 = ty1, ty0
    draw.rounded_rectangle([tx0, ty0, tx1, ty1], radius=int(s*6), fill=color)

# 大手 (成人 - 天蓝色)
draw_hand(hand_cx - 60, hand_cy, 1.0, SKY_BLUE)
# 小手 (儿童 - 暖黄色，略偏右上方)
draw_hand(hand_cx + 30, hand_cy - 40, 0.6, WARM_YELLOW)

# 连接的心形 (大手小手之间)
heart_cx = hand_cx - 10
heart_cy = hand_cy - 70
def draw_heart(cx, cy, size, color):
    # 左半圆
    draw.pieslice([cx-size, cy-size, cx, cy+size//2], 180, 360, fill=color)
    # 右半圆
    draw.pieslice([cx, cy-size, cx+size, cy+size//2], 180, 360, fill=color)
    # 下方三角
    draw.polygon([(cx-size, cy), (cx+size, cy), (cx, cy+size*1.3)], fill=color)

draw_heart(heart_cx, heart_cy, 18, (255, 130, 150))

# ── 小草装饰 (底部) ──
for gx in range(0, W, 60):
    gh = 15 + (gx * 7 % 20)
    draw.line([(gx, H-80), (gx-5, H-80-gh)], fill=SOFT_GREEN, width=2)
    draw.line([(gx, H-80), (gx+5, H-80-gh-5)], fill=DARK_GREEN, width=2)

# ── 云朵装饰 (顶部) ──
def draw_cloud(cx, cy, size, color):
    offsets = [(-size, 0), (0, -size*0.4), (size, 0), (size*0.5, -size*0.3), (-size*0.5, -size*0.3)]
    for ox, oy in offsets:
        r = size * 0.55
        draw.ellipse([cx+ox-r, cy+oy-r, cx+ox+r, cy+oy+r], fill=color)

draw_cloud(400, 120, 50, (240, 248, 255))
draw_cloud(W-1100, 100, 40, (240, 248, 255))
draw_cloud(W//2 - 200, 80, 35, (245, 250, 255))

# ── 主标题文字 ──
main_text = "西雅博才小学"
sub_text = "家长棒棒堂"
slogan = "智慧陪伴 · 共育花开"

# 主标题字体
title_font = load_font(180, bold=True)
sub_font = load_font(150, bold=True)
slogan_font = load_font(90, bold=False)

# 计算文字位置 (居中)
title_bbox = draw.textbbox((0, 0), main_text, font=title_font)
title_w = title_bbox[2] - title_bbox[0]
title_x = (W - title_w) // 2
title_y = 150

# 文字阴影 + 主文字
shadow_offset = 4
draw.text((title_x + shadow_offset, title_y + shadow_offset), main_text, font=title_font, fill=(180, 200, 220))
draw.text((title_x, title_y), main_text, font=title_font, fill=DARK_TEXT)

# 副标题
sub_bbox = draw.textbbox((0, 0), sub_text, font=sub_font)
sub_w = sub_bbox[2] - sub_bbox[0]
sub_x = (W - sub_w) // 2
sub_y = title_y + 220

# 彩色副标题 (天蓝色)
draw.text((sub_x + shadow_offset, sub_y + shadow_offset), sub_text, font=sub_font, fill=(150, 180, 210))
draw.text((sub_x, sub_y), sub_text, font=sub_font, fill=SKY_BLUE)

# 口号
slogan_bbox = draw.textbbox((0, 0), slogan, font=slogan_font)
slogan_w = slogan_bbox[2] - slogan_bbox[0]
slogan_x = (W - slogan_w) // 2
slogan_y = sub_y + 200

draw.text((slogan_x + shadow_offset, slogan_y + shadow_offset), slogan, font=slogan_font, fill=(180, 190, 200))
draw.text((slogan_x, slogan_y), slogan, font=slogan_font, fill=WARM_YELLOW)

# ── 口号下方装饰线 ──
line_y = slogan_y + 120
line_w = slogan_w + 60
line_x = (W - line_w) // 2
# 渐变装饰线
for x in range(line_w):
    ratio = abs(x - line_w/2) / (line_w/2)
    cr = int(SKY_BLUE[0] * (1-ratio) + WARM_YELLOW[0] * ratio)
    cg = int(SKY_BLUE[1] * (1-ratio) + WARM_YELLOW[1] * ratio)
    cb = int(SKY_BLUE[2] * (1-ratio) + WARM_YELLOW[2] * ratio)
    draw.line([(line_x + x, line_y), (line_x + x, line_y + 4)], fill=(cr, cg, cb))

# ── 星星/点缀装饰 ──
def draw_star(cx, cy, size, color):
    points = []
    for i in range(10):
        angle = math.pi / 2 + i * math.pi / 5
        r = size if i % 2 == 0 else size * 0.4
        points.append((cx + math.cos(angle) * r, cy - math.sin(angle) * r))
    draw.polygon(points, fill=color)

draw_star(title_x - 80, title_y + 60, 15, WARM_YELLOW)
draw_star(title_x + title_w + 60, title_y + 60, 15, WARM_YELLOW)
draw_star(sub_x - 60, sub_y + 70, 12, SOFT_ORANGE)
draw_star(sub_x + sub_w + 40, sub_y + 70, 12, SOFT_ORANGE)
draw_star(slogan_x - 50, slogan_y + 40, 10, (255, 180, 200))
draw_star(slogan_x + slogan_w + 30, slogan_y + 40, 10, (255, 180, 200))

# ── 圆点装饰 ──
dots = [(300, 500, 8), (5700, 450, 6), (800, 900, 5), (5200, 850, 7), (1500, 150, 4), (4500, 130, 5)]
for dx, dy, dr in dots:
    draw.ellipse([dx-dr, dy-dr, dx+dr, dy+dr], fill=SKY_BLUE_LIGHT)

# ── 保存 ──
output_path = r'C:\Users\erica\.qclaw\workspace-agent-60546543\家长棒棒堂横幅.png'
img.save(output_path, 'PNG', dpi=(150, 150))
print(f'横幅已保存: {output_path}')
print(f'尺寸: {W} x {H} px')
