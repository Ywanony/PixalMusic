# Copyright (c) 2025 Nand Yaduwanshi <NoxxOP>
# Location: Supaul, Bihar
# All rights reserved.
#
# Intellectual property of Nand Yaduwanshi.
# Enhanced Production Version: Full Advanced Glassmorphism & High-End Vignette Engine.

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

CANVAS_W, CANVAS_H = 1320, 760

FONT_REGULAR_PATH = "ShrutiMusic/assets/font2.ttf"
FONT_BOLD_PATH = "ShrutiMusic/assets/font3.ttf"
DEFAULT_THUMB = "ShrutiMusic/assets/ShrutiBots.jpg"


def wrap_text(draw, text, font, max_width):
    """Wraps text cleanly into lines so it doesn't overflow the canvas"""
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


def apply_premium_vignette(canvas, intensity=190):
    """Creates an ultra-luxury dark blur shadow around all 4 edges of the thumbnail"""
    w, h = canvas.size
    vignette = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    v_draw = ImageDraw.Draw(vignette)
    
    cx, cy = w // 2, h // 2
    max_radius = math.sqrt(cx**2 + cy**2)
    
    for y in range(0, h, 3):
        for x in range(0, w, 5):
            dist = math.sqrt((x - cx)**2 + (y - cy)**2)
            ratio = dist / max_radius
            if ratio > 0.25:
                alpha = int(intensity * ((ratio - 0.25) / 0.75) ** 2)
                alpha = min(230, max(0, alpha))
                v_draw.rectangle([x, y, x+5, y+3], fill=(8, 8, 14, alpha))
                
    vignette = vignette.filter(ImageFilter.GaussianBlur(25))
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
            duration = "0:00"
            views = "Unknown Views"
            channel = "ShrutiBots"
        except:
            traceback.print_exc()
            return None

    try:
        # --- STAGE 1: DYNAMIC BACKGROUND PROCESSING & COLOR GRADIENTS ---
        canvas = Image.new("RGBA", (CANVAS_W, CANVAS_H), (10, 10, 15, 255))
        
        # Creating a beautiful rich blurred background from the YouTube thumbnail itself
        bg_blur = base_img.resize((CANVAS_W, CANVAS_H), Image.LANCZOS)
        bg_graded = ImageEnhance.Contrast(bg_blur).enhance(1.50)
        bg_graded = ImageEnhance.Brightness(bg_graded).enhance(0.55)
        bg_final = bg_graded.filter(ImageFilter.GaussianBlur(55))
        
        # Smooth atmospheric ambient tint layer
        ambient_tint = Image.new("RGBA", (CANVAS_W, CANVAS_H), (12, 14, 22, 100))
        canvas = Image.alpha_composite(bg_final, ambient_tint)
        
        # Injecting the mathematical soft edge dark shadow vignette
        canvas = apply_premium_vignette(canvas, intensity=210)

        # --- STAGE 2: MATHEMATICAL PREMIUM GLASS CONTAINER ---
        card_w, card_h = 1140, 520
        card_x = (CANVAS_W - card_w) // 2
        card_y = (CANVAS_H - card_h) // 2
        card_radius = 45

        # Creating the soft depth drop shadow behind the glass plate
        card_shadow = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        cs_draw = ImageDraw.Draw(card_shadow)
        cs_draw.rounded_rectangle(
            [card_x - 6, card_y - 6, card_x + card_w + 6, card_y + card_h + 6], 
            radius=card_radius, fill=(0, 0, 0, 170)
        )
        card_shadow = card_shadow.filter(ImageFilter.GaussianBlur(35))
        canvas.paste(card_shadow, (0, 0), card_shadow)

        # Alpha-blended frosted glass layer mask mapping
        glass_mask = Image.new("L", (card_w, card_h), 0)
        g_draw = ImageDraw.Draw(glass_mask)
        g_draw.rounded_rectangle([0, 0, card_w, card_h], radius=card_radius, fill=255)
        
        glass_surface = Image.new("RGBA", (card_w, card_h), (255, 255, 255, 14))
        canvas.paste(glass_surface, (card_x, card_y), glass_mask)

        # --- STAGE 3: CRISP RESOLUTION ALBUM ARTWORK ---
        art_size = 380
        art_x = card_x + 55
        art_y = card_y + (card_h - art_size) // 2

        art_mask = Image.new("L", (art_size, art_size), 0)
        am_draw = ImageDraw.Draw(art_mask)
        am_draw.rounded_rectangle([0, 0, art_size, art_size], radius=25, fill=255)

        # Master grade digital tuning for clarity inside the player card
        tuned_art = ImageEnhance.Contrast(base_img).enhance(1.30)
        tuned_art = ImageEnhance.Sharpness(tuned_art).enhance(1.45)
        art_final = tuned_art.resize((art_size, art_size), Image.LANCZOS)
        art_final.putalpha(art_mask)

        # Smooth border back-shadow map specifically for the album image cover
        art_shadow = Image.new("RGBA", (art_size + 40, art_size + 40), (0, 0, 0, 0))
        as_draw = ImageDraw.Draw(art_shadow)
        as_draw.rounded_rectangle([20, 20, art_size + 20, art_size + 20], radius=25, fill=(0, 0, 0, 220))
        art_shadow = art_shadow.filter(ImageFilter.GaussianBlur(22))
        canvas.paste(art_shadow, (art_x - 20, art_y - 20), art_shadow)

        canvas.paste(art_final, (art_x, art_y), art_final)

        # Luxury sleek border stroke on the glass plate edge container
        glass_rim = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
        gr_draw = ImageDraw.Draw(glass_rim)
        gr_draw.rounded_rectangle([0, 0, card_w, card_h], radius=card_radius, outline=(255, 255, 255, 28), width=2)
        canvas.paste(glass_rim, (card_x, card_y), glass_mask)

        # --- STAGE 4: DESIGNER TYPOGRAPHY & TEXT HIERARCHY ---
        draw = ImageDraw.Draw(canvas)
        info_x = art_x + art_size + 65
        max_text_w = (card_x + card_w) - info_x - 55

        # 1. Branding Text (Clean & Minimal sub-head)
        brand_font = ImageFont.truetype(FONT_BOLD_PATH, 26)
        brand_text = f"// {app.username.upper()}"
        brand_y = card_y + 70
        draw.text((info_x, brand_y), brand_text, fill=(255, 255, 255, 130), font=brand_font)

        # 2. Headline Title (Dynamic, Huge & Premium text formatting)
        title_font = ImageFont.truetype(FONT_BOLD_PATH, 52)
        title_lines = wrap_text(draw, title, title_font, max_text_w)
        title_text = "\n".join(title_lines)
        title_y = brand_y + 50
        
        # Drop text shadow padding for clean legibility against any image color bleed
        draw.multiline_text((info_x + 2, title_y + 2), title_text, fill=(0, 0, 0, 190), font=title_font, spacing=8)
        draw.multiline_text((info_x, title_y), title_text, fill=(255, 255, 255, 255), font=title_font, spacing=8)

        # 3. Metadata Layout Arrays (Structured spacing down below)
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

        for idx, meta in enumerate(meta_items):
            y_pos = meta_y + (idx * 46)
            draw.text((info_x + 1, y_pos + 1), meta, fill=(0, 0, 0, 140), font=meta_font)
            draw.text((info_x, y_pos), meta, fill=(215, 220, 240, 225), font=meta_font)

        # Thin peripheral canvas frame line to bind the aesthetic details together
        canvas_frame = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        cf_draw = ImageDraw.Draw(canvas_frame)
        cf_draw.rectangle([0, 0, CANVAS_W, CANVAS_H], outline=(255, 255, 255, 8), width=3)
        canvas = Image.alpha_composite(canvas, canvas_frame)

        # --- STAGE 5: SAVE EXPORT BUFFER ---
        out = CACHE_DIR / f"{videoid}_final.png"
        canvas.save(out, quality=97, optimize=True)

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
