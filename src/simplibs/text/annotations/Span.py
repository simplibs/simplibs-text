Span = tuple[int, int]
"""A range of characters in a text: `(start, end)`, half-open — `text[start:end]` is the range."""


_DESIGN_NOTES = """
# Span — A Range of Characters

## Purpose
The type of one item of the `spans` parameter of `remove_spans`. Everything that
FINDS what to cut (a regex, a tokenizer, a parser) answers with spans, and
`remove_spans` cuts them. The name lets a caller declare the same type in the
signatures of its own functions.

## Why Half-Open
`end` is excluded, exactly as in `re.Match.span()`, in `ast` offsets and in a
slice, so a value can be passed on without adding or subtracting one.

## Characters, Not Bytes
A span counts characters of the text it was found in. A tool that reports bytes
(`ast` does) converts them before it makes a span.

## Why Not `Annotated`
Whether a span fits is known only together with a text: `0 <= start <= end <=
len(text)`. The type therefore checks the shape (two integers) and nothing
more; `remove_spans` checks the fit and reports a bad span with the card
`TEXT_SPAN_INVALID`. Like `Replacement`, it is a plain alias.
"""
