from pathlib import Path

ASSETS_DIR = Path(__file__).parent / "assets" / "cards"
CARD_IMAGES = sorted(ASSETS_DIR.glob("*.png"))

MAX_POINTS = 100
POINTS_PER_SUCCESS = 15

FONT_FAMILY = "Glacial Indifference"
COLOR_PRIMARY = "#0F1516"
COLOR_ACCENT = "#76B6F0"
COLOR_MUTED = "#C9C9C9"
COLOR_HINT = "#AAACB2"
COLOR_PROGRESS_BG = "#EBEBEB"

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 700
