import re
from simplibs.regex.base_class import Regex
from simplibs.regex.compiler import RegexPattern


def is_pattern(value: str | re.Pattern | Regex | RegexPattern) -> bool:
    """Check whether a value is usable as a search pattern.

    Args:
        value: The candidate.

    Returns:
        True for a non-empty `str`, a compiled `re.Pattern`, a `Regex` tree or a
        `RegexPattern`; False for the empty string and for anything else.
    """

    # 1. A text is a literal — the empty one would match between every two characters
    if isinstance(value, str):
        return value != ""

    # 2. A compiled pattern, a `Regex` tree and a `RegexPattern` are taken as they are
    return isinstance(value, (re.Pattern, Regex, RegexPattern))


_DESIGN_NOTES = """
# is_pattern — "Something to Search For"

The rule behind `Pattern`. The empty string is the only `str` that is refused:
as a literal it matches at every position, so `remove_matches(text, "")` would
"succeed" and change nothing, or `keep_matches` would return a pile of nothing.
Better to fail at the signature.

## Why It Does Not Compile
The predicate only answers "is this the right kind of thing". Whether a `Regex`
tree renders into a valid pattern is known only after rendering, and that is
reported by `compile_pattern` with its own card.

## `RegexPattern`
It is accepted as it is. A `RegexPattern` built with `lazy=True` is compiled on
first use, so its own card (from `simplibs-regex`) appears then, not here.
"""
