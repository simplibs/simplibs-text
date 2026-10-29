import pytest
from simplibs.text.logic.decorate import indent
from simplibs.text.logic.remove import dedent


def test_indent_default_is_four_spaces() -> None:
    """In front of every line."""
    assert indent("a\nb") == "    a\n    b"


@pytest.mark.parametrize(
    "prefix, expected",
    [(2, "  a\n  b"), (1, " a\n b"), ("> ", "> a\n> b"), ("\t", "\ta\n\tb"), ("# ", "# a\n# b")],
)
def test_indent_a_number_means_spaces_and_a_text_is_used_as_it_is(prefix, expected) -> None:
    """`2` is two spaces; `"> "` is a quote mark."""
    assert indent("a\nb", prefix) == expected


def test_indent_blank_lines_are_left_as_they_are() -> None:
    """An empty line and a whitespace-only line get no prefix."""
    assert indent("a\n\n  \nb", 2) == "  a\n\n  \n  b"


@pytest.mark.parametrize("text, expected", [("a", "  a"), ("a\n", "  a\n"), ("a\n\n", "  a\n\n")])
def test_indent_keeps_the_final_newline_status(text, expected) -> None:
    """The text ends with a newline exactly when it did before."""
    assert indent(text, 2) == expected


def test_indent_adds_to_an_existing_indentation() -> None:
    """The prefix is put in front of whatever is there."""
    assert indent("  a", 2) == "    a"


@pytest.mark.parametrize("prefix", [0, ""])
def test_indent_nothing_to_add_gives_the_very_same_text(prefix) -> None:
    """The same object comes back."""
    text = "".join(["a", "\n", "b"])
    assert indent(text, prefix) is text


@pytest.mark.parametrize("text", ["", "\n", "\n\n", "  \n"])
def test_indent_a_text_of_blank_lines_is_unchanged(text) -> None:
    """Nothing to put anything before."""
    assert indent(text, 4) == text


@pytest.mark.parametrize("text", ["a\nb", "  a\nb", "a\n\n  b\n", "a\n\tb", "x\n\n\ny"])
@pytest.mark.parametrize("prefix", [2, 4, "\t", "  "])
def test_indent_is_undone_by_dedent_when_a_line_is_flush_left(text, prefix) -> None:
    """The common margin is exactly what was added, so `dedent(indent(x)) == x`."""
    assert dedent(indent(text, prefix)) == text


def test_indent_dedent_also_removes_the_indentation_the_text_had_when_every_line_has_one() -> None:
    """`dedent` takes the whole common margin, not only the part `indent` added."""
    assert dedent(indent("  a\n  b", 2)) == "a\nb"
