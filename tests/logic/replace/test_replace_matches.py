import re
import pytest
from simplibs.exception import ParamError
from simplibs.regex import DIGIT, ONE_OR_MORE, RegexPattern
from simplibs.text.logic.replace import replace_matches


# ----------------------------------------------------------------------
# The four forms of a pattern
# ----------------------------------------------------------------------

def test_replace_matches_a_str_pattern_is_a_literal() -> None:
    """`a.b` is replaced where it stands, not "a, any character, b"."""
    assert replace_matches("a.b axb", "a.b", "X") == "X axb"


def test_replace_matches_a_compiled_pattern() -> None:
    """A `re.Pattern` is a regex."""
    assert replace_matches("a1b22", re.compile(r"\d+"), "#") == "a#b#"


def test_replace_matches_a_regex_tree() -> None:
    """A tree from simplibs-regex."""
    assert replace_matches("a1b22", ONE_OR_MORE(DIGIT), "#") == "a#b#"


def test_replace_matches_a_regex_pattern() -> None:
    """The compiled wrapper from simplibs-regex."""
    assert replace_matches("a1b22", RegexPattern(ONE_OR_MORE(DIGIT)), "#") == "a#b#"


# ----------------------------------------------------------------------
# A str replacement is literal
# ----------------------------------------------------------------------

@pytest.mark.parametrize("replacement", ["\\1", "\\g<0>", "\\n", "\\\\", "$1", "%s"])
def test_replace_matches_a_str_replacement_is_put_in_as_it_is(replacement) -> None:
    """No `\\1`, no `\\g<name>`, no escapes: what you write is what you get."""
    assert replace_matches("x", "x", replacement) == replacement


def test_replace_matches_an_empty_replacement_removes_the_match() -> None:
    """But the line stays, even when it is now empty (use `remove_matches` to drop it)."""
    assert replace_matches("a\nb\n", "a", "") == "\nb\n"


def test_replace_matches_a_replacement_may_hold_a_newline() -> None:
    """Any text is a replacement."""
    assert replace_matches("a,b", ",", "\n") == "a\nb"


# ----------------------------------------------------------------------
# A function as the replacement
# ----------------------------------------------------------------------

def test_replace_matches_a_function_gets_the_match() -> None:
    """Whatever it returns goes in."""
    assert replace_matches("a1b22", re.compile(r"\d+"), lambda match: f"<{match.group(0)}>") == "a<1>b<22>"


def test_replace_matches_a_function_can_use_groups() -> None:
    """The way to use a group: ask the match."""
    result = replace_matches("x=1 y=2", re.compile(r"(\w)=(\d)"), lambda match: f"{match.group(2)}={match.group(1)}")
    assert result == "1=x 2=y"


def test_replace_matches_a_function_is_called_for_every_match_in_order() -> None:
    """With the match positions as `re` reports them."""
    positions: list[int] = []

    def remember(match: re.Match) -> str:
        positions.append(match.start())
        return match.group(0)

    replace_matches("a1b22", re.compile(r"\d+"), remember)

    assert positions == [1, 3]


def test_replace_matches_a_function_may_return_the_empty_text() -> None:
    """Empty is a valid text."""
    assert replace_matches("a1b", re.compile(r"\d"), lambda match: "") == "ab"


@pytest.mark.parametrize("bad_result", [None, 5, ["x"], b"x"])
def test_replace_matches_a_function_returning_no_text_is_refused(bad_result) -> None:
    """The usual cause is a forgotten `return`."""
    with pytest.raises(ParamError):
        replace_matches("a1", re.compile(r"\d"), lambda match: bad_result)


def test_replace_matches_an_error_in_the_function_is_not_hidden() -> None:
    """Whatever the caller's function raises comes out unchanged."""
    def boom(match: re.Match) -> str:
        raise KeyError("boom")

    with pytest.raises(KeyError):
        replace_matches("a1", re.compile(r"\d"), boom)


# ----------------------------------------------------------------------
# Count and flags
# ----------------------------------------------------------------------

@pytest.mark.parametrize(
    "count, expected",
    [(0, "bbbb"), (1, "baaa"), (2, "bbaa"), (4, "bbbb"), (10, "bbbb")],
)
def test_replace_matches_count_limits_the_replacements_from_the_start(count, expected) -> None:
    """`0` means all of them."""
    assert replace_matches("aaaa", "a", "b", count=count) == expected


def test_replace_matches_flags_apply_to_a_str() -> None:
    """`re.IGNORECASE` finds every spelling."""
    assert replace_matches("Ab aB", "ab", "-", flags=re.IGNORECASE) == "- -"
    assert replace_matches("Ab aB", "ab", "-") == "Ab aB"


def test_replace_matches_flags_with_a_compiled_pattern_are_refused() -> None:
    """A compiled pattern has its flags; more would be ignored, so a card is raised."""
    with pytest.raises(ParamError):
        replace_matches("abc", re.compile("a"), "x", flags=re.IGNORECASE)


# ----------------------------------------------------------------------
# What does and does not match
# ----------------------------------------------------------------------

def test_replace_matches_nothing_matched_gives_the_very_same_text() -> None:
    """The same object comes back."""
    text = "".join(["a", "b", "c"])
    assert replace_matches(text, "x", "y") is text


def test_replace_matches_replacing_a_match_with_itself_gives_the_very_same_text() -> None:
    """Nothing changed, so the same object comes back."""
    text = "".join(["a", "b", "c"])
    assert replace_matches(text, "b", "b") is text


def test_replace_matches_an_empty_match_is_a_place_to_insert() -> None:
    """A pattern that matches nothing matches everywhere, and each of those places is replaced."""
    assert replace_matches("abc", re.compile("x*"), "-") == "-a-b-c-"


def test_replace_matches_a_prefix_on_every_line() -> None:
    """`^` in multiline mode also matches after the final newline, so a closed text gets one more prefix."""
    assert replace_matches("a\nb", re.compile("^", re.MULTILINE), "> ") == "> a\n> b"
    assert replace_matches("a\nb\n", re.compile("^", re.MULTILINE), "> ") == "> a\n> b\n> "


def test_replace_matches_works_with_a_nul_character_in_the_text() -> None:
    """Any character may be in the text."""
    assert replace_matches("a\x00b", "\x00", "-") == "a-b"


def test_replace_matches_works_with_non_ascii_text() -> None:
    """Any script."""
    assert replace_matches("čaj č", "č", "c") == "caj c"


def test_replace_matches_empty_text() -> None:
    """Nothing to replace in nothing."""
    assert replace_matches("", "a", "b") == ""
