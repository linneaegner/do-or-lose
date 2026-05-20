from questions import QUESTIONS, Category, QuestionDeck


def test_has_one_hundred_questions() -> None:
    assert len(QUESTIONS) == 100
    ids = {q.id for q in QUESTIONS}
    assert ids == set(range(1, 101))


def test_deck_respects_category_filter() -> None:
    deck = QuestionDeck({Category.TRUTH, Category.DRINK})
    assert deck.total == 40
    drawn = {deck.draw().category for _ in range(40)}
    assert drawn <= {Category.TRUTH, Category.DRINK}


def test_deck_reshuffles_when_empty() -> None:
    deck = QuestionDeck({Category.WILD})
    first_round = [deck.draw().id for _ in range(deck.total)]
    second_round = [deck.draw().id for _ in range(deck.total)]
    assert len(first_round) == 17
    assert len(second_round) == 17
