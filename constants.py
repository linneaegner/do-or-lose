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
CONTENT_MIN_WIDTH = 260
LAYOUT_NARROW_BREAKPOINT = 420
LAYOUT_WIDE_BREAKPOINT = 560
SCREEN_PADDING_X = 24
SCREEN_PADDING_X_NARROW = 12
SCREEN_PADDING_Y = 20
SCREEN_PADDING_Y_NARROW = 12
RADIUS_SM = 10
RADIUS_MD = 16
RADIUS_LG = 24


def layout_metrics(page_width: float | None) -> dict[str, int | bool]:
    """Derive content widths and typography from the current viewport."""
    width = int(page_width or WINDOW_WIDTH)
    narrow = width < LAYOUT_NARROW_BREAKPOINT
    wide = width >= LAYOUT_WIDE_BREAKPOINT
    pad_x = SCREEN_PADDING_X_NARROW if narrow else SCREEN_PADDING_X
    pad_y = SCREEN_PADDING_Y_NARROW if narrow else SCREEN_PADDING_Y
    max_content = CONTENT_WIDTH_WIDE if wide else CONTENT_WIDTH
    content_width = min(max_content, max(CONTENT_MIN_WIDTH, width - pad_x * 2))
    return {
        "narrow": narrow,
        "wide": wide,
        "pad_x": pad_x,
        "pad_y": pad_y,
        "content_width": content_width,
        "card_width": content_width,
        "card_height": 220 if narrow else (300 if wide else 280),
        "title_size": 30 if narrow else (40 if wide else 34),
        "player_name_size": 22 if narrow else 26,
        "card_text_size": 18 if narrow else 22,
        "card_placeholder_size": 16 if narrow else 18,
        "meta_text_size": 12 if narrow else 13,
        "chip_text_size": 15 if narrow else 17,
        "add_btn_width": content_width if narrow else 110,
    }
