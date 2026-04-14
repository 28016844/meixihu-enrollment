#!/usr/bin/env python3
"""
横幅设计 V3 精修版：西雅博才小学家长棒棒堂·智慧陪伴·共育花开
尺寸：300cm x 50cm (11811 x 1969 px @ 100dpi)
风格：温暖治愈、校园亲子主题
主色调：天蓝色、暖黄色、米白色
精修重点：整体视觉平衡、元素精致化、文字排版大气居中
"""

from PIL import Image, ImageDraw, ImageFont
import math, random

# ── 画布 ──
W, H = 11811, 1969

# ── 颜色 ──
SKY_BLUE       = (92, 172, 235)
SKY_BLUE_DEEP  = (55, 135, 205)
SKY_BLUE_LIGHT = (170, 218, 255)
SKY_BLUE_PALE  = (210, 235, 255)
WARM_YELLOW    = (255, 198, 55)
WARM_YELLOW_L  = (255, 230, 140)
WARM_ORANGE    = (255, 175, 80)
CREAM_WHITE    = (255, 250, 240)
SOFT_GREEN     = (115, 195, 115)
DARK_GREEN     = (70, 150, 70)
LEAF_GREEN     = (85, 170, 85)
PINK           = (255, 155, 180)
LIGHT_PINK     = (255, 200, 215)
LAVENDER       = (195, 165, 245)
WHITE          = (255, 255, 255)
DARK_TEXT       = (40, 50, 70)
BLUE_TEXT       = (45, 105, 175)
AMBER          = (220, 155, 50)

# ── 字体 ──
SYS_FONT_DIR = r'C:\Windows\Fonts'

def load_font(size, bold=False):
    if bold:
        paths = [f'{SYS_FONT_DIR}\\msyhbd.ttc', f'{SYS_FONT_DIR}\\simhei.ttf']
    else:
        paths = [f'{SYS_FONT_DIR}\\msyh.ttc', f'{SYS_FONT_DIR}\\simhei.ttf']
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except:
            continue
    return ImageFont.load_default()

img = Image.new('RGB', (W, H), CREAM_WHITE)
draw = ImageDraw.Draw(img)

# ══════════════════════════════════════════════════
# 1. 背景渐变 (天蓝上方 → 米白下方)
# ══════════════════════════════════════════════════
for y in range(H):
    t = y / H
    # 三段渐变：天蓝 → 浅蓝 → 米白
    if t < 0.3:
        r2 = t / 0.3
        r = int(SKY_BLUE_LIGHT[0] * (1-r2) + SKY_BLUE_PALE[0] * r2)
        g = int(SKY_BLUE_LIGHT[1] * (1-r2) + SKY_BLUE_PALE[1] * r2)
        b = int(SKY_BLUE_LIGHT[2] * (1-r2) + SKY_BLUE_PALE[2] * r2)
    else:
        r2 = (t - 0.3) / 0.7
        r = int(SKY_BLUE_PALE[0] * (1-r2) + CREAM_WHITE[0] * r2)
        g = int(SKY_BLUE_PALE[1] * (1-r2) + CREAM_WHITE[1] * r2)
        b = int(SKY_BLUE_PALE[2] * (1-r2) + CREAM_WHITE[2] * r2)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# ══════════════════════════════════════════════════
# 2. 顶部装饰条 (天蓝到暖黄渐变)
# ══════════════════════════════════════════════════
bar_h = 14
for x in range(W):
    t = abs(x - W/2) / (W/2)
    cr = int(SKY_BLUE[0] * t + WARM_YELLOW[0] * (1-t))
    cg = int(SKY_BLUE[1] * t + WARM_YELLOW[1] * (1-t))
    cb = int(SKY_BLUE[2] * t + WARM_YELLOW[2] * (1-t))
    draw.line([(x, 0), (x, bar_h)], fill=(cr, cg, cb))

# ══════════════════════════════════════════════════
# 3. 太阳 (右上)
# ══════════════════════════════════════════════════
sun_cx, sun_cy = W - 700, 380
sun_r = 160
# 柔和光晕
for ro in range(sun_r + 100, sun_r, -2):
    alpha = 1 - (ro - sun_r) / 100
    cr = int(255 * alpha + SKY_BLUE_PALE[0] * (1-alpha))
    cg = int(240 * alpha + SKY_BLUE_PALE[1] * (1-alpha))
    cb = int(160 * alpha + SKY_BLUE_PALE[2] * (1-alpha))
    draw.ellipse([sun_cx-ro, sun_cy-ro, sun_cx+ro, sun_cy+ro], fill=(cr, cg, cb))
# 光芒
for i in range(20):
    angle = i * math.pi / 10
    x1 = sun_cx + math.cos(angle) * (sun_r + 20)
    y1 = sun_cy + math.sin(angle) * (sun_r + 20)
    length = 70 + (i % 2) * 25
    x2 = sun_cx + math.cos(angle) * (sun_r + length)
    y2 = sun_cy + math.sin(angle) * (sun_r + length)
    draw.line([(x1, y1), (x2, y2)], fill=WARM_YELLOW, width=5)
# 本体
for ro in range(sun_r, 0, -1):
    t = ro / sun_r
    cr = int(255 * t + 255 * (1-t))
    cg = int(215 * t + 245 * (1-t))
    cb = int(50 * t + 170 * (1-t))
    draw.ellipse([sun_cx-ro, sun_cy-ro, sun_cx+ro, sun_cy+ro], fill=(cr, cg, cb))

# ══════════════════════════════════════════════════
# 4. 云朵
# ══════════════════════════════════════════════════
def draw_cloud(cx, cy, scale):
    parts = [(-1.0, 0, 0.55), (-0.35, -0.45, 0.7), (0.4, -0.35, 0.65), (1.1, 0, 0.5), (-0.1, 0.05, 0.5)]
    for ox, oy, rs in parts:
        r = scale * rs
        draw.ellipse([cx+ox*scale-r, cy+oy*scale-r, cx+ox*scale+r, cy+oy*scale+r], fill=(248, 252, 255))

draw_cloud(700, 250, 80)
draw_cloud(2200, 200, 55)
draw_cloud(W - 1500, 220, 65)
draw_cloud(W//2 + 600, 180, 50)

# ══════════════════════════════════════════════════
# 5. 底部草地 + 波浪
# ══════════════════════════════════════════════════
grass_top = H - 280
for y in range(grass_top, H):
    t = (y - grass_top) / 280
    r = int(CREAM_WHITE[0] * (1-t) + 140 * t)
    g = int(CREAM_WHITE[1] * (1-t) + 210 * t)
    b = int(CREAM_WHITE[2] * (1-t) + 140 * t)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# 波浪
for x in range(W):
    wy = int(math.sin(x / W * 5 * math.pi) * 15 + grass_top)
    for dy in range(10):
        if wy + dy < H:
            draw.point((x, wy + dy), fill=DARK_GREEN)

# 小草
random.seed(42)
for gx in range(0, W, 50):
    gh = random.randint(12, 30)
    lean = random.randint(-5, 5)
    base_y = grass_top + random.randint(-2, 8)
    draw.line([(gx, base_y), (gx + lean, base_y - gh)], fill=DARK_GREEN, width=2)

# ══════════════════════════════════════════════════
# 6. 简约校园建筑 (左侧)
# ══════════════════════════════════════════════════
bx, by = 300, H - 580
# 主楼
draw.rectangle([bx, by, bx+340, H-280], fill=SKY_BLUE, outline=SKY_BLUE_DEEP, width=3)
# 屋顶
draw.polygon([(bx-25, by), (bx+170, by-120), (bx+365, by)], fill=SKY_BLUE_DEEP)
# 钟窗
draw.polygon([(bx+120, by-60), (bx+170, by-100), (bx+220, by-60)], fill=WARM_YELLOW)
# 门
draw.rectangle([bx+130, by+130, bx+210, H-280], fill=WARM_YELLOW_L, outline=AMBER, width=2)
draw.ellipse([bx+185, H-370, bx+198, H-355], fill=AMBER)
# 窗户
for wx_off in [35, 250]:
    for wy_off in [30, 100]:
        wx = bx + wx_off
        wy = by + wy_off
        draw.rectangle([wx, wy, wx+55, wy+45], fill=WARM_YELLOW_L, outline=SKY_BLUE_DEEP, width=2)
        draw.line([(wx+27, wy), (wx+27, wy+45)], fill=SKY_BLUE_DEEP, width=1)
        draw.line([(wx, wy+22), (wx+55, wy+22)], fill=SKY_BLUE_DEEP, width=1)
# 旗杆
draw.line([(bx+170, by-120), (bx+170, by-280)], fill=DARK_TEXT, width=4)
draw.polygon([(bx+170, by-280), (bx+230, by-260), (bx+170, by-240)], fill=WARM_ORANGE)

# ══════════════════════════════════════════════════
# 7. 书本 + 树苗
# ══════════════════════════════════════════════════
book_cx, book_cy = 920, H - 380
bw, bh = 90, 70
draw.polygon([
    (book_cx, book_cy+30), (book_cx-bw, book_cy-8), (book_cx-bw, book_cy+bh), (book_cx, book_cy+bh+20)
], fill=WHITE, outline=SKY_BLUE, width=3)
draw.polygon([
    (book_cx, book_cy+30), (book_cx+bw, book_cy-8), (book_cx+bw, book_cy+bh), (book_cx, book_cy+bh+20)
], fill=WHITE, outline=SKY_BLUE, width=3)
draw.line([(book_cx, book_cy+30), (book_cx, book_cy+bh+20)], fill=SKY_BLUE_DEEP, width=4)
for i in range(5):
    ly = book_cy + 12 + i * 12
    draw.line([(book_cx-bw+12, ly), (book_cx-10, ly+4)], fill=SKY_BLUE_LIGHT, width=1)
    draw.line([(book_cx+10, ly+4), (book_cx+bw-12, ly)], fill=SKY_BLUE_LIGHT, width=1)

# 树苗
stem_base = book_cy + 15
draw.line([(book_cx, stem_base), (book_cx, stem_base-130)], fill=DARK_GREEN, width=6)
for lx, ly, lw, lh in [(-55, stem_base-90, 28, 14), (45, stem_base-105, 24, 12),
                         (-35, stem_base-130, 20, 10), (40, stem_base-135, 18, 9)]:
    draw.ellipse([book_cx+lx-lw, ly-lh, book_cx+lx+lw, ly+lh], fill=LEAF_GREEN)
draw.ellipse([book_cx-8, stem_base-145, book_cx+8, stem_base-130], fill=SOFT_GREEN)

# ══════════════════════════════════════════════════
# 8. 大手牵小手 (右侧)
# ══════════════════════════════════════════════════
hc_x = W - 1200
hc_y = H // 2 + 80

def draw_simple_hand(cx, cy, scale, color, is_child=False):
    s = scale
    pw, ph = 80*s, 60*s
    draw.rounded_rectangle([cx-pw/2, cy, cx+pw/2, cy+ph], radius=18*s, fill=color)
    finger_w = 16 * s
    finger_h = 50 * s if not is_child else 35 * s
    spacing = 19 * s
    start_x = cx - spacing * 1.5
    for i in range(4):
        fx = start_x + i * spacing
        draw.rounded_rectangle([fx-finger_w/2, cy-finger_h, fx+finger_w/2, cy+8*s], radius=int(8*s), fill=color)
    tx = cx - pw/2 - 8*s
    draw.rounded_rectangle([tx-14*s, cy-30*s, tx+8*s, cy+22*s], radius=int(10*s), fill=color)

draw_simple_hand(hc_x - 50, hc_y - 20, 1.3, SKY_BLUE)
draw_simple_hand(hc_x + 55, hc_y + 5, 0.85, WARM_YELLOW, is_child=True)

# 心形
hx, hy = hc_x + 10, hc_y - 70
draw.ellipse([hx-16, hy-20, hx+1, hy-2], fill=PINK)
draw.ellipse([hx-1, hy-20, hx+16, hy-2], fill=PINK)
draw.polygon([(hx-16, hy-8), (hx+16, hy-8), (hx, hy+18)], fill=PINK)

# ══════════════════════════════════════════════════
# 9. 花朵 (右下)
# ══════════════════════════════════════════════════
def draw_flower(cx, cy, petal_r, color, n=6):
    for i in range(n):
        angle = i * 2 * math.pi / n - math.pi/2
        px = cx + math.cos(angle) * petal_r * 0.65
        py = cy + math.sin(angle) * petal_r * 0.65
        draw.ellipse([px-petal_r*0.45, py-petal_r*0.45, px+petal_r*0.45, py+petal_r*0.45], fill=color)
    draw.ellipse([cx-petal_r*0.25, cy-petal_r*0.25, cx+petal_r*0.25, cy+petal_r*0.25], fill=WARM_YELLOW)

flowers = [
    (W-700, H-350, 35, PINK),
    (W-610, H-300, 25, LIGHT_PINK),
    (W-540, H-370, 30, LAVENDER),
    (W-800, H-310, 22, WARM_ORANGE),
]
for fx, fy, fr, fc in flowers:
    draw.line([(fx, fy+fr*0.5), (fx, grass_top+10)], fill=DARK_GREEN, width=3)
    draw_flower(fx, fy, fr, fc)
# 花茎叶子
draw.ellipse([W-720, H-430, W-695, H-405], fill=SOFT_GREEN)
draw.ellipse([W-570, H-420, W-545, H-395], fill=SOFT_GREEN)

# ══════════════════════════════════════════════════
# 10. 蝴蝶
# ══════════════════════════════════════════════════
def draw_butterfly(cx, cy, size, color):
    draw.ellipse([cx-size*1.6, cy-size, cx-size*0.1, cy+size*0.2], fill=color)
    draw.ellipse([cx-size*1.3, cy-size*0.2, cx-size*0.3, cy+size*0.7], fill=color)
    draw.ellipse([cx+size*0.1, cy-size, cx+size*1.6, cy+size*0.2], fill=color)
    draw.ellipse([cx+size*0.3, cy-size*0.2, cx+size*1.3, cy+size*0.7], fill=color)
    draw.ellipse([cx-size*0.12, cy-size*0.4, cx+size*0.12, cy+size*0.5], fill=DARK_TEXT)
    draw.line([(cx, cy-size*0.4), (cx-size*0.5, cy-size*1.2)], fill=DARK_TEXT, width=1)
    draw.line([(cx, cy-size*0.4), (cx+size*0.5, cy-size*1.2)], fill=DARK_TEXT, width=1)

draw_butterfly(1300, 580, 22, WARM_YELLOW_L)
draw_butterfly(W-1400, 520, 18, LIGHT_PINK)

# ══════════════════════════════════════════════════
# 11. ★ 主标题文字 (核心！居中大气)
# ══════════════════════════════════════════════════
line1 = "西雅博才小学"
line2 = "家长棒棒堂"
line3 = "智慧陪伴 · 共育花开"

font1 = load_font(340, bold=True)
font2 = load_font(300, bold=True)
font3 = load_font(170, bold=False)

# 计算位置
bbox1 = draw.textbbox((0, 0), line1, font=font1)
w1, h1 = bbox1[2]-bbox1[0], bbox1[3]-bbox1[1]
x1 = (W - w1) // 2
y1 = 220

bbox2 = draw.textbbox((0, 0), line2, font=font2)
w2, h2 = bbox2[2]-bbox2[0], bbox2[3]-bbox2[1]
x2 = (W - w2) // 2
y2 = y1 + h1 + 70

bbox3 = draw.textbbox((0, 0), line3, font=font3)
w3, h3 = bbox3[2]-bbox3[0], bbox3[3]-bbox3[1]
x3 = (W - w3) // 2
y3 = y2 + h2 + 80

# 阴影偏移
so = 6
shadow1 = (175, 200, 225)
shadow2 = (160, 190, 215)
shadow3 = (210, 195, 160)

# 第一行 - 深色（校名）
draw.text((x1+so, y1+so), line1, font=font1, fill=shadow1)
draw.text((x1, y1), line1, font=font1, fill=DARK_TEXT)

# 第二行 - 天蓝色（活动名）
draw.text((x2+so, y2+so), line2, font=font2, fill=shadow2)
draw.text((x2, y2), line2, font=font2, fill=BLUE_TEXT)

# 第三行 - 暖黄/橙色（口号）
draw.text((x3+so, y3+so), line3, font=font3, fill=shadow3)
draw.text((x3, y3), line3, font=font3, fill=WARM_ORANGE)

# ══════════════════════════════════════════════════
# 12. 口号下方渐变装饰线
# ══════════════════════════════════════════════════
line_y = y3 + h3 + 55
line_total_w = w3 + 100
line_start_x = (W - line_total_w) // 2
for x in range(line_total_w):
    t = abs(x - line_total_w/2) / (line_total_w/2)
    cr = int(SKY_BLUE[0] * t + WARM_YELLOW[0] * (1-t))
    cg = int(SKY_BLUE[1] * t + WARM_YELLOW[1] * (1-t))
    cb = int(SKY_BLUE[2] * t + WARM_YELLOW[2] * (1-t))
    draw.line([(line_start_x + x, line_y), (line_start_x + x, line_y + 6)], fill=(cr, cg, cb))

# ══════════════════════════════════════════════════
# 13. 星星装饰
# ══════════════════════════════════════════════════
def draw_star(cx, cy, size, color):
    points = []
    for i in range(10):
        angle = math.pi / 2 + i * math.pi / 5
        r = size if i % 2 == 0 else size * 0.4
        points.append((cx + math.cos(angle) * r, cy - math.sin(angle) * r))
    draw.polygon(points, fill=color)

# 标题两侧
draw_star(x1 - 90, y1 + h1//2, 22, WARM_YELLOW)
draw_star(x1 + w1 + 60, y1 + h1//2, 22, WARM_YELLOW)
draw_star(x2 - 70, y2 + h2//2, 17, WARM_ORANGE)
draw_star(x2 + w2 + 50, y2 + h2//2, 17, WARM_ORANGE)
draw_star(x3 - 55, y3 + h3//2, 13, PINK)
draw_star(x3 + w3 + 35, y3 + h3//2, 13, PINK)

# 散落
draw_star(550, 750, 12, WARM_YELLOW_L)
draw_star(W-550, 720, 14, WARM_YELLOW_L)
draw_star(1700, 350, 9, LIGHT_PINK)
draw_star(W-1800, 380, 10, LAVENDER)
draw_star(800, 1600, 8, SKY_BLUE_LIGHT)
draw_star(W-800, 1580, 10, SKY_BLUE_LIGHT)

# ══════════════════════════════════════════════════
# 14. 圆点装饰
# ══════════════════════════════════════════════════
dots = [
    (400, 700, 9, SKY_BLUE_LIGHT), (750, 850, 6, WARM_YELLOW_L),
    (W-400, 680, 8, SKY_BLUE_LIGHT), (W-700, 820, 10, WARM_YELLOW_L),
    (1500, 650, 5, LIGHT_PINK), (W-1400, 680, 6, LAVENDER),
    (2000, 350, 4, SKY_BLUE_LIGHT), (W-2000, 360, 5, SKY_BLUE_LIGHT),
    (1100, 1500, 5, SOFT_GREEN), (W-1000, 1480, 6, SOFT_GREEN),
]
for dx, dy, dr, dc in dots:
    draw.ellipse([dx-dr, dy-dr, dx+dr, dy+dr], fill=dc)

# ══════════════════════════════════════════════════
# 15. 底部装饰条
# ══════════════════════════════════════════════════
for x in range(W):
    t = abs(x - W/2) / (W/2)
    cr = int(WARM_YELLOW[0] * t + SKY_BLUE[0] * (1-t))
    cg = int(WARM_YELLOW[1] * t + SKY_BLUE[1] * (1-t))
    cb = int(WARM_YELLOW[2] * t + SKY_BLUE[2] * (1-t))
    draw.line([(x, H-14), (x, H)], fill=(cr, cg, cb))

# ══════════════════════════════════════════════════
# 16. 保存
# ══════════════════════════════════════════════════
output_path = r'C:\Users\erica\.qclaw\workspace-agent-60546543\西雅博才小学家长棒棒堂横幅.png'
img.save(output_path, 'PNG', dpi=(100, 100))
print(f'横幅已保存: {output_path}')
print(f'像素尺寸: {W} x {H} px @ 100dpi')
print(f'实物尺寸: {W/100*2.54:.0f}cm x {H/100*2.54:.0f}cm')
