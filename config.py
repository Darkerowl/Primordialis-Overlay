# Config
import logging

# Paths (change if yours differ) ↓ EDIT (YOUR_USERNAME\) WITH YOUR PATHS TO THE FILES ↓
BOD_PATH = r"C:\Users\YOUR_USERNAME\AppData\Roaming\Primordialis\save\player.bod"  #←
OUTPUT_PNG = r"C:\Users\YOUR_USERNAME\AppData\Roaming\Primordialis\save\overlay.png" #←
TEMP_OUTPUT = OUTPUT_PNG + ".tmp"
ICONS_DIR = r"C:\Users\YOUR_USERNAME\Pictures\Twitch\Primordialis\cells" #←
MAPPING_JSON = r"C:\Users\YOUR_USERNAME\AppData\Roaming\Primordialis\save\cell_mapping.json" #←

# Visuals / Scale / Orientation
IMAGE_BG = (0, 0, 0, 0)  # RGBA
HEX_SIZE = 22            # hex radius in px (increase to zoom)
ICON_SCALE = 1.09        # icon fits within 2*radius*ICON_SCALE box
PADDING = 120            # border padding to avoid cropping
DEFAULT_COLOR = (160, 160, 160, 255)
HEX_GAP = 2.0            # pixels shaved off the hex radius (1–3 typical)
ICON_INSET = 2.0         # extra inset so icons don’t touch borders

SPACING_SCALE = 0.92     # how tightly hex centers are packed
SUPERSAMPLE = 2          # supersampling factor for smoother edges

# Alignment
USE_FLAT_TOP = False # False = pointy-topof the hexagons (Primordialis default) True= top of hex will be flat.
SWAP_QR = True # try True/False if grid is transposed
MIRROR_X = False # mirror horizontally
MIRROR_Y = False # mirror vertically
OFFSET_X = 0     # pixel nudge X
OFFSET_Y = 0     # pixel nudge Y
ROTATE_AROUND_GRID = True # pivot about grid bbox center
MANUAL_ROTATE_STEPS = 7 # 1=30°, 2=60°, 7=ingame style


# Debug
DEBUG_GRID = True
DEBUG_LABELS = False

# Bounds behavior in parser
ASSUME_BOUNDS_INCLUSIVE = False # spec says width = ux - lx

# Behavior/perf
DEBOUNCE_SECONDS = 0.3
READ_RETRY = 3
READ_RETRY_DELAY = 0.3 
RENDER_WIDTH = 0 # 0 = autosize; else force width and scale height
RENDER_HEIGHT = 0
LOG_LEVEL = logging.INFO


# Feature flags
ICONS_ENABLED = True # can be turned off via CLI

