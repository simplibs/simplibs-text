import re
import pytest
from simplibs.exception import ParamError
from simplibs.regex import DIGIT, ONE_OR_MORE, RegexPattern
from simplibs.text.logic.remove import remove_matches


# ----------------------------------------------------------------------
# The four forms of a pattern
# ----------------------------------------------------------------------

def test_remove_matches_a_str_is_a_literal() -> None:
    """`a.b` removes `a.b`, and is not "a, any character, b"."""
    assert remove_matches("x a.b y", "a.b") == "x  y"
    assert remove_matches("x axb y", "a.b") == "x axb y"


def test_remove_matches_a_compiled_pattern() -> None:
    """A `re.Pattern` is a regex."""
    assert remove_matches("a1b22", re.compile(r"\d+")) == "ab"


def test_remove_matches_a_regex_tree() -> None:
    """A tree from simplibs-regex."""
    assert remove_matches("a1b22", ONE_OR_MORE(DIGIT)) == "ab"


def test_remove_matches_a_regex_pattern() -> None:
    """The compiled wrapper from simplibs-regex."""
    assert remove_matches("a1b22", RegexPattern(ONE_OR_MORE(DIGIT))) == "ab"


def test_remove_matches_regex_symbols_in_a_str_need_no_escaping() -> None:
    """Brackets and stars in a literal are just characters."""
    assert remove_matches("f(x) [y]*", "(x)") == "f [y]*"
    assert remove_matches("f(x) [y]*", "[y]*") == "f(x) "


# ----------------------------------------------------------------------
# Flags
# ----------------------------------------------------------------------

def test_remove_matches_flags_apply_to_a_str() -> None:
    """The whole text is one emptied line, so it disappears."""
    assert remove_matches("Abc abc", "abc", flags=re.IGNORECASE) == ""
    assert remove_matches("Abc abc", "abc", flags=re.IGNORECASE, drop_emptied_lines=False) == " "


def test_remove_matches_without_the_flag_the_case_matters() -> None:
    """Without `re.IGNORECASE` only the exact case matches."""
    assert remove_matches("Abc abc", "abc") == "Abc "


def test_remove_matches_flags_with_a_compiled_pattern_are_refused() -> None:
    """A compiled pattern has its flags; more would be ignored, so a card is raised."""
    with pytest.raises(ParamError):
        remove_matches("abc", re.compile("a"), flags=re.IGNORECASE)


def test_remove_matches_flags_with_a_regex_pattern_are_refused() -> None:
    """The same for the compiled wrapper."""
    with pytest.raises(ParamError):
        remove_matches("abc", RegexPattern(ONE_OR_MORE(DIGIT)), flags=re.IGNORECASE)


# ----------------------------------------------------------------------
# Lines
# ----------------------------------------------------------------------

def test_remove_matches_a_full_line_leaves_no_hole() -> None:
    """The line was emptied by the removal, so it goes."""
    assert remove_matches("code\n# TODO fix\nmore\n", "# TODO fix") == "code\nmore\n"


def test_remove_matches_can_keep_the_skeleton_of_lines() -> None:
    """`drop_emptied_lines=False` leaves the empty line."""
    result = remove_matches("code\n# TODO fix\nmore\n", "# TODO fix", drop_emptied_lines=False)
    assert result == "code\n\nmore\n"


def test_remove_matches_blank_lines_that_were_there_stay() -> None:
    """Only lines made blank by the removal go."""
    assert remove_matches("a\n\n# c\nb\n", "# c") == "a\n\nb\n"


def test_remove_matches_the_rest_of_a_line_stays() -> None:
    """A line with something left on it is shortened, not removed."""
    assert remove_matches("x = 1  # note\n# whole\ny\n", re.compile(r"#.*")) == "x = 1  \ny\n"


def test_remove_matches_a_match_over_several_lines() -> None:
    """A removal may span lines; what remains of the first and last line is joined."""
    block = re.compile(r"/\*.*?\*/", re.DOTALL)
    assert remove_matches("a /* x\ny */ b\n", block) == "a  b\n"
    assert remove_matches("/* x\ny */\nb\n", block) == "b\n"


@pytest.mark.parametrize(
    "text, expected",
    [("abc", ""), ("abc\n", ""), ("x\nabc", "x"), ("x\nabc\n", "x\n")],
)
def test_remove_matches_the_end_of_the_text(text, expected) -> None:
    """The final newline stays when the last line stays."""
    assert remove_matches(text, "abc") == expected


# ----------------------------------------------------------------------
# What does and does not match
# ----------------------------------------------------------------------

def test_remove_matches_nothing_matched_gives_the_very_same_text() -> None:
    """The same object comes back."""
    text = "".join(["a", "b", "c"])
    assert remove_matches(text, "x") is text


def test_remove_matches_matches_do_not_overlap() -> None:
    """Matches are found left to right, as `re` does."""
    assert remove_matches("xaaay", "aa") == "xay"


def test_remove_matches_empty_matches_remove_nothing_and_flag_nothing() -> None:
    """`x*` and `^` match the empty string everywhere; the text, blank lines included, is unchanged."""
    text = "a\n\nb"
    assert remove_matches(text, re.compile("x*")) is text
    assert remove_matches(text, re.compile("^", re.MULTILINE)) is text


def test_remove_matches_works_with_a_nul_character_in_the_text() -> None:
    """No reserved character: NUL in the text is an ordinary character."""
    assert remove_matches("a\x00b\x00", "b") == "a\x00\x00"


def test_remove_matches_works_with_non_ascii_text() -> None:
    """Any script."""
    assert remove_matches("čaj žluťoučký", "č") == "aj žluťouký"


def test_remove_matches_empty_text() -> None:
    """Nothing to remove from nothing."""
    assert remove_matches("", "a") == ""
