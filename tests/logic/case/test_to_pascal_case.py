import pytest
from simplibs.text.logic.case import to_pascal_case, to_snake_case


@pytest.mark.parametrize(
    "text, expected",
    [
        ("my_var_name", "MyVarName"),
        ("my-var-name", "MyVarName"),
        ("my var name", "MyVarName"),
        ("myVarName", "MyVarName"),
        ("MY_VAR_NAME", "MyVarName"),
        ("item_2_name", "Item2Name"),
        ("x Ray", "XRay"),
    ],
)
def test_to_pascal_case_converts_from_any_style(text, expected) -> None:
    """Every word with a capital first letter, joined without a separator."""
    assert to_pascal_case(text) == expected


def test_to_pascal_case_an_acronym_is_not_kept_in_capitals() -> None:
    """The style capitalizes only the first letter of each word."""
    assert to_pascal_case("HTTPServer") == "HttpServer"


def test_to_pascal_case_converts_every_line_on_its_own() -> None:
    """A text with many lines stays a text with many lines; indentation stays."""
    assert to_pascal_case("  my_var\nother-name\n") == "  MyVar\nOtherName\n"


@pytest.mark.parametrize("text", ["MyVarName", "A", "", "AbCd\nEfGh\n", "---"])
def test_to_pascal_case_a_text_that_already_is_pascal_case_is_returned_as_it_is(text) -> None:
    """The same object comes back."""
    probe = "".join(list(text))
    assert to_pascal_case(probe) is probe


@pytest.mark.parametrize("text", ["my_var-name Other", "HTTPServer2Go", "x Ray", "item2 name"])
def test_to_pascal_case_is_idempotent(text) -> None:
    """Running it twice gives the same result."""
    once = to_pascal_case(text)
    assert to_pascal_case(once) == once


def test_to_pascal_case_single_letter_words_are_ambiguous_and_change_once_more() -> None:
    """`AB` may be `A` + `B` or one word `AB`; a second conversion reads it as one word (see its design notes)."""
    assert to_pascal_case("a b") == "AB"
    assert to_pascal_case("AB") == "Ab"


@pytest.mark.parametrize("text", ["my_var_name", "hello_world", "item2_name"])
def test_to_pascal_case_and_back_to_snake_case_for_ordinary_names(text) -> None:
    """The way back works when no word is a single letter and no digit stands alone."""
    assert to_snake_case(to_pascal_case(text)) == text
