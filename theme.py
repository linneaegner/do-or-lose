"""Reusable Flet UI primitives for Rundan."""

from __future__ import annotations

import flet as ft

from constants import (
    COLOR_ACCENT,
    COLOR_ACCENT_SOFT,
    COLOR_BG,
    COLOR_BORDER,
    COLOR_CARD_FACE,
    COLOR_HINT,
    COLOR_MUTED,
    COLOR_ON_PRIMARY,
    COLOR_PRIMARY,
    COLOR_SURFACE,
    RADIUS_LG,
    RADIUS_MD,
)


def label(
    value: str,
    *,
    size: int = 14,
    color: str = COLOR_PRIMARY,
    weight: ft.FontWeight = ft.FontWeight.W_500,
    text_align: ft.TextAlign = ft.TextAlign.LEFT,
) -> ft.Text:
    return ft.Text(
        value,
        size=size,
        color=color,
        weight=weight,
        text_align=text_align,
    )


def screen(
    content: ft.Control,
    *,
    scroll: bool = False,
    horizontal_padding: int = 24,
    vertical_padding: int = 20,
) -> ft.Container:
    wrapper: ft.Control = (
        ft.Column([content], scroll=ft.ScrollMode.AUTO, expand=True)
        if scroll
        else content
    )
    return ft.Container(
        content=wrapper,
        bgcolor=COLOR_BG,
        padding=ft.Padding.symmetric(horizontal=horizontal_padding, vertical=vertical_padding),
        alignment=ft.Alignment(0, -1),
        expand=True,
    )


def surface(*controls: ft.Control, padding: int = 16, width: int | None = None) -> ft.Container:
    from constants import CONTENT_WIDTH

    return ft.Container(
        content=ft.Column(
            controls=list(controls),
            spacing=12,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=COLOR_SURFACE,
        border=ft.Border.all(1, COLOR_BORDER),
        border_radius=RADIUS_MD,
        padding=padding,
        width=width if width is not None else CONTENT_WIDTH,
    )


def primary_button(
    text: str,
    on_click,
    *,
    disabled: bool = False,
    width: int | None = None,
) -> ft.FilledButton:
    return ft.FilledButton(
        content=text,
        on_click=on_click,
        disabled=disabled,
        width=width,
        style=ft.ButtonStyle(
            bgcolor={ft.ControlState.DEFAULT: COLOR_ACCENT, ft.ControlState.DISABLED: COLOR_HINT},
            color={ft.ControlState.DEFAULT: COLOR_ON_PRIMARY, ft.ControlState.DISABLED: COLOR_MUTED},
            shape=ft.RoundedRectangleBorder(radius=RADIUS_MD),
            padding=ft.Padding.symmetric(horizontal=20, vertical=18),
        ),
    )


def secondary_button(text: str, on_click, *, width: int | None = None) -> ft.OutlinedButton:
    return ft.OutlinedButton(
        content=text,
        on_click=on_click,
        width=width,
        style=ft.ButtonStyle(
            color={ft.ControlState.DEFAULT: COLOR_PRIMARY},
            side={ft.ControlState.DEFAULT: ft.BorderSide(1.5, COLOR_ACCENT)},
            shape=ft.RoundedRectangleBorder(radius=RADIUS_MD),
            padding=ft.Padding.symmetric(horizontal=16, vertical=14),
        ),
    )


def name_field(hint: str = "Namn") -> ft.TextField:
    return ft.TextField(
        hint_text=hint,
        hint_style=ft.TextStyle(color=COLOR_HINT, size=14),
        border_color=COLOR_BORDER,
        focused_border_color=COLOR_ACCENT,
        filled=True,
        bgcolor=COLOR_BG,
        border_radius=RADIUS_LG,
        content_padding=ft.Padding.symmetric(horizontal=16, vertical=14),
        text_style=ft.TextStyle(color=COLOR_PRIMARY, size=16, weight=ft.FontWeight.W_500),
        cursor_color=COLOR_ACCENT,
    )


def player_chip(
    name: str,
    on_remove,
    *,
    width: int | None = None,
    name_size: int = 17,
) -> ft.Container:
    from constants import CONTENT_WIDTH

    chip_width = width if width is not None else CONTENT_WIDTH
    return ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.PERSON, size=20, color=COLOR_ACCENT),
                label(name, size=name_size, weight=ft.FontWeight.W_600),
                ft.IconButton(
                    icon=ft.Icons.CLOSE,
                    icon_size=18,
                    icon_color=COLOR_MUTED,
                    tooltip="Ta bort",
                    on_click=on_remove,
                    style=ft.ButtonStyle(padding=0),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor=COLOR_ACCENT_SOFT,
        border_radius=RADIUS_LG,
        padding=ft.Padding.only(left=16, right=4, top=10, bottom=10),
        width=chip_width,
    )


def category_badge(category_key: str, emoji: str, label_text: str) -> ft.Container:
    from constants import COLOR_CATEGORY

    color = COLOR_CATEGORY.get(category_key, COLOR_ACCENT)
    return ft.Container(
        content=ft.Row(
            [label(emoji, size=14), label(label_text, size=12, color=color, weight=ft.FontWeight.W_700)],
            spacing=6,
            tight=True,
        ),
        bgcolor=ft.Colors.with_opacity(0.15, color),
        border=ft.Border.all(1, ft.Colors.with_opacity(0.35, color)),
        border_radius=RADIUS_LG,
        padding=ft.Padding.symmetric(horizontal=12, vertical=6),
    )


def prompt_card(
    text: str,
    *,
    on_click=None,
    placeholder: bool = False,
    text_size: int = 22,
    placeholder_size: int = 18,
) -> ft.Container:
    return ft.Container(
        content=label(
            text,
            size=placeholder_size if placeholder else text_size,
            color=COLOR_PRIMARY if not placeholder else COLOR_MUTED,
            weight=ft.FontWeight.W_600 if not placeholder else ft.FontWeight.W_500,
            text_align=ft.TextAlign.CENTER,
        ),
        border_radius=RADIUS_MD,
        bgcolor=COLOR_CARD_FACE,
        border=ft.Border.all(1, COLOR_BORDER),
        alignment=ft.Alignment.CENTER,
        padding=20,
        on_click=on_click,
        ink=on_click is not None,
    )


def page_header(title: str, subtitle: str | None = None, *, large: bool = False) -> ft.Column:
    items = [
        label(
            title,
            size=40 if large else 34,
            weight=ft.FontWeight.W_700,
            text_align=ft.TextAlign.CENTER,
        )
    ]
    if subtitle:
        items.append(
            label(
                subtitle,
                size=16 if large else 14,
                color=COLOR_MUTED,
                text_align=ft.TextAlign.CENTER,
            )
        )
    return ft.Column(items, spacing=6, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
