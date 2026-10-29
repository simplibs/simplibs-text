import pytest
from simplibs.text.logic.remove import remove_empty_lines, squeeze_blank_lines


@pytest.mark.parametrize(
    "text, expected",
    [
        ("a\n\n\n\nb\n", "a\n\nb\n"),
        ("a\n\nb\n", "a\n\nb\n"),
        ("a\n\n\nb\n\n\nc", "a\n\nb\n\nc"),
        ("\n\n\na", "\na"),
        ("a\n\n\n", "a\n\n"),
    ],
    ids=["run", "single-stays", "each-run-alone", "at-start", "at-end"],
)
def test_squeeze_blank_lines_default_keeps_one_blank_line_per_run(text, expected) -> None:
    """The default `max_consecutive=1`: paragraphs stay apart, gaps shrink."""
    assert squeeze_blank_lines(text) == expected


@pytest.mark.parametrize(
    "max_consecutive, expected",
    [(0, "a\nb"), (1, "a\n\nb"), (2, "a\n\n\nb"), (3, "a\n\n\n\nb"), (4, "a\n\n\n\n\nb")],
)
def test_squeeze_blank_lines_max_consecutive(max_consecutive, expected) -> None:
    """At most that many blank lines in a row stay."""
    assert squeeze_blank_lines("a\n\n\n\n\nb", max_consecutive) == expected


@pytest.mark.parametrize(
    "text",
    ["", "a", "\n", "a\n\nb\n", "\n\n a \n \n\n", "x\n\n\n\ny\n\n"],
)
def test_squeeze_blank_lines_zero_equals_remove_empty_lines(text) -> None:
    """The two functions never disagree."""
    assert squeeze_blank_lines(text, 0) == remove_empty_lines(text)


def test_squeeze_blank_lines_a_whitespace_only_line_counts_as_blank() -> None:
    """The first blank line of a run stays, whatever it holds."""
    assert squeeze_blank_lines("a\n \n\t\n\nb\n") == "a\n \nb\n"


def test_squeeze_blank_lines_nothing_to_shorten_gives_the_very_same_text() -> None:
    """The same object comes back."""
    text = "".join(["a", "\n", "\n", "b"])
    assert squeeze_blank_lines(text) is text
    assert squeeze_blank_lines(text, 5) is text


@pytest.mark.parametrize("text", ["a\n\n\n\nb", "\n\n\n", " \n \n \n", "a\n\n\n"])
@pytest.mark.parametrize("max_consecutive", [0, 1, 2])
def test_squeeze_blank_lines_is_idempotent(text, max_consecutive) -> None:
    """Running it twice gives the same result."""
    once = squeeze_blank_lines(text, max_consecutive)
    assert squeeze_blank_lines(once, max_consecutive) == once
