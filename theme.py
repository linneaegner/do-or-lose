"""Reusable Flet UI primitives for Förfest-spelet."""

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
    RADIUS_SM,
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


def screen(content: ft.Control, *, scroll: bool = True) -> ft.Container:
    return ft.Container(
        content=content,
        bgcolor=COLOR_BG,
        padding=ft.Padding.symmetric(horizontal=24, vertical=20),
        expand=True,
    )


def surface(
    *controls: ft.Control,
    padding: int = 16,
    expand: bool = False,
) -> ft.Container:
    return ft.Container(
        content=ft.Column(controls=controls, spacing=12, tight=True),
        bgcolor=COLOR_SURFACE,
        border=ft.Border.all(1, COLOR_BORDER),
        border_radius=RADIUS_MD,
        padding=padding,
        shadow=ft.BoxShadow(
            blur_radius=18,
            color=ft.Colors.with_opacity(0.08, COLOR_PRIMARY),
            offset=ft.Offset(0, 4),
        ),
        expand=expand,
    )


def primary_button(
    text: str,
    on_click,
    *,
    disabled: bool = False,
    width: int | None = None,
    icon: ft.Icon | None = None,
) -> ft.FilledButton:
    content: ft.Control = label(text, size=15, color=COLOR_ON_PRIMARY, weight=ft.FontWeight.W_600)
    if icon:
        content = ft.Row(
            [icon, label(text, size=15, color=COLOR_ON_PRIMARY, weight=ft.FontWeight.W_600)],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=8,
            tight=True,
        )
    return ft.FilledButton(
        content=content,
        on_click=on_click,
        disabled=disabled,
        width=width,
        style=ft.ButtonStyle(
            bgcolor={ft.ControlState.DEFAULT: COLOR_ACCENT, ft.ControlState.DISABLED: COLOR_HINT},
            shape=ft.RoundedRectangleBorder(radius=RADIUS_MD),
            padding=ft.Padding.symmetric(horizontal=20, vertical=16),
        ),
    )


def secondary_button(text: str, on_click, *, width: int | None = None) -> ft.OutlinedButton:
    return ft.OutlinedButton(
        content=text,
        on_click=on_click,
        width=width,
        style=ft.ButtonStyle(
            side={ft.ControlState.DEFAULT: ft.BorderSide(1.5, COLOR_ACCENT)},
            shape=ft.RoundedRectangleBorder(radius=RADIUS_MD),
            padding=ft.Padding.symmetric(horizontal=16, vertical=12),
        ),
    )


def name_field(hint: str = "Player name") -> ft.TextField:
    return ft.TextField(
        hint_text=hint,
        hint_style=ft.TextStyle(color=COLOR_HINT, size=14),
        border=ft.InputBorder.NONE,
        filled=True,
        bgcolor=COLOR_BG,
        border_radius=RADIUS_LG,
        content_padding=ft.Padding.symmetric(horizontal=18, vertical=14),
        text_style=ft.TextStyle(color=COLOR_PRIMARY, size=15, weight=ft.FontWeight.W_500),
        cursor_color=COLOR_ACCENT,
        autofocus=True,
    )


def player_chip(name: str) -> ft.Container:
    return ft.Container(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.PERSON_OUTLINE, size=16, color=COLOR_ACCENT),
                label(name, size=14, weight=ft.FontWeight.W_600),
            ],
            spacing=6,
            tight=True,
        ),
        bgcolor=COLOR_ACCENT_SOFT,
        border_radius=RADIUS_LG,
        padding=ft.Padding.symmetric(horizontal=14, vertical=8),
    )


def category_badge(category_key: str, emoji: str, label_text: str) -> ft.Container:
    from constants import COLOR_CATEGORY

    color = COLOR_CATEGORY.get(category_key, COLOR_ACCENT)
    return ft.Container(
        content=ft.Row(
            [
                label(emoji, size=14),
                label(label_text, size=12, color=color, weight=ft.FontWeight.W_700),
            ],
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
) -> ft.Container:
    content = label(
        text,
        size=20 if not placeholder else 18,
        color=COLOR_PRIMARY if not placeholder else COLOR_MUTED,
        weight=ft.FontWeight.W_600 if not placeholder else ft.FontWeight.W_500,
        text_align=ft.TextAlign.CENTER,
    )
    return ft.Container(
        content=content,
        width=320,
        height=300,
        border_radius=RADIUS_MD,
        bgcolor=COLOR_CARD_FACE,
        border=ft.Border.all(1, COLOR_BORDER),
        alignment=ft.Alignment.CENTER,
        padding=24,
        on_click=on_click,
        ink=on_click is not None,
    )


def icon_bar(*buttons: ft.IconButton) -> ft.Row:
    return ft.Row(
        controls=list(buttons),
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )


def page_header(title: str, subtitle: str | None = None) -> ft.Column:
    items = [
        label(title, size=34, weight=ft.FontWeight.W_700),
    ]
    if subtitle:
        items.append(label(subtitle, size=14, color=COLOR_MUTED))
    return ft.Column(items, spacing=6, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
