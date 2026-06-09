# Copyright (c) 2025 Nand Yaduwanshi <NoxxOP>
# Location: Supaul, Bihar
# All rights reserved.
# Ultimate Merged Glassmorphic & Cinematic Hybrid Thumbnail Engine.

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


def create_vignette_leather(size, intensity=160):
    """Generates an elite radial vignette gradient mask for high-end shadows"""
    w, h = size
    vignette = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    v_draw = ImageDraw.Draw(vignette)
    
    max_radius = math.sqrt((w/2)**2 + (h/2)**2)
    cx, cy = w // 2, h // 2
    
    # 4-layer dynamic interpolation for a real graphic-tool shadow feel
    for y in range(0, h, 2):
        for x in range(0, w, 4):
            distance = math.sqrt((x - cx)**2 + (y - cy)**2)
            ratio = distance / max_radius
            if ratio > 0.3:
                alpha = int(intensity * ((ratio - 0.3) / 0.7) ** 1.8)
                alpha = min(235, max(0, alpha))
                v_draw.rectangle([x, y, x+4, y+2], fill=(10, 10, 15, alpha))
                
    return vignette.filter(ImageFilter.GaussianBlur(25))


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
        # --- STAGE 1: DYNAMIC CINEMATIC BACKGROUND BLUR ---
        # Resize artwork to full canvas size & pump up contrast for dynamic color bleed
        bg_blur = base_img.resize((CANVAS_W, CANVAS_H), Image.LANCZOS)
        bg_contrast = ImageEnhance.Contrast(bg_blur).enhance(1.4)
        bg_final = bg_contrast.filter(ImageFilter.GaussianBlur(55))
        
        # Apply dark tint mask to merge the colors cleanly
        dark_tint = Image.new("RGBA", (CANVAS_W, CANVAS_H), (12, 12, 18, 110))
        canvas = Image.alpha_composite(bg_final, dark_tint)
        
        # Apply the mathematical Vignette Shadow across all 4 main edges
        vignette_layer = create_vignette_leather((CANVAS_W, CANVAS_H), intensity=190)
        canvas = Image.alpha_composite(canvas, vignette_layer)

        # --- STAGE 2: MATHEMATICAL HYPER-GLASSMORPHIC PLAYER CARD ---
        card_w, card_h = 1140, 520
        card_x = (CANVAS_W - card_w) // 2
        card_y = (CANVAS_H - card_h) // 2
        card_radius = 45

        # Create precise Glass Overlay with rich inner light ambient shadow
        glass_mask = Image.new("L", (card_w, card_h), 0)
        g_draw = ImageDraw.Draw(glass_mask)
        g_draw.rounded_rectangle([0, 0, card_w, card_h], radius=card_radius, fill=255)

        glass_card = Image.new("RGBA", (card_w, card_h), (255, 255, 255, 12)) 
        
        # Soft Outer Shadow for the glass card structure itself
        card_shadow = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        cs_draw = ImageDraw.Draw(card_shadow)
        cs_draw.rounded_rectangle([card_x-4, card_y-4, card_x+card_w+4, card_y+card_h+4], radius=card_radius+2, fill=(0, 0, 0, 180))
        card_shadow = card_shadow.filter(ImageFilter.GaussianBlur(35))
        canvas.paste(card_shadow, (0, 0), card_shadow)

        # Paste the real glass base layer inside the mask boundaries
        canvas.paste(glass_card, (card_x, card_y), glass_mask)

        # --- STAGE 3: THE HIGH-DENSITY ALBUM ARTWORK ---
        art_size = 380
        art_x = card_x + 50
        art_y = card_y + (card_h - art_size) // 2

        art_mask = Image.new("L", (art_size, art_size), 0)
        am_draw = ImageDraw.Draw(art_mask)
        am_draw.rounded_rectangle([0, 0, art_size, art_size], radius=30, fill=255)

        # Master Grade detailing adjustments for the internal card artwork
        graded_art = ImageEnhance.Contrast(base_img).enhance(1.25)
        graded_art = ImageEnhance.Sharpness(graded_art).enhance(1.30)
        art_resized = graded_art.resize((art_size, art_size), Image.LANCZOS)
        art_resized.putalpha(art_mask)

        # Drop shadow underneath album cover
        art_shadow = Image.new("RGBA", (art_size+60, art_size+60), (0, 0, 0, 0))
        as_draw = ImageDraw.Draw(art_shadow)
        as_draw.rounded_rectangle([30, 30, art_size+30, art_size+30], radius=30, fill=(0, 0, 0, 225))
        art_shadow = art_shadow.filter(ImageFilter.GaussianBlur(25))
        canvas.paste(art_shadow, (art_x-30, art_y-30), art_shadow)
        
        canvas.paste(art_resized, (art_x, art_y), art_resized)

        # --- STAGE 4: ULTRA LUXURY ACCENT & EDGE LIGHT SHADOWS (INSIDE CARD) ---
        card_overlay = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
        co_draw = ImageDraw.Draw(card_overlay)
        # Soft white premium rim-light reflection border lines
        co_draw.rounded_rectangle([0, 0, card_w, card_h], radius=card_radius, outline=(255, 255, 255, 30), width=2)
        canvas.paste(card_overlay, (card_x, card_y), glass_mask)

        # --- STAGE 5: PREMIUM CLEAN TYPOGRAPHY SYSTEM ---
        draw = ImageDraw.Draw(canvas)
        
        info_x = art_x + art_size + 60
        max_text_w = (card_x + card_w) - info_x - 50

        # Sub-header: App Username / Branding Header
        brand_font = ImageFont.truetype(FONT_BOLD_PATH, 30)
        brand_text = f"// {app.username.upper()}"
        brand_y = card_y + 65
        draw.text((info_x + 1, brand_y + 1), brand_text, fill=(0, 0, 0, 100), font=brand_font)
        draw.text((info_x, brand_y), brand_text, fill=(255, 255, 255, 140), font=brand_font)

        # Main Header: Track Title Display
        title_font = ImageFont.truetype(FONT_BOLD_PATH, 48)
        title_lines = wrap_text(draw, title, title_font, max_text_w)
        title_text = "\n".join(title_lines)
        title_y = brand_y + 55
        
        draw.multiline_text((info_x + 2, title_y + 2), title_text, fill=(0, 0, 0, 200), font=title_font, spacing=8)
        draw.multiline_text((info_x, title_y), title_text, fill=(255, 255, 255, 255), font=title_font, spacing=8)

        # Metadata Layout Configuration
        meta_font = ImageFont.truetype(FONT_REGULAR_PATH, 28)
        meta_y = title_y + 135
        
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
            y_pos = meta_y + (idx * 48)
            draw.text((info_x + 2, y_pos + 1), meta, fill=(0, 0, 0, 140), font=meta_font)
            draw.text((info_x, y_pos), meta, fill=(215, 220, 235, 235), font=meta_font)

        # Pure Professionalism Aspect Ratio Border Frame (Fine detailing touch)
        edge_detail = Image.new("RGBA", (CANVAS_W, CANVAS_H), (0, 0, 0, 0))
        ed_draw = ImageDraw.Draw(edge_detail)
        ed_draw.rectangle([0, 0, CANVAS_W, CANVAS_H], outline=(255, 255, 255, 10), width=4)
        canvas = Image.alpha_composite(canvas, edge_detail)

        # --- STAGE 6: FINALIZE AND EXPORT ---
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
