import random
import pytest
from simplibs.text.logic.remove._helpers import cut_spans, normalize_spans


def _model(text: str, spans, drop_emptied_lines: bool) -> str:
    """The same rule written the long way: mark every removal site, then judge each line."""
    pieces = []
    position = 0
    for start, end in normalize_spans(spans, len(text)):
        pieces += list(text[position:start]) + [None]
        position = end
    pieces += list(text[position:])

    if not drop_emptied_lines:
        return "".join(piece for piece in pieces if piece is not None)

    lines: list[list] = [[]]
    for piece in pieces:
        if piece == "\n":
            lines.append([])
        else:
            lines[-1].append(piece)

    kept = []
    for line in lines:
        emptied = any(piece is None for piece in line)
        content = "".join(piece for piece in line if piece is not None)
        if not (emptied and content.strip() == ""):
            kept.append(content)
    return "\n".join(kept)


# ----------------------------------------------------------------------
# A plain cut
# ----------------------------------------------------------------------

@pytest.mark.parametrize(
    "text, spans, expected",
    [
        ("abc def", [(3, 7)], "abc"),
        ("abc def", [(0, 4)], "def"),
        ("a1b2c", [(1, 2), (3, 4)], "abc"),
        ("abc", [(0, 3)], ""),
        ("abc", [], "abc"),
        ("", [], ""),
    ],
)
def test_cut_spans_without_dropping_lines_is_a_plain_cut(text, spans, expected) -> None:
    """With `drop_emptied_lines=False` lines are not looked at."""
    assert cut_spans(text, spans, False) == expected


def test_cut_spans_without_dropping_lines_keeps_the_empty_line() -> None:
    """The skeleton of the lines stays."""
    assert cut_spans("a\n# note\nb\n", [(2, 8)], False) == "a\n\nb\n"


# ----------------------------------------------------------------------
# Dropping emptied lines
# ----------------------------------------------------------------------

@pytest.mark.parametrize(
    "text, spans, expected",
    [
        ("code\n# note\nmore\n", [(5, 11)], "code\nmore\n"),
        ("x = 1  # note\n", [(5, 13)], "x = 1\n"),
        ("a\n\nb abc\n", [(5, 8)], "a\n\nb \n"),
        ("  abc\n", [(0, 5)], ""),
        ("a\nb\nc", [(1, 4)], "ac"),
        ("x\nabc\ndef\ny", [(2, 9)], "x\ny"),
    ],
    ids=["whole-line", "rest-of-line", "original-blank-stays", "indent-only-left", "joins-lines", "several-lines"],
)
def test_cut_spans_drops_only_the_lines_the_removal_emptied(text, spans, expected) -> None:
    """A line that is blank BECAUSE of the removal goes; a line that was blank before stays."""
    assert cut_spans(text, spans, True) == expected


@pytest.mark.parametrize(
    "text, spans, expected",
    [
        ("abc", [(0, 3)], ""),
        ("abc\n", [(0, 3)], ""),
        ("x\nabc", [(2, 5)], "x"),
        ("x\nabc\n", [(2, 5)], "x\n"),
        ("abc\nx", [(0, 3)], "x"),
        ("abc\n\nx", [(0, 3)], "\nx"),
        ("a\nb\n", [(0, 4)], ""),
    ],
    ids=["only-line", "only-line-closed", "last-line", "last-line-closed", "first-line", "first-then-blank", "everything"],
)
def test_cut_spans_handles_the_ends_of_the_text(text, spans, expected) -> None:
    """The final newline stays when the last line stays; an emptied last line takes its newline with it."""
    assert cut_spans(text, spans, True) == expected


@pytest.mark.parametrize(
    "text",
    ["", "a", "a\n", "\n", "a\n\nb\n", "  \n \t\nx", "a\n   \n", "\n\n\n"],
)
def test_cut_spans_without_spans_gives_back_the_text(text) -> None:
    """With nothing removed no line counts as emptied, so blank lines are all kept."""
    assert cut_spans(text, [], True) == text


def test_cut_spans_works_with_a_nul_character_in_the_text() -> None:
    """Positions need no reserved character, so any character may be in the text."""
    assert cut_spans("a\x00b\x00\n", [(2, 3)], True) == "a\x00\x00\n"


def test_cut_spans_matches_the_long_way_for_random_texts() -> None:
    """Random texts and spans: the result equals the rule written out step by step."""
    rng = random.Random(1)
    alphabet = "ab \n\t\r#"
    for _ in range(3000):
        length = rng.randint(0, 14)
        text = "".join(rng.choice(alphabet) for _ in range(length))
        spans = []
        for _ in range(rng.randint(0, 4)):
            start = rng.randint(0, length)
            spans.append((start, rng.randint(start, length)))
        normalized = normalize_spans(spans, length)

        for drop in (True, False):
            assert cut_spans(text, normalized, drop) == _model(text, spans, drop), (text, spans, drop)
