import random

import flet as ft

from constants import (
    CARD_IMAGES,
    COLOR_ACCENT,
    COLOR_CARD_FACE,
    COLOR_MUTED,
    COLOR_ON_PRIMARY,
    COLOR_PRIMARY,
    COLOR_PROGRESS_BG,
    COLOR_SUCCESS,
    MAX_POINTS,
    MIN_PLAYERS,
    POINTS_PER_SUCCESS,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from models import Person
from theme import (
    challenge_card_placeholder,
    icon_bar,
    label,
    name_field,
    page_header,
    player_chip,
    primary_button,
    screen,
    secondary_button,
    surface,
)

player_list: list[Person] = []
turn_index = 0
current_player: Person | None = None
game_started = False


def main(page: ft.Page) -> None:
    global turn_index, game_started, current_player

    page.title = "DO or LOSE"
    page.window.width = WINDOW_WIDTH
    page.window.height = WINDOW_HEIGHT
    page.window.resizable = False
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = COLOR_PRIMARY
    page.padding = 0

    def card_alt_text(card_path) -> str:
        card_label = card_path.stem.replace("-", " ").replace("_", " ")
        return f"Challenge card: {card_label}"

    def get_random_card() -> ft.Container:
        card_path = random.choice(CARD_IMAGES)
        return ft.Container(
            content=ft.Image(
                src=str(card_path),
                alt=card_alt_text(card_path),
                fit=ft.BoxFit.COVER,
                border_radius=12,
            ),
            width=280,
            height=280,
            border_radius=12,
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
        )

    def update_points_text(points: int) -> ft.Text:
        return label(f"{points} / {MAX_POINTS} pts", size=15, weight=ft.FontWeight.W_600)

    def update_progress_ring() -> None:
        if current_player is None:
            return
        points = current_player.get_points()
        p_ring.value = points / MAX_POINTS
        points_text_container.content = update_points_text(points)
        page.update()

    def set_active_player(player: Person, blank_card: ft.Container) -> None:
        global current_player
        current_player = player
        card.content = blank_card
        player_name.content = label(
            f"{player.get_name()}'s turn",
            size=22,
            weight=ft.FontWeight.W_700,
            text_align=ft.TextAlign.CENTER,
        )
        turn_badge.value = f"Player {turn_index + 1} of {len(player_list)}"
        update_progress_ring()

    def animate(_: ft.ControlEvent) -> None:
        if current_player is None:
            return
        random_card = get_random_card()
        card.content = random_card
        current_player.set_current_card(random_card)
        page.update()

    def animate_prev(_: ft.ControlEvent) -> None:
        if current_player is None:
            return
        card.content = current_player.get_current_card()
        page.update()

    def update_buttons() -> None:
        buttons.content = two_btn if game_started else go_btn
        if game_started and user_progress_container not in game_column.controls:
            game_column.controls.insert(-1, user_progress_container)
        page.update()

    def refresh_player_list() -> None:
        name_view.controls = [player_chip(p.get_name()) for p in player_list]

    def update_lobby_state() -> None:
        can_start = len(player_list) >= MIN_PLAYERS
        start_btn.disabled = not can_start
        lobby_hint.value = (
            "Ready to play — press Start when everyone is in."
            if can_start
            else f"Add at least {MIN_PLAYERS} players to start."
        )
        lobby_hint.color = COLOR_SUCCESS if can_start else COLOR_MUTED
        refresh_player_list()
        page.update()

    def add_player(_: ft.ControlEvent) -> None:
        name = txt_name.value.strip()
        if not name:
            return
        player_list.append(Person(name))
        txt_name.value = ""
        update_lobby_state()

    def reset_game_state() -> None:
        global turn_index, game_started, current_player
        turn_index = 0
        game_started = False
        current_player = None
        for player in player_list:
            player.points = 0
            player.current_card = None

    def start_game(_: ft.ControlEvent) -> None:
        if len(player_list) >= MIN_PLAYERS:
            reset_game_state()
            navigate_to("/game")

    def next_round(_: ft.ControlEvent) -> None:
        global turn_index, game_started
        if not player_list:
            return
        if not game_started:
            game_started = True
            update_buttons()
            set_active_player(player_list[0], card_blank)
            return

        turn_index = (turn_index + 1) % len(player_list)
        set_active_player(player_list[turn_index], card_blank)

    def yes_clicked(_: ft.ControlEvent) -> None:
        if current_player is None:
            return
        current_player.add_points(POINTS_PER_SUCCESS)
        if current_player.has_won(MAX_POINTS):
            winner_name.value = current_player.get_name()
            navigate_to("/end")
            return
        next_round(_)

    def prev_round(_: ft.ControlEvent) -> None:
        global turn_index
        if not player_list:
            return

        turn_index = (turn_index - 1) % len(player_list)
        player = player_list[turn_index]
        if player.get_points() > 0:
            player.undo_points(POINTS_PER_SUCCESS)
        set_active_player(player, card_blank_prev)

    def route_change(_: ft.RouteChangeEvent | None = None) -> None:
        page.views.clear()
        page.views.append(ft.View(route="/", controls=[screen(lobby)]))
        if page.route == "/game":
            page.views.append(ft.View(route="/game", controls=[screen(game_column)]))
        elif page.route == "/end":
            page.views.append(ft.View(route="/end", controls=[screen(end_column)]))
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
    txt_name = name_field()
    name_view = ft.Row(wrap=True, spacing=8, run_spacing=8)
    lobby_hint = label(
        f"Add at least {MIN_PLAYERS} players to start.",
        size=13,
        color=COLOR_MUTED,
        text_align=ft.TextAlign.CENTER,
    )
    start_btn = primary_button("Start game", start_game, disabled=True, width=320)

    lobby = ft.Column(
        controls=[
            page_header("DO or LOSE", "Turn-based party game · Programming 2, 2023"),
            ft.Container(height=8),
            surface(
                ft.Row(
                    [
                        ft.Container(content=txt_name, expand=True),
                        secondary_button("Add", add_player, width=88),
                    ],
                    spacing=10,
                ),
                label("Players", size=12, color=COLOR_MUTED, weight=ft.FontWeight.W_600),
                name_view,
                lobby_hint,
                tight=True,
            ),
            ft.Container(height=4),
            start_btn,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=20,
        expand=True,
    )

    # —— Game ——
    card_blank = challenge_card_placeholder("Tap to draw", animate)
    card_blank_prev = challenge_card_placeholder("Tap to reveal", animate_prev)
    card_rules = ft.Container(
        content=ft.Column(
            [
                label("How to play", size=20, color=COLOR_ON_PRIMARY, weight=ft.FontWeight.W_700),
                label(
                    "Draw a card, complete the challenge, then pass or score.",
                    size=13,
                    color=ft.Colors.with_opacity(0.75, COLOR_ON_PRIMARY),
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
            alignment=ft.MainAxisAlignment.CENTER,
        ),
        width=280,
        height=280,
        bgcolor=COLOR_CARD_FACE,
        border_radius=12,
        alignment=ft.Alignment.CENTER,
        padding=20,
    )

    card = ft.AnimatedSwitcher(
        card_rules,
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=350,
        width=300,
        height=300,
    )

    go_btn = primary_button("Begin round", next_round, width=300)
    two_btn = ft.Row(
        [
            secondary_button("Skip", next_round, width=140),
            primary_button("+15 pts", yes_clicked, width=140),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=12,
    )
    buttons = ft.Container(content=go_btn, alignment=ft.Alignment.CENTER)

    player_name = ft.Container(
        content=label("Ready?", size=22, weight=ft.FontWeight.W_700, text_align=ft.TextAlign.CENTER),
        alignment=ft.Alignment.CENTER,
    )
    turn_badge = label("", size=12, color=COLOR_MUTED, text_align=ft.TextAlign.CENTER)

    p_ring = ft.ProgressRing(width=22, height=22, stroke_width=5, color=COLOR_ACCENT)
    points_text_container = ft.Container(content=update_points_text(0))
    user_progress = surface(
        ft.Row(
            [
                p_ring,
                ft.Column(
                    [
                        label("Score", size=11, color=COLOR_MUTED),
                        points_text_container,
                    ],
                    spacing=2,
                    tight=True,
                ),
            ],
            spacing=14,
        ),
        padding=12,
    )
    user_progress_container = ft.Container(content=user_progress)

    game_column = ft.Column(
        controls=[
            icon_bar(
                ft.IconButton(
                    icon=ft.Icons.ARROW_BACK_ROUNDED,
                    tooltip="Undo last point",
                    on_click=prev_round,
                ),
                ft.IconButton(
                    icon=ft.Icons.CLOSE_ROUNDED,
                    tooltip="Exit to lobby",
                    on_click=lambda _: navigate_to("/"),
                ),
            ),
            player_name,
            turn_badge,
            ft.Container(card, alignment=ft.Alignment.CENTER),
            buttons,
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=14,
        expand=True,
    )

    # —— Winner ——
    winner_name = label("", size=36, weight=ft.FontWeight.W_700, text_align=ft.TextAlign.CENTER)

    end_column = ft.Column(
        controls=[
            ft.Row(
                [ft.Container(expand=True), ft.IconButton(icon=ft.Icons.CLOSE_ROUNDED, on_click=lambda _: navigate_to("/"))],
            ),
            ft.Container(expand=True),
            ft.Icon(ft.Icons.EMOJI_EVENTS_ROUNDED, size=56, color=COLOR_ACCENT),
            label("Winner", size=14, color=COLOR_MUTED, text_align=ft.TextAlign.CENTER),
            winner_name,
            label(f"First to {MAX_POINTS} points takes it.", size=14, color=COLOR_MUTED, text_align=ft.TextAlign.CENTER),
            ft.Container(height=12),
            primary_button("Back to lobby", lambda _: navigate_to("/"), width=280),
            ft.Container(expand=True),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=10,
        expand=True,
    )

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    route_change()


if __name__ == "__main__":
    ft.run(main)
