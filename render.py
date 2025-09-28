# render.py
import os
import hashlib
import logging
import numpy as np
from PIL import Image, ImageDraw, ImageOps, ImageFont

# Pull only constants that are actually used in this module by name.
from config import (
    IMAGE_BG,
    HEX_SIZE,
    ICON_SCALE,
    PADDING,
    DEFAULT_COLOR,
    HEX_GAP,
    ICON_INSET,
    SUPERSAMPLE,
    SPACING_SCALE,
    USE_FLAT_TOP,
    SWAP_QR,
    MIRROR_X,
    MIRROR_Y,
    OFFSET_X,
    OFFSET_Y,
    ROTATE_AROUND_GRID,
    MANUAL_ROTATE_STEPS,
    DEBUG_GRID,
    DEBUG_LABELS,
    RENDER_WIDTH,
    RENDER_HEIGHT,
    ICONS_DIR,
    MAPPING_JSON,
)

# Also import the module so run-time overrides (e.g., --no-icons) are visible here.
import config as CFG

log = logging.getLogger(__name__)

# ---------- mapping + icon/color helpers ----------

def hex_to_rgba(hexstr: str, alpha: int = 255):
    if not hexstr:
        return None
    s = hexstr.strip()
    if s.startswith("#"):
        s = s[1:]
    if len(s) == 3:
        s = ''.join([c * 2 for c in s])
    if len(s) != 6:
        return None
    r = int(s[0:2], 16)
    g = int(s[2:4], 16)
    b = int(s[4:6], 16)
    return (r, g, b, alpha)


def stable_color_from_name(name: str):
    h = hashlib.md5(name.encode("utf-8")).digest()
    return (h[0], h[1], h[2], 255)


def load_mapping(mapping_json_path: str, icons_dir: str):
    mapping = {}
    try:
        if os.path.isfile(mapping_json_path):
            import json
            with open(mapping_json_path, "r", encoding="utf-8") as fh:
                j = json.load(fh)
            for k, v in j.items():
                color = v.get("color")
                icon = v.get("icon")
                if isinstance(color, str) and color:
                    color = hex_to_rgba(color)
                if icon and not os.path.isabs(icon):
                    icon = os.path.join(icons_dir, icon)
                mapping[k] = {"color": color, "icon": icon}
    except Exception as e:
        log.warning("Failed to load mapping JSON '%s': %s", mapping_json_path, e)
    return mapping


_ICON_CACHE = {}
_COLOR_CACHE = {}

def get_icon_image(path: str, target_box: tuple):
    if not path or not os.path.isfile(path):
        return None
    key = (path, target_box)
    if key in _ICON_CACHE:
        return _ICON_CACHE[key]
    try:
        im = Image.open(path).convert("RGBA")
        im = ImageOps.contain(im, target_box)
        _ICON_CACHE[key] = im
        return im
    except Exception as e:
        log.warning("Failed to load icon '%s': %s", path, e)
        return None


def color_from_icon(path: str):
    if not path or not os.path.isfile(path):
        return None
    key = ("color", path)
    if key in _COLOR_CACHE:
        return _COLOR_CACHE[key]
    try:
        im = Image.open(path).convert("RGBA")
        arr = np.array(im)
        alpha = arr[:, :, 3]
        mask = alpha > 10
        if not mask.any():
            return None
        rgb = arr[:, :, :3][mask]
        mean = rgb.mean(axis=0)
        color = (int(mean[0]), int(mean[1]), int(mean[2]), 255)
        _COLOR_CACHE[key] = color
        return color
    except Exception as e:
        log.warning("Failed to sample color from icon '%s': %s", path, e)
        return None


def _name_or_hex(x):
    if isinstance(x, str):
        return x
    try:
        return f"0x{x:08X}"
    except Exception:
        return str(x)


def combo_key_from_info(combo_info):
    left_key = _name_or_hex(combo_info["left"])
    right_key = _name_or_hex(combo_info["right"])
    return f"{left_key}+{right_key}"


def first_not_none(*vals):
    for v in vals:
        if v is not None:
            return v
    return None


def color_for_normal_name(name4, mapping, default_color_by_name):
    m = mapping.get(name4) if name4 else None
    from_icon = color_from_icon(m.get("icon")) if (m and m.get("icon")) else None
    return first_not_none(
        (m.get("color") if m else None),
        from_icon,
        default_color_by_name.get(name4),
        DEFAULT_COLOR,
    )


def icon_for_normal_name(name4, mapping):
    m = mapping.get(name4) if name4 else None
    return (m.get("icon") if m else None) or None


# ---------- combo resolvers (need parsed dict) ----------

def _int_to_normal_name(cid, normal_ids, normal_names):
    try:
        idx = normal_ids.index(cid)
        return normal_names[idx]
    except ValueError:
        return None


def resolve_combo_cell_index(combo_index, combo_pairs, normal_ids, normal_names, visited=None):
    if visited is None:
        visited = set()
    if combo_index < 0 or combo_index >= len(combo_pairs):
        raise IndexError("combo_index out of range")
    if combo_index in visited:
        raise RuntimeError("Recursive combo detected")
    visited.add(combo_index)
    a, b = combo_pairs[combo_index]

    def resolve_component(val):
        if val & 0x80000000:
            child_idx = val & 0x7FFFFFFF
            return resolve_combo_cell_index(child_idx, combo_pairs, normal_ids, normal_names, visited)
        nm = _int_to_normal_name(val, normal_ids, normal_names)
        return nm if nm is not None else val

    left = resolve_component(a)
    right = resolve_component(b)
    visited.remove(combo_index)
    return {"type": "combo", "index": combo_index, "left": left, "right": right}


def resolve_cell_value(code: int, parsed: dict):
    if code == 0:
        return {"kind": "empty"}
    n_normal = parsed["n_normal"]
    if code <= n_normal:
        idx = code - 1
        return {
            "kind": "normal",
            "index": idx,
            "id_int": parsed["normal_ids"][idx],
            "name": parsed["normal_names"][idx],
        }
    combo_index = code - n_normal - 1
    return {
        "kind": "combo",
        "index": combo_index,
        "combo": resolve_combo_cell_index(
            combo_index, parsed["combo_pairs"], parsed["normal_ids"], parsed["normal_names"]
        ),
    }


# ---------- hex math ----------

SQRT3 = np.sqrt(3.0)

def hex_to_pixel_pointy(q, r, size):
    x = size * SQRT3 * (q + r / 2.0)
    y = size * 1.5 * r
    return x, y


def hex_to_pixel_flat(q, r, size):
    x = size * 1.5 * q
    y = size * SQRT3 * (r + q / 2.0)
    return x, y


def hex_to_pixel(q, r, size):
    return hex_to_pixel_flat(q, r, size) if USE_FLAT_TOP else hex_to_pixel_pointy(q, r, size)


def polygon_corners(cx, cy, size):
    pts = []
    base = 0 if USE_FLAT_TOP else 30
    for k in range(6):
        angle = np.deg2rad(base + 60 * k)
        pts.append((cx + size * np.cos(angle), cy + size * np.sin(angle)))
    return pts


def rotate_point(px, py, cx, cy, angle_rad):
    s = np.sin(angle_rad)
    c = np.cos(angle_rad)
    dx = px - cx
    dy = py - cy
    rx = dx * c - dy * s
    ry = dx * s + dy * c  # FIX: correct rotation formula
    return (cx + rx, cy + ry)


# ---------- main render ----------

def render_overlay(parsed: dict, out_path: str, temp_path: str | None = None):
    mapping = load_mapping(MAPPING_JSON, ICONS_DIR)

    width = parsed["width"]
    height = parsed["height"]
    lx = parsed["lx"]
    ly = parsed["ly"]
    cells = parsed["cell_type_array"]
    colors_idx = parsed["cell_color_array"]
    normal_names = parsed["normal_names"]
    custom_colors = parsed["color_list"]
    n_normal = parsed["n_normal"]

    half_hex_rotation = (parsed.get("half_hex_rotation", 0) + MANUAL_ROTATE_STEPS) % 12
    angle_rad = (half_hex_rotation * 2.0 * np.pi) / 12.0

    SS = max(1, int(SUPERSAMPLE))
    SP = float(SPACING_SCALE)

    # Layout spacing vs. visual radius (both in base pixels; SS applied later)
    layout_size = HEX_SIZE * SP
    radius = max(1, HEX_SIZE - HEX_GAP)

    default_color_by_name = {nm: stable_color_from_name(nm) for nm in normal_names}
    default_color_map = {i + 1: default_color_by_name[nm] for i, nm in enumerate(normal_names)}

    # Compute centers (not supersampled yet)
    centers = []
    for row in range(height):
        for col in range(width):
            if SWAP_QR:
                q = row + lx
                r = col + ly
            else:
                q = col + lx
                r = row + ly

            cc = col if not MIRROR_X else (width - 1 - col)
            rr = row if not MIRROR_Y else (height - 1 - row)
            if SWAP_QR:
                q = rr + lx
                r = cc + ly
            else:
                q = cc + lx
                r = rr + ly

            px, py = hex_to_pixel(q, r, layout_size)
            centers.append((px, py))

    xs = [c[0] for c in centers]
    ys = [c[1] for c in centers]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)

    pad = int(PADDING)
    img_w = int((maxx - minx) + radius * 2 + pad * 2)
    img_h = int((maxy - miny) + radius * 2 + pad * 2)

    # Supersampled canvas
    ss_w = max(1, img_w * SS)
    ss_h = max(1, img_h * SS)

    img = Image.new("RGBA", (ss_w, ss_h), IMAGE_BG)
    draw = ImageDraw.Draw(img, "RGBA")

    # Rotation pivot (in supersampled px)
    if ROTATE_AROUND_GRID:
        pivot_x = ((minx + maxx) / 2.0 - minx + pad + radius) * SS
        pivot_y = ((miny + maxy) / 2.0 - miny + pad + radius) * SS
    else:
        pivot_x = ss_w / 2.0
        pivot_y = ss_h / 2.0

    # Icon target size (supersampled)
    icon_box = max(1, int(2 * (radius - ICON_INSET) * ICON_SCALE * SS))
    icon_target = (icon_box, icon_box)

    idx = 0
    for row in range(height):
        for col in range(width):
            code = cells[idx]
            color_idx = colors_idx[idx]
            idx += 1

            chosen_color = None
            single_icon_path = None
            left_icon_path = None
            right_icon_path = None

            if code != 0 and code <= n_normal:
                # normal
                name4 = normal_names[code - 1]
                mapped = mapping.get(name4)

                if mapped and mapped.get("color"):
                    chosen_color = mapped["color"]
                elif color_idx and 1 <= color_idx <= len(custom_colors):
                    chosen_color = custom_colors[color_idx - 1]
                else:
                    chosen_color = default_color_by_name.get(name4, default_color_map.get(code, DEFAULT_COLOR))

                single_icon_path = (mapped.get("icon") if mapped else None)

            elif code > n_normal:
                # combo
                combo_info = resolve_cell_value(code, parsed)["combo"]
                combo_key = combo_key_from_info(combo_info)
                mapped_combo = mapping.get(combo_key)

                left_name = combo_info["left"] if isinstance(combo_info["left"], str) else None
                right_name = combo_info["right"] if isinstance(combo_info["right"], str) else None

                c_left = color_for_normal_name(left_name, mapping, default_color_by_name)
                c_right = color_for_normal_name(right_name, mapping, default_color_by_name)

                if mapped_combo and mapped_combo.get("color"):
                    chosen_color = mapped_combo["color"]
                else:
                    c1 = c_left or DEFAULT_COLOR
                    c2 = c_right or DEFAULT_COLOR
                    chosen_color = (
                        (c1[0] + c2[0]) // 2,
                        (c1[1] + c2[1]) // 2,
                        (c1[2] + c2[2]) // 2,
                        (c1[3] + c2[3]) // 2,
                    )

                if mapped_combo and mapped_combo.get("icon"):
                    single_icon_path = mapped_combo["icon"]
                else:
                    left_icon_path = icon_for_normal_name(left_name, mapping) if left_name else None
                    right_icon_path = icon_for_normal_name(right_name, mapping) if right_name else None
            else:
                # empty
                continue

            # axial -> pixel (layout) then into image coords (supersampled), with offsets
            if SWAP_QR:
                q = row + lx
                r = col + ly
            else:
                q = col + lx
                r = row + ly

            if MIRROR_X or MIRROR_Y:
                cc = col if not MIRROR_X else (width - 1 - col)
                rr = row if not MIRROR_Y else (height - 1 - row)
                if SWAP_QR:
                    q = rr + lx
                    r = cc + ly
                else:
                    q = cc + lx
                    r = rr + ly

            cx, cy = hex_to_pixel(q, r, layout_size)
            cx = (cx - minx + pad + radius + OFFSET_X) * SS
            cy = (cy - miny + pad + radius + OFFSET_Y) * SS

            if half_hex_rotation:
                cx, cy = rotate_point(cx, cy, pivot_x, pivot_y, angle_rad)

            # hex
            pts = polygon_corners(cx, cy, max(1, int(radius * SS)))
            draw.polygon(pts, fill=chosen_color, outline=(0, 0, 0, 100))

            # debug
            if DEBUG_GRID:
                draw.ellipse((cx - 1, cy - 1, cx + 1, cy + 1), fill=(0, 0, 0, 160))
                draw.ellipse((cx - 3, cy - 3, cx + 3, cy + 3), outline=(255, 255, 255, 90))
            if DEBUG_LABELS:
                try:
                    fnt = ImageFont.load_default()
                    draw.text((cx + 6, cy - 6), f"{q},{r}", fill=(255, 255, 255, 180), font=fnt)
                except Exception:
                    pass

            # icons (guarded by runtime flag)
            if CFG.ICONS_ENABLED:
                if left_icon_path or right_icon_path:
                    small_box = max(1, int(icon_box * 0.72))
                    if left_icon_path:
                        li = get_icon_image(left_icon_path, (small_box, small_box))
                        if li:
                            w, h = li.size
                            img.paste(li, (int(cx - w - 2), int(cy - h / 2)), li)
                    if right_icon_path:
                        ri = get_icon_image(right_icon_path, (small_box, small_box))
                        if ri:
                            w, h = ri.size
                            img.paste(ri, (int(cx + 2), int(cy - h / 2)), ri)
                elif single_icon_path:
                    icon_im = get_icon_image(single_icon_path, icon_target)
                    if icon_im:
                        w, h = icon_im.size
                        img.paste(icon_im, (int(cx - w / 2), int(cy - h / 2)), icon_im)

    # Downsample once at the end if supersampling is on
    if SS > 1:
        img = img.resize((max(1, ss_w // SS), max(1, ss_h // SS)), Image.LANCZOS)

    # Optional final scaling to a target size
    target_w = int(RENDER_WIDTH) if RENDER_WIDTH else 0
    target_h = int(RENDER_HEIGHT) if RENDER_HEIGHT else 0
    if target_w and target_h:
        img = img.resize((target_w, target_h), Image.LANCZOS)
    elif target_w and not target_h:
        scale = target_w / float(img.width)
        img = img.resize((target_w, max(1, int(img.height * scale))), Image.LANCZOS)
    elif target_h and not target_w:
        scale = target_h / float(img.height)
        img = img.resize((max(1, int(img.width * scale)), target_h), Image.LANCZOS)

    # Save atomically if temp_path supplied
    if temp_path:
        img.save(temp_path, "PNG")
        os.replace(temp_path, out_path)
    else:
        img.save(out_path, "PNG")
