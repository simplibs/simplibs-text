import re
import pytest
from simplibs.exception.testing import assert_exception_function
from simplibs.exception import ParamError, ValidationError
from simplibs.regex import DIGIT, NAMED_GROUP, Flag, Literal, RegexPattern
from simplibs.text.logic._common.helpers import compile_pattern


# ----------------------------------------------------------------------
# str — a literal
# ----------------------------------------------------------------------

def test_compile_pattern_returns_a_compiled_pattern_for_a_str() -> None:
    """Whatever comes in, a `re.Pattern` goes out."""
    assert isinstance(compile_pattern("abc"), re.Pattern)


@pytest.mark.parametrize("text", ["a.b", "(", "[", "a+b", "\\d", "^", "$", "a|b", "*"])
def test_compile_pattern_a_str_is_a_literal(text) -> None:
    """Regex symbols in a str mean themselves, so nothing needs escaping."""
    compiled = compile_pattern(text)
    assert compiled.search(f"x{text}y").group(0) == text


def test_compile_pattern_a_str_does_not_match_as_a_regex() -> None:
    """`a.b` is not "a, any character, b"."""
    assert compile_pattern("a.b").search("axb") is None


def test_compile_pattern_flags_work_with_a_str() -> None:
    """`re` flags are applied to the literal."""
    assert compile_pattern("abc", re.IGNORECASE).search("xABCx") is not None
    assert compile_pattern("abc").search("xABCx") is None


def test_compile_pattern_flags_combine_with_a_str() -> None:
    """Several flags joined with `|` all apply."""
    compiled = compile_pattern("a", re.IGNORECASE | re.MULTILINE)
    assert compiled.flags & re.IGNORECASE
    assert compiled.flags & re.MULTILINE


# ----------------------------------------------------------------------
# re.Pattern — taken as it is
# ----------------------------------------------------------------------

def test_compile_pattern_returns_a_compiled_pattern_unchanged() -> None:
    """The very same object comes back, with its own flags."""
    pattern = re.compile("a+", re.IGNORECASE)
    assert compile_pattern(pattern) is pattern


def test_compile_pattern_a_compiled_pattern_is_not_escaped() -> None:
    """A `re.Pattern` is a regex, unlike a str."""
    assert compile_pattern(re.compile("a.b")).search("axb") is not None


# ----------------------------------------------------------------------
# Regex tree
# ----------------------------------------------------------------------

def test_compile_pattern_compiles_a_regex_tree() -> None:
    """A tree is rendered with `to_pattern()` and compiled."""
    tree = Literal("a") + DIGIT
    compiled = compile_pattern(tree)
    assert compiled.pattern == tree.to_pattern()
    assert compiled.search("xa5y").group(0) == "a5"


def test_compile_pattern_flags_work_with_a_regex_tree() -> None:
    """A tree is not compiled yet, so flags can still be given."""
    assert compile_pattern(Literal("a"), re.IGNORECASE).search("A") is not None


# ----------------------------------------------------------------------
# RegexPattern — the compiled wrapper
# ----------------------------------------------------------------------

def test_compile_pattern_takes_the_pattern_held_by_a_regex_pattern() -> None:
    """The `re.Pattern` inside the wrapper is returned, not a new one."""
    wrapper = RegexPattern(Literal("a") + DIGIT)
    assert compile_pattern(wrapper) is wrapper.compiled


def test_compile_pattern_a_regex_pattern_keeps_its_own_flags() -> None:
    """Flags given to the wrapper at its construction are in the result."""
    wrapper = RegexPattern(Literal("a"), flags=frozenset({Flag.IGNORECASE}))
    assert compile_pattern(wrapper).search("A") is not None


def test_compile_pattern_compiles_a_lazy_regex_pattern_on_the_spot() -> None:
    """A `lazy=True` wrapper is compiled at this moment and works afterwards."""
    wrapper = RegexPattern(Literal("a") + DIGIT, lazy=True)
    assert compile_pattern(wrapper).search("a1") is not None


def test_compile_pattern_a_broken_lazy_regex_pattern_reports_the_regex_card() -> None:
    """The wrapper's own diagnostic (from simplibs-regex) is not hidden behind this library's card."""
    broken = NAMED_GROUP(DIGIT, "a") + NAMED_GROUP(DIGIT, "a")
    with pytest.raises(ValidationError):
        compile_pattern(RegexPattern(broken, lazy=True))


# ----------------------------------------------------------------------
# Flags together with a compiled pattern
# ----------------------------------------------------------------------

@pytest.mark.parametrize(
    "pattern",
    [re.compile("a"), RegexPattern(Literal("a"))],
    ids=["re.Pattern", "RegexPattern"],
)
def test_compile_pattern_refuses_flags_with_a_compiled_pattern(subtests, pattern) -> None:
    """A compiled pattern carries its flags, so more of them would be silently ignored."""
    assert_exception_function(
        subtests,
        compile_pattern,
        invalid_params=(pattern, re.IGNORECASE),
        exception_type=ParamError,
        error_name="TEXT_PATTERN_FLAGS_CONFLICT",
        label="flags",
        value=re.IGNORECASE,
        exception=ValueError,
        verbose=False,
    )


def test_compile_pattern_accepts_zero_flags_with_a_compiled_pattern() -> None:
    """`flags=0` is the default and never a conflict."""
    pattern = re.compile("a")
    assert compile_pattern(pattern, 0) is pattern


# ----------------------------------------------------------------------
# Patterns and flags that cannot be compiled
# ----------------------------------------------------------------------

def test_compile_pattern_wraps_a_bad_flag_combination(subtests) -> None:
    """`re.LOCALE` cannot be used with a str pattern; `re` raises ValueError, the card explains."""
    assert_exception_function(
        subtests,
        compile_pattern,
        invalid_params=("a", re.LOCALE),
        valid_params=("a",),
        exception_type=ParamError,
        error_name="TEXT_PATTERN_COMPILE_FAILED",
        label="pattern",
        exception=ValueError,
        verbose=False,
    )


def test_compile_pattern_wraps_a_tree_that_renders_an_invalid_pattern(subtests) -> None:
    """Two groups with one name are only seen by `re.compile`, which raises `re.error`."""
    broken = NAMED_GROUP(DIGIT, "a") + NAMED_GROUP(DIGIT, "a")
    assert_exception_function(
        subtests,
        compile_pattern,
        invalid_params=(broken,),
        exception_type=ParamError,
        error_name="TEXT_PATTERN_COMPILE_FAILED",
        label="pattern",
        exception=ValueError,
        verbose=False,
    )
