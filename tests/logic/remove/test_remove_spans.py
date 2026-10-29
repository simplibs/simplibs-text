import re
import pytest
from simplibs.exception import ParamError
from simplibs.text.logic.remove import remove_matches, remove_spans


@pytest.mark.parametrize(
    "text, spans, expected",
    [
        ("abc def", [(3, 7)], "abc"),
        ("a1b2c", [(1, 2), (3, 4)], "abc"),
        ("a1b2c", [(3, 4), (1, 2)], "abc"),
        ("abcdef", [(0, 4), (2, 5)], "f"),
        ("abcdef", [(0, 3), (3, 6)], ""),
        ("abc", [(0, 3)], ""),
    ],
    ids=["one", "two", "unordered", "overlapping", "touching", "everything"],
)
def test_remove_spans_cuts_the_given_ranges(text, spans, expected) -> None:
    """Half-open `(start, end)` ranges in any order; overlapping and touching ones act as one."""
    assert remove_spans(text, spans) == expected


@pytest.mark.parametrize("spans", [[], (), [(2, 2)], [(0, 0), (3, 3)]])
def test_remove_spans_nothing_to_remove_gives_the_very_same_text(spans) -> None:
    """No spans, or only empty ones, return the same object."""
    text = "".join(["a", "\n", "\n", "b"])
    assert remove_spans(text, spans) is text


def test_remove_spans_accepts_a_tuple_of_tuples() -> None:
    """Any sequence of pairs will do."""
    assert remove_spans("abcdef", ((1, 2), (4, 5))) == "acdf"


def test_remove_spans_drops_emptied_lines_by_default() -> None:
    """A full-line removal leaves no hole."""
    assert remove_spans("a\n# note\nb\n", [(2, 8)]) == "a\nb\n"


def test_remove_spans_can_keep_the_emptied_lines() -> None:
    """`drop_emptied_lines=False` keeps the skeleton of the lines."""
    assert remove_spans("a\n# note\nb\n", [(2, 8)], drop_emptied_lines=False) == "a\n\nb\n"


def test_remove_spans_keeps_blank_lines_that_were_there_before() -> None:
    """Only a removal can make a line disappear."""
    assert remove_spans("a\n\nb xyz\n", [(5, 8)]) == "a\n\nb \n"


def test_remove_spans_an_empty_span_does_not_flag_a_line() -> None:
    """A zero-length span removes nothing, so no blank line is dropped because of it."""
    text = "a\n\nb"
    assert remove_spans(text, [(2, 2)]) == text


@pytest.mark.parametrize(
    "span",
    [(-1, 2), (3, 2), (0, 8), (8, 9)],
    ids=["negative", "backwards", "past-end", "start-past-end"],
)
def test_remove_spans_rejects_a_span_that_does_not_fit(span) -> None:
    """Refused with a card; nothing is cut with a range measured on another text."""
    with pytest.raises(ParamError):
        remove_spans("abcdefg", [span])


def test_remove_spans_rejects_one_bad_span_among_good_ones() -> None:
    """Nothing is cut when any span is wrong."""
    with pytest.raises(ParamError):
        remove_spans("abcdefg", [(0, 1), (2, 99)])


def test_remove_spans_empty_text() -> None:
    """The empty text has no room for a non-empty span, and an empty one is harmless."""
    assert remove_spans("", []) == ""
    assert remove_spans("", [(0, 0)]) == ""


def test_remove_spans_works_with_a_nul_character_in_the_text() -> None:
    """Any character may be in the text."""
    assert remove_spans("a\x00\x00b", [(1, 2)]) == "a\x00b"


@pytest.mark.parametrize(
    "text, pattern",
    [
        ("a1b22c\n", r"\d+"),
        ("x # c\ny\n# d\nz\n", r"#.*"),
        ("aaa\n\nbbb", r"a+"),
    ],
)
def test_remove_spans_with_match_spans_equals_remove_matches(text, pattern) -> None:
    """The spans of a regex handed to `remove_spans` give what `remove_matches` gives."""
    compiled = re.compile(pattern)
    spans = [match.span() for match in compiled.finditer(text)]
    assert remove_spans(text, spans) == remove_matches(text, compiled)
