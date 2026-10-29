import pytest
from simplibs.text.logic.case import to_snake_case


@pytest.mark.parametrize(
    "text, expected",
    [
        ("myVarName", "my_var_name"),
        ("MyVarName", "my_var_name"),
        ("my-var-name", "my_var_name"),
        ("my var name", "my_var_name"),
        ("MY_VAR_NAME", "my_var_name"),
        ("HTTPServer", "http_server"),
        ("base64Encode", "base64_encode"),
        ("item_2_name", "item_2_name"),
        ("hello, world!", "hello_world"),
    ],
)
def test_to_snake_case_converts_from_any_style(text, expected) -> None:
    """Words in lowercase joined by an underscore."""
    assert to_snake_case(text) == expected


def test_to_snake_case_converts_every_line_on_its_own() -> None:
    """A text with many lines stays a text with many lines."""
    assert to_snake_case("myVar\nother-name\n") == "my_var\nother_name\n"


def test_to_snake_case_keeps_the_indentation_and_the_lines_without_words() -> None:
    """Indentation is not part of the name; blank and punctuation-only lines stay."""
    assert to_snake_case("    myVar\n\n---\n\tother") == "    my_var\n\n---\n\tother"


def test_to_snake_case_trailing_whitespace_of_a_line_is_not_kept() -> None:
    """The line is rewritten from its words."""
    assert to_snake_case("my var  ") == "my_var"


def test_to_snake_case_other_scripts() -> None:
    """Czech and Devanagari."""
    assert to_snake_case("p\u0159\u00ed\u0161ern\u011b\u017dlut\u00fd") == "p\u0159\u00ed\u0161ern\u011b_\u017elut\u00fd"
    assert to_snake_case("\u0939\u093f\u0902\u0926\u0940 \u092d\u093e\u0937\u093e") == "\u0939\u093f\u0902\u0926\u0940_\u092d\u093e\u0937\u093e"


@pytest.mark.parametrize("text", ["my_var_name", "a", "x_1", "", "a_b\nc_d\n", "   ", "---"])
def test_to_snake_case_a_text_that_already_is_snake_case_is_returned_as_it_is(text) -> None:
    """The same object comes back."""
    probe = "".join(list(text))
    assert to_snake_case(probe) is probe


@pytest.mark.parametrize("text", ["myVar-name Other", "HTTPServer2Go", "a  b", "x\n\ny_Z"])
def test_to_snake_case_is_idempotent(text) -> None:
    """Running it twice gives the same result."""
    once = to_snake_case(text)
    assert to_snake_case(once) == once
