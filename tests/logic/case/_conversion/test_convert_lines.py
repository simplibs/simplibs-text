import pytest
from simplibs.text.logic.case._conversion import convert_lines


def _bars(words: list[str]) -> str:
    return "|".join(words)


def test_convert_lines_rewrites_every_line_from_its_words() -> None:
    """Each line is split into words and put together again."""
    assert convert_lines("my var\nother_name\n", _bars) == "my|var\nother|name\n"


def test_convert_lines_keeps_the_indentation() -> None:
    """It is not part of the name."""
    assert convert_lines("    my var\n\tother", _bars) == "    my|var\n\tother"


@pytest.mark.parametrize("line", ["", "   ", "---", "!!! ...", "\t"])
def test_convert_lines_a_line_without_words_is_kept_as_it_is(line) -> None:
    """Blank and punctuation-only lines do not vanish."""
    assert convert_lines(f"a b\n{line}\nc d", _bars) == f"a|b\n{line}\nc|d"


@pytest.mark.parametrize("text, expected", [("a b", "a|b"), ("a b\n", "a|b\n"), ("a b\n\n", "a|b\n\n")])
def test_convert_lines_keeps_the_final_newline_status(text, expected) -> None:
    """The text ends with a newline exactly when it did before."""
    assert convert_lines(text, _bars) == expected


def test_convert_lines_the_function_gets_the_words_of_a_line_only_for_lines_with_words() -> None:
    """It is never called with an empty list."""
    seen: list[list[str]] = []

    def remember(words: list[str]) -> str:
        seen.append(list(words))
        return " ".join(words)

    convert_lines("a-b\n\n!!!\nc", remember)

    assert seen == [["a", "b"], ["c"]]


def test_convert_lines_nothing_changed_gives_the_very_same_text() -> None:
    """The same object comes back."""
    text = "".join(["a", "|", "b", "\n", "", "c"])
    assert convert_lines(text, _bars) is text


def test_convert_lines_empty_text() -> None:
    """No lines, no calls."""
    assert convert_lines("", _bars) == ""
