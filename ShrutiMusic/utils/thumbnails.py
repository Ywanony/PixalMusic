# Copyright (c) 2025 Nand Yaduwanshi <NoxxOP>
# Location: Supaul, Bihar
# All rights reserved.
# Code Enhanced for Premium Shadow and Professional Aesthetics.

import os
import random
import aiohttp
import aiofiles
import traceback
import io
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
from py_yt import VideosSearch
from ShrutiMusic import app
import math

CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)

CANVAS_W, CANVAS_H = 1320, 760

FONT_REGULAR_PATH = "ShrutiMusic/assets/font2.ttf"
FONT_BOLD_PATH = "ShrutiMusic/assets/font3.ttf"
DEFAULT_THUMB = "ShrutiMusic/assets/ShrutiBots.jpg"


def wrap_text(draw, text, font, max_width):
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        test_line = current_line + (" " if current_line else "") + word
        if draw.textlength(test_line, font=font) <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    return lines[:2]


def random_gradient():
    colors = [
        [(15, 12, 41), (48, 43, 99), (36, 36, 62)],
        [(10, 10, 10), (35, 35, 40), (20, 20, 25)],
        [(26, 26, 46), (56, 56, 86), (40, 40, 60)],
        [(20, 25, 35), (45, 50, 70), (30, 35, 50)],
        [(12, 17, 30), (38, 43, 65), (25, 30, 45)],
        [(18, 18, 28), (48, 48, 68), (32, 32, 48)],
        [(8, 15, 25), (28, 40, 55), (18, 28, 40)],
        [(22, 22, 35), (52, 52, 75), (35, 35, 55)],
        [(14, 20, 28), (44, 50, 68), (28, 35, 48)],
        [(16, 14, 38), (46, 44, 88), (30, 28, 60)],
    ]
    return random.choice(colors)


def apply_gradient(canvas, colors):
    overlay = Image.new('RGBA', canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    
    for y in range(CANVAS_H):
        progress = y / CANVAS_H
        
        if progress < 0.4:
            t = progress / 0.4
            r = int(colors[0][0] * (1-t) + colors[1][0] * t)
            g = int(colors[0][1] * (1-t) + colors[1][1] * t)
            b = int(colors[0][2] * (1-t) + colors[2][2] * t)
        else:
            t = (progress - 0.4) / 0.6
            r = int(colors[1][0] * (1-t) + colors[2][0] * t)
            g = int(colors[1][1] * (1-t) + colors[2][1] * t)
            b = int(colors[1][2] * (1-t) + colors[2][2] * t)
        
        draw.line([(0, y), (CANVAS_W, y)], fill=(r, g, b, 255))
    
    return Image.alpha_composite(canvas, overlay)


def random_layout():
    layouts = [
        {
            'art_size': random.randint(440, 500),
            'art_x': random.randint(80, 130),
            'art_shape': 'rounded',
            'text_align': 'right',
            'accent_style': 'glow',
            'show_particles': False
        },
        {
            'art_size': random.randint(440, 500),
            'art_x': CANVAS_W - random.randint(540, 600),
            'art_shape': 'rounded',
            'text_align': 'left',
            'accent_style': 'glow',
            'show_particles': False
        }
    ]
    return random.choice(layouts)


def create_shape_mask(size, shape):
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    radius = 35  # Clean professional rounded corners like Spotify/Apple Music
    draw.rounded_rectangle([0, 0, size, size], radius=radius, fill=255)
    return mask


def random_accent_color():
    colors = [
        (88, 166, 255),
        (138, 180, 248),
        (156, 163, 255),
        (200, 200, 220),
        (180, 190, 254),
        (120, 200, 255),
        (165, 177, 255),
        (148, 226, 213),
    ]
    return random.choice(colors)


def add_premium_edge_shadow(canvas):
    """
    Creates that deep, professional light shadow/vignette effect 
    around all 4 edges of the thumbnail just like requested.
    """
    shadow_mask = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_mask)
    
    # Outer dark edge vignette frame
    border_thickness = 45
    for i in range(border_thickness):
        alpha = int(140 * (1.0 - (i / border_thickness)))
        s_draw.rectangle(
            [i, i, CANVAS_W - i, CANVAS_H - i], 
            outline=(10, 10, 15, alpha), 
            width=1
        )
        
    shadow_mask = shadow_mask.filter(ImageFilter.GaussianBlur(18))
    return Image.alpha_composite(canvas, shadow_mask)


def add_glow_ring(canvas, x, y, size, color, blur_amount):
    ring_size = size + 30
    ring_img = Image.new("RGBA", (ring_size, ring_size), (0, 0, 0, 0))
    rdraw = ImageDraw.Draw(ring_img)
    
    for i in range(4):
        offset = i * 4
        alpha = 100 - (i * 25)
        rdraw.ellipse([offset, offset, ring_size - offset, ring_size - offset],
                     outline=(*color, alpha), width=2)
    
    ring_img = ring_img.filter(ImageFilter.GaussianBlur(blur_amount))
    canvas.paste(ring_img, (x - 15, y - 15), ring_img)


async def gen_thumb(videoid: str):
    url = f"https://www.youtube.com/watch?v={videoid}"
    thumb_path = None
    
    try:
        results = VideosSearch(url, limit=1)
        result = (await results.next())["result"][0]

        title = result.get("title", "Unknown Title")
        duration = result.get("duration", "Unknown")
        thumburl = result["thumbnails"][0]["url"].split("?")[0]
        views = result.get("viewCount", {}).get("short", "Unknown Views")
        channel = result.get("channel", {}).get("name", "Unknown Channel")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(thumburl) as resp:
                    if resp.status == 200:
                        thumb_path = CACHE_DIR / f"thumb{videoid}.png"
                        async with aiofiles.open(thumb_path, "wb") as f:
                            await f.write(await resp.read())
        except Exception as img_err:
            print(f"[Image Download Error] {img_err}")

        if thumb_path and thumb_path.exists():
            base_img = Image.open(thumb_path).convert("RGBA")
        else:
            base_img = Image.open(DEFAULT_THUMB).convert("RGBA")

    except Exception as e:
        print(f"[gen_thumb Error - Using Default] {e}")
        try:
            base_img = Image.open(DEFAULT_THUMB).convert("RGBA")
            title = "ShrutiMusic"
            duration = "Unknown"
            views = "Unknown Views"
            channel = "ShrutiBots"
        except:
            traceback.print_exc()
            return None

    try:
        canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 255))
        
        gradient_colors = random_gradient()
        canvas = apply_gradient(canvas, gradient_colors)
        
        layout = random_layout()
        accent_color = random_accent_color()
        
        art_size = layout['art_size']
        art_x = layout['art_x']
        art_y = (CANVAS_H - art_size) // 2
        
        # High level color grading for album art
        contrast_en = ImageEnhance.Contrast(base_img)
        graded_img = contrast_en.enhance(1.30)
        sharp_en = ImageEnhance.Sharpness(graded_img)
        graded_img = sharp_en.enhance(1.35)
        
        mask = create_shape_mask(art_size, layout['art_shape'])
        art = graded_img.resize((art_size, art_size), Image.LANCZOS)
        art.putalpha(mask)
        
        # Album Art Drop Shadow
        glow_padding = 140
        glow_canvas_size = art_size + glow_padding
        glow_layer = Image.new("RGBA", (glow_canvas_size, glow_canvas_size), (0, 0, 0, 0))
        glow_draw = ImageDraw.Draw(glow_layer)
        
        glow_draw.ellipse(
            [25, 25, glow_canvas_size - 25, glow_canvas_size - 25],
            fill=(0, 0, 0, 150)
        )
        glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(50))
        canvas.paste(glow_layer, (art_x - (glow_padding // 2), art_y - (glow_padding // 2)), glow_layer)
        
        add_glow_ring(canvas, art_x, art_y, art_size, accent_color, 12)
        canvas.paste(art, (art_x, art_y), art)
        
        draw = ImageDraw.Draw(canvas)
        
        brand_font = ImageFont.truetype(FONT_BOLD_PATH, 42)
        brand_x = 65
        brand_y = 50
        
        draw.text((brand_x + 2, brand_y + 2), app.username, fill=(0, 0, 0, 150), font=brand_font)
        draw.text((brand_x, brand_y), app.username, fill=(255, 255, 255, 230), font=brand_font)
        
        if layout['text_align'] == 'right':
            info_x = art_x + art_size + 80
            max_text_w = CANVAS_W - info_x - 65
        else:
            info_x = 80
            max_text_w = art_x - info_x - 60
        
        np_font = ImageFont.truetype(FONT_BOLD_PATH, 60)
        np_text = "NOW PLAYING"
        np_y = 150
        
        draw.text((info_x + 2, np_y + 2), np_text, fill=(0, 0, 0, 180), font=np_font)
        draw.text((info_x, np_y), np_text, fill=(*accent_color, 255), font=np_font)
        
        title_font = ImageFont.truetype(FONT_BOLD_PATH, 44)
        title_lines = wrap_text(draw, title, title_font, max_text_w)
        title_text = "\n".join(title_lines)
        title_y = np_y + 90
        
        draw.multiline_text((info_x + 2, title_y + 2), title_text, fill=(0, 0, 0, 180), font=title_font, spacing=10)
        draw.multiline_text((info_x, title_y), title_text, fill=(255, 255, 255, 255), font=title_font, spacing=10)
        
        meta_font = ImageFont.truetype(FONT_REGULAR_PATH, 32)
        meta_y = title_y + 140
        line_spacing = 55
        
        duration_label = duration
        if duration and ":" in duration:
            parts = duration.split(":")
            if len(parts) == 2 and parts[0].isdigit():
                duration_label = f"{parts[0]}m {parts[1]}s"
        
        meta_items = [
            f"Views: {views}",
            f"Duration: {duration_label}",
            f"Channel: {channel}"
        ]
        
        for idx, meta in enumerate(meta_items):
            y = meta_y + (idx * line_spacing)
            draw.text((info_x + 2, y + 2), meta, fill=(0, 0, 0, 150), font=meta_font)
            draw.text((info_x, y), meta, fill=(220, 220, 230, 255), font=meta_font)
            
        # --- APPLYING THE ULTRA LUXURY BLURRED EDGE SHADOW ---
        canvas = add_premium_edge_shadow(canvas)
        
        out = CACHE_DIR / f"{videoid}_final.png"
        canvas.save(out, quality=95, optimize=True)

        if thumb_path and thumb_path.exists():
            try:
                os.remove(thumb_path)
            except:
                pass

        return str(out)

    except Exception as e:
        print(f"[gen_thumb Processing Error] {e}")
        traceback.print_exc()
        return None
