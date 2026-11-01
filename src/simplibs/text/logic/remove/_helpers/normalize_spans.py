from collections.abc import Sequence
# Outers
from ....annotations import Span
# Inners
from .._validations import raise_invalid_span_error


def normalize_spans(
    spans: Sequence[Span],
    text_length: int,
) -> list[Span]:
    """Check spans against the text length and turn them into sorted, separate ranges.

    Args:
        spans: `(start, end)` pairs in any order; they may overlap or touch.
        text_length: Length of the text the spans refer to.

    Returns:
        Sorted spans that neither overlap nor touch. Empty spans are dropped.

    Raises:
        ParamError: If a span does not satisfy `0 <= start <= end <= text_length`.
    """

    # 1. Check every span and drop the empty ones (nothing to remove, nothing emptied)
    valid: list[Span] = []
    for index, span in enumerate(spans):
        start, end = span
        if not 0 <= start <= end <= text_length:
            raise_invalid_span_error(span, index, text_length)
        if end > start:
            valid.append((start, end))

    # 2. Sort, then merge spans that overlap or touch
    merged: list[Span] = []
    for start, end in sorted(valid):
        if merged and start <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], end))
        else:
            merged.append((start, end))

    return merged


_DESIGN_NOTES = """
# normalize_spans — Ranges That Cannot Disagree

## Purpose
Cutting needs spans that are sorted and separate. Callers should not have to
guarantee that: a tokenizer may report a decorator inside a class, a regex may
match a comment twice through two alternatives.

## Touching Spans
`(0, 3)` and `(3, 5)` become `(0, 5)`. Nothing is lost by merging them, and one
continuous removal marks its line as emptied once, not twice.

## Empty Spans
`(4, 4)` removes nothing, so it is dropped. Otherwise a zero-length regex match
(for example `^`) would flag lines as "emptied" without changing them, and
`drop_emptied_lines` would delete original blank lines.
"""
