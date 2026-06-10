# Copyright (c) 2025 Nand Yaduwanshi <NoxxOP>
# Location: Supaul, Bihar
# All rights reserved.
#
# Highly Optimized Left-Thumbnail / Right-Text Seamless Grid Engine.
# Enhanced with Pro Color Grading, Vignette Blending & Alpha Shadow Maps.

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

        # --- STAGE 2: WHITE CONTAINER PANEL WITH BLUR SHADOWS ---
        card_w, card_h = 1160, 520
        card_x = (CANVAS_W - card_w) // 2
        card_y = (CANVAS_H - card_h) // 2
        card_radius = 45

        # Premium Drop Shadow for the main container plate
        card_shadow = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        cs_draw = ImageDraw.Draw(card_shadow)
        cs_draw.rounded_rectangle(
            [card_x - 14, card_y - 14, card_x + card_w + 14, card_y + card_h + 14], 
            radius=card_radius, fill=(0, 0, 0, 240)
        )
        card_shadow = card_shadow.filter(ImageFilter.GaussianBlur(40))
        canvas.paste(card_shadow, (0, 0), card_shadow)

        # Retaining the exact original White Card Border Matrix
        glass_mask = Image.new("L", (card_w, card_h), 0)
        g_draw = ImageDraw.Draw(glass_mask)
        g_draw.rounded_rectangle([0, 0, card_w, card_h], radius=card_radius, fill=255)
        
        white_card_surface = Image.new("RGBA", (card_w, card_h), (255, 255, 255, 255))
        canvas.paste(white_card_surface, (card_x, card_y), glass_mask)

        # --- STAGE 3: INNER PROFESSIONAL GRADIENT (LIGHT BLACK BACKDROP) ---
        # Seamlessly blends fonts and thumbnail together over a rich dark matte surface inside the white frame
        internal_panel = Image.new("RGBA", (card_w - 24, card_h - 24), (16, 18, 24, 250)) 
        internal_mask = Image.new("L", (card_w - 24, card_h - 24), 0)
        int_draw = ImageDraw.Draw(internal_mask)
        int_draw.rounded_rectangle([0, 0, card_w - 24, card_h - 24], radius=38, fill=255)
        
        canvas.paste(internal_panel, (card_x + 12, card_y + 12), internal_mask)

        # --- STAGE 4: FIXED LEFT SIDE THUMBNAIL POSITIONING ---
        # Placed exactly on the left, matching your font layout's previous dimension specs
        art_w, art_h = 440, 340  
        art_x = card_x + 55
        art_y = card_y + (card_h - art_h) // 2

        art_mask = Image.new("L", (art_w, art_h), 0)
        am_draw = ImageDraw.Draw(art_mask)
        am_draw.rounded_rectangle([0, 0, art_w, art_h], radius=25, fill=255)

        # Fine-tuning parameters for maximum image clarity inside the container
        tuned_art = ImageEnhance.Contrast(base_img).enhance(1.35)
        tuned_art = ImageEnhance.Sharpness(tuned_art).enhance(1.50)
        art_final = tuned_art.resize((art_w, art_h), Image.LANCZOS)
        art_final.putalpha(art_mask)

        # Professional Ambient Drop Shadow under the left-side thumbnail artwork block
        art_shadow = Image.new("RGBA", (art_w + 40, art_h + 40), (0, 0, 0, 0))
        as_draw = ImageDraw.Draw(art_shadow)
        as_draw.rounded_rectangle([20, 20, art_w + 20, art_h + 20], radius=25, fill=(0, 0, 0, 255))
        art_shadow = art_shadow.filter(ImageFilter.GaussianBlur(22))
        canvas.paste(art_shadow, (art_x - 20, art_y - 20), art_shadow)

        # Paste the final dynamic music thumbnail inside the left segment
        canvas.paste(art_final, (art_x, art_y), art_final)

        # Inner container outline white rim stroke mapping
        glass_rim = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
        gr_draw = ImageDraw.Draw(glass_rim)
        gr_draw.rounded_rectangle([0, 0, card_w, card_h], radius=card_radius, outline=(255, 255, 255, 35), width=2)
        canvas.paste(glass_rim, (card_x, card_y), glass_mask)

        # --- STAGE 5: RIGHT ALIGNED FONTS & TEXT HIERARCHY ---
        # All details shifted to the right segment right next to the video thumbnail image
        draw = ImageDraw.Draw(canvas)
        info_x = art_x + art_w + 55
        max_text_w = (card_x + card_w) - info_x - 55

        # 1. Premium Brand Sub-Header
        brand_font = ImageFont.truetype(FONT_BOLD_PATH, 24)
        brand_text = f"// {app.username.upper()}"
        brand_y = card_y + 80
        draw.text((info_x, brand_y), brand_text, fill=(56, 189, 248, 210), font=brand_font) # Neon Cyan Tone

        # 2. Main Track Title Headline (Crisp Bold White over dark backdrop surface)
        title_font = ImageFont.truetype(FONT_BOLD_PATH, 46)
        title_lines = wrap_text(draw, title, title_font, max_text_w)
        title_text = "\n".join(title_lines)
        title_y = brand_y + 45
        
        # Heavy shadow layers to prevent white blending text bleed
        draw.multiline_text((info_x + 2, title_y + 2), title_text, fill=(0, 0, 0, 240), font=title_font, spacing=8)
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

        # Multi-color texture parsing loop (Silver vs Gold Premium Combination)
        for idx, (label, val) in enumerate(meta_items):
            y_pos = meta_y + (idx * 48)
            full_text = f"{label}{val}"
            
            draw.text((info_x + 1, y_pos + 1), full_text, fill=(0, 0, 0, 200), font=meta_font)
            draw.text((info_x, y_pos), label, fill=(156, 163, 175, 255), font=meta_font) # Premium Silver Grey
            label_w = draw.textlength(label, font=meta_font)
            draw.text((info_x + label_w, y_pos), val, fill=(252, 211, 77, 240), font=meta_font) # Matte Gold Value

        # Canvas Outer Structural Frame Outline
        canvas_frame = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        cf_draw = ImageDraw.Draw(canvas_frame)
        cf_draw.rectangle([0, 0, CANVAS_W, CANVAS_H], outline=(255, 255, 255, 8), width=3)
        canvas = Image.alpha_composite(canvas, canvas_frame)

        # --- STAGE 6: SAVE EXPORT BUFFER ---
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
