from simplibs.actions import create_action
# Outers
from ...logic.keep import keep_matches


KeepMatches = create_action(
    keep_matches,
    main_param="text",
    class_name="KeepMatches",
)
"""Action wrapping `keep_matches` — keeps only the matches of a pattern, joined with a separator."""


_DESIGN_NOTES = """
# KeepMatches — Action Over `keep_matches`

## Purpose
`KeepMatches(pattern=re.compile(r"\\d+"))` — all the numbers of a text.

## Shape
Main input: `text`. Options: `pattern` (required), `flags`, `separator`. Text in, text out.
"""
