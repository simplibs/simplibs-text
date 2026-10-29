import pytest
from simplibs.text.logic.clean import remove_punctuation, replace_punctuation


@pytest.mark.parametrize(
    "text, expected",
    [("a,b.c", "a b c"), ("a-b_c", "a b c"), ("(x)", " x "), ("\u201cq\u201d", " q ")],
)
def test_replace_punctuation_default_is_a_space(text, expected) -> None:
    """Every punctuation character becomes one space."""
    assert replace_punctuation(text) == expected


@pytest.mark.parametrize(
    "replacement, expected",
    [("", "ab"), ("_", "a_b"), ("--", "a--b"), ("\\1", "a\\1b"), ("\n", "a\nb")],
)
def test_replace_punctuation_the_replacement_is_used_literally(replacement, expected) -> None:
    """Whatever it is, including an empty text."""
    assert replace_punctuation("a,b", replacement) == expected


@pytest.mark.parametrize("text", ["", "a b", "a,b", "a-b\nc.", "x(y)z", "\u00abq\u00bb!"])
def test_replace_punctuation_with_an_empty_replacement_equals_remove_punctuation(text) -> None:
    """The two functions never disagree."""
    assert replace_punctuation(text, "") == remove_punctuation(text)


@pytest.mark.parametrize("text", ["a+b", "$5", "a b", ""])
def test_replace_punctuation_nothing_to_replace_gives_the_very_same_text(text) -> None:
    """The same object comes back."""
    probe = "".join(list(text))
    assert replace_punctuation(probe) is probe
