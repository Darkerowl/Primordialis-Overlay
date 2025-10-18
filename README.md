`Click→` To NAV <img width="157" height="83" alt="image" src="https://github.com/user-attachments/assets/9ff77903-dd78-45d3-9fcb-2dcb7d40165a" /> **For dropdown to all sections**  `→↑`

# $\color{blue}{\text{Primordialis Overlay}}$
$\color{blue}{\text{Primordialis Overlay}}$
This project provides a live overlay renderer for **Primordialis**, reading the game’s `.bod` save file and producing an **overlay.png** that can be displayed in OBS or other streaming software. This version is considered **beta**: functionality works, but visuals and performance may improve in future updates.

#### Must have Python to use this mod 
**This is all coded in in [Python 3.13](https://www.python.org/downloads/release/python-3137/)** 
- Python `3.8` through `3.13x` will work with this mod.
---

## Project Structure
The repo includes:

- **Python files:**
  - [Config.py](config.py) – Your paths and tunable settings
  - [main.py](main.py) – CLI entrypoint (`--once`, `--watch`, `--bod`, `--out`, `--no-icons`)
  - [bod_parser.py](bod_parser.py) – Reads/decompresses/parses `.bod`
  - [render.py](render.py) – Hex math, colors, icons, combos, PNG writing
  - [watcher.py](watcher.py) – Watchdog + debounce + checksum
  - [required_downloads.py](required_downloads.py) - This is a `.py script` that will check that you have the right `Python` and `deps`.

   **Batch files (.bat):**
  - [run_once.bat](run_once.bat)
  - [run_once_no_icons.bat](run_once_no_icons.bat)
  - [run_watch.bat](run_watch.md)
  - [Install_requirments.bat](iInstall_requirments.bat) - Downloads the Deps for Python through `CMD`.
  - 
- **Folders:**
  - `__pycache__` – Python cache files || [pycache](__pycache__)
  - `cells` – Holds all cell PNGs used in rendering  || [cells](cells)

**Other files:**
  - [cell_mapping.json](cell_mapping.json) – Maps 4-letter cell codes (e.g., `HART`, `SPIK`, `SEEK`) to icon PNGs and `-optional colors-` **read bug section to see**
  -[overlay.png](overlay.png) – The rendered overlay that updates alongside your `.bod`
  - [README.md](README.md) – This document

---

---

## Setup Info
#### Treat run_watch.bat as a mini .exe
You can keep the files anywhere you like. Make backups if you plan to edit.
--
### ⚠️ Important: 
- Python `3.8-3.15`is required make sure you download `Python` so the mod will run correctly. *Python `2.0`-> `3.0-3.7` is not supported anymore or the used deps are not on those versions, use at own risk bellow `PY_3.8`.
- Next `main.py` does a check for Pyton 3.8-3.13 and the deps, having none of the deps or Python downloaded will trigger a warning↓. 
---
### ⚠️ **Must know**↓  
- If you`launch`-|-|->`run_watch.bat`-or->`run_once.bat`-or->`run_once_no_incons.bat`-|> any one of them first.| They all run [main.py](main.py)  with  [required_downloads.py](required_downloads.py) which has a set prompt and a `(y/n)` asking you to confirm. *I thought it would me a little innapropriate for me to download python deps onto your pc without permission, no matter how small and harmless they maybe*
- If `y` the downloads will start in a bash(`CMD`) window, if `n` you will get a message asking you to download the required files on your own. , [Install_requirments.bat](iInstall_requirments.bat) and instal "Python 3.13"
---

---
# Setup Instructions:
## Editing `config.py`
### ⚠️ **Important:** You must edit [Config.py](config.py) to match your system paths.
---
Replace `YOUR_USERNAME` with your Windows user folder name. 

Example:
### Example Config Paths
```
C:\Program Files\MyApplication\bin
C:\Users\YOUR_USERNAME\AppData\Roaming\Primordialis\save
C:\Users\YOUR_USERNAME\Documents\Primordialis Overlay Mod
```
Example:
```python
# Paths (change if yours differ)
BOD_PATH = r"C:\Users\YOUR_USERNAME\AppData\Roaming\Primordialis\save\player.bod"
OUTPUT_PNG = r"C:\Users\YOUR_USERNAME\AppData\Roaming\Primordialis\save\overlay.png"
TEMP_OUTPUT = OUTPUT_PNG + ".tmp"
ICONS_DIR = r"C:\Users\YOUR_USERNAME\Documents\Primordialis Overlay Mod\cells"
MAPPING_JSON = r"C:\Users\YOUR_USERNAME\AppData\Roaming\Primordialis\save\cell_mapping.json"
```

👉 Fast way to get to `%AppData%`: press **Win+R**, type `%AppData%/Primordialis/save`, and hit **Enter**.

`ICONS_DIR` should point to the [cells](cells) folder containing your PNGs.

---

## Running the Overlay

There are 3 modes:

- **run_Once:** renders `overlay.png` a single time and exits.
- **run_once_no_icons:** run once to update `overlay.png` a single time with icons of the cells `.png` and exits.
- **run_watch:** continuously watches the `.bod` file for changes and re-renders.
- 
`--no-icons` speeds up rendering by skipping PNG icons (color-only mode).

### Using Bat Files

Included `.bat` code blocks: this is already writen into the `bat` files included this is just exaples of the code used.

```bat
@echo off
REM === Run overlay in watch mode ===
python main.py --watch
pause
```

```bat
@echo off
REM === Run overlay once ===
python main.py --once
```

```bat
@echo off
REM === Run overlay once without icons ===
python main.py --once --no-icons
```

📌 Notes:
- Removing ***pause*** makes the script close after running once (useful for testing `config.py` edits).
- Keep the `.bat` names as provided; arguments rely on them.

### Running in PowerShell / CMD

```bash
python main.py --once
```

```bash
python main.py --watch
```

```bash
python main.py --once --no-icons
```

`--once --no-icons` speeds up rendering by skipping PNG icons (color-only mode).

---
#pip dep code `CMD` or `powershell`

*To download its very easy* 
***Copy and paste into powershell or comand prompt.***

```bash

pip install watchdog lz4 pillow numpy

pip install black pylint

```
---

## OBS Setup

OBS doesn’t support live-updating images directly. Workaround: use a **Slideshow** source.

1. Add a new *Slideshow* source into OBS.
2. Point it at your `overlay.png` in `%AppData%/Primordialis/save`. -> `win+r` type `%AppData%/Primordialis/save` into **run** and hit enter to go to file location fast.
3. Configure:
   - **Visibility Behavior:** Always play even when not visible
   - **Slide Mode:** Automatic
   - **Transition:** Fade (or your choice)
   - **Time Between Slides:** `50 ms`
   - **Transition Speed:** `50 ms`
   - **Playback Mode:** Loop
   - **Bounding Size/Aspect Ratio:** e.g. `800x800` (any size; image scales)
---
##✅ Final Checklist
 - ✅ overlay.png + cell_mapping.json in save dir
 - - ✅✅  Correct paths in config.py (username + icons dir)
 - ✅ Python 3.8 through 3.13x installed (1 version)
 - - ✅ ✅  Run run_watch.bat (or one of the other .bat) it will instal the - Deps(pip install watchdog lz4 pillow numpy) *or install them on your own.
 - ✅ OBS slideshow configured
 - ✅  Run run_watch.bat and enjoy!
---

## Notes

- **Config explained:** see `Primordialis config explained.md` for detailed breakdown of each setting.
- `.bod` parsing uses retries + debounce to avoid race conditions.
- The render system supports both color-only and icon-enhanced overlays.
- You can tweak visuals (hex size, spacing, rotation, etc.) directly in `config.py`.
- To explicitly color cells, add a `"color": "#RRGGBB"` in `cell_mapping.json` alongside the `"icon"` entry.

Future improvements may include:
- Faster OBS integration (Lua script instead of slideshow hack)
- More CLI overrides (`--hex-size`, `--rotate-steps`, etc.)
- Smarter caching for icons/colors
## Bugs
- <del>Missing .png for the cells inside Beta version of the game, | `Impact_cell` | `Ink_cell` | `Wandering_neuron` | `Electromagnetic_cell` |  These cells were not in the wiki which is were I got my photos for the cells from, I can make some .PNG real fast.</del> ****Fixed 9/29/25****
- There is a known issue with Combo cells right now, im working to fix this issue, I just need a photo of every combo cell type in `85x85` pixel res, this would allow me to put those photos into `cells` folder and write code for them into- `cell_mapping.json` this file is what tells my code through hex from `.bod`  to which `.png` to grab from `cells` folder.
- this is how I had my code setup for early testing way before I split the files and still had this code inside the `.py` files. I was thinking about doing more testing on this front since combo cells are a more uniqe form in game and truly could have unlimited possibilities, I was also thinking of just changing the script to know when a combo cell is being used and pull the icon from the `cells` folder and put them all into 1 hexagon, my worry with this is it may become to small and hard to see. 
```JSON
{
  "BODY": { "color": "#A0C8FF", "icon": "Cell_Basic.png" },
  "SPIK": { "color": "#ffffff",  "icon": "Cell_spike.png" },
 "LIGT": { "color": "#E9E7A1", "icon": "Cell_lightweight.png" },
 "BODY+SPIK": { "color": "#FFD888", "icon": "Cell_Combo.png" }
}  
```
### MOD↓ Example of bug
[![overlay.png](https://i.postimg.cc/kgpLL2bR/overlay.png)](https://postimg.cc/v45PVHXG)

### Ingame↓ Ref
<img width="1309" height="952" alt="image" src="https://github.com/user-attachments/assets/11f8fc9c-87b1-4807-89eb-045cde7cda90" />



---
- Another bug I have is the Icon are not quite as centered in the hexagons as I would like, the **icons** I used are from the Wiki page were I used a script to scrape the page and download them for me, I then removed the background from each image and saved them. But this creates a issue were each `.png` file is not `85x85` like I would want it to be, I can work to fix this also or if I can somehow find out were the dev keeps the images for the ingame icon files, I have zero idea were.
- the colors for behind the **icons** in the hexagons, well the colors are pretty much random and have zero bearing on each cell, this can be changed and each cell van have a specified color very easily. In `cell_mapping.json`  you can add:  Preferred JSON format (example):`"color": "#A0C8FF",` added to the `.json` file for each cell this will tell my code that this ***hexagon***  needs to be this color if X cell is in that location.

'''
- Hexgon spacing my not seem exactly perfect depending on what your screen size and look it, I did testing in other resolutions, but if they space between each hex is wrong or not looking right, go to `config.py` to fix and read `primordialis config explained.md` [primordialis config explained.md]("Primordialis Overlay Mod\primordialis config explained.md") to know what all settings do. these settings will allow for changed in this manor can be edited ` 1, 0.1, 0.01, 0.001` anything less will be to small to see, bigger is drastic changes, start small and move around `0.1` for each change to tune to your pref, 
```python
# Visuals / Scale / Orientation
HEX_GAP = 2.0
ICON_INSET = 2.0 
```
'''
- **_There maybe other bugs please report more found to my github and I will fix them as soon as I see the reports_**
---
**Part 2↓**
---
# Primordialis Overlay – `config.py`

This document explains every setting in **config.py** and how it affects rendering or behavior.

---

## Paths inside python script.
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
  Extra rotation applied in **30° steps** (each step = 30°). E.g., `7` → 210°. Combined with the save’s `half_hex_rotation`. `7` I found to be exactly ingame look in rotation in my testing.

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

# Batch file code:`.bat`

[run_watch](run_watch.md)
```
@echo off
python main.py --watch
pause
```

[run_once](run_once.bat)
```batch
@echo off
python main.py --once
```

[run_once_no_icons](run_once_no_icons.bat)
```batch
@echo off
python main.py --once --no-icons
```
Explained in [readme.md](readme.md)

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

Place icons in `ICONS_DIR`. Relative icon paths are resolved against [cell_mapping.json](cell_mapping.json) directory.
---
**end**
---
#Tip 
---
***Links*** *click images to go to them*

[![StreamElements tips](https://github.com/user-attachments/assets/d48d44a4-8b9d-400e-acc0-787cdd35aee5)](https://streamelements.com/darkerowls/tip)

 [<img width="100" height="100" alt="image" src="https://github.com/user-attachments/assets/00d3b098-1ca2-4507-9fc4-b272d2257cf5" />](https://www.twitch.tv/darkerowls)

 ---
 **Ony if if you think its worth it↓!**
`https://streamelements.com/darkerowls/tip`

**Or you can follow/sub to my** `twitch.tv/darkerowls`!
