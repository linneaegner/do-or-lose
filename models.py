from __future__ import annotations

from typing import Any


class Person:
    """A player in the turn-based game."""

    def __init__(self, name: str, current_card: Any = None, points: int = 0) -> None:
        self.name = name
        self.current_card = current_card
        self.points = points

    def __str__(self) -> str:
        return f"{self.name}: {self.points} poäng"

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str) -> None:
        self.name = name

    def get_current_card(self) -> Any:
        return self.current_card

    def set_current_card(self, new_card: Any) -> None:
        self.current_card = new_card

    def get_points(self) -> int:
        return self.points

    def add_points(self, num: int) -> None:
        self.points += num

    def undo_points(self, num: int) -> None:
        self.points -= num

    def has_won(self, max_points: int) -> bool:
        return self.points >= max_points
