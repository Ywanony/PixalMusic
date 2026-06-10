# Copyright (c) 2025 Nand Yaduwanshi <NoxxOP>
# Location: Supaul, Bihar
# All rights reserved.
#
# Replacement Engine: White Background Replaced with Dynamic Video Thumbnail.
# Smooth Right-Gradient Shadow Overlay for Maximum Typography Contrast.

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

# Master Premium Canvas Dimensions
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
        
        bg_blur = base_img.resize((CANVAS_W, CANVAS_H), Image.LANCZOS)
        bg_graded = ImageEnhance.Contrast(bg_blur).enhance(1.80)
        bg_graded = ImageEnhance.Brightness(bg_graded).enhance(0.42)
        bg_graded = ImageEnhance.Color(bg_graded).enhance(1.45)
        bg_final = bg_graded.filter(ImageFilter.GaussianBlur(65))
        
        dim_mesh = Image.new("RGBA", (CANVAS_W, CANVAS_H), (8, 10, 16, 130))
        canvas = Image.alpha_composite(bg_final, dim_mesh)
        canvas = apply_premium_outer_glow(canvas, intensity=240)

        # --- STAGE 2: CONTAINER DIMENSIONS & DROP SHADOW ---
        card_w, card_h = 1160, 520
        card_x = (CANVAS_W - card_w) // 2
        card_y = (CANVAS_H - card_h) // 2
        card_radius = 45

        # Glowing Outer Drop Shadow for the main container plate
        card_shadow = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        cs_draw = ImageDraw.Draw(card_shadow)
        cs_draw.rounded_rectangle(
            [card_x - 14, card_y - 14, card_x + card_w + 14, card_y + card_h + 14], 
            radius=card_radius, fill=(0, 0, 0, 245)
        )
        card_shadow = card_shadow.filter(ImageFilter.GaussianBlur(35))
        canvas.paste(card_shadow, (0, 0), card_shadow)

        # Create mask layer for rounding the main center content
        glass_mask = Image.new("L", (card_w, card_h), 0)
        g_draw = ImageDraw.Draw(glass_mask)
        g_draw.rounded_rectangle([0, 0, card_w, card_h], radius=card_radius, fill=255)

        # --- STAGE 3: THE FIXED THUMBNAIL (Sits where the white box used to be) ---
        # Tuning real music image parameters to look vibrant
        tuned_main = ImageEnhance.Contrast(base_img).enhance(1.20)
        tuned_main = ImageEnhance.Brightness(tuned_main).enhance(0.95)
        main_card_surface = tuned_main.resize((card_w, card_h), Image.LANCZOS)
        
        # Paste the real video image directly as the container background
        canvas.paste(main_card_surface, (card_x, card_y), glass_mask)

        # --- STAGE 4: RIGHT-SIDE SMOOTH DARK GRADIENT FOR FONT READABILITY ---
        # This shadow layer blends smoothly from transparent (left) to dark black (right)
        # It guarantees that fonts are perfectly visible without making the card look isolated.
        shadow_overlay = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
        so_draw = ImageDraw.Draw(shadow_overlay)
        
        for x_pos in range(card_w):
            if x_pos > card_w // 3:  # Gradient starts from 1/3rd of the card length
                factor = (x_pos - (card_w // 3)) / (card_w * 2 / 3)
                alpha_val = int(factor * 235)  # Soft peak density shadow
                alpha_val = min(235, max(0, alpha_val))
                so_draw.line([(x_pos, 0), (x_pos, card_h)], fill=(12, 14, 20, alpha_val))
                
        canvas.paste(shadow_overlay, (card_x, card_y), glass_mask)

        # Sleek inner border rim profile
        glass_rim = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
        gr_draw = ImageDraw.Draw(glass_rim)
        gr_draw.rounded_rectangle([0, 0, card_w, card_h], radius=card_radius, outline=(255, 255, 255, 45), width=2)
        canvas.paste(glass_rim, (card_x, card_y), glass_mask)

        # --- STAGE 5: FONTS POSITIONING & TYPOGRAPHY HIERARCHY ---
        # Placed on the right side over the custom shadow mesh gradient
        draw = ImageDraw.Draw(canvas)
        info_x = card_x + (card_w // 2) - 30  # Plenty of safe horizontal grid room
        max_text_w = (card_x + card_w) - info_x - 55

        # 1. Premium Brand Sub-Header
        brand_font = ImageFont.truetype(FONT_BOLD_PATH, 24)
        brand_text = f"// {app.username.upper()}"
        brand_y = card_y + 85
        draw.text((info_x, brand_y), brand_text, fill=(56, 189, 248, 230), font=brand_font) # Neon Cyan Accent

        # 2. Main Track Headline Title
        title_font = ImageFont.truetype(FONT_BOLD_PATH, 46)
        title_lines = wrap_text(draw, title, title_font, max_text_w)
        title_text = "\n".join(title_lines)
        title_y = brand_y + 45
        
        # Heavy drop shadow layers to back up crisp white text tracking
        draw.multiline_text((info_x + 3, title_y + 3), title_text, fill=(0, 0, 0, 255), font=title_font, spacing=8)
        draw.multiline_text((info_x, title_y), title_text, fill=(255, 255, 255, 255), font=title_font, spacing=8)

        # 3. Custom Metadata Fields
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

        # Process metadata loops side by side with matte gold and silver grey values
        for idx, (label, val) in enumerate(meta_items):
            y_pos = meta_y + (idx * 48)
            full_text = f"{label}{val}"
            
            draw.text((info_x + 2, y_pos + 2), full_text, fill=(0, 0, 0, 230), font=meta_font)
            draw.text((info_x, y_pos), label, fill=(203, 213, 225, 255), font=meta_font) # Ultra Clean Light Slate
            label_w = draw.textlength(label, font=meta_font)
            draw.text((info_x + label_w, y_pos), val, fill=(252, 211, 77, 245), font=meta_font) # Luxurious Yellow-Gold

        # Outer canvas boundary out-rim frame profile line
        canvas_frame = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        cf_draw = ImageDraw.Draw(canvas_frame)
        cf_draw.rectangle([0, 0, CANVAS_W, CANVAS_H], outline=(255, 255, 255, 8), width=3)
        canvas = Image.alpha_composite(canvas, canvas_frame)

        # --- STAGE 6: SAVE EXPORT LOGIC BUFFER ---
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
