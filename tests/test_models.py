from models import Person


def test_person_name() -> None:
    player = Person("Alex")
    assert player.get_name() == "Alex"
