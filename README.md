# Primordialis Overlay

This project provides a live overlay renderer for **Primordialis**, reading the game’s `.bod` save file and producing an **overlay.png** that can be displayed in OBS or other streaming software. This version is considered **beta**: functionality works, but visuals and performance may improve in future updates.

---

## Project Structure

The repo includes:

- **Python files:**
  - `config.py` – Your paths and tunable settings
  - `main.py` – CLI entrypoint (`--once`, `--watch`, `--bod`, `--out`, `--no-icons`)
  - `bod_parser.py` – Reads/decompresses/parses `.bod`
  - `render.py` – Hex math, colors, icons, combos, PNG writing
  - `watcher.py` – Watchdog + debounce + checksum

- **Batch files (.bat):**
  - `run_once.bat`
  - `run_once_no_icons.bat`
  - `run_watch.bat`

- **Folders:**
  - `__pycache__` – Python cache files
  - `cells/` – Holds all cell PNGs used in rendering

- **Other files:**
  - `cell_mapping.json` – Maps 4-letter cell codes (e.g., `HART`, `SPIK`, `SEEK`) to icon PNGs and `-optional colors-` **read bug section to see**
  - `overlay.png` – The rendered overlay that updates alongside your `.bod`
  - `README.md` – This document

---

## Setup Instructions

You can keep the files anywhere you like. Make backups if you plan to edit.

⚠️ **Important:** You must edit `config.py` to match your system paths.

### Editing `config.py`

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




`ICONS_DIR` should point to the `cells/` folder containing your PNGs.

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
- There is a known issue with Combo cells right now, im working to fix this issue, I just need a photo of every combo cell type in `85x85` pixel res, this would allow me to put those photos into `cells` folder and write code for them into `cell_mapping.json` this file is what tells my code through hex from `.bod`  to which `.png` to grab from `cells` folder.
- Another bug I have is the Icon are not quite as centered in the hexagons as I would like, the **icons** I used are from the Wiki page were I used a script to scrape the page and download them for me, I then removed the background from each image and saved them. But this creates a issue were each `.png` file is not `85x85` like I would want it to be, I can work to fix this also or if I can somehow find out were the dev keeps the images for the ingame icon files, I have zero idea were.
- the colors for behind the **icons** in the hexagons, well the colors are pretty much random and have zero bearing on each cell, this can be changed and each cell van have a specified color very easily. In `cell_mapping.json`  you can add:  Preferred JSON format (example):`"color": "#A0C8FF",` added to the `.json` file for each cell this will tell my code that this ***hexagon***  needs to be this color if X cell is in that location.
```JSON
{
  "BODY": { "color": "#A0C8FF", "icon": "Cell_Basic.png" },
  "SPIK": { "color": "#ffffff",  "icon": "Cell_spike.png" },
 "LIGT": { "color": "#E9E7A1", "icon": "Cell_lightweight.png" },
 "BODY+SPIK": { "color": "#FFD888", "icon": "Cell_Combo.png" }
}  
```
this is how I had my code setup for early testing way before I split the files and still had this code inside the `.py` files. I was thinking about doing more testing on this front since combo cells are a more uniqe form in game and truly could have unlimited possibilities, I was also thinking of just changing the script to know when a combo cell is being used and pull the icon from the `cells` folder and put them all into 1 hexagon, my worry with this is it may become to small and hard to see. 
'''
- Hexgon spacing my not seem exactly perfect depending on what your screen size and look it, I did testing in other resolutions, but if they space between each hex is wrong or not looking right, go to `config.py` to fix and read `primordialis config explained.md` [primordialis config explained.md]("Primordialis Overlay Mod\primordialis config explained.md") to know what all settings do. these settings will allow for changed in this manor can be edited ` 1, 0.1, 0.01, 0.001` anything less will be to small to see, bigger is drastic changes, start small and move around `0.1` for each change to tune to your pref, 
```python
# Visuals / Scale / Orientation
HEX_GAP = 2.0
ICON_INSET = 2.0 
```
'''
- **_There maybe other bugs please report more found to my github and I will fix them as soon as I see the reports_**
