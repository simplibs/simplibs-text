import re
import pytest
from simplibs.regex import DIGIT, NAMED_GROUP, Literal, RegexPattern
from simplibs.text.annotations._helpers import is_pattern


@pytest.mark.parametrize("value", ["a", " ", "  ", "a.b", "(", "\\d+", "\n", "příliš"])
def test_is_pattern_accepts_a_non_empty_text(value) -> None:
    """Any non-empty str is a literal to look for, whitespace and regex symbols included."""
    assert is_pattern(value) is True


def test_is_pattern_rejects_the_empty_text() -> None:
    """The empty literal matches between every two characters, so it is refused."""
    assert is_pattern("") is False


@pytest.mark.parametrize("source", ["a", "", "a|b", "[0-9]+"])
def test_is_pattern_accepts_a_compiled_pattern(source) -> None:
    """A compiled pattern is taken as it is, even one that can match nothing."""
    assert is_pattern(re.compile(source)) is True


def test_is_pattern_accepts_a_regex_tree() -> None:
    """A `Regex` tree from simplibs-regex is a pattern."""
    assert is_pattern(Literal("a") + DIGIT) is True


def test_is_pattern_accepts_a_regex_pattern() -> None:
    """The compiled wrapper from simplibs-regex is a pattern."""
    assert is_pattern(RegexPattern(Literal("a"))) is True


def test_is_pattern_accepts_a_lazy_regex_pattern_without_compiling_it() -> None:
    """The predicate only asks what the value IS; a tree that cannot compile does not raise here."""
    broken = NAMED_GROUP(DIGIT, "a") + NAMED_GROUP(DIGIT, "a")
    assert is_pattern(RegexPattern(broken, lazy=True)) is True


@pytest.mark.parametrize(
    "value",
    [None, 1, 1.5, True, b"a", ["a"], ("a",), {"a"}, {"a": 1}, object(), str],
)
def test_is_pattern_rejects_other_types_without_raising(value) -> None:
    """Anything that is not one of the four forms is rejected quietly."""
    assert is_pattern(value) is False
