# main.py
import argparse
import logging
import config as CFG  # import the module so we can override values

from config import (
    LOG_LEVEL,
    BOD_PATH as _BOD_PATH,
    OUTPUT_PNG as _OUTPUT_PNG,
    TEMP_OUTPUT as _TEMP_OUTPUT,
)

logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s %(levelname)s: %(message)s")

def main():
    parser = argparse.ArgumentParser(description="Primordialis overlay renderer")

    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--once",  action="store_true", help="Render once and exit")
    mode.add_argument("--watch", action="store_true", help="Watch the .bod file and update overlay")

    parser.add_argument("--bod",   default=_BOD_PATH,    help="Path to player.bod")
    parser.add_argument("--out",   default=_OUTPUT_PNG,  help="Path to output overlay.png")
    parser.add_argument("--temp",  default=_TEMP_OUTPUT, help="Path to temp output (for atomic replace)")
    parser.add_argument("--no-icons", action="store_true", help="Disable icon drawing (faster)")

    args = parser.parse_args()

    # Apply CLI overrides to the shared config
    CFG.BOD_PATH      = args.bod
    CFG.OUTPUT_PNG    = args.out
    CFG.TEMP_OUTPUT   = args.temp
    CFG.ICONS_ENABLED = (not args.no_icons)

    # Import AFTER overrides so modules pick up the final values
    from bod_parser import parse_bod_file
    from render import render_overlay
    from watcher import watch_loop

    if args.once:
        parsed = parse_bod_file(CFG.BOD_PATH)
        render_overlay(parsed, CFG.OUTPUT_PNG, CFG.TEMP_OUTPUT)
        print(f"Wrote {CFG.OUTPUT_PNG}")
    else:
        watch_loop()

if __name__ == "__main__":
    main()
