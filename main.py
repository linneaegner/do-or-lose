"""Förfest — party card game for friends before going out."""

from __future__ import annotations

import flet as ft

from constants import (
    COLOR_BG,
    COLOR_MUTED,
    COLOR_PRIMARY,
    COLOR_SUCCESS,
    CONTENT_WIDTH,
    CONTENT_WIDTH_WIDE,
    LAYOUT_WIDE_BREAKPOINT,
    MIN_PLAYERS,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from models import Person
from questions import CATEGORY_EMOJI, CATEGORY_LABELS, Category, Question, QuestionDeck
from theme import (
    category_badge,
    label,
    name_field,
    page_header,
    player_chip,
    primary_button,
    prompt_card,
    screen,
    secondary_button,
    surface,
)

CARD_PLACEHOLDER = "Tryck här för nästa kort"


def main(page: ft.Page) -> None:
    players: list[Person] = []
    turn_index = 0
    deck: QuestionDeck | None = None
    selected_categories: set[Category] = set(Category)
    name_buffer = ""

    page.title = "Förfest"
    page.window.width = WINDOW_WIDTH
    page.window.height = WINDOW_HEIGHT
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = COLOR_BG
    page.padding = 0

    def refresh() -> None:
        page.update()

    # —— Lobby ——
    txt_name = name_field("Skriv namn…")
    txt_name.expand = True

    player_list = ft.Column(spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    players_empty = ft.Text(
        "Inga spelare än.\nLägg till alla som ska vara med!",
        size=16,
        color=COLOR_MUTED,
        text_align=ft.TextAlign.CENTER,
    )
    player_count = ft.Text("0 spelare", size=15, color=COLOR_MUTED, text_align=ft.TextAlign.CENTER)
    lobby_hint = ft.Text(
        f"Lägg till minst {MIN_PLAYERS} personer för att starta.",
        size=13,
        color=COLOR_MUTED,
        text_align=ft.TextAlign.CENTER,
    )

    content_width = CONTENT_WIDTH

    def rebuild_lobby() -> None:
        count = len(players)
        can_start = count >= MIN_PLAYERS

        player_list.controls = []
        if players:
            for index, person in enumerate(players):

                def remove_player(e: ft.ControlEvent, i: int = index) -> None:
                    if 0 <= i < len(players):
                        players.pop(i)
                        rebuild_lobby()
                        refresh()

                player_list.controls.append(
                    player_chip(person.get_name(), remove_player, width=content_width)
                )
        else:
            player_list.controls.append(players_empty)

        player_count.value = (
            f"{count} spelare — redo att starta!" if can_start else f"{count} spelare ({MIN_PLAYERS - count} kvar)"
        )
        player_count.color = COLOR_SUCCESS if can_start else COLOR_MUTED

        lobby_hint.value = (
            "Alla är med! Tryck Starta förfest."
            if can_start
            else f"Lägg till minst {MIN_PLAYERS} personer."
        )
        lobby_hint.color = COLOR_SUCCESS if can_start else COLOR_MUTED

        start_btn.disabled = not can_start
        refresh()

    def on_name_change(e: ft.ControlEvent) -> None:
        nonlocal name_buffer
        name_buffer = (getattr(e.control, "value", None) or "").strip()

    def add_player(e: ft.ControlEvent | None = None) -> None:
        nonlocal name_buffer
        if e is not None and isinstance(e.control, ft.TextField):
            name = (e.control.value or name_buffer or "").strip()
        else:
            name = (txt_name.value or name_buffer or "").strip()

        if not name:
            lobby_hint.value = "Skriv ett namn först."
            lobby_hint.color = COLOR_MUTED
            refresh()
            return

        if any(p.get_name().lower() == name.lower() for p in players):
            lobby_hint.value = f"{name} finns redan!"
            lobby_hint.color = COLOR_MUTED
            refresh()
            return

        players.append(Person(name))
        txt_name.value = ""
        name_buffer = ""
        rebuild_lobby()

    txt_name.on_change = on_name_change
    txt_name.on_submit = add_player

    category_row = ft.Row(
        wrap=True,
        spacing=10,
        run_spacing=10,
        width=CONTENT_WIDTH,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    def refresh_categories() -> None:
        category_row.controls = [
            ft.Chip(
                label=f"{CATEGORY_EMOJI[cat]} {CATEGORY_LABELS[cat]}",
                selected=cat in selected_categories,
                show_checkmark=True,
                on_click=lambda e, c=cat: toggle_category(c),
            )
            for cat in Category
        ]

    def toggle_category(cat: Category) -> None:
        nonlocal selected_categories
        if cat in selected_categories:
            if len(selected_categories) > 1:
                selected_categories -= {cat}
        else:
            selected_categories |= {cat}
        refresh_categories()
        refresh()

    refresh_categories()

    def start_game(e: ft.ControlEvent) -> None:
        nonlocal turn_index, deck
        if len(players) < MIN_PLAYERS:
            return
        turn_index = 0
        deck = QuestionDeck(selected_categories)
        lobby_stack.visible = False
        game_stack.visible = True
        begin_turn()
        refresh()

    start_btn = primary_button("Starta förfest", start_game, disabled=True, width=CONTENT_WIDTH)
    lobby_header = page_header("Förfest", "100 kort · förfest med gänget")
    lobby_surface = surface(
        ft.Row(
            [txt_name, secondary_button("Lägg till", add_player, width=110)],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        player_count,
        player_list,
        lobby_hint,
    )

    lobby_content = ft.Column(
        [
            lobby_header,
            lobby_surface,
            label("Kategorier", size=13, color=COLOR_MUTED, text_align=ft.TextAlign.CENTER),
            category_row,
            start_btn,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=16,
        scroll=ft.ScrollMode.AUTO,
    )

    def apply_layout() -> None:
        nonlocal content_width
        wide = (page.width or WINDOW_WIDTH) >= LAYOUT_WIDE_BREAKPOINT
        content_width = CONTENT_WIDTH_WIDE if wide else CONTENT_WIDTH

        lobby_panel.width = content_width
        game_panel.width = content_width
        lobby_surface.width = content_width
        player_list.width = content_width
        category_row.width = content_width
        start_btn.width = content_width
        card_body.width = min(content_width + 20, 520)
        card_body.height = 300 if wide else 280

        lobby_header.controls[0].size = 40 if wide else 34
        if len(lobby_header.controls) > 1:
            lobby_header.controls[1].size = 16 if wide else 14
        player_count.size = 16 if wide else 15
        lobby_hint.size = 15 if wide else 13
        players_empty.size = 17 if wide else 16

        if players:
            rebuild_lobby()
        refresh()

    # —— Game ——
    player_name = ft.Text("—", size=26, color=COLOR_PRIMARY, weight=ft.FontWeight.W_700, text_align=ft.TextAlign.CENTER)
    turn_badge = ft.Text("", size=13, color=COLOR_MUTED, text_align=ft.TextAlign.CENTER)
    counter_badge = ft.Text("", size=12, color=COLOR_MUTED, text_align=ft.TextAlign.CENTER)
    category_slot = ft.Container()
    card_body = prompt_card(CARD_PLACEHOLDER, placeholder=True)

    def sync_game_header() -> None:
        person = players[turn_index % len(players)]
        player_name.value = f"{person.get_name()}s tur"
        turn_badge.value = f"Spelare {turn_index + 1} av {len(players)}"
        if deck:
            counter_badge.value = f"{deck.left} kort kvar"

    def set_card(text: str, *, placeholder: bool = False, on_click=None) -> None:
        card_body.content = ft.Text(
            text,
            size=22 if not placeholder else 18,
            color=COLOR_PRIMARY if not placeholder else COLOR_MUTED,
            weight=ft.FontWeight.W_600 if not placeholder else ft.FontWeight.W_500,
            text_align=ft.TextAlign.CENTER,
        )
        card_body.on_click = on_click
        card_body.ink = on_click is not None

    def draw_card(e: ft.ControlEvent | None = None) -> None:
        if deck is None:
            return
        question = deck.draw()
        if question is None:
            set_card("Inga kort i valda kategorier.", placeholder=True, on_click=draw_card)
            refresh()
            return
        category_slot.content = category_badge(
            question.category.value,
            CATEGORY_EMOJI[question.category],
            CATEGORY_LABELS[question.category],
        )
        set_card(question.text)
        refresh()

    def begin_turn() -> None:
        sync_game_header()
        category_slot.content = ft.Container()
        set_card(CARD_PLACEHOLDER, placeholder=True, on_click=draw_card)
        refresh()

    def next_player(e: ft.ControlEvent) -> None:
        nonlocal turn_index
        turn_index = (turn_index + 1) % len(players)
        begin_turn()

    def back_to_lobby(e: ft.ControlEvent) -> None:
        game_stack.visible = False
        lobby_stack.visible = True
        rebuild_lobby()

    game_content = ft.Column(
        [
            ft.Row(
                [
                    ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color=COLOR_PRIMARY, on_click=back_to_lobby),
                    ft.Container(expand=True),
                ],
            ),
            player_name,
            turn_badge,
            counter_badge,
            category_slot,
            ft.Container(card_body, alignment=ft.Alignment.CENTER),
            ft.Row(
                [
                    secondary_button("Nytt kort", draw_card, width=150),
                    primary_button("Nästa", next_player, width=150),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            primary_button("Dra kort", draw_card, width=320),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    lobby_panel = ft.Container(content=lobby_content, width=CONTENT_WIDTH)
    game_panel = ft.Container(content=game_content, width=CONTENT_WIDTH)

    def centered_row(panel: ft.Container) -> ft.Row:
        return ft.Row(
            [panel],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.START,
            expand=True,
        )

    lobby_stack = ft.Container(content=centered_row(lobby_panel), expand=True, visible=True)
    game_stack = ft.Container(content=centered_row(game_panel), expand=True, visible=False)

    page.on_resize = lambda e: apply_layout()

    page.add(
        screen(
            ft.Stack([lobby_stack, game_stack], expand=True),
            scroll=False,
        )
    )
    rebuild_lobby()
    apply_layout()


if __name__ == "__main__":
    ft.run(main)
