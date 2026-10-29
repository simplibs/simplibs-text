import pytest
from simplibs.text.logic.case import to_kebab_case


@pytest.mark.parametrize(
    "text, expected",
    [
        ("myVarName", "my-var-name"),
        ("MyVarName", "my-var-name"),
        ("my_var_name", "my-var-name"),
        ("my var name", "my-var-name"),
        ("HTTPServer", "http-server"),
        ("item_2_name", "item-2-name"),
        ("base64Encode", "base64-encode"),
    ],
)
def test_to_kebab_case_converts_from_any_style(text, expected) -> None:
    """Words in lowercase joined by a hyphen."""
    assert to_kebab_case(text) == expected


def test_to_kebab_case_converts_every_line_on_its_own() -> None:
    """A text with many lines stays a text with many lines; indentation stays."""
    assert to_kebab_case("  myVar\nother_name\n") == "  my-var\nother-name\n"


@pytest.mark.parametrize("text", ["my-var-name", "a", "", "a-b\nc-d\n", "---"])
def test_to_kebab_case_a_text_that_already_is_kebab_case_is_returned_as_it_is(text) -> None:
    """The same object comes back."""
    probe = "".join(list(text))
    assert to_kebab_case(probe) is probe


@pytest.mark.parametrize("text", ["myVar_name Other", "HTTPServer2Go", "a  b"])
def test_to_kebab_case_is_idempotent(text) -> None:
    """Running it twice gives the same result."""
    once = to_kebab_case(text)
    assert to_kebab_case(once) == once


@pytest.mark.parametrize("text", ["my-var-name", "a-b", "x-1-y", "base64-encode"])
def test_to_kebab_case_and_to_snake_case_convert_back_and_forth(text) -> None:
    """The two styles carry their separators, so nothing is lost."""
    from simplibs.text.logic.case import to_snake_case

    assert to_kebab_case(to_snake_case(text)) == text
