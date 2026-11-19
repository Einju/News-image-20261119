#!/usr/bin/env python3
import os
import sys
import zlib
import struct
import binascii

# --- PURE PYTHON STANDARD LIBRARY PNG ENCODER & INFOGRAPHIC GENERATOR ---
# Generates a 2048x2048 supersampled canvas, draws the 19 November 2026 news infographic,
# downsamples via 2x2 box filter to 1024x1024, and writes a valid PNG.

WIDTH = 2048
HEIGHT = 2048
OUT_WIDTH = 1024
OUT_HEIGHT = 1024

# 5x7 Bitmap Font definitions (ASCII 32 to 95)
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
    ':': (0x00, 0x04, 0x00, 0x00, 0x04, 0x00, 0x00),
    ';': (0x00, 0x04, 0x00, 0x00, 0x04, 0x04, 0x08),
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

# --- Canvas operations ---
def create_canvas():
    canvas = bytearray(WIDTH * HEIGHT * 3)
    for y in range(HEIGHT):
        r = int(15 + (30 - 15) * (y / HEIGHT))
        g = int(23 + (41 - 23) * (y / HEIGHT))
        b = int(42 + (59 - 42) * (y / HEIGHT))
        row_offset = y * WIDTH * 3
        row_bytes = bytes([r, g, b]) * WIDTH
        canvas[row_offset:row_offset + WIDTH * 3] = row_bytes
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

# --- Story Icon Drawing Helpers (Enlarged by ~50%) ---
def draw_icon_diplomacy(canvas, cx, cy):
    # Three meeting figures / nodes connected (APEC / Trilateral Summit) - enlarged ~50%
    for dx, dy in [(-60, 0), (0, -45), (60, 0)]:
        draw_rounded_rect(canvas, cx+dx-22, cy+dy-22, cx+dx+22, cy+dy+22, 12, 59, 130, 246)
    fill_rect(canvas, cx-45, cy-8, cx+45, cy+8, 147, 197, 253)

def draw_icon_tech(canvas, cx, cy):
    # NASDAQ / Anthropic stock chart & AI chip icon - enlarged ~50%
    draw_rounded_rect(canvas, cx-75, cy-60, cx+75, cy+60, 15, 16, 185, 129)
    fill_rect(canvas, cx-52, cy+15, cx-30, cy+38, 255, 255, 255)
    fill_rect(canvas, cx-18, cy-15, cx+4, cy+38, 255, 255, 255)
    fill_rect(canvas, cx+16, cy-38, cx+38, cy+38, 255, 255, 255)

def draw_icon_conflict(canvas, cx, cy):
    # Conflict: Flame / Explosion shape (replaced red cross) - enlarged ~50%
    draw_rounded_rect(canvas, cx-68, cy-68, cx+68, cy+68, 33, 239, 68, 68)
    # Explosion burst rays and core in white/yellow
    fill_rect(canvas, cx-50, cy-12, cx+50, cy+12, 255, 255, 255)
    fill_rect(canvas, cy-12, cy-50, cx+12, cy+50, 255, 255, 255)
    fill_rect(canvas, cx-35, cy-35, cx+35, cy+35, 254, 240, 138)
    fill_rect(canvas, cx-18, cy-18, cx+18, cy+18, 255, 255, 255)

def draw_icon_gaming(canvas, cx, cy):
    # GTA VI Game Controller badge - enlarged ~50%
    draw_rounded_rect(canvas, cx-75, cy-52, cx+75, cy+52, 24, 168, 85, 247)
    draw_text(canvas, "VI", cx-32, cy-26, 6, 255, 255, 255)

def draw_icon_economy(canvas, cx, cy):
    # EU / Euro loan symbol - enlarged ~50%
    draw_rounded_rect(canvas, cx-68, cy-68, cx+68, cy+68, 33, 234, 179, 8)
    draw_text(canvas, "EUR", cx-48, cy-21, 4, 15, 23, 42)

def draw_icon_weather(canvas, cx, cy):
    # Cyclone spiral icon - compact concentric arcs curving inward, light blue and white, no vertical lines
    draw_rounded_rect(canvas, cx-68, cy-68, cx+68, cy+68, 33, 56, 189, 248)
    
    # Outer arc segments
    for x_off, y_off in [
        (-35, -20), (-28, -32), (-12, -38), (5, -36), (22, -28), (35, -12),
        (38, 8), (30, 25), (15, 36), (-5, 38), (-22, 30), (-35, 15), (-38, -2)
    ]:
        fill_rect(canvas, cx + x_off - 3, cy + y_off - 3, cx + x_off + 3, cy + y_off + 3, 240, 249, 255)

    # Middle arc segments
    for x_off, y_off in [
        (-22, -10), (-16, -22), (-2, -26), (12, -22), (20, -8),
        (18, 10), (6, 20), (-10, 18), (-18, 5)
    ]:
        fill_rect(canvas, cx + x_off - 3, cy + y_off - 3, cx + x_off + 3, cy + y_off + 3, 255, 255, 255)

    # Inner core arc segments
    for x_off, y_off in [
        (-10, -5), (-6, -12), (2, -14), (10, -6), (6, 6), (-2, 10), (-8, 2)
    ]:
        fill_rect(canvas, cx + x_off - 2, cy + y_off - 2, cx + x_off + 2, cy + y_off + 2, 240, 249, 255)


def main():
    print("Generating 2048x2048 infographic canvas...")
    canvas = create_canvas()

    # --- Header Section ---
    draw_text(canvas, "THURSDAY 19 NOVEMBER 2026", 100, 90, 5, 255, 255, 255)
    draw_text(canvas, "THE WORLD TODAY IN SIX STORIES", 100, 160, 3, 148, 163, 184)

    # Accent decorative bar under header
    fill_rect(canvas, 100, 205, 1948, 213, 59, 130, 246)

    # --- Stories Data (2x3 Grid with enriched details and no dollar signs) ---
    stories = [
        {
            "category": "DIPLOMACY",
            "cat_color": (59, 130, 246),
            "headline": "TRUMP, XI & PUTIN MEET IN SHENZHEN",
            "desc": "First-ever trilateral summit of the three global leaders at APEC puts nuclear arms control firmly on the agenda; the three leaders hold the first trilateral in history.",
            "icon": draw_icon_diplomacy
        },
        {
            "category": "TECHNOLOGY",
            "cat_color": (16, 185, 129),
            "headline": "ANTHROPIC DEBUTS ON NASDAQ",
            "desc": "Ticker ANT debuts, priced at 83 dollars a share with a 1.4 trillion dollar valuation in the largest AI IPO ever recorded; 825 million shares sold during the initial public offering.",
            "icon": draw_icon_tech
        },
        {
            "category": "CONFLICT",
            "cat_color": (239, 68, 68),
            "headline": "GULF WAR WIDENS OVERNIGHT",
            "desc": "Iran fires on US sites in Kuwait; UAE oil tanker struck in Strait of Hormuz with 11 crew injured and 1 missing; Houthi drones intercepted over Riyadh.",
            "icon": draw_icon_conflict
        },
        {
            "category": "GAMING",
            "cat_color": (168, 85, 247),
            "headline": "GTA VI LAUNCHES WORLDWIDE",
            "desc": "Global rollout begins to unprecedented fanfare, accompanied by universal acclaim and a 99 score on Metacritic; midnight rollout started in Australia.",
            "icon": draw_icon_gaming
        },
        {
            "category": "ECONOMY",
            "cat_color": (234, 179, 8),
            "headline": "EU PLANS EUR 45B UKRAINE LOAN",
            "desc": "New sweeping financial support package covers Ukraine's 70 billion euro deficit, structured so repayment occurs exclusively after Russian reparations.",
            "icon": draw_icon_economy
        },
        {
            "category": "WEATHER",
            "cat_color": (56, 189, 248),
            "headline": "CYCLONE AKVAN NEARS INDIA",
            "desc": "Severe tropical cyclone on direct collision course to cross the coast between Machilipatnam and Puri; India reviews railway preparedness.",
            "icon": draw_icon_weather
        }
    ]

    # --- Grid Layout Parameters (Balanced vertical layout filling canvas) ---
    grid_x = 100
    grid_y = 240
    card_w = 900
    card_h = 564
    gap_x = 48
    gap_y = 45

    for idx, story in enumerate(stories):
        col = idx % 2
        row = idx // 2
        cx = grid_x + col * (card_w + gap_x)
        cy = grid_y + row * (card_h + gap_y)

        # Draw card background (rounded rect, dark slate)
        draw_rounded_rect(canvas, cx, cy, cx + card_w, cy + card_h, 24, 30, 41, 59)
        # Card top accent strip
        draw_rounded_rect(canvas, cx, cy, cx + card_w, cy + 14, 6, story["cat_color"][0], story["cat_color"][1], story["cat_color"][2])

        # Category Tag
        draw_text(canvas, story["category"], cx + 45, cy + 42, 3, story["cat_color"][0], story["cat_color"][1], story["cat_color"][2])

        # Icon on top-right of card
        story["icon"](canvas, cx + card_w - 95, cy + 85)

        # Headline (enlarged text scale by one step to 4, adjusted wrap and spacing)
        headline_lines = wrap_text(story["headline"], 27)
        h_y = cy + 100
        for h_line in headline_lines:
            draw_text(canvas, h_line, cx + 45, h_y, 4, 255, 255, 255)
            h_y += 38

        # Separator line inside card
        fill_rect(canvas, cx + 45, h_y + 12, cx + card_w - 45, h_y + 15, 51, 65, 85)

        # Description wrapped text (enlarged text scale by one step to 3, increased line spacing and adjusted wrap)
        desc_lines = wrap_text(story["desc"], 40)
        d_y = h_y + 30
        for d_line in desc_lines:
            draw_text(canvas, d_line, cx + 45, d_y, 3, 203, 213, 225)
            d_y += 34

    # Bottom margin verification: grid ends at 240 + 3*564 + 2*45 = 240 + 1692 + 90 = 2022 px.
    # Total canvas height 2048 px -> 26 px margin at bottom (>= 24 px required on 2048x2048 canvas, i.e., 12 px at 1024x1024).

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
