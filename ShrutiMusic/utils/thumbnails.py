# Copyright (c) 2025 Nand Yaduwanshi <NoxxOP>
# Location: Supaul, Bihar
# All rights reserved.
#
# Ultra-Luxury Premium Glassmorphic Thumbnail Engine.
# High-End Design Parameters Inspired by Next-Gen Player Aesthetics.

import os
import random
import aiohttp
import aiofiles
import traceback
import io
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance
from py_yt import VideosSearch
from ShrutiMusic import app

CACHE_DIR = Path("cache")
CACHE_DIR.mkdir(exist_ok=True)

# Master Premium Canvas Resolution
CANVAS_W, CANVAS_H = 1320, 760

FONT_REGULAR_PATH = "ShrutiMusic/assets/font2.ttf"
FONT_BOLD_PATH = "ShrutiMusic/assets/font3.ttf"
DEFAULT_THUMB = "ShrutiMusic/assets/ShrutiBots.jpg"


def wrap_text(draw, text, font, max_width):
    """Wraps title text dynamically to ensure clean layout without overflow."""
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


def apply_premium_outer_glow(canvas, intensity=240):
    """Generates an elite level ambient vignette/outer shadow to give massive depth."""
    w, h = canvas.size
    vignette = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    v_draw = ImageDraw.Draw(vignette)
    
    cx, cy = w // 2, h // 2
    max_radius = math.sqrt(cx**2 + cy**2)
    
    for y in range(0, h, 4):
        for x in range(0, w, 6):
            dist = math.sqrt((x - cx)**2 + (y - cy)**2)
            ratio = dist / max_radius
            if ratio > 0.12:
                alpha = int(intensity * ((ratio - 0.12) / 0.88) ** 2)
                alpha = min(245, max(0, alpha))
                v_draw.rectangle([x, y, x+6, y+4], fill=(5, 5, 10, alpha))
                
    vignette = vignette.filter(ImageFilter.GaussianBlur(40))
    return Image.alpha_composite(canvas, vignette)


async def gen_thumb(videoid: str):
    url = f"https://www.youtube.com/watch?v={videoid}"
    thumb_path = None
    
    try:
        results = VideosSearch(url, limit=1)
        result = (await results.next())["result"][0]

        title = result.get("title", "Unknown Title")
        duration = result.get("duration", "0:00")
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
            print(f"[Image Fetch Error Override] {img_err}")

        if thumb_path and thumb_path.exists():
            base_img = Image.open(thumb_path).convert("RGBA")
        else:
            base_img = Image.open(DEFAULT_THUMB).convert("RGBA")

    except Exception as e:
        print(f"[Engine Fallback Activation] {e}")
        try:
            base_img = Image.open(DEFAULT_THUMB).convert("RGBA")
            title = "ShrutiMusic"
            duration = "0:00"
            views = "Premium Quality"
            channel = "ShrutiBots"
        except:
            traceback.print_exc()
            return None

    try:
        # --- STAGE 1: CINEMATIC COLOR GRADING BACKGROUND ---
        canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (6, 6, 10, 255))
        
        # Super-sampling and high contrast mapping for extreme background depth
        bg_blur = base_img.resize((CANVAS_W, CANVAS_H), Image.LANCZOS)
        bg_graded = ImageEnhance.Contrast(bg_blur).enhance(1.80)
        bg_graded = ImageEnhance.Brightness(bg_graded).enhance(0.42)
        bg_graded = ImageEnhance.Color(bg_graded).enhance(1.45) # Deep vibrant saturation
        bg_final = bg_graded.filter(ImageFilter.GaussianBlur(65))
        
        # Soft atmospheric color dim layer mesh
        dim_mesh = Image.new("RGBA", (CANVAS_W, CANVAS_H), (8, 10, 16, 130))
        canvas = Image.alpha_composite(bg_final, dim_mesh)
        canvas = apply_premium_outer_glow(canvas, intensity=240)

        # --- STAGE 2: PREMIUM HIGH-END METRIC GLASS CONTAINER ---
        card_w, card_h = 1160, 520
        card_x = (CANVAS_W - card_w) // 2
        card_y = (CANVAS_H - card_h) // 2
        card_radius = 45

        # Double-Layer Ultra Soft Border Blur Shadow (Matches your image sample 1000023891)
        card_shadow = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        cs_draw = ImageDraw.Draw(card_shadow)
        cs_draw.rounded_rectangle(
            [card_x - 12, card_y - 12, card_x + card_w + 12, card_y + card_h + 12], 
            radius=card_radius, fill=(0, 0, 0, 235)
        )
        card_shadow = card_shadow.filter(ImageFilter.GaussianBlur(45))
        canvas.paste(card_shadow, (0, 0), card_shadow)

        # Mask logic for frosted surface plate
        glass_mask = Image.new("L", (card_w, card_h), 0)
        g_draw = ImageDraw.Draw(glass_mask)
        g_draw.rounded_rectangle([0, 0, card_w, card_h], radius=card_radius, fill=255)
        
        # Balanced Dark Luxury Glass Mesh (Completely removes blinding white glitch)
        glass_surface = Image.new("RGBA", (card_w, card_h), (12, 14, 22, 195))
        canvas.paste(glass_surface, (card_x, card_y), glass_mask)

        # --- STAGE 3: LEFT SIDE DYNAMIC THUMBNAIL PICTURE ---
        art_w, art_h = 440, 340  # Perfect widescreen display aspect ratio inside the card
        art_x = card_x + 55
        art_y = card_y + (card_h - art_h) // 2

        art_mask = Image.new("L", (art_w, art_h), 0)
        am_draw = ImageDraw.Draw(art_mask)
        am_draw.rounded_rectangle([0, 0, art_w, art_h], radius=30, fill=255)

        # High level tuning for crisp illustration inside the card plate
        tuned_art = ImageEnhance.Contrast(base_img).enhance(1.30)
        tuned_art = ImageEnhance.Sharpness(tuned_art).enhance(1.45)
        art_final = tuned_art.resize((art_w, art_h), Image.LANCZOS)
        art_final.putalpha(art_mask)

        # Accent perimeter shadow map for the video artwork block
        art_shadow = Image.new("RGBA", (art_w + 40, art_h + 40), (0, 0, 0, 0))
        as_draw = ImageDraw.Draw(art_shadow)
        as_draw.rounded_rectangle([20, 20, art_w + 20, art_h + 20], radius=30, fill=(0, 0, 0, 250))
        art_shadow = art_shadow.filter(ImageFilter.GaussianBlur(25))
        canvas.paste(art_shadow, (art_x - 20, art_y - 20), art_shadow)

        # Paste the dynamically fitted thumbnail safely onto the left side
        canvas.paste(art_final, (art_x, art_y), art_final)

        # Sleek glowing border rim stroke outline around the plate container
        glass_rim = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
        gr_draw = ImageDraw.Draw(glass_rim)
        gr_draw.rounded_rectangle([0, 0, card_w, card_h], radius=card_radius, outline=(255, 255, 255, 25), width=2)
        canvas.paste(glass_rim, (card_x, card_y), glass_mask)

        # --- STAGE 4: DESIGNER TYPOGRAPHY & COLOR HIERARCHY SYSTEM ---
        draw = ImageDraw.Draw(canvas)
        info_x = art_x + art_w + 55
        max_text_w = (card_x + card_w) - info_x - 55

        # 1. Premium Brand Sub-Header
        brand_font = ImageFont.truetype(FONT_BOLD_PATH, 24)
        brand_text = f"// {app.username.upper()}"
        brand_y = card_y + 75
        draw.text((info_x, brand_y), brand_text, fill=(56, 189, 248, 190), font=brand_font) # Neon Cyan Accent Line

        # 2. Main Track Headline Title (Pure Crisp White for instant eye capture)
        title_font = ImageFont.truetype(FONT_BOLD_PATH, 48)
        title_lines = wrap_text(draw, title, title_font, max_text_w)
        title_text = "\n".join(title_lines)
        title_y = brand_y + 45
        
        # Multi-layer deep text drop shadow to guarantee highest readability
        draw.multiline_text((info_x + 3, title_y + 3), title_text, fill=(0, 0, 0, 230), font=title_font, spacing=8)
        draw.multiline_text((info_x, title_y), title_text, fill=(255, 255, 255, 255), font=title_font, spacing=8)

        # 3. Sub-Fonts Configuration (Separated Colors for Pro Hierarchy Contrast)
        meta_font = ImageFont.truetype(FONT_REGULAR_PATH, 28)
        meta_y = title_y + 135
        
        duration_label = duration
        if duration and ":" in duration:
            parts = duration.split(":")
            if len(parts) == 2 and parts[0].isdigit():
                duration_label = f"{parts[0]}m {parts[1]}s"

        meta_items = [
            ("Channel:", f" {channel}"),
            ("Views:", f"   {views}"),
            ("Duration:", f" {duration_label}")
        ]

        # Multi-color texture parsing loop
        for idx, (label, val) in enumerate(meta_items):
            y_pos = meta_y + (idx * 48)
            full_text = f"{label}{val}"
            
            # Crisp drop shadow behind details block
            draw.text((info_x + 1, y_pos + 1), full_text, fill=(0, 0, 0, 190), font=meta_font)
            
            # Rendering labels using Premium Pastel Slate Grey
            draw.text((info_x, y_pos), label, fill=(148, 163, 184, 240), font=meta_font)
            label_w = draw.textlength(label, font=meta_font)
            # Rendering values using Luxurious Deep Matte Gold for high-end look
            draw.text((info_x + label_w, y_pos), val, fill=(252, 211, 77, 235), font=meta_font)

        # Outer canvas boundary profile frame line mapping
        canvas_frame = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        cf_draw = ImageDraw.Draw(canvas_frame)
        cf_draw.rectangle([0, 0, CANVAS_W, CANVAS_H], outline=(255, 255, 255, 8), width=3)
        canvas = Image.alpha_composite(canvas, canvas_frame)

        # --- STAGE 5: SAVE EXPORT LOGIC BUFFER ---
        out = CACHE_DIR / f"{videoid}_final.png"
        canvas.save(out, quality=98, optimize=True)

        if thumb_path and thumb_path.exists():
            try:
                os.remove(thumb_path)
            except:
                pass

        return str(out)

    except Exception as e:
        print(f"[Thumbnail Compilation System Critical Error] {e}")
        traceback.print_exc()
        return None
