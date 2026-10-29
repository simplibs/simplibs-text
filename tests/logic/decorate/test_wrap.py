import random
import pytest
from simplibs.text.logic.decorate import wrap


# ----------------------------------------------------------------------
# What is wrapped and what is not
# ----------------------------------------------------------------------

def test_wrap_a_line_that_fits_is_not_touched() -> None:
    """Short lines come back as the same text."""
    text = "".join(["short\n", "lines\n"])
    assert wrap(text, 80) is text


def test_wrap_a_line_exactly_as_long_as_the_width_fits() -> None:
    """The width is the longest allowed line."""
    assert wrap("abcdefg", 7) == "abcdefg"
    assert wrap("abc def", 7) == "abc def"


def test_wrap_breaks_a_long_line_between_words() -> None:
    """Words are never cut, the line is."""
    assert wrap("aaa bbb ccc ddd", 7) == "aaa bbb\nccc ddd"


def test_wrap_every_line_is_wrapped_on_its_own() -> None:
    """Existing newlines stay; short lines are not joined."""
    assert wrap("aaaa bbbb\ncc", 5) == "aaaa\nbbbb\ncc"


@pytest.mark.parametrize("text, expected", [("aaa bbb\n", "aaa\nbbb\n"), ("aaa bbb", "aaa\nbbb")])
def test_wrap_keeps_the_final_newline_status(text, expected) -> None:
    """The text ends with a newline exactly when it did before."""
    assert wrap(text, 5) == expected


def test_wrap_a_blank_line_is_never_touched() -> None:
    """Even a long one made of spaces."""
    text = "a\n" + " " * 100 + "\nb"
    assert wrap(text, 10) == text


def test_wrap_the_default_width_is_eighty() -> None:
    """A line of 80 fits, one of 81 does not."""
    fits = "abcd " * 15 + "abcde"
    too_long = "abcd " * 15 + "abcdef"
    assert (len(fits), len(too_long)) == (80, 81)
    assert wrap(fits) == fits
    assert wrap(too_long) == "abcd " * 14 + "abcd\nabcdef"


def test_wrap_empty_text() -> None:
    """Nothing to wrap."""
    assert wrap("", 10) == ""


# ----------------------------------------------------------------------
# Indentation
# ----------------------------------------------------------------------

def test_wrap_the_continuation_lines_keep_the_indentation() -> None:
    """All lines of the wrapped line start at the same column."""
    assert wrap("    aaa bbb ccc", 10) == "    aaa\n    bbb\n    ccc"


def test_wrap_a_tab_indentation_is_kept_as_it_is() -> None:
    """Tabs are not expanded to spaces."""
    assert wrap("\taaa bbb ccc", 8) == "\taaa bbb\n\tccc"


# ----------------------------------------------------------------------
# Long words and hyphens
# ----------------------------------------------------------------------

def test_wrap_does_not_break_on_hyphens() -> None:
    """`kebab-case-name` is one identifier."""
    assert wrap("kebab-case-name x", 10) == "kebab-case-name\nx"


def test_wrap_a_word_longer_than_the_width_stays_whole() -> None:
    """Better an overflow than a broken link."""
    assert wrap("see http://example.com/long/path ok", 10) == "see\nhttp://example.com/long/path\nok"


def test_wrap_can_break_long_words_on_request() -> None:
    """`break_long_words=True` cuts the word at the width."""
    assert wrap("abcdefghij", 4, break_long_words=True) == "abcd\nefgh\nij"


def test_wrap_an_indentation_wider_than_the_width_does_not_fail() -> None:
    """Every word then gets its own line."""
    assert wrap("      word word", 4) == "      word\n      word"


def test_wrap_the_trailing_spaces_of_a_wrapped_line_are_lost() -> None:
    """Only a line that is too long is rebuilt; this is the price."""
    assert wrap("aaa bbb   ", 5) == "aaa\nbbb"


# ----------------------------------------------------------------------
# Properties
# ----------------------------------------------------------------------

@pytest.mark.parametrize("break_long_words", [False, True])
def test_wrap_random_lines_keep_their_words_fit_the_width_and_wrap_only_once(break_long_words) -> None:
    """For random texts: no word lost, no line too long (unless one long word), and a second wrap changes nothing."""
    rng = random.Random(2)
    words = ["ab", "kebab-case-name", "x" * 30, "c", "dd", "eee", "http://example.com/" + "a" * 40]
    for _ in range(300):
        width = rng.randint(5, 30)
        lead = rng.choice(["", "  ", "    ", "\t"])
        line = lead + " ".join(rng.choice(words) for _ in range(rng.randint(1, 12)))
        text = "\n".join([line, "", "short"]) + rng.choice(["", "\n"])

        result = wrap(text, width, break_long_words=break_long_words)

        if break_long_words:
            assert "".join(result.split()) == "".join(text.split())
        else:
            assert result.split() == text.split()
            for wrapped_line in result.split("\n"):
                assert len(wrapped_line) <= width or len(wrapped_line.split()) <= 1
        assert wrap(result, width, break_long_words=break_long_words) == result
