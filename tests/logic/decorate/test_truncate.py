import pytest
from simplibs.exception import ParamError
from simplibs.text.logic.decorate import truncate

MARKER = "… (truncated)"


# ----------------------------------------------------------------------
# Lines
# ----------------------------------------------------------------------

def test_truncate_max_lines_keeps_the_first_lines_and_adds_the_marker() -> None:
    """The marker stands on its own line."""
    assert truncate("a\nb\nc\nd", max_lines=2) == f"a\nb\n{MARKER}"


def test_truncate_max_lines_one_keeps_only_the_first_line() -> None:
    """The smallest limit."""
    assert truncate("a\nb\nc", max_lines=1) == f"a\n{MARKER}"


@pytest.mark.parametrize("text, max_lines", [("a\nb\nc\nd", 4), ("a\nb\nc\nd", 10), ("a\nb\n", 2), ("a", 1)])
def test_truncate_a_text_that_fits_the_lines_is_returned_as_it_is(text, max_lines) -> None:
    """The same object comes back, no marker."""
    probe = "".join(list(text))
    assert truncate(probe, max_lines=max_lines) is probe


def test_truncate_a_blank_line_is_a_line() -> None:
    """Blank lines count against the limit and may end the kept part."""
    assert truncate("a\n\n\nb", max_lines=2) == f"a\n\n{MARKER}"


def test_truncate_lines_are_split_on_the_line_feed_only() -> None:
    """A carriage return is not a line break here."""
    text = "a\rb\rc"
    assert truncate(text, max_lines=1) is text


# ----------------------------------------------------------------------
# Characters
# ----------------------------------------------------------------------

def test_truncate_max_chars_cuts_even_in_the_middle_of_a_line() -> None:
    """The marker keeps the cut text tidy by standing on its own line."""
    assert truncate("abcdef", max_chars=3) == f"abc\n{MARKER}"


@pytest.mark.parametrize("text, max_chars", [("abc", 3), ("abc", 10), ("", 5)])
def test_truncate_a_text_that_fits_the_characters_is_returned_as_it_is(text, max_chars) -> None:
    """The same object comes back, no marker."""
    probe = "".join(list(text))
    assert truncate(probe, max_chars=max_chars) is probe


def test_truncate_the_marker_does_not_count_into_max_chars() -> None:
    """The text is cut at `max_chars`; the marker comes on top of that."""
    assert len(truncate("abcdef", max_chars=3)) > 3


def test_truncate_a_final_newline_counts_as_a_character() -> None:
    """A text of exactly `max_chars` characters plus its newline is cut by that newline and gets the marker."""
    assert truncate("abc\n", max_chars=3) == f"abc\n{MARKER}"


# ----------------------------------------------------------------------
# Both limits and the marker
# ----------------------------------------------------------------------

def test_truncate_lines_are_applied_first_and_then_characters() -> None:
    """`max_chars` counts what is left after `max_lines`."""
    assert truncate("aaaa\nbbbb\ncccc", max_lines=2, max_chars=6) == f"aaaa\nb\n{MARKER}"


def test_truncate_both_limits_met_returns_the_text_as_it_is() -> None:
    """Nothing cut, nothing added."""
    text = "".join(["ab", "\n", "cd"])
    assert truncate(text, max_lines=2, max_chars=5) is text


def test_truncate_a_custom_marker() -> None:
    """Any text, on its own line."""
    assert truncate("abcdef", max_chars=3, marker="[...]") == "abc\n[...]"


def test_truncate_an_empty_marker_cuts_without_a_trace() -> None:
    """No marker line at all."""
    assert truncate("abcdef", max_chars=3, marker="") == "abc"
    assert truncate("a\nb\nc", max_lines=2, marker="") == "a\nb"


# ----------------------------------------------------------------------
# A limit is required
# ----------------------------------------------------------------------

def test_truncate_without_a_limit_is_refused() -> None:
    """There is nothing to truncate to."""
    with pytest.raises(ParamError):
        truncate("abc")
