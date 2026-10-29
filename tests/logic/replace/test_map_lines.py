import pytest
from simplibs.exception import ParamError
from simplibs.text.logic.replace import map_lines


def test_map_lines_applies_the_function_to_every_line() -> None:
    """Every line, the final newline kept."""
    assert map_lines("a\nb\n", str.upper) == "A\nB\n"


@pytest.mark.parametrize("text, expected", [("a\nb", "A\nB"), ("a\nb\n", "A\nB\n"), ("a", "A"), ("a\n", "A\n")])
def test_map_lines_keeps_the_final_newline_status(text, expected) -> None:
    """The text ends with a newline exactly when it did before."""
    assert map_lines(text, str.upper) == expected


def test_map_lines_the_function_gets_lines_without_their_newline() -> None:
    """Blank lines are lines too, in order."""
    seen: list[str] = []

    def remember(line: str) -> str:
        seen.append(line)
        return line

    map_lines("a\n\nb\n", remember)

    assert seen == ["a", "", "b"]


def test_map_lines_a_carriage_return_stays_on_the_line() -> None:
    """A text with `\\r\\n` is not normalized here; the function sees `a\\r`."""
    seen: list[str] = []

    def remember(line: str) -> str:
        seen.append(line)
        return line

    map_lines("a\r\nb\r\n", remember)

    assert seen == ["a\r", "b\r"]


def test_map_lines_the_empty_text_calls_the_function_never() -> None:
    """No lines, no calls."""
    calls: list[str] = []
    assert map_lines("", calls.append) == ""
    assert calls == []


def test_map_lines_a_single_newline_is_one_empty_line() -> None:
    """The function is called once, with the empty line."""
    assert map_lines("\n", lambda line: "x") == "x\n"


def test_map_lines_returning_the_empty_text_leaves_an_empty_line() -> None:
    """The line is not deleted; `remove_lines_matching` does that."""
    assert map_lines("a\nb\n", lambda line: "" if line == "a" else line) == "\nb\n"


def test_map_lines_a_result_with_a_newline_becomes_more_lines() -> None:
    """The function decides what the new line looks like, newline included."""
    assert map_lines("a\n", lambda line: line + "\nX") == "a\nX\n"


def test_map_lines_nothing_changed_gives_the_very_same_text() -> None:
    """The same object comes back."""
    text = "".join(["a", "\n", "b"])
    assert map_lines(text, lambda line: line) is text


@pytest.mark.parametrize("bad_result", [None, 5, ["x"], b"x"])
def test_map_lines_a_function_returning_no_text_is_refused(bad_result) -> None:
    """The usual cause is a forgotten `return`."""
    with pytest.raises(ParamError):
        map_lines("a\nb\n", lambda line: bad_result)


def test_map_lines_an_error_in_the_function_is_not_hidden() -> None:
    """Whatever the caller's function raises comes out unchanged."""
    def boom(line: str) -> str:
        raise KeyError("boom")

    with pytest.raises(KeyError):
        map_lines("a", boom)
