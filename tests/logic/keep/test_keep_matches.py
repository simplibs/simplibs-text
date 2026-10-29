import re
import pytest
from simplibs.exception import ParamError
from simplibs.regex import DIGIT, ONE_OR_MORE, RegexPattern
from simplibs.text.logic.keep import keep_matches


# ----------------------------------------------------------------------
# The four forms of a pattern
# ----------------------------------------------------------------------

def test_keep_matches_a_str_is_a_literal() -> None:
    """`a.b` is kept where it stands, not "a, any character, b"."""
    assert keep_matches("a.b axb a.b", "a.b") == "a.b\na.b"


def test_keep_matches_a_compiled_pattern() -> None:
    """A `re.Pattern` is a regex."""
    assert keep_matches("a1b22c333", re.compile(r"\d+")) == "1\n22\n333"


def test_keep_matches_a_regex_tree() -> None:
    """A tree from simplibs-regex."""
    assert keep_matches("a1b22c333", ONE_OR_MORE(DIGIT)) == "1\n22\n333"


def test_keep_matches_a_regex_pattern() -> None:
    """The compiled wrapper from simplibs-regex."""
    assert keep_matches("a1b22c333", RegexPattern(ONE_OR_MORE(DIGIT))) == "1\n22\n333"


# ----------------------------------------------------------------------
# Separator and flags
# ----------------------------------------------------------------------

@pytest.mark.parametrize(
    "separator, expected",
    [("\n", "1\n22\n333"), (",", "1,22,333"), (" | ", "1 | 22 | 333"), ("", "122333")],
)
def test_keep_matches_joins_the_matches_with_the_separator(separator, expected) -> None:
    """The default newline keeps the matches apart; any other text will do."""
    assert keep_matches("a1b22c333", re.compile(r"\d+"), separator=separator) == expected


def test_keep_matches_flags_apply_to_a_str() -> None:
    """`re.IGNORECASE` finds every spelling."""
    assert keep_matches("Ab aB ab", "ab", flags=re.IGNORECASE) == "Ab\naB\nab"
    assert keep_matches("Ab aB ab", "ab") == "ab"


def test_keep_matches_flags_with_a_compiled_pattern_are_refused() -> None:
    """A compiled pattern has its flags; more would be ignored, so a card is raised."""
    with pytest.raises(ParamError):
        keep_matches("abc", re.compile("a"), flags=re.IGNORECASE)


# ----------------------------------------------------------------------
# What does and does not match
# ----------------------------------------------------------------------

@pytest.mark.parametrize("text", ["", "abc", "123"])
def test_keep_matches_nothing_matched_gives_an_empty_text(text) -> None:
    """No match, nothing to keep."""
    assert keep_matches(text, "x") == ""


def test_keep_matches_empty_matches_carry_nothing() -> None:
    """A pattern that matches the empty string everywhere keeps nothing."""
    assert keep_matches("abc", re.compile("x*")) == ""


def test_keep_matches_matches_do_not_overlap() -> None:
    """Matches are found left to right, as `re` does."""
    assert keep_matches("aaaa", "aa") == "aa\naa"
    assert keep_matches("aaaaa", "aa") == "aa\naa"


def test_keep_matches_a_match_may_span_lines() -> None:
    """The text is searched as a whole, so a match can include a newline."""
    assert keep_matches("xa\nby", re.compile(r"a\nb")) == "a\nb"


def test_keep_matches_works_with_non_ascii_text() -> None:
    """Any script."""
    assert keep_matches("čaj č", "č") == "č\nč"
