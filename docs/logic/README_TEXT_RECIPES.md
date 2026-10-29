# 🍳 `logic/recipes` — Ready-Made Combinations

The `recipes` package holds the **two cleanups people reach for most often**, built once from the
functions of [`remove`](README_TEXT_REMOVE.md): `cleanup_whitespace` tidies a text, `compact` makes
it as short as whitespace allows. A recipe is the one place in `logic/` that looks *sideways* — it
**combines** other functions, so it stands above them (`recipes` imports `remove`, never the other
way round).

```python
from simplibs.text import cleanup_whitespace, compact
```

Both take the **text first** and return a **new text**; neither touches a file. Each is wrapped in
`@validate_call`, so an argument of the wrong type is rejected with a `ValidationError` before the
body runs. They have no action counterpart — their counterparts are the two chains
`CLEANUP_WHITESPACE` and `COMPACT` in the [presets](../README_TEXT_PRESETS.md), which give the same
result inside a pipeline.

## Tidy, or compact

| Function             | Trailing spaces and tabs | Runs of blank lines              | Blank lines at the edges |
|----------------------|--------------------------|----------------------------------|--------------------------|
| `cleanup_whitespace` | removed                  | shortened to **one**             | removed                  |
| `compact`            | removed                  | **all** removed                  | removed (they are blank lines too) |

`cleanup_whitespace` is what an editor's "clean up" does: invisible noise goes, the **paragraphs
stay**. `compact` is the stronger sibling for a prompt or a report where every line counts. Both
leave the content of the lines — including their indentation — untouched.

## A note on order

Both start with [`strip_trailing_spaces`](README_TEXT_REMOVE.md#strip_trailing_spaces). A line made
of spaces already counts as blank for `squeeze_blank_lines`, but that function keeps the **first**
line of a run as it is — so without the strip the one blank line that survives could still be a line
of spaces. Stripped first, it is a truly empty line.

## A note on nothing to do

A text that is already tidy comes back as the very same text, and running either function twice gives
the same result.

---

## 🧭 Table of Contents

* [`cleanup_whitespace`](#cleanup_whitespace)
* [`compact`](#compact)
* [Errors of this package](#errors-of-this-package)

[⬅️ Back to main README](../../README.md#-logicrecipes--ready-made-combinations)

---

### `cleanup_whitespace`

Tidies the whitespace of a text without removing its structure: trailing spaces and tabs go, runs of
blank lines shrink to one, and blank lines at the start and at the end go.

**Parameters:**

* `text` (*str*): The text.

**Returns:**

* `str`: The tidied text; the same text if it was tidy. Running it twice gives the same result.

**Example usage:**

```python
cleanup_whitespace("a  \n\n\n\nb \n\n")               # -> 'a\n\nb\n'
cleanup_whitespace("\n\n  a\n  \n\n b\t\n")           # -> '  a\n\n b\n'      the indentation stays, the line of spaces became the one blank line
cleanup_whitespace("  x\n\n\n\n  y")                  # -> '  x\n\n  y'       no final newline before, none after
cleanup_whitespace("\n\n")                            # -> ''
cleanup_whitespace("a\nb\n")                          # -> 'a\nb\n'           already tidy: the very same text back
```

**Under the hood:**

```python
@validate_call
def cleanup_whitespace(text: str) -> str:
    cleaned = strip_trailing_spaces(text)             # line ends first: a line of spaces becomes an empty line
    cleaned = squeeze_blank_lines(cleaned, 1)         # one blank line between blocks, never more
    return trim_blank_edges(cleaned)                  # a clean start and a clean end
```

The same chain exists as the preset `CLEANUP_WHITESPACE`:
`StripTrailingSpaces() >> SqueezeBlankLines(max_consecutive=1) >> TrimBlankEdges()`.

[▲ Back to top](#-table-of-contents)

---

### `compact`

Makes a text as short as whitespace allows: no trailing spaces, no blank lines.

**Parameters:**

* `text` (*str*): The text.

**Returns:**

* `str`: The compacted text; the same text if it was compact. Running it twice gives the same result.

**Example usage:**

```python
compact("a  \n\n\n\nb \n\n")                          # -> 'a\nb\n'
compact("\n\n  a\n  \n\n b\t\n")                      # -> '  a\n b\n'        the indentation stays
compact("  x\n\n\n\n  y")                             # -> '  x\n  y'
compact("\n\n")                                       # -> ''
compact("a\nb\n")                                     # -> 'a\nb\n'           already compact: the very same text back
```

**Under the hood:**

```python
@validate_call
def compact(text: str) -> str:
    compacted = strip_trailing_spaces(text)           # line ends
    return remove_empty_lines(compacted)              # no blank lines at all — this covers the edges too
```

There is no third step: after `remove_empty_lines` no blank line is left, so there is nothing at the
edges to trim. The same chain exists as the preset `COMPACT`:
`StripTrailingSpaces() >> RemoveEmptyLines()`.

[▲ Back to top](#-table-of-contents)

---

## Errors of this package

This package raises **no cards of its own**: both recipes accept any text, so there is no invalid
value to report. An argument of the wrong type is a `ValidationError` from `@validate_call` and never
reaches the body.

[▲ Back to top](#-table-of-contents)
