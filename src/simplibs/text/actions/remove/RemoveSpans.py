from simplibs.actions import create_action
# Outers
from ...logic.remove import remove_spans


RemoveSpans = create_action(
    remove_spans,
    main_param="text",
    class_name="RemoveSpans",
)
"""Action wrapping `remove_spans` — cuts the given character ranges out of the text flowing in."""


_DESIGN_NOTES = """
# RemoveSpans — Action Over `remove_spans`

## Purpose
A tokenizer finds the spans, `RemoveSpans(spans=found)` cuts them: `Tokenize() >> RemoveSpans(spans=...)` style steps.

## Shape
Main input: `text`. Options: `spans` (required), `drop_emptied_lines`. Text in, text out.
"""
