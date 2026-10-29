import pytest
from simplibs.text.logic.clean import remove_symbols


@pytest.mark.parametrize(
    "text, expected",
    [
        ("a+b=c", "abc"),
        ("$5 < 10", "5  10"),
        ("~|^`", ""),
        ("\u20ac10", "10"),
        ("\u00a9 2026", " 2026"),
        ("a\U0001f600b", "ab"),
        ("x \u2264 y", "x  y"),
    ],
    ids=["math", "currency-and-less", "ascii-symbols", "euro", "copyright", "emoji", "less-or-equal"],
)
def test_remove_symbols_removes_the_symbol_family(text, expected) -> None:
    """Math, currency, modifier and other symbols, emoji included."""
    assert remove_symbols(text) == expected


@pytest.mark.parametrize("text", ["a-b", "a_b", "Hello, world!", "(x)", "\u00abx\u00bb"])
def test_remove_symbols_punctuation_survives(text) -> None:
    """Punctuation is another family (`remove_punctuation`)."""
    assert remove_symbols(text) == text


def test_remove_symbols_the_joiners_of_a_compound_emoji_stay_behind() -> None:
    """The invisible zero-width joiners are not symbols themselves."""
    family = "\U0001f468\u200d\U0001f469\u200d\U0001f467"
    assert remove_symbols(f"a{family}b") == "a\u200d\u200db"


@pytest.mark.parametrize("text", ["abc 123", "", "a-b", "\u00e9\n"])
def test_remove_symbols_nothing_to_remove_gives_the_very_same_text(text) -> None:
    """The same object comes back."""
    probe = "".join(list(text))
    assert remove_symbols(probe) is probe


def test_remove_symbols_a_plus_survives_remove_punctuation_but_not_remove_symbols() -> None:
    """The two functions are a deliberate split."""
    from simplibs.text.logic.clean import remove_punctuation

    assert remove_punctuation("a+b") == "a+b"
    assert remove_symbols("a+b") == "ab"
