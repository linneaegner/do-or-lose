"""Capture README screenshots from the live Rundan web app."""

from __future__ import annotations

import time
from pathlib import Path

from PIL import Image
from playwright.sync_api import Page, sync_playwright

BASE_URL = "https://linneaegner.github.io/rundan/"
OUT_DIR = Path(__file__).resolve().parent.parent / "docs" / "screenshots"
VIEWPORT = {"width": 420, "height": 900}

NAME_FIELD = (164, 152)
ADD_BUTTON = (318, 152)
ACCENT = (255, 107, 157)


def wait_for_app(page: Page) -> None:
    page.goto(BASE_URL, wait_until="networkidle", timeout=120_000)
    time.sleep(35)


def click_at(page: Page, x: float, y: float, delay: float = 0.6) -> None:
    page.mouse.click(x, y)
    time.sleep(delay)


def add_player(page: Page, name: str) -> None:
    click_at(page, *NAME_FIELD, delay=0.4)
    page.keyboard.press("Meta+A")
    page.keyboard.press("Backspace")
    page.keyboard.type(name, delay=35)
    click_at(page, *ADD_BUTTON, delay=0.4)


def find_accent_button(image: Image.Image, *, min_width: int = 120) -> tuple[int, int]:
    rgb = image.convert("RGB")
    width, height = rgb.size
    best_y = height - 1
    best_x = width // 2
    best_run = 0

    for y in range(height // 2, height):
        run_start = None
        for x in range(width):
            r, g, b = rgb.getpixel((x, y))
            matches = r > 220 and 80 < g < 140 and 120 < b < 190
            if matches:
                if run_start is None:
                    run_start = x
            elif run_start is not None:
                run_len = x - run_start
                if run_len > best_run and run_len >= min_width:
                    best_run = run_len
                    best_x = run_start + run_len // 2
                    best_y = y
                run_start = None
        if run_start is not None:
            run_len = width - run_start
            if run_len > best_run and run_len >= min_width:
                best_run = run_len
                best_x = run_start + run_len // 2
                best_y = y

    if best_run == 0:
        raise RuntimeError("Could not locate accent button in screenshot")
    return best_x, best_y


def capture_png(page: Page) -> Image.Image:
    return Image.open(__import__("io").BytesIO(page.screenshot(full_page=True)))


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport=VIEWPORT)
        try:
            wait_for_app(page)
            add_player(page, "Alex")
            add_player(page, "Sam")
            time.sleep(0.5)
            lobby = capture_png(page)
            lobby.save(OUT_DIR / "lobby.png")

            start_x, start_y = find_accent_button(lobby)
            click_at(page, start_x, start_y, delay=1.0)

            game = capture_png(page)
            draw_x, draw_y = find_accent_button(game)
            click_at(page, draw_x, draw_y, delay=0.8)
            click_at(page, game.size[0] // 2, game.size[1] // 2 - 40, delay=0.8)
            capture_png(page).save(OUT_DIR / "game.png")
        finally:
            browser.close()
    print(f"Saved screenshots to {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
