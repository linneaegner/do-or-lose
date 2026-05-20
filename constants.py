from pathlib import Path

ASSETS_DIR = Path(__file__).parent / "assets" / "cards"
CARD_IMAGES = sorted(ASSETS_DIR.glob("*.png"))


def card_image_src(card_path: Path) -> str:
    """Path relative to Flet assets root (`-a assets` → `cards/…`)."""
    return f"cards/{card_path.name}"

MIN_PLAYERS = 2
MAX_POINTS = 100
POINTS_PER_SUCCESS = 15

# Design tokens
COLOR_BG = "#F4F1EB"
COLOR_SURFACE = "#FFFFFF"
COLOR_PRIMARY = "#1A2332"
COLOR_ACCENT = "#2F6F8F"
COLOR_ACCENT_SOFT = "#D6E8F2"
COLOR_MUTED = "#6B7280"
COLOR_HINT = "#9CA3AF"
COLOR_BORDER = "#E0DAD0"
COLOR_PROGRESS_BG = "#EDE8DF"
COLOR_CARD_FACE = "#1A2332"
COLOR_SUCCESS = "#2D6A4F"
COLOR_ON_PRIMARY = "#F8FAFC"

WINDOW_WIDTH = 420
WINDOW_HEIGHT = 760
RADIUS_SM = 10
RADIUS_MD = 16
RADIUS_LG = 24
