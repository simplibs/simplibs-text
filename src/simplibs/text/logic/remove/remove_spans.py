from collections.abc import Sequence
from simplibs.validate import validate_call
# Outers
from ...annotations import Span
# Inners
from ._helpers import cut_spans, normalize_spans


@validate_call
def remove_spans(
    text: str,
    spans: Sequence[Span],
    *,
    drop_emptied_lines: bool = True,
) -> str:
    """Remove given character ranges from a text.

    The shared primitive for everything that FINDS what to remove in its own way
    (a regex, a parser, a tokenizer) and wants the cutting done the same way.

    Args:
        text: The text.
        spans: `(start, end)` pairs, half-open (`text[start:end]` is removed).
            Any order; overlapping and touching spans are merged.
        drop_emptied_lines: A line that is blank only because of the removal
            disappears whole. Blank lines that were there before stay.

    Returns:
        The text without the spans; the same text if there is nothing to remove.

    Raises:
        ParamError: If a span does not satisfy `0 <= start <= end <= len(text)`.
    """

    # 1. Check, sort and merge the spans
    merged = normalize_spans(spans, len(text))

    # 2. Nothing to remove — the very same text back
    if not merged:
        return text

    # 3. Cut
    return cut_spans(text, merged, drop_emptied_lines)


_DESIGN_NOTES = """
# remove_spans — Cut Where You Are Told

## Purpose
`remove_matches` finds spans with a regex. The code extractor finds them with
`ast`, `tokenize` and a JavaScript scanner. This function is what they share.

## Why Half-Open Spans
`(start, end)` with `end` excluded is how `re.Match.span()`, `ast` offsets and
slices all work, so values can be passed straight through.

## Cost of Validation
`@validate_call` checks every pair. For thousands of spans in one file that is
still cheap next to parsing the file.
"""
