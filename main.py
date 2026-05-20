"""Förfest — party card game for friends before going out."""

from __future__ import annotations

import flet as ft

from constants import COLOR_BG, COLOR_MUTED, COLOR_PRIMARY, COLOR_SUCCESS, MIN_PLAYERS, WINDOW_HEIGHT, WINDOW_WIDTH
from models import Person
from questions import (
    CATEGORY_EMOJI,
    CATEGORY_LABELS,
    Category,
    Question,
    QuestionDeck,
)
from theme import (
    category_badge,
    icon_bar,
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

player_list: list[Person] = []
turn_index = 0
deck: QuestionDeck | None = None
current_question: Question | None = None
selected_categories: set[Category] = set(Category)


def main(page: ft.Page) -> None:
    global turn_index, deck, current_question, selected_categories

    page.title = "Förfest"
    page.window.width = WINDOW_WIDTH
    page.window.height = WINDOW_HEIGHT
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = COLOR_BG
    page.padding = 0

    name_input_buffer = ""

    def on_name_change(e: ft.ControlEvent) -> None:
        nonlocal name_input_buffer
        value = getattr(e.control, "value", None) if e.control else None
        name_input_buffer = (value or getattr(e, "data", None) or "").strip()

    def refresh_player_list() -> None:
        name_view.controls = [player_chip(p.get_name()) for p in player_list]

    def update_lobby_state() -> None:
        can_start = len(player_list) >= MIN_PLAYERS
        start_btn.disabled = not can_start
        lobby_hint.value = (
            "Redo att dra kort? Tryck Start."
            if can_start
            else f"Lägg till minst {MIN_PLAYERS} personer."
        )
        lobby_hint.color = COLOR_SUCCESS if can_start else COLOR_MUTED
        refresh_player_list()
        page.update()

    def add_player(e: ft.ControlEvent | None = None) -> None:
        nonlocal name_input_buffer
        if e is not None and isinstance(e.control, ft.TextField):
            name = (e.control.value or name_input_buffer or "").strip()
        else:
            name = (txt_name.value or name_input_buffer or "").strip()
        if not name:
            lobby_hint.value = "Skriv ett namn och tryck Lägg till."
            lobby_hint.color = COLOR_MUTED
            page.update()
            return
        if any(p.get_name().lower() == name.lower() for p in player_list):
            lobby_hint.value = f"{name} finns redan i gänget."
            lobby_hint.color = COLOR_MUTED
            page.update()
            return
        player_list.append(Person(name))
        txt_name.value = ""
        name_input_buffer = ""
        update_lobby_state()

    def toggle_category(cat: Category) -> None:
        global selected_categories
        if cat in selected_categories:
            if len(selected_categories) > 1:
                selected_categories = selected_categories - {cat}
        else:
            selected_categories = selected_categories | {cat}
        refresh_category_chips()
        page.update()

    def refresh_category_chips() -> None:
        category_row.controls = [
            ft.Chip(
                label=f"{CATEGORY_EMOJI[cat]} {CATEGORY_LABELS[cat]}",
                selected=cat in selected_categories,
                show_checkmark=True,
                on_click=lambda e, c=cat: toggle_category(c),
            )
            for cat in Category
        ]

    def current_player() -> Person | None:
        if not player_list:
            return None
        return player_list[turn_index % len(player_list)]

    def update_turn_header() -> None:
        player = current_player()
        if player is None:
            return
        player_name.content = label(
            f"{player.get_name()}s tur",
            size=24,
            color=COLOR_PRIMARY,
            weight=ft.FontWeight.W_700,
            text_align=ft.TextAlign.CENTER,
        )
        turn_badge.value = f"Spelare {turn_index + 1} av {len(player_list)}"
        if deck:
            counter_badge.value = f"Kort {deck.drawn_count} · {deck.left} kvar av {deck.total}"

    def show_question(q: Question) -> None:
        global current_question
        current_question = q
        category_slot.content = category_badge(
            q.category.value,
            CATEGORY_EMOJI[q.category],
            CATEGORY_LABELS[q.category],
        )
        card_slot.content = prompt_card(q.text)
        page.update()

    def show_placeholder() -> None:
        global current_question
        current_question = None
        category_slot.content = ft.Container()
        card_slot.content = prompt_card("Tryck för att dra kort", placeholder=True, on_click=draw_card)
        page.update()

    def draw_card(_: ft.ControlEvent | None = None) -> None:
        if deck is None:
            return
        question = deck.draw()
        if question is None:
            card_slot.content = prompt_card("Inga kort i valda kategorier.", placeholder=True)
            page.update()
            return
        show_question(question)

    def next_player(_: ft.ControlEvent) -> None:
        global turn_index
        if not player_list:
            return
        turn_index = (turn_index + 1) % len(player_list)
        update_turn_header()
        show_placeholder()

    def skip_card(_: ft.ControlEvent) -> None:
        draw_card()

    def start_game(_: ft.ControlEvent) -> None:
        global turn_index, deck, current_question
        if len(player_list) < MIN_PLAYERS:
            return
        turn_index = 0
        current_question = None
        deck = QuestionDeck(selected_categories)
        navigate_to("/game")
        update_turn_header()
        show_placeholder()

    def route_change(_: ft.RouteChangeEvent | None = None) -> None:
        page.views.clear()
        page.views.append(ft.View(route="/", controls=[screen(lobby)]))
        if page.route == "/game":
            page.views.append(ft.View(route="/game", controls=[screen(game_column)]))
        page.update()

    def view_pop(e: ft.ViewPopEvent) -> None:
        if e.view is not None:
            page.views.remove(e.view)
        elif page.views:
            page.views.pop()
        if page.views:
            page.navigate(page.views[-1].route)

    def navigate_to(route: str) -> None:
        page.navigate(route)

    # —— Lobby ——
    txt_name = name_field("Ditt namn")
    txt_name.expand = True
    txt_name.on_change = on_name_change
    txt_name.on_submit = add_player
    name_view = ft.Column(spacing=8, width=320)
    lobby_hint = label(
        f"Lägg till minst {MIN_PLAYERS} personer.",
        size=13,
        color=COLOR_MUTED,
        text_align=ft.TextAlign.CENTER,
    )
    start_btn = primary_button("Starta förfest", start_game, disabled=True, width=320)
    category_row = ft.Row(wrap=True, spacing=8, run_spacing=8, width=320)
    refresh_category_chips()

    lobby = ft.Column(
        controls=[
            page_header("Förfest", "100 kort · sanning, utmaning, drick & mer"),
            ft.Container(height=4),
            surface(
                ft.Row(
                    [txt_name, secondary_button("Lägg till", add_player, width=100)],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                label("Gänget", size=12, color=COLOR_MUTED, weight=ft.FontWeight.W_600),
                name_view,
                lobby_hint,
            ),
            label("Kategorier (välj minst en)", size=12, color=COLOR_MUTED),
            category_row,
            start_btn,
            label("Drick ansvarsfullt · hoppa över när du vill", size=11, color=COLOR_MUTED, text_align=ft.TextAlign.CENTER),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=16,
        expand=True,
    )

    # —— Game ——
    category_slot = ft.Container()
    card_slot = ft.Container(
        content=prompt_card("Tryck för att dra kort", placeholder=True),
        alignment=ft.Alignment.CENTER,
    )
    player_name = ft.Container(
        content=label("Redo?", size=24, color=COLOR_PRIMARY, weight=ft.FontWeight.W_700, text_align=ft.TextAlign.CENTER),
        alignment=ft.Alignment.CENTER,
    )
    turn_badge = label("", size=12, color=COLOR_MUTED, text_align=ft.TextAlign.CENTER)
    counter_badge = label("", size=11, color=COLOR_MUTED, text_align=ft.TextAlign.CENTER)

    game_column = ft.Column(
        controls=[
            icon_bar(
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK_ROUNDED,
                    icon_color=COLOR_PRIMARY,
                    tooltip="Tillbaka till lobby",
                    on_click=lambda _: navigate_to("/"),
                ),
                ft.Container(expand=True),
            ),
            player_name,
            turn_badge,
            counter_badge,
            category_slot,
            card_slot,
            ft.Row(
                [
                    secondary_button("Hoppa över", skip_card, width=150),
                    primary_button("Nästa spelare", next_player, width=150),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                spacing=12,
            ),
            primary_button("Dra nytt kort", draw_card, width=320),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=12,
        expand=True,
    )

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    update_lobby_state()
    route_change()


if __name__ == "__main__":
    ft.run(main)
