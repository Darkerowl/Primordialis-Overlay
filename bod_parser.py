# bod_parser.py
import os
import struct
import lz4.block

from config import (
    ASSUME_BOUNDS_INCLUSIVE,
)

def linear_to_srgb(v: float) -> float:
    """Convert linear float (0..1) to sRGB float."""
    if v <= 0.0031308:
        return v * 12.92
    return 1.055 * (v ** (1.0 / 2.4)) - 0.055


def parse_bod_file(path: str) -> dict:
    if not os.path.isfile(path):
        raise FileNotFoundError(path)

    with open(path, "rb") as f:
        header = f.read(20)
        if len(header) < 20:
            raise ValueError("File too small for .bod header")

        version = struct.unpack_from("<I", header, 0)[0]
        compressed_size = struct.unpack_from("<Q", header, 4)[0]
        uncompressed_size = struct.unpack_from("<Q", header, 12)[0]

        blob = f.read(compressed_size)
        if len(blob) < compressed_size:
            # fallback: read the rest of file as the compressed blob
            f.seek(20)
            blob = f.read()

    try:
        data = lz4.block.decompress(blob, uncompressed_size=uncompressed_size)
    except Exception as e:
        raise RuntimeError(f"lz4.decompress failed: {e}")
    if len(data) != uncompressed_size:
        raise RuntimeError("decompressed size mismatch")

    offset = 0

    def read(fmt):
        nonlocal offset
        size = struct.calcsize(fmt)
        if offset + size > len(data):
            raise EOFError(f"Not enough bytes to read {fmt} at {offset}")
        v = struct.unpack_from(fmt, data, offset)
        offset += size
        return v if len(v) > 1 else v[0]

    half_hex_rotation = read("<I")
    n_normal = read("<I")
    n_combos = read("<I")
    n_colors = read("<I")
    lx = read("<i")
    ly = read("<i")
    ux = read("<i")
    uy = read("<i")

    if ASSUME_BOUNDS_INCLUSIVE:
        width  = ux - lx + 1
        height = uy - ly + 1
    else:
        width  = ux - lx
        height = uy - ly
        if width <= 0 or height <= 0:
            raise ValueError("Invalid bounds in .bod")

    normal_ids, normal_names = [], []
    for _ in range(n_normal):
        cid = read("<I")
        normal_ids.append(cid)
        try:
            ascii_name = cid.to_bytes(4, "little").decode("ascii", errors="replace")
        except Exception:
            ascii_name = str(cid)
        normal_names.append(ascii_name)

    combo_pairs = []
    for _ in range(n_combos):
        a = read("<I")
        b = read("<I")
        combo_pairs.append((a, b))

    color_list = []
    for _ in range(n_colors):
        r = read("<f")
        g = read("<f")
        b = read("<f")
        a = read("<f")
        sr = int(max(0, min(255, round(linear_to_srgb(r) * 255))))
        sg = int(max(0, min(255, round(linear_to_srgb(g) * 255))))
        sb = int(max(0, min(255, round(linear_to_srgb(b) * 255))))
        sa = int(max(0, min(255, round(a * 255))))
        color_list.append((sr, sg, sb, sa))

    expected = width * height
    cell_type_array = [read("<I") for _ in range(expected)]
    cell_color_array = [read("<I") for _ in range(expected)]

    return {
        "version": version,
        "half_hex_rotation": half_hex_rotation,
        "n_normal": n_normal,
        "n_combos": n_combos,
        "n_colors": n_colors,
        "lx": lx,
        "ly": ly,
        "ux": ux,
        "uy": uy,
        "width": width,
        "height": height,
        "normal_ids": normal_ids,
        "normal_names": normal_names,
        "combo_pairs": combo_pairs,
        "color_list": color_list,
        "cell_type_array": cell_type_array,
        "cell_color_array": cell_color_array,
    }
