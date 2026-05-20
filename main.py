import random

import flet as ft

from constants import (
    CARD_IMAGES,
    COLOR_ACCENT,
    COLOR_HINT,
    COLOR_MUTED,
    COLOR_PRIMARY,
    COLOR_PROGRESS_BG,
    FONT_FAMILY,
    MAX_POINTS,
    MIN_PLAYERS,
    POINTS_PER_SUCCESS,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from models import Person

player_list: list[Person] = []
turn_index = 0
current_player: Person | None = None
game_started = False


def main(page: ft.Page) -> None:
    page.title = "DO or LOSE"
    page.window.width = WINDOW_WIDTH
    page.window.height = WINDOW_HEIGHT
    page.window.resizable = False
    page.window.title_bar_hidden = True

    def bold_text(content: str, **kwargs) -> ft.Text:
        return ft.Text(content, font_family=FONT_FAMILY, weight="bold", **kwargs)

    def card_alt_text(card_path) -> str:
        label = card_path.stem.replace("-", " ").replace("_", " ")
        return f"Challenge card: {label}"

    def get_random_card() -> ft.Container:
        card_path = random.choice(CARD_IMAGES)
        return ft.Container(
            content=ft.Image(
                src=str(card_path),
                alt=card_alt_text(card_path),
                border_radius=8,
            ),
            width=300,
            height=300,
            margin=8,
        )

    def update_points_text(points: int) -> ft.Text:
        return bold_text(
            f"{points} / {MAX_POINTS} poäng",
            color=COLOR_PRIMARY,
            size=16,
        )

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
        player_name.content = bold_text(
            player.get_name(),
            color=COLOR_PRIMARY,
            size=36,
        )
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
        if game_started:
            buttons.content = two_btn.content
            if user_progress_container not in game.controls:
                game.controls.append(user_progress_container)
        else:
            buttons.content = go_btn.content
        page.update()

    def update_lobby_state() -> None:
        can_start = len(player_list) >= MIN_PLAYERS
        start_elevated.disabled = not can_start
        lobby_hint.value = (
            ""
            if can_start
            else f"Add at least {MIN_PLAYERS} players to start."
        )
        page.update()

    def add_player(_: ft.ControlEvent) -> None:
        name = txt_name.value.strip()
        if not name:
            return
        player_list.append(Person(name))
        name_view.content.controls.append(
            bold_text(name, color=COLOR_PRIMARY),
        )
        txt_name.value = ""
        update_lobby_state()

    def start_game(_: ft.ControlEvent) -> None:
        if len(player_list) >= MIN_PLAYERS:
            navigate_to("/game")

    def next_round(_: ft.ControlEvent) -> None:
        global turn_index, game_started
        if not player_list:
            return
        if not game_started:
            game_started = True
            update_buttons()

        turn_index = (turn_index + 1) % len(player_list)
        set_active_player(player_list[turn_index], card_blank)

    def yes_clicked(_: ft.ControlEvent) -> None:
        if current_player is None:
            return
        current_player.add_points(POINTS_PER_SUCCESS)
        if current_player.has_won(MAX_POINTS):
            winner.content = ft.Text(
                current_player.get_name(),
                style=ft.TextThemeStyle.DISPLAY_MEDIUM,
            )
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
        page.views.append(ft.View(route="/", controls=[start]))
        if page.route == "/game":
            page.views.append(ft.View(route="/game", controls=[game]))
        elif page.route == "/end":
            page.views.append(ft.View(route="/end", controls=[end]))
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

    def on_hover(e: ft.ControlEvent) -> None:
        e.control.content = bold_text(
            "+ ADD MORE",
            size=16,
            color=COLOR_ACCENT if e.data == "true" else COLOR_MUTED,
        )
        e.control.update()

    txt_name = ft.TextField(
        hint_text="NAME",
        hint_style=ft.TextStyle(
            font_family=FONT_FAMILY,
            weight="bold",
            color=COLOR_HINT,
        ),
        border=ft.InputBorder.NONE,
        filled=True,
        cursor_color=COLOR_PRIMARY,
        autofocus=True,
        text_style=ft.TextStyle(
            font_family=FONT_FAMILY,
            weight="bold",
            color=COLOR_PRIMARY,
        ),
    )

    titel = ft.Container(
        content=bold_text("DO or LOSE", color=ft.Colors.BLACK_87, size=52),
        alignment=ft.Alignment(0, 0),
        margin=20,
    )

    name_view = ft.Container(
        ft.Column(),
        alignment=ft.Alignment(0, 0),
        height=200,
        margin=10,
    )

    start_elevated = ft.ElevatedButton(
        content=bold_text("START GAME", size=28, color=COLOR_ACCENT),
        style=ft.ButtonStyle(
            shape=ft.ContinuousRectangleBorder(radius=20),
            bgcolor=COLOR_PRIMARY,
        ),
        width=240,
        height=80,
        disabled=True,
        on_click=start_game,
    )
    start_btn = ft.Container(
        content=start_elevated,
        alignment=ft.Alignment(0, 0),
    )
    lobby_hint = ft.Text(
        f"Add at least {MIN_PLAYERS} players to start.",
        font_family=FONT_FAMILY,
        size=12,
        color=COLOR_HINT,
        text_align=ft.TextAlign.CENTER,
    )

    start = ft.Column(
        controls=[
            ft.Container(height=20),
            titel,
            ft.Container(height=20),
            ft.Row(
                controls=[
                    ft.Container(
                        content=txt_name,
                        width=220,
                        margin=ft.Margin(left=20),
                        border_radius=25,
                    ),
                    ft.Container(
                        content=ft.TextButton(
                            content=bold_text("+ ADD MORE", size=16, color=COLOR_MUTED),
                            style=ft.ButtonStyle(
                                shape=ft.ContinuousRectangleBorder(radius=30)
                            ),
                            on_hover=on_hover,
                            on_click=add_player,
                        )
                    ),
                ],
            ),
            name_view,
            lobby_hint,
            start_btn,
        ]
    )

    card_blank = ft.Container(
        bold_text("TURN CARD", color=ft.Colors.WHITE_70, size=24),
        width=300,
        height=300,
        margin=8,
        border_radius=8,
        bgcolor=ft.Colors.BLACK_87,
        alignment=ft.Alignment(0, 0),
        on_click=animate,
    )

    card_blank_prev = ft.Container(
        bold_text("TURN CARD", color=ft.Colors.WHITE_70, size=24),
        width=300,
        height=300,
        margin=8,
        border_radius=8,
        bgcolor=ft.Colors.BLACK_87,
        alignment=ft.Alignment(0, 0),
        on_click=animate_prev,
    )

    card_start = ft.Container(
        ft.Text(
            "regler",
            style=ft.TextThemeStyle.DISPLAY_MEDIUM,
            color=ft.Colors.WHITE_38,
        ),
        bgcolor=ft.Colors.BLACK_87,
        height=300,
        width=300,
        margin=40,
        border_radius=8,
        alignment=ft.Alignment(0, 0),
    )

    go_btn = ft.Container(
        content=ft.ElevatedButton(
            content=bold_text("LET'S GO", size=28, color=COLOR_ACCENT),
            style=ft.ButtonStyle(
                shape=ft.ContinuousRectangleBorder(radius=20),
                bgcolor=COLOR_PRIMARY,
            ),
            width=240,
            height=80,
            on_click=next_round,
        ),
        alignment=ft.Alignment(0, 0),
    )

    top_buttons = ft.Row(
        [
            ft.IconButton(icon=ft.Icons.ARROW_BACK_ROUNDED, on_click=prev_round),
            ft.IconButton(
                icon=ft.Icons.CLOSE_ROUNDED,
                on_click=lambda _: navigate_to("/"),
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    player_name = ft.Container(
        content=bold_text("Är ni redo?", color=COLOR_PRIMARY, size=36),
        alignment=ft.Alignment(0, 0),
    )

    card = ft.AnimatedSwitcher(
        card_start,
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=400,
        width=400,
    )

    buttons = ft.Container(
        content=go_btn.content,
        alignment=ft.Alignment(0, 0),
        margin=24,
    )

    button_style = ft.ButtonStyle(
        shape=ft.ContinuousRectangleBorder(radius=20),
        bgcolor=COLOR_PRIMARY,
    )

    two_btn = ft.Container(
        content=ft.Row(
            [
                ft.ElevatedButton(
                    content=bold_text("I FAILED", size=16, color="#F1F1F1"),
                    style=button_style,
                    width=160,
                    height=60,
                    on_click=next_round,
                ),
                ft.ElevatedButton(
                    content=bold_text("EASY PEASY", size=16, color=COLOR_ACCENT),
                    style=button_style,
                    width=160,
                    height=60,
                    on_click=yes_clicked,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=15,
        ),
    )

    p_ring = ft.ProgressRing(width=20, height=20, stroke_width=6)
    points_text_container = ft.Container(content=update_points_text(0))
    user_progress = ft.Card(
        content=ft.Container(
            ft.Column(
                [
                    ft.Row(
                        controls=[
                            ft.Container(content=p_ring, padding=12),
                            ft.Column(
                                [
                                    ft.Text(
                                        "Dina poäng",
                                        font_family=FONT_FAMILY,
                                        color=ft.Colors.BLACK_87,
                                        size=12,
                                    ),
                                    points_text_container,
                                ],
                                spacing=2,
                            ),
                        ]
                    )
                ],
            ),
            padding=8,
            width=360,
            height=60,
            bgcolor=COLOR_PROGRESS_BG,
            border_radius=8,
        ),
        elevation=4,
        margin=ft.Margin(top=20),
    )
    user_progress_container = ft.Container(
        content=user_progress,
        margin=0,
        padding=0,
        alignment=ft.Alignment(0, 0),
    )

    game = ft.Column(
        controls=[
            ft.Container(height=8),
            top_buttons,
            player_name,
            card,
            buttons,
        ],
    )

    x_button = ft.Container(
        ft.IconButton(
            icon=ft.Icons.CLOSE_ROUNDED,
            on_click=lambda _: navigate_to("/"),
        ),
        alignment=ft.Alignment(1, 0),
    )

    winner = ft.Container(
        content=ft.Text(""),
        alignment=ft.Alignment(0, 0),
    )

    end = ft.Column(
        controls=[
            x_button,
            ft.Container(
                ft.Text("Vinnare!!", style=ft.TextThemeStyle.DISPLAY_MEDIUM),
                alignment=ft.Alignment(0, 0),
                padding=40,
            ),
            winner,
        ]
    )

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    route_change()


if __name__ == "__main__":
    ft.run(main)
