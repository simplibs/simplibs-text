from .convert_lines import convert_lines


_DESIGN_NOTES = """
# Case Conversion Sub-Package

## Purpose
The shared step of every case conversion. It stands above `split_words`
(it calls it), which is why it is not part of `_helpers`: `split_words` imports
`_helpers`, and a helper that imported `split_words` back would be a cycle.

## Internal Components Registry

| Component       | Type     | Description                                                |
| :-------------- | :------- | :--------------------------------------------------------- |
| `convert_lines` | Function | Rewrites each line as one identifier built from its words. |
"""
