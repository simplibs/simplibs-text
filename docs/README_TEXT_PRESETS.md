# 🧩 `presets` — Ready-Made Pipeline Steps

The `presets` package holds **chains of actions, built once**: the two cleanups of
[`recipes`](logic/README_TEXT_RECIPES.md) in the form of a pipeline step. Where a recipe is a
*function* you call on a text, a preset is an *object* you drop into a pipeline:

```python
import re
from simplibs.text.actions import RemoveMatches
from simplibs.text.presets import CLEANUP_WHITESPACE, COMPACT

strip_comments = RemoveMatches(pattern=re.compile(r"#.*")) >> CLEANUP_WHITESPACE
strip_comments("a  # c\n\n\n# d\n\n\nb\n")          # -> 'a\n\nb\n'
```

Presets are **not** exported from `simplibs.text` itself or from `simplibs.text.actions` — they are a
domain of their own, imported through `simplibs.text.presets`, which defines `__all__`. They stand at
the very top of the layers (`annotations` ← `logic` ← `actions` ← `presets`) because a preset is
built **from actions**.

## The two presets

| Preset               | Chain                                                                              | Function form        |
|----------------------|------------------------------------------------------------------------------------|----------------------|
| `CLEANUP_WHITESPACE` | `StripTrailingSpaces() >> SqueezeBlankLines(max_consecutive=1) >> TrimBlankEdges()` | `cleanup_whitespace` |
| `COMPACT`            | `StripTrailingSpaces() >> RemoveEmptyLines()`                                      | `compact`            |

For every text the preset and its function form give **exactly the same result**; the preset is the
one to use when the cleanup is a *step* in a longer chain, the function when it is a plain call.

## A note on sharing one object

A preset is created **once**, at import, and used wherever it is needed. That is safe because an
action holds only its options and no state between calls, so the same object can serve any number of
pipelines. Each is declared `Final`, so a type checker stops an
accidental reassignment.

## A note on the last pass

A preset is the usual **last pass**: other steps — a removal, a replacement — leave holes and trailing
spaces behind, and one step at the end puts the text in order. `RemoveMatches(...) >> CLEANUP_WHITESPACE`
is the whole idiom.

---

## 🧭 Table of Contents

* [`CLEANUP_WHITESPACE`](#cleanup_whitespace)
* [`COMPACT`](#compact)
* [Errors of this package](#errors-of-this-package)

[⬅️ Back to main README](../README.md#-presets--ready-made-chains)

---

### `CLEANUP_WHITESPACE`

Tidies the whitespace of a text without removing its structure: no trailing spaces, at most one blank
line in a row, no blank lines at the start and at the end. Paragraphs stay.

**Main input:** the text (`str`). **Returns:** `str`.

**Example usage:**

```python
CLEANUP_WHITESPACE("a  \n\n\n\nb \n\n")                  # -> 'a\n\nb\n'
CLEANUP_WHITESPACE("\n\n  a\n  \n\n b\t\n")              # -> '  a\n\n b\n'     the indentation stays

# the usual last pass
(RemoveMatches(pattern="# ") >> CLEANUP_WHITESPACE)("# a  \n\n\n\n# b  \n")     # -> 'a\n\nb\n'
```

<details>
<summary>🔍 Under the hood</summary>

```python
CLEANUP_WHITESPACE: Final = (
    StripTrailingSpaces()
    >> SqueezeBlankLines(max_consecutive=1)
    >> TrimBlankEdges()
)
```

The order matters for the same reason as in [`cleanup_whitespace`](logic/README_TEXT_RECIPES.md#a-note-on-order):
the line ends are stripped first, so the one blank line that survives a run is truly empty.

</details>

[▲ Back to top](#-table-of-contents)

---

### `COMPACT`

Makes a text as short as whitespace allows: no trailing spaces, no blank lines at all.

**Main input:** the text (`str`). **Returns:** `str`.

**Example usage:**

```python
COMPACT("a  \n\n\n\nb \n\n")                             # -> 'a\nb\n'
COMPACT("\n\n  a\n  \n\n b\t\n")                         # -> '  a\n b\n'       the indentation stays
```

<details>
<summary>🔍 Under the hood</summary>

```python
COMPACT: Final = (
    StripTrailingSpaces()
    >> RemoveEmptyLines()
)
```

There is no third step: after `RemoveEmptyLines` no blank line is left, so there is nothing at the
edges to trim.

</details>

[▲ Back to top](#-table-of-contents)

---

## Errors of this package

This package raises **no cards of its own** and takes no options: a preset accepts any text. An
argument that is not a `str` is a `ValidationError` from the action that receives it.

[▲ Back to top](#-table-of-contents)
