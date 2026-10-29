import re
from typing import Annotated
from simplibs.regex.base_class import Regex
from simplibs.regex.compiler import RegexPattern
# Inners
from ._helpers import is_pattern


Pattern = Annotated[str | re.Pattern | Regex | RegexPattern, is_pattern]
"""What to look for: a literal `str`, a compiled `re.Pattern`, a `Regex` tree or a `RegexPattern`. The empty string is rejected."""


_DESIGN_NOTES = """
# Pattern — Four Ways to Say "This"

## Purpose
The type of the `pattern` parameter in every function that looks for something.

## What Each Form Means
* **`str`** — a LITERAL. `"a.b"` finds `a.b`, not `a` + any character + `b`.
  The same rule `Literal` (`simplibs-regex`) and `Contains` (`simplibs-rules`)
  use, so there is no silent trap in `"("` or `"."`.
* **`re.Pattern`** — used as it is, with its own flags.
* **`Regex`** — a tree from `simplibs-regex` (and so any term from
  `simplibs-patterns`), rendered with `to_pattern()` and compiled.
* **`RegexPattern`** — the compiled wrapper of `simplibs-regex`. The
  `re.Pattern` inside it is used as it is, with the flags it was built with.

## Why `Annotated`
Same as `ByteCount` in `simplibs-file`: an editor sees a plain union and offers
hints, while `@validate_call` reads the predicate and checks the value.

## Flags
`flags=` belongs to the forms that are not compiled yet (`str`, `Regex`).
A `re.Pattern` and a `RegexPattern` already carry theirs, so `flags=` with
them is refused instead of being silently ignored.
"""
