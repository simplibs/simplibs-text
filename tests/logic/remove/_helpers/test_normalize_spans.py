import random
import pytest
from simplibs.exception import ParamError
from simplibs.text.logic.remove._helpers import normalize_spans


@pytest.mark.parametrize(
    "spans, expected",
    [
        ([(2, 4)], [(2, 4)]),
        ([(5, 7), (0, 2)], [(0, 2), (5, 7)]),
        ([(0, 4), (2, 6)], [(0, 6)]),
        ([(0, 3), (3, 5)], [(0, 5)]),
        ([(0, 10), (2, 3)], [(0, 10)]),
        ([(1, 2), (1, 2)], [(1, 2)]),
        ([(4, 6), (0, 1), (1, 4)], [(0, 6)]),
        ([(0, 2), (4, 6)], [(0, 2), (4, 6)]),
    ],
    ids=["one", "unsorted", "overlapping", "touching", "contained", "duplicate", "chain", "apart"],
)
def test_normalize_spans_sorts_and_merges(spans, expected) -> None:
    """Spans come out sorted, and spans that overlap or touch become one."""
    assert normalize_spans(spans, 10) == expected


@pytest.mark.parametrize(
    "spans, expected",
    [
        ([], []),
        ([(4, 4)], []),
        ([(0, 0)], []),
        ([(10, 10)], []),
        ([(0, 0), (2, 3), (5, 5)], [(2, 3)]),
    ],
    ids=["none", "empty-middle", "empty-start", "empty-end", "empty-among-others"],
)
def test_normalize_spans_drops_empty_spans(spans, expected) -> None:
    """A span that removes nothing is not a removal: otherwise it would mark a line as emptied."""
    assert normalize_spans(spans, 10) == expected


@pytest.mark.parametrize("span", [(0, 10), (0, 1), (9, 10), (3, 3), (10, 10)])
def test_normalize_spans_accepts_spans_up_to_the_text_length(span) -> None:
    """`0 <= start <= end <= length` is valid, the end of the text included."""
    normalize_spans([span], 10)


@pytest.mark.parametrize(
    "span",
    [(-1, 2), (-5, -1), (3, 2), (0, 11), (11, 12), (10, 11)],
    ids=["negative-start", "all-negative", "backwards", "past-end", "start-past-end", "one-past-end"],
)
def test_normalize_spans_rejects_a_span_that_does_not_fit(span) -> None:
    """Out of range or backwards: refused, never silently clipped."""
    with pytest.raises(ParamError):
        normalize_spans([span], 10)


def test_normalize_spans_checks_every_span_not_only_the_first() -> None:
    """A bad span in the middle is found."""
    with pytest.raises(ParamError):
        normalize_spans([(0, 1), (2, 3), (4, 99)], 10)


def test_normalize_spans_does_not_change_its_input() -> None:
    """The caller's list stays as it was."""
    spans = [(5, 7), (0, 2)]
    normalize_spans(spans, 10)
    assert spans == [(5, 7), (0, 2)]


def test_normalize_spans_covers_the_same_characters_as_the_input() -> None:
    """Random spans: the result covers exactly the same positions, sorted, apart and never empty."""
    rng = random.Random(0)
    for _ in range(500):
        length = rng.randint(0, 20)
        spans = []
        for _ in range(rng.randint(0, 6)):
            start = rng.randint(0, length)
            spans.append((start, rng.randint(start, length)))

        merged = normalize_spans(spans, length)

        covered = {position for start, end in spans for position in range(start, end)}
        assert {position for start, end in merged for position in range(start, end)} == covered
        assert all(start < end for start, end in merged)
        assert all(left[1] < right[0] for left, right in zip(merged, merged[1:]))
