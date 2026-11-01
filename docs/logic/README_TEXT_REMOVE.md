# 🧹 `logic/remove` — Take Something Away

The `remove` package holds the functions that **take something out of a text**: the matches of a
pattern, whole lines, given character ranges, and the blank space that is left behind. Two of them
find *what* to remove (`remove_matches`, `remove_lines_matching`); one is told (`remove_spans`);
the rest tidy whitespace (`remove_empty_lines`, `strip_trailing_spaces`, `squeeze_blank_lines`,
`trim_blank_edges`, `dedent`).

```python
from simplibs.text import (
    remove_spans, remove_matches, remove_lines_matching, remove_empty_lines,
    strip_trailing_spaces, squeeze_blank_lines, trim_blank_edges, dedent,
)
```

Every function takes the **text first** and returns a **new text**; none of them touches a file.
Each is wrapped in `@validate_call`, so an argument of the wrong type (or an empty `str` as a
[`Pattern`](../README_TEXT_ANNOTATIONS.md#pattern)) is rejected with a `ValidationError` before the
body runs. Each has an [action](../README_TEXT_ACTIONS.md#remove) counterpart for pipelines.

## Who finds, who cuts

| Function                | Finds what to remove by …           | Removes …                              |
|-------------------------|-------------------------------------|----------------------------------------|
| `remove_spans`          | **you** — `(start, end)` positions  | exactly those characters               |
| `remove_matches`        | a pattern                           | each match, the rest of its line stays |
| `remove_lines_matching` | a pattern                           | the **whole line** of each match       |
| `remove_empty_lines`    | blankness                           | every blank line                       |
| `squeeze_blank_lines`   | runs of blank lines                 | all but the first few of each run      |
| `trim_blank_edges`      | blank lines at the start and the end| only those                             |
| `strip_trailing_spaces` | spaces and tabs at a line's end     | only those                             |
| `dedent`                | the indentation all lines share     | that common part                       |

`remove_matches` and `remove_spans` end in **the same cutting code**. A comment cut out by a regex
and a docstring cut out by a parser (which hands over its positions) therefore behave identically.

## A note on lines

* Only `"\n"` separates lines — `read_text` of `simplibs-file` already hands over that ending.
  The characters `\x0b`, `\x0c`, `\x1c`, `\u2028` and the like are ordinary content here, not
  line breaks (which is why `str.splitlines()` is not used).
* **The final newline is remembered.** A text that ended with `"\n"` still does, and one that did
  not still does not. Removing every line leaves the empty text `""`, never a lone newline.
* **A line is blank** when it is empty or holds only whitespace (`line.strip() == ""`). One
  definition for all of these functions, so they never disagree about a line with a single space.
* **Nothing to do, nothing changed.** A function that finds nothing to remove returns the very
  same text (the same object, not a copy).

## A note on emptied lines

`remove_matches` and `remove_spans` have `drop_emptied_lines=True` by default: a line that became
blank **because of** the removal disappears whole, so a full-line comment leaves no hole. Blank
lines that were in the text from the start **stay**. A removed span may contain newlines (a
docstring over five lines): what is left before and after it is joined into one line, and that
one line is judged as a whole.

```python
remove_matches("a\n\n# c\nb\n", re.compile(r"#.*"))                              # -> 'a\n\nb\n'     the comment line is gone, the original blank line stays
remove_matches("a\n\n# c\nb\n", re.compile(r"#.*"), drop_emptied_lines=False)    # -> 'a\n\n\nb\n'    a plain cut
```

## A note on what a pattern knows

A pattern knows nothing about a language. A regex for `#` comments also removes the `#` inside
the string `'a # b'`. Correct removal in source code needs a real parser that finds the positions
and hands them to `remove_spans` — that is what `remove_spans` is for.

---

## 🧭 Table of Contents

* [`remove_spans`](#remove_spans)
* [`remove_matches`](#remove_matches)
* [`remove_lines_matching`](#remove_lines_matching)
* [`remove_empty_lines`](#remove_empty_lines)
* [`strip_trailing_spaces`](#strip_trailing_spaces)
* [`squeeze_blank_lines`](#squeeze_blank_lines)
* [`trim_blank_edges`](#trim_blank_edges)
* [`dedent`](#dedent)
* [Errors of this package](#errors-of-this-package)

[⬅️ Back to main README](../../README.md#-logicremove--take-something-away)

---

### `remove_spans`

Cuts given character ranges out of a text — the shared primitive for everything that **finds** what
to remove in its own way (a regex, a parser, a tokenizer).

**Parameters:**

* `text` (*str*): The text.
* `spans` (*Sequence[Span]*): [`Span`](../README_TEXT_ANNOTATIONS.md#span) pairs `(start, end)`, **half-open** — `text[start:end]` is
  removed, exactly as `re.Match.span()`, `ast` offsets and slices work, so values can be passed
  straight through. Any order; overlapping and touching spans are merged; empty spans
  (`start == end`) are ignored.
* `drop_emptied_lines` (*bool*, keyword-only, default `True`): A line that is blank only because of
  the removal disappears whole. Blank lines that were there before stay.

**Returns:**

* `str`: The text without the spans; the same text if there is nothing to remove.

**Raises:**

* `ParamError` (`TEXT_SPAN_INVALID`): A span does not satisfy `0 <= start <= end <= len(text)`.

**Example usage:**

```python
remove_spans("hello world", [(0, 6)])                      # -> 'world'
remove_spans("hello world", [(8, 11), (0, 2), (1, 4)])     # -> 'o wo'      any order, the overlap is merged
remove_spans("a\n# c\nb\n", [(2, 5)])                      # -> 'a\nb\n'    the emptied line is gone
remove_spans("a\n# c\nb\n", [(2, 5)], drop_emptied_lines=False)   # -> 'a\n\nb\n'
remove_spans("keep\n\nme\n", [(5, 5)])                     # -> 'keep\n\nme\n'   an empty span removes nothing, the blank line stays
remove_spans("ab\n", [(0, 2), (2, 3)])                     # -> ''          touching spans become one
remove_spans("ab", [(1, 5)])                               # raises ParamError (TEXT_SPAN_INVALID)

# a multi-line docstring, cut out by its positions
source = 'def f():\n    """doc\nmore"""\n    return 1\n'
start = source.index('"""')
end = source.rindex('"""') + 3
remove_spans(source, [(start, end)])                       # -> 'def f():\n    return 1\n'
```

**Under the hood:**

```python
@validate_call
def remove_spans(text: str, spans: Sequence[Span], *, drop_emptied_lines: bool = True) -> str:
    merged = normalize_spans(spans, len(text))        # check, drop empty ones, sort, merge
    if not merged:
        return text                                   # nothing to remove — the very same text back
    return cut_spans(text, merged, drop_emptied_lines)
```

`normalize_spans` makes the callers' life easy: a tokenizer may report a decorator inside a class, a
regex may match a comment twice through two alternatives, and `(0, 3)` with `(3, 5)` becomes `(0, 5)`
so that one continuous removal marks its line as emptied once, not twice. Empty spans are dropped on
purpose: otherwise a zero-length regex match (for example `^`) would flag lines as "emptied" without
changing them, and `drop_emptied_lines` would delete original blank lines. `cut_spans` works with
**positions**, not with a marker character, so it has no reserved character and no restriction on
the input — a text may contain `"\x00"` or anything else. `@validate_call` checks every pair; for
thousands of spans in one file that is still cheap next to parsing the file.

[▲ Back to top](#-table-of-contents)

---

### `remove_matches`

Removes every match of a pattern from a text.

**Parameters:**

* `text` (*str*): The text.
* `pattern` ([*Pattern*](../README_TEXT_ANNOTATIONS.md#pattern)): A literal `str`, a compiled
  `re.Pattern`, a `Regex` tree or a `RegexPattern`. A `str` is searched for **literally**.
* `flags` (*int*, keyword-only, default `0`): `re` flags (`re.IGNORECASE`, ...). They work with a
  `str` literal too. Not allowed together with a compiled pattern (`re.Pattern` or `RegexPattern`), which carries its own.
* `drop_emptied_lines` (*bool*, keyword-only, default `True`): A line that is blank only because of
  the removal disappears whole. Blank lines that were there before stay.

**Returns:**

* `str`: The text without the matches; the same text if nothing matched.

**Raises:**

* `ParamError` (`TEXT_PATTERN_COMPILE_FAILED`): The pattern or the flags cannot be compiled.
* `ParamError` (`TEXT_PATTERN_FLAGS_CONFLICT`): `flags` were given with a compiled pattern.

**Example usage:**

```python
remove_matches("a.b a.b\nA.B\n", "a.b")                    # -> 'A.B\n'       a str is literal: "a.b" does not match "aXb"
remove_matches("a(b)c", "(b)")                              # -> 'ac'          nothing needs escaping
remove_matches("Abc xyz", "abc", flags=re.IGNORECASE)       # -> ' xyz'
remove_matches("a # b\n", "# b")                            # -> 'a \n'        the rest of the line stays (see strip_trailing_spaces)
remove_matches("x = 1\n", re.compile(r"a*"))                # -> 'x = 1\n'     an empty match removes nothing
remove_matches("zzz", "a")                                  # -> 'zzz'         the very same text back
remove_matches("a", re.compile("a"), flags=re.I)            # raises ParamError (TEXT_PATTERN_FLAGS_CONFLICT)

remove_matches("a\n\n# c\nb\n", re.compile(r"#.*"))         # -> 'a\n\nb\n'   the comment-only line is gone, the original blank line stays
remove_matches("print('a # b')  # c\n", re.compile(r"#.*")) # -> "print('a \n"   a pattern does not know about strings
```

**Under the hood:**

```python
@validate_call
def remove_matches(text: str, pattern: Pattern, *, flags: int = 0, drop_emptied_lines: bool = True) -> str:
    compiled = compile_pattern(pattern, flags)                                        # one door for every kind of pattern
    spans = normalize_spans([m.span() for m in compiled.finditer(text)], len(text))  # empty matches are dropped here
    if not spans:
        return text
    return cut_spans(text, spans, drop_emptied_lines)
```

`compile_pattern` is shared by every function that searches: a `str` goes through `re.escape`
(hence "literal"), a `Regex` tree renders itself with `to_pattern()`, a `RegexPattern` hands over the
`re.Pattern` it holds, and a compiled pattern is used as it is. Flags with a compiled pattern are **refused with a card** rather than silently ignored,
because `remove_matches(text, re.compile("a"), flags=re.I)` is almost certainly a mistake.

[▲ Back to top](#-table-of-contents)

---

### `remove_lines_matching`

Removes every line that contains a match of a pattern — the **whole line**, even if the match is
only a part of it.

**Parameters:**

* `text` (*str*): The text.
* `pattern` ([*Pattern*](../README_TEXT_ANNOTATIONS.md#pattern)): A literal `str`, a compiled
  `re.Pattern`, a `Regex` tree or a `RegexPattern`.
* `flags` (*int*, keyword-only, default `0`): `re` flags; not allowed with a compiled pattern.

**Returns:**

* `str`: The text without the matching lines; the same text if no line matched.

**Raises:**

* `ParamError` (`TEXT_PATTERN_COMPILE_FAILED`): The pattern or the flags cannot be compiled.
* `ParamError` (`TEXT_PATTERN_FLAGS_CONFLICT`): `flags` were given with a compiled pattern.

**Example usage:**

```python
remove_lines_matching("import os\nx = 1\nimport re\n", "import ")   # -> 'x = 1\n'
remove_lines_matching("a\n  # c\nb\n", re.compile(r"^\s*#"))         # -> 'a\nb\n'    ^ is the start of a line, no re.MULTILINE needed
remove_lines_matching("a\nb", "a")                                    # -> 'b'       no final newline before, none after
remove_lines_matching("a\nb\n", "a")                                  # -> 'b\n'
```

**Under the hood:**

```python
@validate_call
def remove_lines_matching(text: str, pattern: Pattern, *, flags: int = 0) -> str:
    compiled = compile_pattern(pattern, flags)
    lines, has_end = split_lines(text)
    kept = [line for line in lines if not compiled.search(line)]
    if len(kept) == len(lines):
        return text                                   # nothing matched — the very same text back
    return join_lines(kept, has_end)
```

The pattern is searched in **each line separately**, so `^` and `$` mean the start and the end of a
line without `re.MULTILINE`, and a match can never span lines. Compare with
[`remove_matches`](#remove_matches), which cuts out the match and leaves the rest of the line; its
mirror is [`keep_lines_matching`](README_TEXT_KEEP.md#keep_lines_matching) — the two split any text
between them, with no line lost and none counted twice.

[▲ Back to top](#-table-of-contents)

---

### `remove_empty_lines`

Removes every line that is empty or holds only whitespace — the compact form of a text.

**Parameters:**

* `text` (*str*): The text.

**Returns:**

* `str`: The text without blank lines; the same text if there were none. Running it twice gives the
  same result.

**Example usage:**

```python
remove_empty_lines("a\n\n  \n\tb\n")     # -> 'a\n\tb\n'
remove_empty_lines(" \n\n")              # -> ''
```

**Under the hood:**

```python
@validate_call
def remove_empty_lines(text: str) -> str:
    lines, has_end = split_lines(text)
    kept = [line for line in lines if not is_blank(line)]
    if len(kept) == len(lines):
        return text
    return join_lines(kept, has_end)
```

For a gentler cleanup — one blank line between blocks — use [`squeeze_blank_lines`](#squeeze_blank_lines).
`squeeze_blank_lines(text, max_consecutive=0)` is the same as this function, so the two never
disagree.

[▲ Back to top](#-table-of-contents)

---

### `strip_trailing_spaces`

Removes spaces and tabs from the end of every line.

**Parameters:**

* `text` (*str*): The text.

**Returns:**

* `str`: The text with clean line ends; the same text if nothing changed. Running it twice gives the
  same result.

**Example usage:**

```python
strip_trailing_spaces("a  \nb\t\n c")          # -> 'a\nb\n c'     the leading space of " c" stays
strip_trailing_spaces("a\u00a0\nb\x0c")        # -> 'a\xa0\nb\x0c'  only spaces and tabs are noise
```

**Under the hood:**

```python
@validate_call
def strip_trailing_spaces(text: str) -> str:
    lines, has_end = split_lines(text)
    stripped = [line.rstrip(" \t") for line in lines]
    if stripped == lines:
        return text
    return join_lines(stripped, has_end)
```

`str.rstrip()` without an argument would also remove `\x0b`, `\x0c`, `\u00a0` and other characters
that are real content in some files. "Trailing whitespace" in the editor sense is a space or a tab,
and that is all this removes.

[▲ Back to top](#-table-of-contents)

---

### `squeeze_blank_lines`

Shortens every run of blank lines to at most `max_consecutive` lines.

**Parameters:**

* `text` (*str*): The text.
* `max_consecutive` (*int_non_negative*, default `1`): How many blank lines in a row may stay.
  `0` removes them all.

**Returns:**

* `str`: The text with shorter runs of blank lines; the same text if no run was too long. Running it
  twice gives the same result.

**Example usage:**

```python
squeeze_blank_lines("a\n\n\n\nb\n\n\nc\n")       # -> 'a\n\nb\n\nc\n'
squeeze_blank_lines("a\n\n\n\nb\n", 2)           # -> 'a\n\n\nb\n'
squeeze_blank_lines("a\n\n\n\nb\n", 0)           # -> 'a\nb\n'       the same as remove_empty_lines
squeeze_blank_lines("a\n\n\nb\n\n\n\n")          # -> 'a\n\nb\n\n'   a run at the end is shortened too
squeeze_blank_lines("a\n   \n\nb\n")             # -> 'a\n   \nb\n'  the first line of the run stays — here the one with spaces
```

**Under the hood:**

```python
@validate_call
def squeeze_blank_lines(text: str, max_consecutive: int_non_negative = 1) -> str:
    lines, has_end = split_lines(text)
    kept, run = [], 0
    for line in lines:
        run = run + 1 if is_blank(line) else 0          # blank lines in a row
        if run <= max_consecutive:
            kept.append(line)
    if len(kept) == len(lines):
        return text
    return join_lines(kept, has_end)
```

Code with three blank lines between functions becomes code with one. The **first** lines of a run
stay and the rest is dropped; as the content of a blank line does not matter, a whitespace-only line
may stay while an empty one goes. Combine with [`strip_trailing_spaces`](#strip_trailing_spaces) (or
use the `CLEANUP_WHITESPACE` [preset](../README_TEXT_PRESETS.md)) when the exact result matters.

[▲ Back to top](#-table-of-contents)

---

### `trim_blank_edges`

Removes blank lines from the start and from the end of a text; the inside is left alone.

**Parameters:**

* `text` (*str*): The text.

**Returns:**

* `str`: The text without leading and trailing blank lines; the same text if there were none.
  A text made only of blank lines becomes `""`. Running it twice gives the same result.

**Example usage:**

```python
trim_blank_edges("\n  \na\n\nb\n\n\n")    # -> 'a\n\nb\n'     the blank line between a and b stays
trim_blank_edges("\na")                  # -> 'a'            no final newline before, none after
trim_blank_edges("\n\n")                 # -> ''
```

**Under the hood:**

```python
@validate_call
def trim_blank_edges(text: str) -> str:
    lines, has_end = split_lines(text)
    first = 0
    while first < len(lines) and is_blank(lines[first]):
        first += 1
    last = len(lines)
    while last > first and is_blank(lines[last - 1]):
        last -= 1
    if first == 0 and last == len(lines):
        return text
    return join_lines(lines[first:last], has_end)
```

Useful after other steps removed content and the text begins or ends with an empty stretch.

[▲ Back to top](#-table-of-contents)

---

### `dedent`

Removes the indentation that every non-blank line has in common.

**Parameters:**

* `text` (*str*): The text.

**Returns:**

* `str`: The text moved to the left. Whitespace-only lines become empty lines.

**Example usage:**

```python
dedent("    def f():\n        return 1\n")   # -> 'def f():\n    return 1\n'   the body of a function cut out of a class
dedent("    a\n   \n    b\n")                # -> 'a\n\nb\n'                  the whitespace-only line is ignored, then emptied
dedent("  a\n b\n")                          # -> ' a\nb\n'                  only the common one space goes
dedent("\ta\n    b\n")                       # -> '\ta\n    b\n'             a tab and spaces are different characters: nothing in common
```

**Under the hood:**

```python
@validate_call
def dedent(text: str) -> str:
    return textwrap.dedent(text)                      # the standard library already does exactly this
```

`textwrap.dedent` turns whitespace-only lines into empty lines and ignores them when it looks for the
common indentation. That is intended and not hidden: the result of `dedent` on an already flush-left
text that has such lines is **not** byte-identical to the input.

[▲ Back to top](#-table-of-contents)

---

## Errors of this package

These functions raise `ParamError` cards of [`simplibs-exception`](https://pypi.org/project/simplibs-exception/);
the package defines no exceptions of its own. The card's `label` names the offending parameter and
its `value` is what was given.

| Error name                    | Wraps        | Raised by                                    | Fix                                                                    |
|-------------------------------|--------------|----------------------------------------------|------------------------------------------------------------------------|
| `TEXT_SPAN_INVALID`           | `ValueError` | `remove_spans`                               | Measure the spans on exactly this text; measure again if it was changed |
| `TEXT_PATTERN_COMPILE_FAILED` | `ValueError` | `remove_matches`, `remove_lines_matching`    | Check the pattern and the flags; pass plain text as a `str` to search it literally |
| `TEXT_PATTERN_FLAGS_CONFLICT` | `ValueError` | `remove_matches`, `remove_lines_matching`    | Put the flags into `re.compile(...)` or `RegexPattern(tree, flags=...)` instead of passing `flags=`        |

An argument of the wrong type is a `ValidationError` from `@validate_call` and never reaches these.

[▲ Back to top](#-table-of-contents)
