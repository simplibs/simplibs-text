import pytest
from simplibs.text.logic.case._helpers import starts_new_word


@pytest.mark.parametrize(
    "text, index, expected",
    [
        ("fooBar", 3, True),
        ("fooBar", 4, False),
        ("fooBar", 5, False),
        ("HTMLParser", 4, True),
        ("HTMLParser", 3, False),
        ("HTMLParser", 1, False),
        ("v2Beta", 2, True),
        ("utf8", 3, False),
        ("base64Encode", 6, True),
        ("ABC", 2, False),
        ("ABc", 1, True),
        ("Foo", 1, False),
    ],
)
def test_starts_new_word_decides_by_the_neighbours(text, index, expected) -> None:
    """A capital after a lowercase letter or digit, or the last capital of an acronym before lowercase."""
    assert starts_new_word(text, index) is expected


@pytest.mark.parametrize("text, index", [("a1", 1), ("ab", 1), ("1a", 1), ("a5b", 1)])
def test_starts_new_word_digits_and_lowercase_never_start_a_word(text, index) -> None:
    """Only a capital can."""
    assert starts_new_word(text, index) is False


def test_starts_new_word_looks_past_a_combining_mark_before() -> None:
    """`e` + an accent is still the lowercase `e`."""
    assert starts_new_word("cafe\u0301Bar", 5) is True


def test_starts_new_word_looks_past_a_combining_mark_after() -> None:
    """The acronym rule needs the letter after the capital, not its accent."""
    assert starts_new_word("HTMP\u0301arser", 3) is True
    assert starts_new_word("HTMP\u0301Arser", 3) is False
