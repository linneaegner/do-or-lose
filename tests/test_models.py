import pytest

from constants import MAX_POINTS, POINTS_PER_SUCCESS
from models import Person


def test_person_starts_with_zero_points() -> None:
    player = Person("Alex")
    assert player.get_name() == "Alex"
    assert player.get_points() == 0


def test_add_and_undo_points() -> None:
    player = Person("Alex")
    player.add_points(POINTS_PER_SUCCESS)
    assert player.get_points() == POINTS_PER_SUCCESS
    player.undo_points(POINTS_PER_SUCCESS)
    assert player.get_points() == 0


def test_has_won_at_max_points() -> None:
    player = Person("Alex", points=MAX_POINTS - POINTS_PER_SUCCESS)
    player.add_points(POINTS_PER_SUCCESS)
    assert player.has_won(MAX_POINTS)


def test_has_not_won_below_max_points() -> None:
    player = Person("Alex", points=30)
    assert not player.has_won(MAX_POINTS)
