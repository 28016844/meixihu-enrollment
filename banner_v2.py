#!/usr/bin/env python3
"""
横幅设计 V2：西雅博才小学家长棒棒堂·智慧陪伴·共育花开
尺寸：300cm x 50cm 印刷级横幅
风格：温暖治愈、校园亲子主题
主色调：天蓝色、暖黄色、米白色
"""

from PIL import Image, ImageDraw, ImageFont
import math

# ── 画布尺寸 (300cm x 50cm @ 100dpi → 印刷级) ──
# 300cm / 2.54 * 100dpi = 11811, 50cm / 2.54 * 100dpi = 1969
W, H = 11811, 1969

# ── 颜色定义 ──
SKY_BLUE       = (92, 172, 235)
SKY_BLUE_DEEP  = (60, 140, 210)
SKY_BLUE_LIGHT = (170, 218, 255)
WARM_YELLOW    = (255, 198, 55)
WARM_YELLOW_L  = (255, 228, 130)
WARM_ORANGE    = (255, 175, 80)
CREAM_WHITE    = (255, 250, 240)
SOFT_GREEN     = (115, 195, 115)
DARK_GREEN     = (70, 150, 70)
LEAF_GREEN     = (85, 170, 85)
PINK           = (255, 160, 185)
LIGHT_PINK     = (255, 200, 215)
LAVENDER       = (195, 165, 245)
WHITE          = (255, 255, 255)
DARK_TEXT       = (45, 55, 75)
BLUE_TEXT       = (50, 110, 180)

# ── 字体加载 ──
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

# ── 创建画布 ──
img = Image.new('RGB', (W, H), CREAM_WHITE)
draw = ImageDraw.Draw(img)

# ══════════════════════════════════════════════════
# 背景渐变 (天蓝上方 → 米白下方)
# ══════════════════════════════════════════════════
for y in range(H):
    ratio = y / H
    r = int(SKY_BLUE_LIGHT[0] * (1 - ratio*0.8) + CREAM_WHITE[0] * ratio*0.8)
    g = int(SKY_BLUE_LIGHT[1] * (1 - ratio*0.8) + CREAM_WHITE[1] * ratio*0.8)
    b = int(SKY_BLUE_LIGHT[2] * (1 - ratio*0.8) + CREAM_WHITE[2] * ratio*0.8)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# ══════════════════════════════════════════════════
# 底部草地渐变 + 波浪
# ══════════════════════════════════════════════════
grass_top = H - 180
for y in range(grass_top, H):
    ratio = (y - grass_top) / 180
    r = int(CREAM_WHITE[0] * (1-ratio) + SOFT_GREEN[0] * ratio * 0.6)
    g = int(CREAM_WHITE[1] * (1-ratio) + SOFT_GREEN[1] * ratio * 0.6)
    b = int(CREAM_WHITE[2] * (1-ratio) + SOFT_GREEN[2] * ratio * 0.6)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# 波浪线
for x in range(W):
    wy = int(math.sin(x / W * 4 * math.pi) * 12 + grass_top)
    for dy in range(8):
        if wy + dy < H:
            draw.point((x, wy + dy), fill=DARK_GREEN)

# ══════════════════════════════════════════════════
# 太阳 (右侧)
# ══════════════════════════════════════════════════
sun_cx, sun_cy = W - 480, 240
sun_r = 120
# 柔和光晕
for r_off in range(sun_r + 80, sun_r, -1):
    alpha = int(40 * (1 - (r_off - sun_r) / 80))
    color = (255, 230, min(255, 150 + alpha), )
    draw.ellipse([sun_cx-r_off, sun_cy-r_off, sun_cx+r_off, sun_cy+r_off], fill=(255, 245, 210))
# 光芒
for i in range(16):
    angle = i * math.pi / 8
    x1 = sun_cx + math.cos(angle) * (sun_r + 15)
    y1 = sun_cy + math.sin(angle) * (sun_r + 15)
    x2 = sun_cx + math.cos(angle) * (sun_r + 55 + (i%2)*15)
    y2 = sun_cy + math.sin(angle) * (sun_r + 55 + (i%2)*15)
    draw.line([(x1, y1), (x2, y2)], fill=WARM_YELLOW, width=6)
# 太阳本体
for r_off in range(sun_r, 0, -1):
    ratio3 = r_off / sun_r
    cr = int(255 * ratio3 + 255 * (1 - ratio3))
    cg = int(210 * ratio3 + 240 * (1 - ratio3))
    cb = int(50 * ratio3 + 160 * (1 - ratio3))
    draw.ellipse([sun_cx-r_off, sun_cy-r_off, sun_cx+r_off, sun_cy+r_off], fill=(cr, cg, cb))

# ══════════════════════════════════════════════════
# 云朵 (多组)
# ══════════════════════════════════════════════════
def draw_cloud(cx, cy, scale):
    parts = [
        (-1.0, 0, 0.6),
        (-0.3, -0.4, 0.7),
        (0.5, -0.3, 0.65),
        (1.2, 0, 0.55),
        (0.0, 0.1, 0.5),
    ]
    for ox, oy, rs in parts:
        r = scale * rs
        draw.ellipse([cx+ox*scale-r, cy+oy*scale-r, cx+ox*scale+r, cy+oy*scale+r], fill=(248, 252, 255))

draw_cloud(550, 160, 65)
draw_cloud(1800, 110, 45)
draw_cloud(W - 1200, 130, 55)
draw_cloud(W//2 + 400, 100, 40)

# ══════════════════════════════════════════════════
# 简约校园建筑 (左侧)
# ══════════════════════════════════════════════════
bx, by = 240, H - 380
# 主楼
draw.rectangle([bx, by, bx+260, H-180], fill=SKY_BLUE, outline=SKY_BLUE_DEEP, width=2)
# 屋顶
draw.polygon([(bx-20, by), (bx+130, by-90), (bx+280, by)], fill=SKY_BLUE_DEEP)
# 钟/三角窗
draw.polygon([(bx+90, by-50), (bx+130, by-80), (bx+170, by-50)], fill=WARM_YELLOW)
# 门
draw.rectangle([bx+100, by+90, bx+160, H-180], fill=WARM_YELLOW_L, outline=WARM_ORANGE, width=2)
draw.ellipse([bx+140, H-250, bx+150, H-240], fill=WARM_ORANGE)  # 门把手
# 窗户
for wx_off in [30, 190]:
    for wy_off in [25, 70]:
        wx = bx + wx_off
        wy = by + wy_off
        draw.rectangle([wx, wy, wx+40, wy+30], fill=WARM_YELLOW_L, outline=SKY_BLUE_DEEP, width=2)
        draw.line([(wx+20, wy), (wx+20, wy+30)], fill=SKY_BLUE_DEEP, width=1)
        draw.line([(wx, wy+15), (wx+40, wy+15)], fill=SKY_BLUE_DEEP, width=1)
# 旗杆
draw.line([(bx+130, by-90), (bx+130, by-200)], fill=DARK_TEXT, width=3)
flag_pts = [(bx+130, by-200), (bx+175, by-185), (bx+130, by-170)]
draw.polygon(flag_pts, fill=WARM_ORANGE)

# ══════════════════════════════════════════════════
# 书本 + 树苗 (左侧偏中)
# ══════════════════════════════════════════════════
book_cx, book_cy = 700, H - 250
# 书本 - 打开的书
bw, bh = 70, 50
# 左页
draw.polygon([
    (book_cx, book_cy+20),
    (book_cx-bw, book_cy-5),
    (book_cx-bw, book_cy+bh),
    (book_cx, book_cy+bh+15)
], fill=WHITE, outline=SKY_BLUE, width=2)
# 右页
draw.polygon([
    (book_cx, book_cy+20),
    (book_cx+bw, book_cy-5),
    (book_cx+bw, book_cy+bh),
    (book_cx, book_cy+bh+15)
], fill=WHITE, outline=SKY_BLUE, width=2)
# 书脊
draw.line([(book_cx, book_cy+20), (book_cx, book_cy+bh+15)], fill=SKY_BLUE_DEEP, width=3)
# 页面线条
for i in range(4):
    ly = book_cy + 10 + i * 11
    draw.line([(book_cx-bw+10, ly), (book_cx-8, ly+3)], fill=SKY_BLUE_LIGHT, width=1)
    draw.line([(book_cx+8, ly+3), (book_cx+bw-10, ly)], fill=SKY_BLUE_LIGHT, width=1)

# 树苗 (从书本上方生长)
stem_base = book_cy + 10
draw.line([(book_cx, stem_base), (book_cx, stem_base-100)], fill=DARK_GREEN, width=5)
# 叶子
leaf_data = [
    (-40, stem_base-70, 22, 12, -30),
    (35, stem_base-80, 20, 10, 25),
    (-25, stem_base-100, 18, 9, -40),
    (30, stem_base-105, 16, 8, 35),
]
for lx, ly, lw, lh, angle_deg in leaf_data:
    draw.ellipse([book_cx+lx-lw, ly-lh, book_cx+lx+lw, ly+lh], fill=LEAF_GREEN)

# 小芽
draw.ellipse([book_cx-6, stem_base-112, book_cx+6, stem_base-100], fill=SOFT_GREEN)

# ══════════════════════════════════════════════════
# 大手牵小手 (右侧偏中)
# ══════════════════════════════════════════════════
hand_cx = W - 900
hand_cy = H // 2 + 60

def draw_simple_hand(cx, cy, scale, color, is_child=False):
    """绘制简洁的手掌轮廓"""
    s = scale
    # 手掌 (圆角矩形)
    pw, ph = 70*s, 55*s
    draw.rounded_rectangle([cx-pw/2, cy, cx+pw/2, cy+ph], radius=15*s, fill=color)
    # 四指
    finger_w = 14 * s
    finger_h = 45 * s if not is_child else 30 * s
    spacing = 17 * s
    start_x = cx - spacing * 1.5
    for i in range(4):
        fx = start_x + i * spacing
        draw.rounded_rectangle(
            [fx - finger_w/2, cy - finger_h, fx + finger_w/2, cy + 5*s],
            radius=int(7*s), fill=color
        )
    # 拇指
    tx = cx - pw/2 - 5*s
    ty = cy + 10*s
    draw.rounded_rectangle(
        [tx - 12*s, ty - 25*s, tx + 8*s, ty + 20*s],
        radius=int(8*s), fill=color
    )

# 大手（成人 - 天蓝色）
draw_simple_hand(hand_cx - 40, hand_cy - 20, 1.2, SKY_BLUE)
# 小手（儿童 - 暖黄色，贴近大手）
draw_simple_hand(hand_cx + 40, hand_cy, 0.75, WARM_YELLOW, is_child=True)

# 牵手的小心形
hx = hand_cx + 5
hy = hand_cy - 55
draw.ellipse([hx-12, hy-15, hx, hy], fill=PINK)
draw.ellipse([hx, hy-15, hx+12, hy], fill=PINK)
draw.polygon([(hx-12, hy-5), (hx+12, hy-5), (hx, hy+15)], fill=PINK)

# ══════════════════════════════════════════════════
# 花朵 (右下角区域)
# ══════════════════════════════════════════════════
def draw_flower(cx, cy, petal_r, color, n_petals=6):
    for i in range(n_petals):
        angle = i * 2 * math.pi / n_petals - math.pi/2
        px = cx + math.cos(angle) * petal_r * 0.65
        py = cy + math.sin(angle) * petal_r * 0.65
        draw.ellipse([px-petal_r*0.45, py-petal_r*0.45, px+petal_r*0.45, py+petal_r*0.45], fill=color)
    draw.ellipse([cx-petal_r*0.25, cy-petal_r*0.25, cx+petal_r*0.25, cy+petal_r*0.25], fill=WARM_YELLOW)

flowers = [
    (W - 550, H - 240, 28, PINK),
    (W - 480, H - 200, 20, LIGHT_PINK),
    (W - 420, H - 260, 24, LAVENDER),
    (W - 620, H - 210, 18, WARM_ORANGE),
]
for fx, fy, fr, fc in flowers:
    # 花茎
    draw.line([(fx, fy + fr*0.5), (fx, H - 180)], fill=DARK_GREEN, width=2)
    # 叶子
    if fr > 20:
        draw.ellipse([fx+5, H-260, fx+22, H-240], fill=SOFT_GREEN)
    draw_flower(fx, fy, fr, fc)

# ══════════════════════════════════════════════════
# 小草点缀
# ══════════════════════════════════════════════════
import random
random.seed(42)
for gx in range(0, W, 35):
    gh = random.randint(10, 25)
    lean = random.randint(-4, 4)
    base_y = H - 180 + random.randint(-3, 3)
    draw.line([(gx, base_y), (gx + lean, base_y - gh)], fill=DARK_GREEN, width=2)
    if gh > 15:
        draw.line([(gx, base_y), (gx - lean*0.5, base_y - gh*0.7)], fill=LEAF_GREEN, width=1)

# ══════════════════════════════════════════════════
# 蝴蝶装饰
# ══════════════════════════════════════════════════
def draw_butterfly(cx, cy, size, color):
    # 左翅
    draw.ellipse([cx-size*1.5, cy-size, cx, cy+size*0.3], fill=color)
    draw.ellipse([cx-size*1.2, cy-size*0.3, cx-size*0.2, cy+size*0.8], fill=color)
    # 右翅
    draw.ellipse([cx, cy-size, cx+size*1.5, cy+size*0.3], fill=color)
    draw.ellipse([cx+size*0.2, cy-size*0.3, cx+size*1.2, cy+size*0.8], fill=color)
    # 身体
    draw.ellipse([cx-size*0.15, cy-size*0.5, cx+size*0.15, cy+size*0.6], fill=DARK_TEXT)
    # 触角
    draw.line([(cx, cy-size*0.5), (cx-size*0.4, cy-size*1.3)], fill=DARK_TEXT, width=1)
    draw.line([(cx, cy-size*0.5), (cx+size*0.4, cy-size*1.3)], fill=DARK_TEXT, width=1)

draw_butterfly(950, 350, 18, WARM_YELLOW_L)
draw_butterfly(W - 1050, 320, 15, LIGHT_PINK)

# ══════════════════════════════════════════════════
# ★ 主标题文字 (居中排版)
# ══════════════════════════════════════════════════
line1 = "西雅博才小学"
line2 = "家长棒棒堂"
line3 = "智慧陪伴 · 共育花开"

font1 = load_font(340, bold=True)   # 学校名
font2 = load_font(300, bold=True)   # 家长棒棒堂
font3 = load_font(170, bold=False)  # 口号

# 文字位置计算
bbox1 = draw.textbbox((0, 0), line1, font=font1)
w1 = bbox1[2] - bbox1[0]
x1 = (W - w1) // 2
y1 = 180

bbox2 = draw.textbbox((0, 0), line2, font=font2)
w2 = bbox2[2] - bbox2[0]
x2 = (W - w2) // 2
y2 = y1 + (bbox1[3] - bbox1[1]) + 60

bbox3 = draw.textbbox((0, 0), line3, font=font3)
w3 = bbox3[2] - bbox3[0]
x3 = (W - w3) // 2
y3 = y2 + (bbox2[3] - bbox2[1]) + 70

# 文字阴影 (柔和)
shadow_color = (180, 200, 225)
so = 5  # shadow offset

# 第一行 - 深色
draw.text((x1+so, y1+so), line1, font=font1, fill=shadow_color)
draw.text((x1, y1), line1, font=font1, fill=DARK_TEXT)

# 第二行 - 天蓝色（主标题色）
draw.text((x2+so, y2+so), line2, font=font2, fill=shadow_color)
draw.text((x2, y2), line2, font=font2, fill=BLUE_TEXT)

# 第三行 - 暖黄色
shadow3 = (210, 195, 160)
draw.text((x3+so, y3+so), line3, font=font3, fill=shadow3)
draw.text((x3, y3), line3, font=font3, fill=WARM_ORANGE)

# ══════════════════════════════════════════════════
# 装饰元素 - 口号下方渐变线
# ══════════════════════════════════════════════════
line_y = y3 + (bbox3[3] - bbox3[1]) + 45
line_total_w = w3 + 80
line_start_x = (W - line_total_w) // 2
for x in range(line_total_w):
    t = abs(x - line_total_w/2) / (line_total_w/2)
    cr = int(SKY_BLUE[0] * t + WARM_YELLOW[0] * (1-t))
    cg = int(SKY_BLUE[1] * t + WARM_YELLOW[1] * (1-t))
    cb = int(SKY_BLUE[2] * t + WARM_YELLOW[2] * (1-t))
    draw.line([(line_start_x + x, line_y), (line_start_x + x, line_y + 5)], fill=(cr, cg, cb))

# ══════════════════════════════════════════════════
# 星星点缀
# ══════════════════════════════════════════════════
def draw_star(cx, cy, size, color):
    points = []
    for i in range(10):
        angle = math.pi / 2 + i * math.pi / 5
        r = size if i % 2 == 0 else size * 0.4
        points.append((cx + math.cos(angle) * r, cy - math.sin(angle) * r))
    draw.polygon(points, fill=color)

# 标题两侧星星
draw_star(x1 - 70, y1 + 80, 18, WARM_YELLOW)
draw_star(x1 + w1 + 50, y1 + 80, 18, WARM_YELLOW)
draw_star(x2 - 55, y2 + 70, 14, WARM_ORANGE)
draw_star(x2 + w2 + 40, y2 + 70, 14, WARM_ORANGE)
draw_star(x3 - 45, y3 + 35, 11, PINK)
draw_star(x3 + w3 + 30, y3 + 35, 11, PINK)

# 散落星星
draw_star(450, 500, 10, WARM_YELLOW_L)
draw_star(W-500, 500, 12, WARM_YELLOW_L)
draw_star(1300, 200, 8, LIGHT_PINK)
draw_star(W-1400, 250, 9, LAVENDER)

# ══════════════════════════════════════════════════
# 圆点装饰
# ══════════════════════════════════════════════════
dots = [
    (350, 500, 7, SKY_BLUE_LIGHT), (600, 600, 5, WARM_YELLOW_L),
    (W-350, 480, 6, SKY_BLUE_LIGHT), (W-600, 580, 8, WARM_YELLOW_L),
    (1200, 450, 4, LIGHT_PINK), (W-1100, 460, 5, LAVENDER),
    (1600, 180, 3, SKY_BLUE_LIGHT), (W-1600, 190, 4, SKY_BLUE_LIGHT),
]
for dx, dy, dr, dc in dots:
    draw.ellipse([dx-dr, dy-dr, dx+dr, dy+dr], fill=dc)

# ══════════════════════════════════════════════════
# 顶部和底部边框装饰条
# ══════════════════════════════════════════════════
# 顶部细线
for x in range(W):
    t = abs(x - W/2) / (W/2)
    cr = int(SKY_BLUE[0] * t + WARM_YELLOW[0] * (1-t))
    cg = int(SKY_BLUE[1] * t + WARM_YELLOW[1] * (1-t))
    cb = int(SKY_BLUE[2] * t + WARM_YELLOW[2] * (1-t))
    draw.line([(x, 0), (x, 8)], fill=(cr, cg, cb))

# 底部细线
for x in range(W):
    t = abs(x - W/2) / (W/2)
    cr = int(WARM_YELLOW[0] * t + SKY_BLUE[0] * (1-t))
    cg = int(WARM_YELLOW[1] * t + SKY_BLUE[1] * (1-t))
    cb = int(WARM_YELLOW[2] * t + SKY_BLUE[2] * (1-t))
    draw.line([(x, H-8), (x, H)], fill=(cr, cg, cb))

# ══════════════════════════════════════════════════
# 保存
# ══════════════════════════════════════════════════
output_path = r'C:\Users\erica\.qclaw\workspace-agent-60546543\西雅博才小学家长棒棒堂横幅.png'
img.save(output_path, 'PNG', dpi=(100, 100))
print(f'横幅已保存: {output_path}')
print(f'尺寸: {W} x {H} px @ 100dpi')
print(f'实物尺寸: {W/100*2.54:.0f}cm x {H/100*2.54:.0f}cm')
