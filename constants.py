from pathlib import Path

# Legacy card images (optional, not used in förfest mode)
ASSETS_DIR = Path(__file__).parent / "assets" / "cards"
CARD_IMAGES = sorted(ASSETS_DIR.glob("*.png"))


def card_image_src(card_path: Path) -> str:
    return f"cards/{card_path.name}"


MIN_PLAYERS = 2

# Design tokens — warm pre-party palette
COLOR_BG = "#1A1028"
COLOR_SURFACE = "#2A1F3D"
COLOR_PRIMARY = "#F8F4FF"
COLOR_ACCENT = "#FF6B9D"
COLOR_ACCENT_SOFT = "#3D2E52"
COLOR_MUTED = "#B8A9C9"
COLOR_HINT = "#7A6B8A"
COLOR_BORDER = "#4A3858"
COLOR_CARD_FACE = "#352847"
COLOR_SUCCESS = "#7EE787"
COLOR_ON_PRIMARY = "#1A1028"
COLOR_CATEGORY: dict[str, str] = {
    "sanning": "#6CB4EE",
    "utmaning": "#FF9F5A",
    "drick": "#C77DFF",
    "rösta": "#FF6B9D",
    "vild": "#FFE066",
}

WINDOW_WIDTH = 480
WINDOW_HEIGHT = 800
CONTENT_WIDTH = 400
CONTENT_WIDTH_WIDE = 500
LAYOUT_WIDE_BREAKPOINT = 560
RADIUS_SM = 10
RADIUS_MD = 16
RADIUS_LG = 24
