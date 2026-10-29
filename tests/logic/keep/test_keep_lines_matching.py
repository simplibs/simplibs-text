import re
import pytest
from simplibs.exception import ParamError
from simplibs.regex import Literal, RegexPattern
from simplibs.text.logic.keep import keep_lines_matching
from simplibs.text.logic.remove import remove_lines_matching
from simplibs.text.logic._common.helpers import split_lines


def test_keep_lines_matching_keeps_the_whole_line() -> None:
    """The match may be only a part of the line."""
    assert keep_lines_matching("a\nx TODO y\nb\n", "TODO") == "x TODO y\n"


@pytest.mark.parametrize(
    "text, expected",
    [("a\nTODO", "TODO"), ("a\nTODO\n", "TODO\n"), ("TODO\na", "TODO"), ("TODO\na\n", "TODO\n")],
)
def test_keep_lines_matching_keeps_the_final_newline_status(text, expected) -> None:
    """The text ends with a newline exactly when it did before."""
    assert keep_lines_matching(text, "TODO") == expected


def test_keep_lines_matching_a_str_is_a_literal() -> None:
    """`a.b` does not match `axb`."""
    assert keep_lines_matching("a.b\naxb\n", "a.b") == "a.b\n"


def test_keep_lines_matching_a_compiled_pattern_works_line_by_line() -> None:
    """`^` is the start of each line, without `re.MULTILINE`."""
    assert keep_lines_matching("# a\nb # c\n#d\n", re.compile("^#")) == "# a\n#d\n"


def test_keep_lines_matching_a_regex_tree_and_a_regex_pattern() -> None:
    """The other two forms of a pattern."""
    assert keep_lines_matching("a\nb\n", Literal("a")) == "a\n"
    assert keep_lines_matching("a\nb\n", RegexPattern(Literal("b"))) == "b\n"


def test_keep_lines_matching_flags_apply_to_a_str() -> None:
    """`re.IGNORECASE` finds `Todo`."""
    assert keep_lines_matching("a\nTodo\n", "todo", flags=re.IGNORECASE) == "Todo\n"


def test_keep_lines_matching_flags_with_a_compiled_pattern_are_refused() -> None:
    """A compiled pattern has its flags."""
    with pytest.raises(ParamError):
        keep_lines_matching("a", re.compile("a"), flags=re.IGNORECASE)


def test_keep_lines_matching_a_match_cannot_span_lines() -> None:
    """The pattern is searched in each line separately."""
    assert keep_lines_matching("a\nb\n", re.compile("a\nb")) == ""


def test_keep_lines_matching_an_empty_line_can_match() -> None:
    """`^$` is an empty line."""
    assert keep_lines_matching("a\n\nb\n", re.compile("^$")) == "\n"


def test_keep_lines_matching_every_line_kept_gives_the_very_same_text() -> None:
    """The same object comes back."""
    text = "".join(["a", "\n", "a"])
    assert keep_lines_matching(text, "a") is text


@pytest.mark.parametrize("text", ["", "abc", "a\nb\n"])
def test_keep_lines_matching_no_line_matching_gives_an_empty_text(text) -> None:
    """Nothing is kept."""
    assert keep_lines_matching(text, "x") == ""


@pytest.mark.parametrize("text", ["a\nab\nb\n", "ab\nab", "x\ny\n", "\n\nab\n"])
def test_keep_lines_matching_and_remove_lines_matching_split_the_lines(text) -> None:
    """Every line goes to exactly one of the two."""
    kept, _ = split_lines(keep_lines_matching(text, "a"))
    removed, _ = split_lines(remove_lines_matching(text, "a"))
    assert len(kept) + len(removed) == len(split_lines(text)[0])
