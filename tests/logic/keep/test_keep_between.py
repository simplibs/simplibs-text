import re
import pytest
from simplibs.exception import ParamError
from simplibs.regex import Literal, RegexPattern
from simplibs.text.logic.keep import keep_between


# ----------------------------------------------------------------------
# The basic use
# ----------------------------------------------------------------------

def test_keep_between_keeps_the_markers_by_default() -> None:
    """Each part from the start marker to the end marker, markers included."""
    assert keep_between("[a] x [b] y", "[", "]") == "[a]\n[b]"


def test_keep_between_can_leave_the_markers_out() -> None:
    """Only what stands between them."""
    assert keep_between("[a] x [b] y", "[", "]", include_markers=False) == "a\nb"


def test_keep_between_a_start_without_an_end_is_ignored() -> None:
    """The unfinished part at the end of the text is not kept."""
    assert keep_between("[a] x [b", "[", "]") == "[a]"
    assert keep_between("[a", "[", "]") == ""


def test_keep_between_an_end_before_the_start_is_not_a_part() -> None:
    """The end marker is looked for AFTER the start marker."""
    assert keep_between("] a [", "[", "]") == ""


@pytest.mark.parametrize("text", ["", "abc", "no markers here"])
def test_keep_between_no_markers_give_an_empty_text(text) -> None:
    """Nothing to keep."""
    assert keep_between(text, "[", "]") == ""


@pytest.mark.parametrize("separator, expected", [("\n", "[a]\n[b]"), ("|", "[a]|[b]"), ("", "[a][b]")])
def test_keep_between_joins_the_parts_with_the_separator(separator, expected) -> None:
    """The default newline keeps the parts apart."""
    assert keep_between("[a] x [b]", "[", "]", separator=separator) == expected


def test_keep_between_an_empty_part_is_still_a_part() -> None:
    """`[]` between the markers keeps the empty text, and the separator shows it."""
    assert keep_between("[][]", "[", "]", include_markers=False, separator="|") == "|"


# ----------------------------------------------------------------------
# Nesting and equal markers
# ----------------------------------------------------------------------

def test_keep_between_does_not_nest() -> None:
    """The first end marker closes the part, whatever was opened inside it."""
    assert keep_between("[a[b]c]", "[", "]") == "[a[b]"


def test_keep_between_the_same_marker_opens_and_closes() -> None:
    """With one marker, the parts are the pairs."""
    assert keep_between("xAyAz", "A", "A") == "AyA"
    assert keep_between("xAyAz", "A", "A", include_markers=False) == "y"
    assert keep_between("AaAbA", "A", "A") == "AaA"


# ----------------------------------------------------------------------
# The four forms of a marker, and flags
# ----------------------------------------------------------------------

def test_keep_between_markers_may_be_regex_patterns() -> None:
    """A compiled pattern for each marker."""
    result = keep_between("a<b>c<d>e", re.compile("<"), re.compile(">"), include_markers=False)
    assert result == "b\nd"


def test_keep_between_markers_may_be_a_regex_tree_and_a_regex_pattern() -> None:
    """The other two forms."""
    assert keep_between("a<b>c", Literal("<"), RegexPattern(Literal(">")), include_markers=False) == "b"


def test_keep_between_flags_apply_to_both_markers() -> None:
    """`re.IGNORECASE` finds `<A` and `>` alike."""
    assert keep_between("x <A> y", "<a", ">", flags=re.IGNORECASE) == "<A>"


@pytest.mark.parametrize("which", ["start", "end"])
def test_keep_between_flags_with_a_compiled_marker_are_refused(which) -> None:
    """A compiled pattern has its flags; more would be ignored, so a card is raised."""
    markers = {"start": "[", "end": "]"}
    markers[which] = re.compile(re.escape(markers[which]), re.IGNORECASE)
    with pytest.raises(ParamError):
        keep_between("[a]", markers["start"], markers["end"], flags=re.IGNORECASE)


def test_keep_between_the_end_marker_sees_the_text_before_the_start() -> None:
    """A lookbehind in a marker looks at the whole text, not at the part from the search position."""
    end = re.compile(r"(?<=x)\]")
    assert keep_between("[a] [bx]", "[", end) == "[a] [bx]"


# ----------------------------------------------------------------------
# Markers that can match nothing
# ----------------------------------------------------------------------

def test_keep_between_empty_markers_per_line() -> None:
    """`^` and `$` in multiline mode keep the lines, and the search moves on."""
    result = keep_between("a\nb", re.compile("^", re.MULTILINE), re.compile("$", re.MULTILINE))
    assert result == "a\nb"


def test_keep_between_markers_that_match_nothing_always_finish() -> None:
    """Two empty markers give empty parts, but never an endless loop."""
    assert isinstance(keep_between("abc", re.compile(""), re.compile("")), str)
