# Primordialis Overlay – `config.py` reference

This document explains every setting in **config.py** and how it affects rendering or behavior. Use it as a README section for your GitHub repo.

---

## Paths
- **`BOD_PATH`** *(str)*  
  Full path to the game’s `player.bod` save file that the watcher reads.

- **`OUTPUT_PNG`** *(str)*  
  Where the final overlay image is written.

- **`TEMP_OUTPUT`** *(str)*  
  Temporary file used for atomic saves (write → rename). Keep in the same folder as `OUTPUT_PNG`.

- **`ICONS_DIR`** *(str)*  
  Folder containing the PNG icons for each cell.

- **`MAPPING_JSON`** *(str)*  
  JSON file mapping 4‑char cell codes (and combo keys) to icon filenames and/or colors.

> **Tip:** If you move files, you can also override these at runtime via CLI flags in `main.py`.

---

## Visuals / Scale / Orientation
- **`IMAGE_BG`** *(RGBA tuple)*  
  Background color of the generated PNG (default fully transparent).

- **`HEX_SIZE`** *(int)*  
  **Layout radius** of each hex in pixels. Bigger = larger grid. Affects spacing math and icon sizing indirectly.

- **`ICON_SCALE`** *(float)*  
  Scales icon relative to the hex’s diameter. Effective icon box = `2 * (hex_radius - ICON_INSET) * ICON_SCALE`.

- **`PADDING`** *(int)*  
  Border around the grid to prevent cropping. Increase if hexes touch image edges after rotation.

- **`DEFAULT_COLOR`** *(RGBA tuple)*  
  Fallback cell color when no color is provided by mapping, per‑cell color list, or sampled from icon.

- **`HEX_GAP`** *(float)*  
  Visually trims the drawn hex radius to avoid overlap.  
  Render radius ≈ `HEX_SIZE - HEX_GAP`. Typical values: **1–3**.

- **`ICON_INSET`** *(float)*  
  Extra inset to keep icons from touching hex borders.

- **`SPACING_SCALE`** *(float)*  
  Multiplier on center‑to‑center spacing. **1.00** = default; **< 1.0** packs hexes tighter to close visible gaps. Try **0.97 ~ 0.92**.

- **`SUPERSAMPLE`** *(int)*  
  Renders at `SUPERSAMPLE×` resolution, then downsamples for smoother edges. Use **2** for OBS‑friendly anti‑aliasing. **1** disables.

---

## Alignment
- **`USE_FLAT_TOP`** *(bool)*  
  `False` = pointy‑top (Primordialis default). `True` = flat‑top hex math.

- **`SWAP_QR`** *(bool)*  
  Swaps axial coordinates derived from the save’s row/col to match the game’s orientation.

- **`MIRROR_X` / `MIRROR_Y`** *(bool)*  
  Horizontal / vertical mirroring in index space to correct flipped layouts.

- **`OFFSET_X` / `OFFSET_Y`** *(int)*  
  Final pixel nudge after layout (useful for fine alignment in OBS).

- **`ROTATE_AROUND_GRID`** *(bool)*  
  If `True`, rotation pivots around the grid’s bounding box center instead of the image center.

- **`MANUAL_ROTATE_STEPS`** *(int)*  
  Extra rotation applied in **30° steps** (each step = 30°). E.g., `7` → 210°. Combined with the save’s `half_hex_rotation`.

---

## Debug
- **`DEBUG_GRID`** *(bool)*  
  Draws small dots at hex centers.

- **`DEBUG_LABELS`** *(bool)*  
  Writes axial coordinates `q,r` near each cell (low‑noise font). Useful for diagnosing mapping issues.

---

## Bounds behavior in parser
- **`ASSUME_BOUNDS_INCLUSIVE`** *(bool)*  
  Controls how `width`/`height` are computed from save bounds `(lx, ly) .. (ux, uy)`.
  - `False`: `width = ux - lx`, `height = uy - ly` (spec default).
  - `True`:  `width = ux - lx + 1`, `height = uy - ly + 1` (if your build uses inclusive upper bounds).
**not exactly the most needed info but I was thinknig this maybe not perfect might be a error here**

---

## Behavior / Performance
- **`DEBOUNCE_SECONDS`** *(float)*  
  How long the watcher waits for file changes to “settle” before re‑rendering.

- **`READ_RETRY` / `READ_RETRY_DELAY`** *(int / float)*  
  Number of parse retries and delay between retries when the save file is mid‑write.

- **`RENDER_WIDTH` / `RENDER_HEIGHT`** *(int)*  
  Optional **final** scaling after rendering. 0 means auto size.  
  If only one dimension is set, the other scales to preserve aspect ratio.

- **`LOG_LEVEL`**  
  Python logging level (e.g., `logging.INFO`, `logging.DEBUG`).

---

## Feature flags
- **`ICONS_ENABLED`** *(bool)*  
  Master toggle for drawing icons. Can be overridden at runtime with `--no-icons` CLI flag.

---

## Color & Icon resolution order
For each cell:
1. **Mapping JSON** color (if set)
2. **Per‑cell color** from the save’s `color_list`
3. **Sampled color from icon** (average of visible pixels)
4. **`DEFAULT_COLOR`** fallback

## Combo cells:
- Mapping color/icon for key: `"LEFT+RIGHT"` (e.g., `"BODY+SPIK"`)
- Otherwise blend component colors and draw component icons side‑by‑side
  ***this is one way that I have thought of doing the code to be used with combo cells, this will put the 2 icons for `cells .png` in `cells` folder side by side in a mini format***
   I was having issues getting my code to read the hex created by combo cells. The dev does explain how he put in and does combo cells in 
   `C:\Program Files (x86)\Steam\steamapps\common\Primordialis\data\documentation` `bod_file_format` but its much different to how normals cells are read out in `hex`.
   *for example:hex*

   ```hex
   4C 49 47 54 42 4F 44  59 53 45 45 4B 48 41 52 44 LIGTBODYSEEKHARD
   53 45 45 4B 53 57 49 4D 4A 45 54 54 41 43 49 44 4C 49 47 54 SEEKSWIMJETTACIDLIGT
   ```
**this is hex ↑ for those cells**

---

## CLI overrides (from `main.py`)
- `--once` or `--watch` (mutually exclusive)
- `--bod <path>` overrides `BOD_PATH`
- `--out <path>` overrides `OUTPUT_PNG`
- `--temp <path>` overrides `TEMP_OUTPUT`
- `--no-icons` sets `ICONS_ENABLED = False`

**Example:**
```
python main.py --watch --bod "C:\Users\YOUR_USERNAME\AppData\Roaming\Primordialis\save\player.bod" --out overlay.png
```

# Batch file code:

**run_watch.bat**
```
@echo off
python main.py --watch
pause
```

**run_once.bat**
```batch
@echo off
python main.py --once
```

**run_once_no_icons.bat**
```batch
@echo off
python main.py --once --no-icons
```
Explained in [readme.md](main/readme.md)

---

## Quick tuning guide
- Whole `png` cut off at top/bottom `→` increase **PADDING**.
- Hex gaps feel too large `→` lower **SPACING_SCALE** slightly `(e.g., 0.95)`.
- Hex overlaps/too tight `→` raise **HEX_GAP** `or` **SPACING_SCALE**.
- Jaggy edges in `OBS` `→` set **SUPERSAMPLE = 2**.
- Rotation off by `30°` increments `→` adjust **MANUAL_ROTATE_STEPS**.
- Wrong orientation ***try↑*** before `→→` toggle **SWAP_QR**, **MIRROR_X**, **MIRROR_Y**, or **USE_FLAT_TOP**.

---

## Mapping JSON format (snippet)
```JSON
{
  "BODY": { "color": "#A0C8FF", "icon": "Cell_Basic.png" },
  "SPIK": { "color": "#ffffff",  "icon": "Cell_spike.png" },
 "LIGT": { "color": "#E9E7A1", "icon": "Cell_lightweight.png" },
 "BODY+SPIK": { "color": "#FFD888", "icon": "Cell_Combo.png" }
}  
```

Place icons in `ICONS_DIR`. Relative icon paths are resolved against `cell_mapping.json` directory.
[cell_mapping.json](main\cell_mapping.json)
