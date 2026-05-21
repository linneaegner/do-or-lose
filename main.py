"""Rundan — party card game for friends before going out."""

from __future__ import annotations

import flet as ft

from constants import (
    COLOR_BG,
    COLOR_MUTED,
    COLOR_PRIMARY,
    MIN_PLAYERS,
    layout_metrics,
)
from models import Person
from questions import CATEGORY_EMOJI, CATEGORY_LABELS, Category, QUESTIONS, Question, QuestionDeck
from theme import (
    category_badge,
    name_field,
    page_header,
    player_chip,
    primary_button,
    prompt_card,
    screen,
    secondary_button,
    surface,
)

CARD_SWAP_HINT = "Tryck på kortet om du vill byta kort"


def main(page: ft.Page) -> None:
    players: list[Person] = []
    turn_index = 0
    deck: QuestionDeck | None = None
    selected_categories: set[Category] = set(Category)
    name_buffer = ""

    page.title = "Rundan"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = COLOR_BG
    page.padding = 0

    layout = layout_metrics(page.width)
    content_width = layout["content_width"]
    card_text_size = layout["card_text_size"]
    card_placeholder_size = layout["card_placeholder_size"]

    def refresh() -> None:
        page.update()

    # —— Lobby ——
    txt_name = name_field("Skriv namn…")
    txt_name.expand = True

    player_list = ft.Column(spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def show_snack(message: str) -> None:
        page.snack_bar = ft.SnackBar(content=ft.Text(message), duration=2000)
        page.snack_bar.open = True

    def rebuild_lobby() -> None:
        count = len(players)
        can_start = count >= MIN_PLAYERS

        player_list.controls = []
        for index, person in enumerate(players):

            def remove_player(e: ft.ControlEvent, i: int = index) -> None:
                if 0 <= i < len(players):
                    players.pop(i)
                    rebuild_lobby()
                    refresh()

            player_list.controls.append(
                player_chip(
                    person.get_name(),
                    remove_player,
                    width=content_width,
                    name_size=layout["chip_text_size"],
                )
            )

        start_btn.disabled = not can_start
        start_btn.content = "Starta rundan" if can_start else f"Starta ({count}/{MIN_PLAYERS} spelare)"
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
            show_snack("Skriv ett namn först.")
            refresh()
            return

        if any(p.get_name().lower() == name.lower() for p in players):
            show_snack(f"{name} finns redan.")
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
        alignment=ft.MainAxisAlignment.CENTER,
    )

    add_player_btn = secondary_button("Lägg till", add_player, width=layout["add_btn_width"])
    name_input_slot = ft.Container()

    def rebuild_name_input(metrics: dict[str, int | bool]) -> None:
        add_player_btn.width = metrics["add_btn_width"]
        txt_name.expand = not metrics["narrow"]
        if metrics["narrow"]:
            txt_name.width = metrics["content_width"]
            name_input_slot.content = ft.Column(
                [txt_name, add_player_btn],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        else:
            txt_name.width = None
            name_input_slot.content = ft.Row(
                [txt_name, add_player_btn],
                spacing=10,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
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

    start_btn = primary_button("Starta (0/2 spelare)", start_game, disabled=True, width=content_width)
    lobby_header = page_header("Rundan")
    rebuild_name_input(layout)
    lobby_surface = surface(
        name_input_slot,
        player_list,
    )

    lobby_content = ft.Column(
        [
            lobby_header,
            lobby_surface,
            category_row,
            start_btn,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=16,
        scroll=ft.ScrollMode.AUTO,
    )

    def apply_layout() -> None:
        nonlocal content_width, card_text_size, card_placeholder_size, layout
        layout = layout_metrics(page.width)
        content_width = layout["content_width"]
        card_text_size = layout["card_text_size"]
        card_placeholder_size = layout["card_placeholder_size"]

        screen_shell.padding = ft.Padding.symmetric(
            horizontal=layout["pad_x"],
            vertical=layout["pad_y"],
        )
        lobby_panel.width = content_width
        game_panel.width = content_width
        lobby_surface.width = content_width
        player_list.width = content_width
        category_row.width = content_width
        start_btn.width = content_width
        next_btn.width = content_width
        card_body.width = layout["card_width"]
        card_body.height = layout["card_height"]
        card_body.padding = 16 if layout["narrow"] else 20

        lobby_header.controls[0].size = layout["title_size"]
        player_name.size = layout["player_name_size"]
        game_meta.size = layout["meta_text_size"]
        card_content = card_body.content
        if isinstance(card_content, ft.Column):
            for i, control in enumerate(card_content.controls):
                if isinstance(control, ft.Text):
                    control.size = layout["meta_text_size"] if i > 0 else (
                        card_placeholder_size if control.color == COLOR_MUTED else card_text_size
                    )
        elif isinstance(card_content, ft.Text):
            card_content.size = (
                card_placeholder_size if card_content.color == COLOR_MUTED else card_text_size
            )
        rebuild_name_input(layout)
        rebuild_lobby()
        refresh()

    # —— Game ——
    player_name = ft.Text(
        "—",
        size=layout["player_name_size"],
        color=COLOR_PRIMARY,
        weight=ft.FontWeight.W_700,
        text_align=ft.TextAlign.CENTER,
    )
    game_meta = ft.Text("", size=layout["meta_text_size"], color=COLOR_MUTED, text_align=ft.TextAlign.CENTER)
    category_slot = ft.Container(alignment=ft.Alignment.CENTER)
    card_body = prompt_card(
        "",
        placeholder=True,
        text_size=card_text_size,
        placeholder_size=card_placeholder_size,
    )

    def sync_game_header() -> None:
        person = players[turn_index % len(players)]
        player_name.value = f"{person.get_name()}s tur"
        left = deck.left if deck else 0
        game_meta.value = f"{turn_index + 1} av {len(players)} · {left} kort kvar"

    def show_category(question: Question | None) -> None:
        if question is None:
            category_slot.content = ft.Container()
            return
        category_slot.content = category_badge(
            question.category.value,
            CATEGORY_EMOJI[question.category],
            CATEGORY_LABELS[question.category],
        )

    def set_card(text: str, *, placeholder: bool = False, on_click=None) -> None:
        card_text = ft.Text(
            text,
            size=card_placeholder_size if placeholder else card_text_size,
            color=COLOR_PRIMARY if not placeholder else COLOR_MUTED,
            weight=ft.FontWeight.W_600 if not placeholder else ft.FontWeight.W_500,
            text_align=ft.TextAlign.CENTER,
        )
        if on_click is not None:
            card_body.content = ft.Column(
                [
                    card_text,
                    ft.Text(
                        CARD_SWAP_HINT,
                        size=layout["meta_text_size"],
                        color=COLOR_MUTED,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                spacing=12,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                alignment=ft.MainAxisAlignment.CENTER,
            )
        else:
            card_body.content = card_text
        card_body.on_click = on_click
        card_body.ink = on_click is not None

    def draw_card(e: ft.ControlEvent | None = None) -> None:
        if deck is None:
            return
        question = deck.draw()
        if question is None:
            show_category(None)
            set_card("Inga kort i valda kategorier.", placeholder=True, on_click=draw_card)
            next_btn.visible = False
            next_btn.disabled = True
            refresh()
            return
        show_category(question)
        set_card(question.text, on_click=draw_card)
        sync_game_header()
        next_btn.visible = True
        next_btn.disabled = False
        refresh()

    def begin_turn() -> None:
        sync_game_header()
        draw_card()

    def next_player(e: ft.ControlEvent) -> None:
        nonlocal turn_index
        turn_index = (turn_index + 1) % len(players)
        begin_turn()

    def back_to_lobby(e: ft.ControlEvent) -> None:
        game_stack.visible = False
        lobby_stack.visible = True
        rebuild_lobby()

    next_btn = primary_button("Nästa spelare", next_player, width=content_width, disabled=True)
    next_btn.visible = False

    game_content = ft.Column(
        [
            ft.Row(
                [
                    ft.IconButton(icon=ft.Icons.ARROW_BACK, icon_color=COLOR_PRIMARY, on_click=back_to_lobby),
                    ft.Container(expand=True),
                ],
            ),
            player_name,
            game_meta,
            category_slot,
            ft.Container(card_body, alignment=ft.Alignment.CENTER),
            next_btn,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    lobby_panel = ft.Container(content=lobby_content, width=content_width)
    game_panel = ft.Container(content=game_content, width=content_width)

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

    screen_shell = screen(
        ft.Stack([lobby_stack, game_stack], expand=True),
        scroll=False,
        horizontal_padding=layout["pad_x"],
        vertical_padding=layout["pad_y"],
    )

    page.add(screen_shell)
    rebuild_lobby()
    apply_layout()


if __name__ == "__main__":
    ft.run(main)
