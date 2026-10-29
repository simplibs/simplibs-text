import re
import pytest
from simplibs.exception import ParamError
from simplibs.regex import Literal, RegexPattern
from simplibs.text.logic.remove import remove_lines_matching


def test_remove_lines_matching_removes_the_whole_line() -> None:
    """The match may be only a part of the line."""
    assert remove_lines_matching("a\nx TODO y\nb\n", "TODO") == "a\nb\n"


@pytest.mark.parametrize(
    "text, expected",
    [("a\nTODO", "a"), ("a\nTODO\n", "a\n"), ("TODO\na", "a"), ("TODO\n", ""), ("TODO", "")],
)
def test_remove_lines_matching_keeps_the_final_newline_when_the_last_line_stays(text, expected) -> None:
    """The text ends with a newline only if it did, and only if there is a line left."""
    assert remove_lines_matching(text, "TODO") == expected


def test_remove_lines_matching_a_str_is_a_literal() -> None:
    """`a.b` does not match `axb`."""
    assert remove_lines_matching("a.b\naxb\n", "a.b") == "axb\n"


def test_remove_lines_matching_a_compiled_pattern_works_line_by_line() -> None:
    """`^` is the start of each line, without `re.MULTILINE`."""
    assert remove_lines_matching("# a\nb # c\n#d\n", re.compile("^#")) == "b # c\n"


def test_remove_lines_matching_a_regex_tree_and_a_regex_pattern() -> None:
    """The other two forms of a pattern."""
    assert remove_lines_matching("a\nb\n", Literal("a")) == "b\n"
    assert remove_lines_matching("a\nb\n", RegexPattern(Literal("b"))) == "a\n"


def test_remove_lines_matching_flags_apply_to_a_str() -> None:
    """`re.IGNORECASE` finds `Todo`."""
    assert remove_lines_matching("a\nTodo\n", "todo", flags=re.IGNORECASE) == "a\n"


def test_remove_lines_matching_flags_with_a_compiled_pattern_are_refused() -> None:
    """A compiled pattern has its flags."""
    with pytest.raises(ParamError):
        remove_lines_matching("a", re.compile("a"), flags=re.IGNORECASE)


def test_remove_lines_matching_a_match_cannot_span_lines() -> None:
    """The pattern is searched in each line separately."""
    text = "a\nb\n"
    assert remove_lines_matching(text, re.compile("a\nb")) is text


def test_remove_lines_matching_an_empty_line_can_match() -> None:
    """`^$` is an empty line."""
    assert remove_lines_matching("a\n\nb\n", re.compile("^$")) == "a\nb\n"


def test_remove_lines_matching_nothing_matched_gives_the_very_same_text() -> None:
    """The same object comes back."""
    text = "".join(["a", "\n", "b"])
    assert remove_lines_matching(text, "x") is text


def test_remove_lines_matching_every_line_removed_gives_an_empty_text() -> None:
    """No lines left, no text."""
    assert remove_lines_matching("a\na\n", "a") == ""


def test_remove_lines_matching_empty_text() -> None:
    """Nothing to remove from nothing."""
    assert remove_lines_matching("", "a") == ""
