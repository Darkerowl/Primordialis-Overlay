# required_downloads.py
import sys
import subprocess

# List of required dependencies
REQUIRED_PACKAGES = [
    ("watchdog", "watchdog (for filesystem watching)"),
    ("lz4", "lz4 (for .bod decompression)"),
    ("pillow", "Pillow (for image rendering)"),
    ("numpy", "NumPy (for math + arrays)"),
]

def check_and_install():
    print("The following dependencies are required:")
    for pkg, desc in REQUIRED_PACKAGES:
        print(f"  - {pkg}: {desc}")

    choice = input("\nDo you want to install these now? [y/n]: ").strip().lower()
    if choice != "y":
        print("Aborted. Please install the dependencies manually with pip.")
        sys.exit(1)

    for pkg, _ in REQUIRED_PACKAGES:
        try:
            __import__(pkg if pkg != "pillow" else "PIL")
            print(f"✔ {pkg} already installed")
        except ImportError:
            print(f"Installing {pkg}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

    print("\nAll dependencies are installed and ready.")

if __name__ == "__main__":
    # Python version check (3.8–3.13 required)
    if not ((3, 8) <= sys.version_info[:2] <= (3, 13)):
        print(
            f"Error: Python 3.8 through 3.13 is required. "
            f"You are running {sys.version_info.major}.{sys.version_info.minor}."
        )
        sys.exit(1)

    check_and_install()
