from questions import QUESTIONS, Category, QuestionDeck


def test_has_one_hundred_fifty_one_questions() -> None:
    assert len(QUESTIONS) == 151
    ids = {q.id for q in QUESTIONS}
    assert ids == set(range(1, 152))


def test_deck_respects_category_filter() -> None:
    deck = QuestionDeck({Category.TRUTH, Category.DRINK})
    assert deck.total == 60
    drawn = {deck.draw().category for _ in range(60)}
    assert drawn <= {Category.TRUTH, Category.DRINK}


def test_deck_reshuffles_when_empty() -> None:
    deck = QuestionDeck({Category.WILD})
    first_round = [deck.draw().id for _ in range(deck.total)]
    second_round = [deck.draw().id for _ in range(deck.total)]
    assert len(first_round) == 27
    assert len(second_round) == 27
