import pytest
from simplibs.text.logic.case import to_camel_case, to_snake_case


@pytest.mark.parametrize(
    "text, expected",
    [
        ("my_var_name", "myVarName"),
        ("my-var-name", "myVarName"),
        ("my var name", "myVarName"),
        ("MyVarName", "myVarName"),
        ("MY_VAR_NAME", "myVarName"),
        ("item_2_name", "item2Name"),
        ("x Ray", "xRay"),
        ("single", "single"),
        ("Single", "single"),
    ],
)
def test_to_camel_case_converts_from_any_style(text, expected) -> None:
    """The first word in lowercase, every other with a capital first letter."""
    assert to_camel_case(text) == expected


def test_to_camel_case_an_acronym_is_not_kept_in_capitals() -> None:
    """The style capitalizes only the first letter of each word."""
    assert to_camel_case("HTTPServer") == "httpServer"


def test_to_camel_case_converts_every_line_on_its_own() -> None:
    """A text with many lines stays a text with many lines; indentation stays."""
    assert to_camel_case("  my_var\nOther-name\n") == "  myVar\notherName\n"


@pytest.mark.parametrize("text", ["myVarName", "a", "", "abCd\nefGh\n", "---"])
def test_to_camel_case_a_text_that_already_is_camel_case_is_returned_as_it_is(text) -> None:
    """The same object comes back."""
    probe = "".join(list(text))
    assert to_camel_case(probe) is probe


@pytest.mark.parametrize("text", ["my_var-name Other", "HTTPServer2Go", "a  b", "x Ray"])
def test_to_camel_case_is_idempotent(text) -> None:
    """Running it twice gives the same result."""
    once = to_camel_case(text)
    assert to_camel_case(once) == once


def test_to_camel_case_digits_stay_with_the_word_before_them_on_the_way_back() -> None:
    """`item_2_name` becomes `item2Name`, and that is read as `item2` + `Name`."""
    assert to_camel_case("item_2_name") == "item2Name"
    assert to_snake_case("item2Name") == "item2_name"


@pytest.mark.parametrize("text", ["my_var_name", "hello_world", "item2_name"])
def test_to_camel_case_and_back_to_snake_case_for_ordinary_names(text) -> None:
    """The way back works when no word is a single letter and no digit stands alone."""
    assert to_snake_case(to_camel_case(text)) == text
