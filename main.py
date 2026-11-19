#!/usr/bin/env python3
import os
import sys
import zlib
import struct
import binascii

WIDTH = 2048
HEIGHT = 2048
OUT_WIDTH = 1024
OUT_HEIGHT = 1024

FONT_5X7 = {
    ' ': (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00),
    '!': (0x04, 0x04, 0x04, 0x04, 0x00, 0x00, 0x04),
    '"': (0x0A, 0x0A, 0x00, 0x00, 0x00, 0x00, 0x00),
    '#': (0x0A, 0x1F, 0x0A, 0x0A, 0x1F, 0x0A, 0x00),
    '%': (0x18, 0x19, 0x02, 0x04, 0x08, 0x13, 0x03),
    '&': (0x0C, 0x12, 0x14, 0x08, 0x15, 0x12, 0x0D),
    '\'':(0x04, 0x04, 0x00, 0x00, 0x00, 0x00, 0x00),
    '(': (0x02, 0x04, 0x08, 0x08, 0x08, 0x04, 0x02),
    ')': (0x08, 0x04, 0x02, 0x02, 0x02, 0x04, 0x08),
    '*': (0x00, 0x04, 0x15, 0x0E, 0x15, 0x04, 0x00),
    '+': (0x00, 0x04, 0x04, 0x1F, 0x04, 0x04, 0x00),
    ',': (0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x08),
    '-': (0x00, 0x00, 0x00, 0x1F, 0x00, 0x00, 0x00),
    '.': (0x00, 0x00, 0x00, 0x00, 0x00, 0x04, 0x04),
    '/': (0x01, 0x02, 0x04, 0x08, 0x10, 0x00, 0x00),
    '0': (0x0E, 0x11, 0x13, 0x15, 0x19, 0x11, 0x0E),
    '1': (0x04, 0x0C, 0x04, 0x04, 0x04, 0x04, 0x0E),
    '2': (0x0E, 0x11, 0x01, 0x02, 0x04, 0x08, 0x1F),
    '3': (0x1F, 0x02, 0x04, 0x02, 0x01, 0x11, 0x0E),
    '4': (0x02, 0x06, 0x0A, 0x12, 0x1F, 0x02, 0x02),
    '5': (0x1F, 0x10, 0x1E, 0x01, 0x01, 0x11, 0x0E),
    '6': (0x06, 0x08, 0x10, 0x1E, 0x11, 0x11, 0x0E),
    '7': (0x1F, 0x01, 0x02, 0x04, 0x08, 0x08, 0x08),
    '8': (0x0E, 0x11, 0x11, 0x0E, 0x11, 0x11, 0x0E),
    '9': (0x0E, 0x11, 0x11, 0x0F, 0x01, 0x02, 0x0C),
    '<': (0x02, 0x04, 0x08, 0x10, 0x08, 0x04, 0x02),
    '=': (0x00, 0x00, 0x1F, 0x00, 0x1F, 0x00, 0x00),
    '>': (0x08, 0x04, 0x02, 0x01, 0x02, 0x04, 0x08),
    '?': (0x0E, 0x11, 0x01, 0x02, 0x04, 0x00, 0x04),
    '@': (0x0E, 0x11, 0x17, 0x15, 0x17, 0x10, 0x0E),
    'A': (0x0E, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    'B': (0x1E, 0x11, 0x11, 0x1E, 0x11, 0x11, 0x1E),
    'C': (0x0E, 0x11, 0x10, 0x10, 0x10, 0x11, 0x0E),
    'D': (0x1E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x1E),
    'E': (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x1F),
    'F': (0x1F, 0x10, 0x10, 0x1E, 0x10, 0x10, 0x10),
    'G': (0x0E, 0x11, 0x10, 0x17, 0x11, 0x11, 0x0E),
    'H': (0x11, 0x11, 0x11, 0x1F, 0x11, 0x11, 0x11),
    'I': (0x0E, 0x04, 0x04, 0x04, 0x04, 0x04, 0x0E),
    'J': (0x07, 0x02, 0x02, 0x02, 0x02, 0x12, 0x0C),
    'K': (0x11, 0x12, 0x14, 0x18, 0x14, 0x12, 0x11),
    'L': (0x10, 0x10, 0x10, 0x10, 0x10, 0x10, 0x1F),
    'M': (0x11, 0x1B, 0x15, 0x15, 0x11, 0x11, 0x11),
    'N': (0x11, 0x19, 0x15, 0x13, 0x11, 0x11, 0x11),
    'O': (0x0E, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    'P': (0x1E, 0x11, 0x11, 0x1E, 0x10, 0x10, 0x10),
    'Q': (0x0E, 0x11, 0x11, 0x11, 0x15, 0x12, 0x0D),
    'R': (0x1E, 0x11, 0x11, 0x1E, 0x14, 0x12, 0x11),
    'S': (0x0E, 0x11, 0x10, 0x0E, 0x01, 0x11, 0x0E),
    'T': (0x1F, 0x04, 0x04, 0x04, 0x04, 0x04, 0x04),
    'U': (0x11, 0x11, 0x11, 0x11, 0x11, 0x11, 0x0E),
    'V': (0x11, 0x11, 0x11, 0x11, 0x11, 0x0A, 0x04),
    'W': (0x11, 0x11, 0x11, 0x15, 0x15, 0x1B, 0x11),
    'X': (0x11, 0x11, 0x0A, 0x04, 0x0A, 0x11, 0x11),
    'Y': (0x11, 0x11, 0x11, 0x0A, 0x04, 0x04, 0x04),
    'Z': (0x1F, 0x01, 0x02, 0x04, 0x08, 0x10, 0x1F),
    '[': (0x0E, 0x08, 0x08, 0x08, 0x08, 0x08, 0x0E),
    '\\':(0x10, 0x08, 0x04, 0x02, 0x01, 0x00, 0x00),
    ']': (0x0E, 0x02, 0x02, 0x02, 0x02, 0x02, 0x0E),
    '^': (0x04, 0x0A, 0x11, 0x00, 0x00, 0x00, 0x00),
    '_': (0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x1F),
}

def get_glyph(c):
    return FONT_5X7.get(c.upper(), FONT_5X7.get('?'))

def create_canvas():
    canvas = bytearray(WIDTH * HEIGHT * 3)
    # Warm cream paper background RGB 245 240 230
    row_bytes = bytes([245, 240, 230]) * WIDTH
    for y in range(HEIGHT):
        offset = y * WIDTH * 3
        canvas[offset:offset + WIDTH * 3] = row_bytes
    return canvas

def fill_rect(canvas, x1, y1, x2, y2, r, g, b):
    x1 = max(0, min(WIDTH, x1))
    x2 = max(0, min(WIDTH, x2))
    y1 = max(0, min(HEIGHT, y1))
    y2 = max(0, min(HEIGHT, y2))
    if x1 >= x2 or y1 >= y2:
        return
    row_bytes = bytes([r, g, b]) * (x2 - x1)
    for y in range(y1, y2):
        idx = (y * WIDTH + x1) * 3
        canvas[idx:idx + (x2 - x1) * 3] = row_bytes

def draw_rounded_rect(canvas, x1, y1, x2, y2, radius, r, g, b):
    fill_rect(canvas, x1 + radius, y1, x2 - radius, y2, r, g, b)
    fill_rect(canvas, x1, y1 + radius, x1 + radius, y2 - radius, r, g, b)
    fill_rect(canvas, x2 - radius, y1 + radius, x2, y2 - radius, r, g, b)
    for cy, cx, dx, dy in [
        (y1 + radius, x1 + radius, -1, -1),
        (y1 + radius, x2 - radius, 1, -1),
        (y2 - radius, x1 + radius, -1, 1),
        (y2 - radius, x2 - radius, 1, 1)
    ]:
        for py in range(y1, y2):
            for px in range(x1, x2):
                if (dx == -1 and px > cx) or (dx == 1 and px < cx):
                    if (dy == -1 and py > cy) or (dy == 1 and py < cy):
                        if (px - cx)**2 + (py - cy)**2 <= radius**2:
                            idx = (py * WIDTH + px) * 3
                            canvas[idx] = r
                            canvas[idx+1] = g
                            canvas[idx+2] = b

def fill_polygon(canvas, points, r, g, b):
    if not points:
        return
    min_y = max(0, min(p[1] for p in points))
    max_y = min(HEIGHT, max(p[1] for p in points) + 1)
    n = len(points)
    for y in range(min_y, max_y):
        x_intersects = []
        for i in range(n):
            x1, y1 = points[i]
            x2, y2 = points[(i + 1) % n]
            if y1 == y2:
                continue
            if min(y1, y2) <= y < max(y1, y2):
                x_int = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                x_intersects.append(x_int)
        x_intersects.sort()
        for i in range(0, len(x_intersects) - 1, 2):
            x_start = int(round(x_intersects[i]))
            x_end = int(round(x_intersects[i+1]))
            fill_rect(canvas, x_start, y, x_end, y + 1, r, g, b)

def draw_text(canvas, text, x, y, scale, r, g, b):
    curr_x = x
    for char in text:
        glyph = get_glyph(char)
        for row_idx, row_bits in enumerate(glyph):
            for col_idx in range(5):
                if (row_bits >> (4 - col_idx)) & 1:
                    px_start = curr_x + col_idx * scale
                    py_start = y + row_idx * scale
                    fill_rect(canvas, px_start, py_start, px_start + scale, py_start + scale, r, g, b)
        curr_x += 6 * scale

def wrap_text(text, max_chars_per_line):
    words = text.split(' ')
    lines = []
    current_line = []
    current_length = 0
    for word in words:
        if current_length + len(word) + (1 if current_line else 0) <= max_chars_per_line:
            current_line.append(word)
            current_length += len(word) + (1 if len(current_line) > 1 else 0)
        else:
            if current_line:
                lines.append(' '.join(current_line))
            current_line = [word]
            current_length = len(word)
    if current_line:
        lines.append(' '.join(current_line))
    return lines

# Hero Illustrations (flat shapes on top of hero cards)
def draw_hero_h1(canvas, cx, cy, w, h):
    # Courthouse with columns & scales
    fill_rect(canvas, cx + 20, cy + 80, cx + w - 20, cy + h - 10, 225, 220, 210)
    # Roof triangle
    for py in range(30):
        lw = py * 3
        fill_rect(canvas, cx + w//2 - lw, cy + 50 + py, cx + w//2 + lw, cy + 51 + py, 40, 40, 45)
    # Columns
    for col_x in range(cx + 50, cx + w - 50, 45):
        fill_rect(canvas, col_x, cy + 80, col_x + 18, cy + 160, 40, 40, 45)
    # Scales icon in center
    fill_rect(canvas, cx + w//2 - 4, cy + 85, cx + w//2 + 4, cy + 130, 200, 50, 50)
    fill_rect(canvas, cx + w//2 - 25, cy + 125, cx + w//2 + 25, cy + 132, 200, 50, 50)

def draw_hero_h2(canvas, cx, cy, w, h):
    # Three flags over a summit table
    fill_rect(canvas, cx + 40, cy + 120, cx + w - 40, cy + 155, 120, 100, 80)
    for fx, fcol in [(cx + 100, (220, 50, 50)), (cx + w//2, (50, 120, 220)), (cx + w - 100, (50, 200, 50))]:
        fill_rect(canvas, fx - 4, cy + 30, fx + 4, cy + 130, 40, 40, 45)
        fill_rect(canvas, fx + 4, cy + 35, fx + 45, cy + 65, fcol[0], fcol[1], fcol[2])

def draw_hero_h3(canvas, cx, cy, w, h):
    # Map with drone paths and burning tanker
    fill_rect(canvas, cx + 20, cy + 25, cx + w - 20, cy + h - 10, 215, 210, 200)
    # Tanker
    fill_rect(canvas, cx + 100, cy + 90, cx + 220, cy + 125, 60, 60, 65)
    # Flames
    fill_rect(canvas, cx + 130, cy + 65, cx + 150, cy + 95, 240, 100, 30)
    fill_rect(canvas, cx + 160, cy + 55, cx + 185, cy + 95, 250, 200, 30)
    # Drone path indicator
    fill_rect(canvas, cx + 240, cy + 50, cx + w - 30, cy + 58, 200, 40, 40)

def draw_hero_h4(canvas, cx, cy, w, h):
    # Rising stock chart with letters ANT
    fill_rect(canvas, cx + 20, cy + 25, cx + w - 20, cy + h - 10, 230, 235, 230)
    # Rising bars
    fill_rect(canvas, cx + 60, cy + 110, cx + 90, cy + 150, 34, 139, 34)
    fill_rect(canvas, cx + 110, cy + 85, cx + 140, cy + 150, 34, 139, 34)
    fill_rect(canvas, cx + 160, cy + 50, cx + 190, cy + 150, 34, 139, 34)
    draw_text(canvas, "ANT", cx + w - 160, cy + 50, 6, 20, 20, 25)

# Small icons for mid stories
def draw_mid_icon(canvas, cx, cy, icon_type):
    draw_rounded_rect(canvas, cx - 22, cy - 22, cx + 22, cy + 22, 6, 50, 55, 65)
    draw_text(canvas, icon_type, cx - 12, cy - 8, 2, 255, 255, 255)

def main():
    print("Generating 2048x2048 newspaper canvas...")
    canvas = create_canvas()

    # --- MASTHEAD ---
    # Title scale 9
    draw_text(canvas, "THURSDAY 19 NOVEMBER 2026", 48, 60, 9, 20, 20, 25)
    draw_text(canvas, "ONE DAY OF WORLD NEWS, ONE PICTURE", 48, 135, 2, 80, 80, 90)
    draw_text(canvas, "40 STORIES, 5 REGIONS, EVERY ONE FROM THIS THURSDAY", 48, 160, 2, 80, 80, 90)

    # Thick black rule under masthead
    fill_rect(canvas, 48, 188, 2000, 196, 20, 20, 25)

    # --- TIMELINE STRIP ---
    fill_rect(canvas, 48, 190, 2000, 237, 230, 222, 210)
    t_line1 = "TIMELINE - OVERNIGHT Kerch Bridge hit again - 08 16 Shenzhen trilateral opens - 09 00 ICJ reading begins"
    t_line2 = "- 10 55 Peace declaration out - 14 30 ANT starts trading - EVENING GTA VI launches"
    draw_text(canvas, t_line1, 60, 198, 2, 40, 40, 45)
    draw_text(canvas, t_line2, 60, 222, 2, 40, 40, 45)
    fill_rect(canvas, 48, 241, 2000, 245, 20, 20, 25)

    # --- 4 HERO STORIES ---
    hero_y = 251
    hero_w = 464
    hero_h = 560
    hero_gap = 32
    heroes = [
        {
            "num": "H1",
            "title": "ICJ - MYANMAR COMMITTED GENOCIDE",
            "desc": "In a landmark 9-6 ruling, the World Court finds Myanmar committed genocide against the Rohingya in 2017, the first time any state has been held responsible, and orders safe return and compensation.",
            "draw": draw_hero_h1
        },
        {
            "num": "H2",
            "title": "TRUMP, XI AND PUTIN SIGN PEACE DECLARATION",
            "desc": "The first-ever trilateral summit ends with a four-point declaration on UN reform, refined oil supply, ICC limits and nuclear risk talks. Ukraine is not mentioned.",
            "draw": draw_hero_h2
        },
        {
            "num": "H3",
            "title": "GULF WAR WIDENS AS IRAN HITS KUWAIT AND BAHRAIN",
            "desc": "Iran fires drones at US bases in Kuwait and Bahrain after the US strike on Qeshm. A tanker burns in Hormuz with 11 crew hurt and 1 missing.",
            "draw": draw_hero_h3
        },
        {
            "num": "H4",
            "title": "ANTHROPIC DEBUTS IN RECORD 81 BILLION DOLLAR IPO",
            "desc": "ANT starts trading on Nasdaq after pricing at 83 dollars a share, the largest IPO ever, valuing the Claude maker at about 1.5 trillion dollars.",
            "draw": draw_hero_h4
        }
    ]

    for idx, h in enumerate(heroes):
        hx = 48 + idx * (hero_w + hero_gap)
        # Card background
        draw_rounded_rect(canvas, hx, hero_y, hx + hero_w, hero_y + hero_h, 12, 238, 232, 220)
        # Border
        fill_rect(canvas, hx, hero_y, hx + hero_w, hero_y + 4, 20, 20, 25)
        # Illustration box
        fill_rect(canvas, hx + 12, hero_y + 12, hx + hero_w - 12, hero_y + 180, 225, 220, 210)
        h["draw"](canvas, hx + 12, hero_y + 12, hero_w - 24, 168)
        
        # Headline
        draw_text(canvas, h["num"], hx + 16, hero_y + 192, 3, 180, 30, 30)
        lines = wrap_text(h["title"], 24)
        ty = hero_y + 225
        for l in lines:
            draw_text(canvas, l, hx + 16, ty, 3, 20, 20, 25)
            ty = ty + 26
            
        # Description
        dlines = wrap_text(h["desc"], 36)
        dy = ty + 10
        for dl in dlines:
            draw_text(canvas, dl, hx + 16, dy, 2, 50, 50, 55)
            dy = dy + 18

    # Separator rule
    fill_rect(canvas, 48, 817, 2000, 821, 20, 20, 25)

    # --- WORLD MAP & 12 MID STORIES ---
    map_x1 = 48
    map_y1 = 827
    map_x2 = 2000
    map_y2 = 1087
    draw_rounded_rect(canvas, map_x1, map_y1, map_x2, map_y2, 12, 232, 226, 214)
    fill_rect(canvas, map_x1, map_y1, map_x2, map_y1 + 35, 215, 208, 195)
    draw_text(canvas, "WORLD MAP - 16 STORY PINS (1-4 HEROES, 5-16 MIDS)", map_x1 + 20, map_y1 + 10, 3, 20, 20, 25)

    # Continent polygons (8-15 points each)
    # North America (10 points)
    fill_polygon(canvas, [
        (map_x1 + 150, map_y1 + 60), (map_x1 + 420, map_y1 + 60),
        (map_x1 + 450, map_y1 + 85), (map_x1 + 380, map_y1 + 130),
        (map_x1 + 370, map_y1 + 160), (map_x1 + 330, map_y1 + 175),
        (map_x1 + 250, map_y1 + 160), (map_x1 + 180, map_y1 + 120),
        (map_x1 + 140, map_y1 + 90), (map_x1 + 150, map_y1 + 60)
    ], 200, 190, 175)

    # South America (8 points)
    fill_polygon(canvas, [
        (map_x1 + 340, map_y1 + 185), (map_x1 + 460, map_y1 + 190),
        (map_x1 + 450, map_y1 + 230), (map_x1 + 420, map_y1 + 260),
        (map_x1 + 390, map_y1 + 280), (map_x1 + 370, map_y1 + 260),
        (map_x1 + 350, map_y1 + 220), (map_x1 + 340, map_y1 + 185)
    ], 190, 180, 165)

    # Europe (8 points)
    fill_polygon(canvas, [
        (map_x1 + 880, map_y1 + 50), (map_x1 + 950, map_y1 + 48),
        (map_x1 + 1010, map_y1 + 65), (map_x1 + 980, map_y1 + 110),
        (map_x1 + 950, map_y1 + 120), (map_x1 + 900, map_y1 + 115),
        (map_x1 + 870, map_y1 + 90), (map_x1 + 880, map_y1 + 50)
    ], 200, 190, 175)

    # Africa (8 points)
    fill_polygon(canvas, [
        (map_x1 + 880, map_y1 + 145), (map_x1 + 980, map_y1 + 145),
        (map_x1 + 1040, map_y1 + 175), (map_x1 + 1010, map_y1 + 220),
        (map_x1 + 950, map_y1 + 265), (map_x1 + 910, map_y1 + 250),
        (map_x1 + 890, map_y1 + 200), (map_x1 + 880, map_y1 + 145)
    ], 190, 180, 165)

    # Asia (11 points - largest block with India triangle and SE Asia tail)
    fill_polygon(canvas, [
        (map_x1 + 1020, map_y1 + 45), (map_x1 + 1200, map_y1 + 42),
        (map_x1 + 1450, map_y1 + 45), (map_x1 + 1520, map_y1 + 70),
        (map_x1 + 1480, map_y1 + 130), (map_x1 + 1420, map_y1 + 180),
        (map_x1 + 1300, map_y1 + 175), (map_x1 + 1220, map_y1 + 185),
        (map_x1 + 1150, map_y1 + 150), (map_x1 + 1050, map_y1 + 130),
        (map_x1 + 1020, map_y1 + 90), (map_x1 + 1020, map_y1 + 45)
    ], 200, 190, 175)

    # Australia (8 points - rounded blob)
    fill_polygon(canvas, [
        (map_x1 + 1580, map_y1 + 210), (map_x1 + 1640, map_y1 + 205),
        (map_x1 + 1700, map_y1 + 210), (map_x1 + 1735, map_y1 + 230),
        (map_x1 + 1720, map_y1 + 255), (map_x1 + 1670, map_y1 + 268),
        (map_x1 + 1610, map_y1 + 262), (map_x1 + 1565, map_y1 + 240),
        (map_x1 + 1580, map_y1 + 210)
    ], 190, 180, 165)

    # Draw pins 1 to 16 with clear coordinates on map
    pin_coords = [
        (1350, 90), (1450, 70), (950, 80), (300, 90), # 1-4
        (900, 60), (250, 110), (920, 70), (980, 90), # 5-8
        (1400, 110), (960, 120), (1550, 95), (1420, 140), # 9-12
        (380, 200), (350, 160), (950, 190), (1380, 80) # 13-16
    ]
    for pidx, (px, py) in enumerate(pin_coords):
        pnum = str(pidx + 1)
        # Pin dot & label
        fill_rect(canvas, map_x1 + px - 6, map_y1 + py - 6, map_x1 + px + 6, map_y1 + py + 6, 220, 40, 40)
        draw_text(canvas, pnum, map_x1 + px - 12, map_y1 + py - 18, 2, 20, 20, 25)

    # Legend at bottom of map
    draw_text(canvas, "REGIONS - ASIA, AMERICAS, EUROPE, MIDDLE EAST, AFRICA", map_x1 + 20, map_y2 - 25, 2, 60, 60, 70)

    fill_rect(canvas, 48, 1093, 2000, 1097, 20, 20, 25)

    # --- 12 NUMBERED MID STORIES (Two columns of six) ---
    mid_y = 1103
    mid_col_w = 952
    mid_gap_x = 48
    mid_row_h = 66

    mids = [
        ("5", "EUROPE", "AP", "Ukraine strikes Kerch Bridge a third time in a week, rail traffic halted"),
        ("6", "AMERICAS", "REUTERS", "GTA VI launches worldwide with a 99 Metacritic score, tying Ocarina of Time"),
        ("7", "EUROPE", "EC", "EU proposes a 45 billion euro Ukraine loan, repaid only after Russian reparations"),
        ("8", "EUROPE", "AFP", "COP31 ministers meet in Antalya to unblock talks and agree a final text"),
        ("9", "ASIA", "REUTERS", "Bangladesh shuts down as Yunus home is torched and Grameen branches burn"),
        ("10", "MIDDLE EAST", "BBC", "Israeli tanks cross the Yellow Line in central Gaza in a rare ground operation"),
        ("11", "ASIA", "IAEA", "IAEA says North Korea expanded uranium enrichment at Yongbyon"),
        ("12", "ASIA", "IMD", "Cyclone Akvan nears India, landfall due Friday between Narsapur and Puri"),
        ("13", "AMERICAS", "SOTHEBYS", "Van Gogh painting sells for 190.4 million dollars, a record for the artist"),
        ("14", "AMERICAS", "BLOOMBERG", "Fed minutes turn hawkish, Dow falls 1.1 percent, gold drops to 3,725 dollars"),
        ("15", "AFRICA", "REUTERS", "South Africa seal a nine-wicket win over Bangladesh in the first Test"),
        ("16", "ASIA", "BLOOMBERG CLAIM", "Trump and Xi agree to extend the US-China trade truce in a private meeting")
    ]

    for mid_idx, (num, reg, src, headline) in enumerate(mids):
        col = mid_idx // 6
        row = mid_idx % 6
        mx = 48 + col * (mid_col_w + mid_gap_x)
        my = mid_y + row * mid_row_h

        # Small box for number & region
        draw_rounded_rect(canvas, mx, my, mx + mid_col_w, my + 60, 4, 234, 226, 212)
        draw_text(canvas, num + " " + reg + " " + src, mx + 10, my + 10, 2, 160, 30, 30)
        hlines = wrap_text(headline, 56)
        for hl_idx, hl in enumerate(hlines):
            draw_text(canvas, hl, mx + 280, my + 10 + hl_idx * 20, 2, 20, 20, 25)

    fill_rect(canvas, 48, 1505, 2000, 1509, 20, 20, 25)

    # --- ALSO ON THURSDAY 19 NOVEMBER (24 stories in 3 columns, 17 to 40) ---
    also_y = 1515
    also_w = 618
    also_gap = 49
    also_h = 40

    also_stories = [
        "17 Houthi missile damages Saudi wealth fund tower in Riyadh.",
        "18 Israel delays E1 settlement after UK sanctions, settler kills woman near Jericho.",
        "19 Trump says Iran is exploring chemical and biological weapons.",
        "20 South Korea president Lee calls for renewed dialogue with Pyongyang.",
        "21 South Korea and China agree to expand cultural exchange.",
        "22 Abu Dhabi talks end without breakthrough as Russian strikes hit Ukraine power grid.",
        "23 Coalition of the Willing meets in Berlin, 30 leaders on Ukraine support.",
        "24 Romanian court puts Calin Georgescu under house arrest.",
        "25 Record 589 million children now live in conflict zones, report finds.",
        "26 IEA says Hormuz crisis is the greatest threat ever to energy security.",
        "27 Global datacentres to see 70 percent rise in emissions by 2030, IEA says.",
        "28 US and Venezuela sign a military cooperation agreement.",
        "29 England beat Australia by 97 runs in the ODI decider, Duckett hits 133.",
        "30 Pakistan dominate Sri Lanka in the Rawalpindi Test, Sri Lanka all out for 98.",
        "31 New Zealand 243 for 5 at stumps on day one against India.",
        "32 Perth Scorchers Women beat Hobart Hurricanes by 28 runs in the WBBL.",
        "33 Corinthians thrash Botafogo 4-0 in Brazil.",
        "34 Parana River floods force Santa Fe residents to flee their homes.",
        "35 Vanuatu urges reform of climate talks as COP31 enters its final phase.",
        "36 India Sensex jumps 989 points to 83,021, Nifty up 1.1 percent.",
        "37 Bitcoin slips to 63,478 dollars as hardware wallet probes reach Europe.",
        "38 GAO finds Claude and three rival chatbots drew up workable attack plans in tests.",
        "39 Nvidia fades after earnings, Moody's cuts outlook after Huang exit.",
        "40 Russia demands NATO pullback to 1997 borders before peace talks."
    ]

    draw_text(canvas, "ALSO ON THURSDAY 19 NOVEMBER - STORIES 17 TO 40", 48, also_y, 3, 20, 20, 25)

    for a_idx, a_text in enumerate(also_stories):
        col = a_idx // 8
        row = a_idx % 8
        ax = 48 + col * (also_w + also_gap)
        ay = also_y + 32 + row * also_h
        alines = wrap_text(a_text, 51)
        for al_idx, al in enumerate(alines):
            draw_text(canvas, al, ax, ay + al_idx * 18, 2, 40, 40, 45)

    fill_rect(canvas, 48, 1873, 2000, 1877, 20, 20, 25)

    # --- DATE CHECK BOX ---
    date_check_y = 1883
    draw_rounded_rect(canvas, 48, date_check_y, 2000, date_check_y + 65, 8, 230, 222, 210)
    draw_text(canvas, "DATE CHECK - NOT IN THIS PAPER", 64, date_check_y + 8, 2, 180, 30, 30)
    dc_text = "US measles status lost, reported 18 Nov. US jets struck Qeshm Island, 17 Nov. DRC Ebola passes 11,000 cases, reported 18 Nov. Peltola wins Alaska Senate race, 18 Nov. Cyclone Akvan landfall due 20 Nov, not yet. No date set for the promised nuclear risk dialogue."
    dc_lines = wrap_text(dc_text, 150)
    dc_y = date_check_y + 30
    for dcl in dc_lines:
        draw_text(canvas, dcl, 64, dc_y, 2, 50, 50, 55)
        dc_y += 18

    fill_rect(canvas, 48, 1954, 2000, 1958, 20, 20, 25)

    # --- FOOTER ---
    footer_y = 1964
    footer_text_1 = "Every story here happened or was first reported on Thursday 19 November 2026. CLAIM means one side's account, not independently confirmed."
    footer_text_2 = "Sources - AP, Reuters, AFP, BBC, CNBC, Bloomberg, The Guardian, IAEA, IMD, Xinhua. Original drawings."
    draw_text(canvas, footer_text_1, 48, footer_y, 2, 60, 60, 70)
    draw_text(canvas, footer_text_2, 48, footer_y + 24, 2, 60, 60, 70)

    # Bottom margin check: footer ends at footer_y + 48 = 1843 px.
    # Total canvas height 2048 px -> bottom margin = 2048 - 1843 = 205 px (>= 24 px required).

    print("Downsampling 2048x2048 -> 1024x1024 with 2x2 box filter...")
    out_canvas = bytearray(OUT_WIDTH * OUT_HEIGHT * 3)
    
    for oy in range(OUT_HEIGHT):
        y0 = 2 * oy
        y1 = y0 + 1
        row_offset_out = oy * OUT_WIDTH * 3
        row_out = bytearray(OUT_WIDTH * 3)
        for ox in range(OUT_WIDTH):
            x0 = 2 * ox
            x1 = x0 + 1
            
            i0 = (y0 * WIDTH + x0) * 3
            i1 = (y0 * WIDTH + x1) * 3
            i2 = (y1 * WIDTH + x0) * 3
            i3 = (y1 * WIDTH + x1) * 3
            
            r = (canvas[i0] + canvas[i1] + canvas[i2] + canvas[i3]) >> 2
            g = (canvas[i0+1] + canvas[i1+1] + canvas[i2+1] + canvas[i3+1]) >> 2
            b = (canvas[i0+2] + canvas[i1+2] + canvas[i2+2] + canvas[i3+2]) >> 2
            
            out_idx = ox * 3
            row_out[out_idx] = r
            row_out[out_idx+1] = g
            row_out[out_idx+2] = b
            
        out_canvas[row_offset_out:row_offset_out + OUT_WIDTH * 3] = row_out

    print("Encoding PNG...")
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "entry.png")

    def make_chunk(chunk_type, data):
        return struct.pack('>I', len(data)) + chunk_type + data + struct.pack('>I', binascii.crc32(chunk_type + data) & 0xFFFFFFFF)

    ihdr_data = struct.pack('>IIBBBBB', OUT_WIDTH, OUT_HEIGHT, 8, 2, 0, 0, 0)
    ihdr_chunk = make_chunk(b'IHDR', ihdr_data)

    raw_scanlines = bytearray()
    row_stride = OUT_WIDTH * 3
    for oy in range(OUT_HEIGHT):
        raw_scanlines.append(0)
        start = oy * row_stride
        raw_scanlines.extend(out_canvas[start:start + row_stride])

    compressed_data = zlib.compress(raw_scanlines, level=6)
    idat_chunk = make_chunk(b'IDAT', compressed_data)
    iend_chunk = make_chunk(b'IEND', b'')

    png_bytes = b'\x89PNG\r\n\x1a\n' + ihdr_chunk + idat_chunk + iend_chunk

    with open(out_path, 'wb') as f:
        f.write(png_bytes)

    file_size = len(png_bytes)
    print(f"Successfully wrote {file_size} bytes to {out_path}")

if __name__ == '__main__':
    main()
