from typing import NoReturn
from simplibs.exception import ParamError


def raise_invalid_span_error(
    span: tuple[int, int],
    index: int,
    text_length: int,
) -> NoReturn:
    """Raise ParamError when a span does not fit into the text.

    Args:
        span: The offending `(start, end)` pair.
        index: Its position in the `spans` sequence.
        text_length: Length of the text the spans refer to.
    """

    # 1. Raise structured ParamError wrapping a ValueError
    raise ParamError(
        error_name="TEXT_SPAN_INVALID",
        label=f"spans[{index}]",
        value=span,
        problem=(
            f"The span {span!r} does not fit into a text of {text_length} characters.",
            "A span is a half-open range: start is included, end is not.",
        ),
        expected=f"0 <= start <= end <= {text_length}",
        how_to_fix=(
            "Make sure the spans were measured on exactly this text.",
            "If the text was changed after measuring (e.g. stripped), measure again.",
        ),
        exception=ValueError,
    )


_DESIGN_NOTES = """
# raise_invalid_span_error — a Range From Another Text

## Purpose
Spans usually come from a parser or a tokenizer. A span that is out of range
almost always means it was measured on a different text (before a strip or a
newline normalization). Cutting with it would silently remove the wrong part,
so it is refused with the index of the offending span.
"""
