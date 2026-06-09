# Copyright (c) 2025 Nand Yaduwanshi <NoxxOP>
# Location: Supaul, Bihar
# Production Grade Highly-Optimized Custom Thumbnail Engine
# Strictly Designed for Premium Contrast and Typography Hierarchy.

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

# Master Canvas Dimensions
CANVAS_W, CANVAS_H = 1320, 760

FONT_REGULAR_PATH = "ShrutiMusic/assets/font2.ttf"
FONT_BOLD_PATH = "ShrutiMusic/assets/font3.ttf"
DEFAULT_THUMB = "ShrutiMusic/assets/ShrutiBots.jpg"


def wrap_text(draw, text, font, max_width):
    """Wraps headline text intelligently to prevent layout breaks."""
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


def apply_trustworthy_shadow(canvas, intensity=220):
    """Generates a high-end ambient occlusion shadow around the periphery."""
    w, h = canvas.size
    vignette = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    v_draw = ImageDraw.Draw(vignette)
    
    cx, cy = w // 2, h // 2
    max_radius = math.sqrt(cx**2 + cy**2)
    
    for y in range(0, h, 4):
        for x in range(0, w, 6):
            dist = math.sqrt((x - cx)**2 + (y - cy)**2)
            ratio = dist / max_radius
            if ratio > 0.2:
                alpha = int(intensity * ((ratio - 0.2) / 0.8) ** 2)
                alpha = min(240, max(0, alpha))
                v_draw.rectangle([x, y, x+6, y+4], fill=(5, 5, 12, alpha))
                
    vignette = vignette.filter(ImageFilter.GaussianBlur(35))
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
            print(f"[Image Fetch Error] {img_err}")

        if thumb_path and thumb_path.exists():
            base_img = Image.open(thumb_path).convert("RGBA")
        else:
            base_img = Image.open(DEFAULT_THUMB).convert("RGBA")

    except Exception as e:
        print(f"[Engine Fallback Activation] {e}")
        try:
            base_img = Image.open(DEFAULT_THUMB).convert("RGBA")
            title = "ShrutiMusic Engine"
            duration = "0:00"
            views = "Premium Stream"
            channel = "ShrutiBots"
        except:
            traceback.print_exc()
            return None

    try:
        # --- PHASE 1: COLOR GRADING & BACKGROUND CANVAS ---
        canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (12, 12, 18, 255))
        
        # Super-sampling and high contrast mapping for background depth
        bg_blur = base_img.resize((CANVAS_W, CANVAS_H), Image.LANCZOS)
        bg_graded = ImageEnhance.Contrast(bg_blur).enhance(1.65)
        bg_graded = ImageEnhance.Brightness(bg_graded).enhance(0.50)
        bg_graded = ImageEnhance.Color(bg_graded).enhance(1.30)  # Rich saturation bleed
        bg_final = bg_graded.filter(ImageFilter.GaussianBlur(65))
        
        # Soft atmospheric overlay to bind background colors
        ambient_mesh = Image.new("RGBA", (CANVAS_W, CANVAS_H), (14, 16, 26, 110))
        canvas = Image.alpha_composite(bg_final, ambient_mesh)
        canvas = apply_trustworthy_shadow(canvas, intensity=225)

        # --- PHASE 2: GLASSMORPHIC CARD COGNITION ---
        card_w, card_h = 1160, 520
        card_x = (CANVAS_W - card_w) // 2
        card_y = (CANVAS_H - card_h) // 2
        card_radius = 45

        # 3D Soft Drop Blur Shadow below the Container Plate
        card_shadow = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        cs_draw = ImageDraw.Draw(card_shadow)
        cs_draw.rounded_rectangle(
            [card_x - 8, card_y - 8, card_x + card_w + 8, card_y + card_h + 8], 
            radius=card_radius, fill=(0, 0, 0, 195)
        )
        card_shadow = card_shadow.filter(ImageFilter.GaussianBlur(40))
        canvas.paste(card_shadow, (0, 0), card_shadow)

        # Frosted glass panel generation (prevents the solid blinding white glitch)
        glass_mask = Image.new("L", (card_w, card_h), 0)
        g_draw = ImageDraw.Draw(glass_mask)
        g_draw.rounded_rectangle([0, 0, card_w, card_h], radius=card_radius, fill=255)
        
        # Balanced glass alpha opacity
        glass_surface = Image.new("RGBA", (card_w, card_h), (255, 255, 255, 16))
        canvas.paste(glass_surface, (card_x, card_y), glass_mask)

        # --- PHASE 3: THE EMBEDDED THUMBNAIL (LEFT SIDE FIX) ---
        art_w, art_h = 420, 380  # True designer aspect-ratio alignment
        art_x = card_x + 55
        art_y = card_y + (card_h - art_h) // 2

        art_mask = Image.new("L", (art_w, art_h), 0)
        am_draw = ImageDraw.Draw(art_mask)
        am_draw.rounded_rectangle([0, 0, art_w, art_h], radius=25, fill=255)

        # High level asset calibration for the inside card presentation
        calibrated_art = ImageEnhance.Contrast(base_img).enhance(1.25)
        calibrated_art = ImageEnhance.Sharpness(calibrated_art).enhance(1.50)
        art_final = calibrated_art.resize((art_w, art_h), Image.LANCZOS)
        art_final.putalpha(art_mask)

        # Ambient glow background box for the artwork frame
        art_shadow = Image.new("RGBA", (art_w + 40, art_h + 40), (0, 0, 0, 0))
        as_draw = ImageDraw.Draw(art_shadow)
        as_draw.rounded_rectangle([20, 20, art_w + 20, art_h + 20], radius=25, fill=(0, 0, 0, 230))
        art_shadow = art_shadow.filter(ImageFilter.GaussianBlur(25))
        canvas.paste(art_shadow, (art_x - 20, art_y - 20), art_shadow)

        # Dynamic paste to clear the white-box area completely
        canvas.paste(art_final, (art_x, art_y), art_final)

        # Refined glass inner stroke border rim
        glass_rim = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
        gr_draw = ImageDraw.Draw(glass_rim)
        gr_draw.rounded_rectangle([0, 0, card_w, card_h], radius=card_radius, outline=(255, 255, 255, 30), width=2)
        canvas.paste(glass_rim, (card_x, card_y), glass_mask)

        # --- PHASE 4: TYPOGRAPHY HIERARCHY SYSTEM ---
        draw = ImageDraw.Draw(canvas)
        info_x = art_x + art_w + 60
        max_text_w = (card_x + card_w) - info_x - 55

        # A. Subtle Brand Signature
        brand_font = ImageFont.truetype(FONT_BOLD_PATH, 26)
        brand_text = f"// {app.username.upper()}"
        brand_y = card_y + 75
        draw.text((info_x, brand_y), brand_text, fill=(255, 255, 255, 140), font=brand_font)

        # B. Bold Master Headline (Pure Crisp White)
        title_font = ImageFont.truetype(FONT_BOLD_PATH, 50)
        title_lines = wrap_text(draw, title, title_font, max_text_w)
        title_text = "\n".join(title_lines)
        title_y = brand_y + 50
        
        # Soft contrast drop text shadow
        draw.multiline_text((info_x + 2, title_y + 2), title_text, fill=(0, 0, 0, 200), font=title_font, spacing=8)
        draw.multiline_text((info_x, title_y), title_text, fill=(255, 255, 255, 255), font=title_font, spacing=8)

        # C. Metadata Custom Fonts (Color Changed for Hierarchy Contrast)
        meta_font = ImageFont.truetype(FONT_REGULAR_PATH, 28)
        meta_y = title_y + 145
        
        duration_label = duration
        if duration and ":" in duration:
            parts = duration.split(":")
            if len(parts) == 2 and parts[0].isdigit():
                duration_label = f"{parts[0]}m {parts[1]}s"

        meta_items = [
            f"Channel:  {channel}",
            f"Views:    {views}",
            f"Duration: {duration_label}"
        ]

        # Using a highly professional soft pastel color scheme for data
        for idx, meta in enumerate(meta_items):
            y_pos = meta_y + (idx * 45)
            # Text Deep Drop shadow
            draw.text((info_x + 1, y_pos + 1), meta, fill=(0, 0, 0, 160), font=meta_font)
            # Core Text rendering using distinct Soft Premium Ice-Blue Tint
            draw.text((info_x, y_pos), meta, fill=(165, 180, 252, 240), font=meta_font)

        # Thin framing profile around the entire thumbnail boundary
        canvas_rim = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        cr_draw = ImageDraw.Draw(canvas_rim)
        cr_draw.rectangle([0, 0, CANVAS_W, CANVAS_H], outline=(255, 255, 255, 10), width=3)
        canvas = Image.alpha_composite(canvas, canvas_rim)

        # --- PHASE 5: PRODUCTION EXPORT ---
        out = CACHE_DIR / f"{videoid}_final.png"
        canvas.save(out, quality=98, optimize=True)

        if thumb_path and thumb_path.exists():
            try:
                os.remove(thumb_path)
            except:
                pass

        return str(out)

    except Exception as e:
        print(f"[Thumbnail Generation Failure] {e}")
        traceback.print_exc()
        return None
