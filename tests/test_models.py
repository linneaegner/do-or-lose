from models import Person


def test_person_name() -> None:
    player = Person("Alex")
    assert player.get_name() == "Alex"


def test_person_points_and_win() -> None:
    player = Person("Alex")
    player.add_points(15)
    assert player.get_points() == 15
    assert not player.has_won(100)
    player.add_points(85)
    assert player.has_won(100)


def test_person_undo_points() -> None:
    player = Person("Alex", points=20)
    player.undo_points(5)
    assert player.get_points() == 15
