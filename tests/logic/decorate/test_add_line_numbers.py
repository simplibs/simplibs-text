import pytest
from simplibs.exception import ParamError
from simplibs.text.logic.decorate import add_line_numbers


def test_add_line_numbers_numbers_every_line_from_one() -> None:
    """The default template `{number}: {line}`."""
    assert add_line_numbers("a\nb\nc\n") == "1: a\n2: b\n3: c\n"


@pytest.mark.parametrize("text, expected", [("a", "1: a"), ("a\n", "1: a\n"), ("a\nb", "1: a\n2: b")])
def test_add_line_numbers_keeps_the_final_newline_status(text, expected) -> None:
    """The text ends with a newline exactly when it did before."""
    assert add_line_numbers(text) == expected


def test_add_line_numbers_blank_lines_are_numbered_too() -> None:
    """They are lines."""
    assert add_line_numbers("a\n\nb") == "1: a\n2: \n3: b"


def test_add_line_numbers_an_empty_text_stays_empty() -> None:
    """No lines, nothing to number."""
    assert add_line_numbers("") == ""


def test_add_line_numbers_a_single_newline_is_one_empty_line() -> None:
    """It gets the number 1."""
    assert add_line_numbers("\n") == "1: \n"


def test_add_line_numbers_the_numbers_are_right_aligned_to_the_last_one() -> None:
    """Ten lines need two digits, so the first ones get a space in front."""
    result = add_line_numbers("\n".join(["x"] * 10)).split("\n")
    assert result[0] == " 1: x"
    assert result[8] == " 9: x"
    assert result[9] == "10: x"


def test_add_line_numbers_start_sets_the_first_number() -> None:
    """The width follows the last number, not the number of lines."""
    assert add_line_numbers("a\nb", start=9) == " 9: a\n10: b"
    assert add_line_numbers("a\nb", start=0) == "0: a\n1: b"


def test_add_line_numbers_an_explicit_width_is_used() -> None:
    """Instead of the computed one."""
    assert add_line_numbers("a", width=4) == "   1: a"


def test_add_line_numbers_a_width_that_is_too_small_does_not_cut_the_number() -> None:
    """The number just takes more room."""
    assert add_line_numbers("\n".join(["x"] * 10), width=1).split("\n")[9] == "10: x"


@pytest.mark.parametrize(
    "template, expected",
    [
        ("{number}| {line}", "1| a\n2| b"),
        ("{line} #{number}", "a #1\nb #2"),
        ("{number:0{width}d} {line}", "1 a\n2 b"),
        ("{line}", "a\nb"),
        ("{{{number}}} {line}", "{1} a\n{2} b"),
    ],
    ids=["after-bar", "after-line", "zero-padded", "no-number", "literal-braces"],
)
def test_add_line_numbers_a_custom_template(template, expected) -> None:
    """The fields are `{number}`, `{line}` and `{width}`."""
    assert add_line_numbers("a\nb", template=template) == expected


def test_add_line_numbers_braces_in_the_text_are_just_text() -> None:
    """Only the template is a format string."""
    assert add_line_numbers("{x} {0}\n") == "1: {x} {0}\n"


@pytest.mark.parametrize("template", ["{foo}", "{0}", "{number.x}", "{", "{number:z}"])
def test_add_line_numbers_a_template_that_cannot_be_filled_in_is_refused(template) -> None:
    """With a card, and also for a text so short that the mistake would not show."""
    with pytest.raises(ParamError):
        add_line_numbers("a\nb", template=template)


@pytest.mark.parametrize("text", ["", "a"])
def test_add_line_numbers_a_bad_template_is_refused_even_for_a_short_or_empty_text(text) -> None:
    """The template is tried before the text is looked at."""
    with pytest.raises(ParamError):
        add_line_numbers(text, template="{foo}")
