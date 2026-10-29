# 🎯 `logic/keep` — Keep Only a Chosen Part

The `keep` package holds the functions that **keep what you name and drop the rest**: the matches
of a pattern, the lines that contain one, a range of lines, or the parts between two markers. It is
the opposite verb of [`remove`](README_TEXT_REMOVE.md) — and the only other verb the library has, so
a step either removes or keeps, never "extracts", "highlights" or "copies".

```python
from simplibs.text import keep_matches, keep_lines_matching, keep_line_range, keep_between
```

Every function takes the **text first** and returns a **new text**; none of them touches a file.
Each is wrapped in `@validate_call`, so an argument of the wrong type (or an empty `str` as a
[`Pattern`](../README_TEXT_ANNOTATIONS.md#pattern)) is rejected with a `ValidationError` before the
body runs. Each has an [action](../README_TEXT_ACTIONS.md#keep) counterpart for pipelines.

## Whole text, whole lines, or pieces

| Function              | Keeps …                                   | The result is …                                            |
|-----------------------|-------------------------------------------|------------------------------------------------------------|
| `keep_matches`        | only the **matches** themselves           | the pieces joined by a separator — the text around is gone |
| `keep_lines_matching` | the **whole lines** that contain a match  | a text of the original lines                               |
| `keep_line_range`     | the lines `start` … `end`                 | a text of the original lines                               |
| `keep_between`        | the parts from a **start marker** to an **end marker** | the parts joined by a separator, may span lines |

## A note on lines

* Only `"\n"` separates lines — `read_text` of `simplibs-file` already hands over that ending. The
  line functions (`keep_lines_matching`, `keep_line_range`) remember the final newline: a text that
  ended with one still does, one that did not still does not. Keeping no line gives `""`.
* `keep_lines_matching` returns the very same text when every line was kept.
* The pattern of `keep_lines_matching` is searched in **each line separately**, so `^` and `$` mean
  the start and the end of a line without `re.MULTILINE`. `keep_matches` and `keep_between`, on the
  contrary, look at the **whole text** at once, so their matches and markers may span lines.

## A note on empty matches

A pattern that can match nothing (`a*`) matches an empty string at every position. Those matches
carry nothing to keep, so `keep_matches` skips them (otherwise every position would add an empty piece
and a separator), and `keep_between` always moves at least one character forward so that it can never
loop forever.

---

## 🧭 Table of Contents

* [`keep_matches`](#keep_matches)
* [`keep_lines_matching`](#keep_lines_matching)
* [`keep_line_range`](#keep_line_range)
* [`keep_between`](#keep_between)
* [Errors of this package](#errors-of-this-package)

[⬅️ Back to main README](../../README.md#-logickeep--keep-only-a-chosen-part)

---

### `keep_matches`

Keeps only the matches of a pattern — pulls the pieces out of a text: all the function names, all the
numbers. The opposite of [`remove_matches`](README_TEXT_REMOVE.md#remove_matches).

**Parameters:**

* `text` (*str*): The text.
* `pattern` ([*Pattern*](../README_TEXT_ANNOTATIONS.md#pattern)): A literal `str`, a compiled
  `re.Pattern`, a `Regex` tree or a `RegexPattern`. A `str` is searched for **literally**.
* `flags` (*int*, keyword-only, default `0`): `re` flags. They work with a `str` literal too. Not
  allowed together with a compiled pattern (`re.Pattern` or `RegexPattern`), which carries its own.
* `separator` (*str*, keyword-only, default `"\n"`): What goes between the matches.

**Returns:**

* `str`: The matches joined with the separator; an empty text if nothing matched.

**Raises:**

* `ParamError` (`TEXT_PATTERN_COMPILE_FAILED`): The pattern or the flags cannot be compiled.
* `ParamError` (`TEXT_PATTERN_FLAGS_CONFLICT`): `flags` were given with a compiled pattern.

**Example usage:**

```python
keep_matches("def a(): def bb():", re.compile(r"def \w+"))       # -> 'def a\ndef bb'
keep_matches("a1 b22 c333", re.compile(r"\d+"), separator=", ")   # -> '1, 22, 333'
keep_matches("a1 b22", re.compile(r"\d+"), separator="")          # -> '122'
keep_matches("Abc abc", "abc", flags=re.IGNORECASE)               # -> 'Abc\nabc'
keep_matches("x a* y", "a*")                                      # -> 'a*'    a str is literal: the text "a*", not "zero or more a"
keep_matches("abc", r"\d")                                        # -> ''      nothing matched; the str is literal, so this looks for the characters \d
keep_matches("ab", re.compile(r"a*"))                             # -> 'a'     the empty matches are skipped
```

**Under the hood:**

```python
@validate_call
def keep_matches(text: str, pattern: Pattern, *, flags: int = 0, separator: str = "\n") -> str:
    compiled = compile_pattern(pattern, flags)        # one door for every kind of pattern
    found = [m.group(0) for m in compiled.finditer(text) if m.end() > m.start()]    # empty matches carry nothing
    return separator.join(found)
```

The result is a list of pieces joined with the separator, **not** the original text with everything
else blanked out — the text around the matches is gone, and so are their positions. A text that has
no match gives `""`, not the original.

[▲ Back to top](#-table-of-contents)

---

### `keep_lines_matching`

Keeps only the lines that contain a match of a pattern — whole lines. `keep_lines_matching(source,
"def ")` is an outline of a file.

**Parameters:**

* `text` (*str*): The text.
* `pattern` ([*Pattern*](../README_TEXT_ANNOTATIONS.md#pattern)): A literal `str`, a compiled
  `re.Pattern`, a `Regex` tree or a `RegexPattern`.
* `flags` (*int*, keyword-only, default `0`): `re` flags; not allowed with a compiled pattern.

**Returns:**

* `str`: The matching lines, whole; an empty text if none matches; the same text if every line
  matches.

**Raises:**

* `ParamError` (`TEXT_PATTERN_COMPILE_FAILED`): The pattern or the flags cannot be compiled.
* `ParamError` (`TEXT_PATTERN_FLAGS_CONFLICT`): `flags` were given with a compiled pattern.

**Example usage:**

```python
keep_lines_matching("def a():\n    x\ndef b():\n", "def ")      # -> 'def a():\ndef b():\n'
keep_lines_matching("a\nb\n", "zzz")                              # -> ''
keep_lines_matching("a\nb", "b")                                  # -> 'b'      no final newline before, none after

# the mirror of remove_lines_matching: together they split a text, no line lost, none counted twice
keep_lines_matching("a\nb\nc\n", "b")                             # -> 'b\n'
remove_lines_matching("a\nb\nc\n", "b")                           # -> 'a\nc\n'
```

**Under the hood:**

```python
@validate_call
def keep_lines_matching(text: str, pattern: Pattern, *, flags: int = 0) -> str:
    compiled = compile_pattern(pattern, flags)
    lines, has_end = split_lines(text)
    kept = [line for line in lines if compiled.search(line)]
    if len(kept) == len(lines):
        return text                                   # every line kept — the very same text back
    return join_lines(kept, has_end)
```

The mirror of [`remove_lines_matching`](README_TEXT_REMOVE.md#remove_lines_matching); the pattern is
searched in each line separately, exactly as there.

[▲ Back to top](#-table-of-contents)

---

### `keep_line_range`

Keeps only the lines from `start` to `end` — a part of a file the way an editor numbers it: the first
line is 1 and **both ends are included**.

**Parameters:**

* `text` (*str*): The text.
* `start` ([*LineNumber*](../README_TEXT_ANNOTATIONS.md#linenumber), default `1`): The first line to
  keep, counted from 1. Zero, negatives and `bool` are rejected by `@validate_call`.
* `end` ([*LineNumber*](../README_TEXT_ANNOTATIONS.md#linenumber) `| None`, default `None`): The
  last line to keep (included); `None` means up to the last line.

**Returns:**

* `str`: The lines of the range. The result ends with a newline if the text did, also when the range
  stops in the middle of the text — each kept line is a closed line.

**Raises:**

* `ParamError` (`TEXT_LINE_RANGE_INVALID`): `end` is lower than `start`.

**Example usage:**

```python
keep_line_range("1\n2\n3\n4\n5\n", 2, 4)     # -> '2\n3\n4\n'
keep_line_range("1\n2\n3\n4\n5\n", 4)        # -> '4\n5\n'       from line 4 to the end
keep_line_range("1\n2\n3\n", 2, 2)           # -> '2\n'          one line
keep_line_range("1\n2\n3", 1, 2)             # -> '1\n2'         the text had no final newline, the result has none
keep_line_range("1\n2\n3\n", 2, 99)          # -> '2\n3\n'       an end past the last line is the same as end=None
keep_line_range("1\n2\n3\n", 5)              # -> ''             a start past the last line gives an empty text
keep_line_range("1\n2\n3\n", 3, 2)           # raises ParamError (TEXT_LINE_RANGE_INVALID)
```

**Under the hood:**

```python
@validate_call
def keep_line_range(text: str, start: LineNumber = 1, end: LineNumber | None = None) -> str:
    if end is not None and end < start:
        raise_invalid_line_range_error(start, end)    # a backwards range is a mistake, not an empty selection
    lines, has_end = split_lines(text)
    return join_lines(lines[start - 1:end], has_end)  # lines are counted from 1, both ends are included
```

A range that reaches **past the text** is not an error: a file may simply be shorter than the caller
hoped, and the caller usually cannot know that in advance. A range that runs **backwards** is, because
it can only come from a mistake (swapped values) — and the card says so.

[▲ Back to top](#-table-of-contents)

---

### `keep_between`

Keeps only the parts of a text between a start marker and an end marker — everything between
`# region` and `# endregion`, or between `<body>` and `</body>`.

**Parameters:**

* `text` (*str*): The text.
* `start` ([*Pattern*](../README_TEXT_ANNOTATIONS.md#pattern)): The marker where a kept part begins.
* `end` ([*Pattern*](../README_TEXT_ANNOTATIONS.md#pattern)): The marker where it ends; looked for
  **after** the start marker.
* `include_markers` (*bool*, keyword-only, default `True`): Keep the markers themselves too.
* `flags` (*int*, keyword-only, default `0`): `re` flags for **both** markers; not allowed with a
  compiled pattern.
* `separator` (*str*, keyword-only, default `"\n"`): What goes between the parts.

**Returns:**

* `str`: The parts joined with the separator; an empty text if there is none.

**Raises:**

* `ParamError` (`TEXT_PATTERN_COMPILE_FAILED`): A marker or the flags cannot be compiled.
* `ParamError` (`TEXT_PATTERN_FLAGS_CONFLICT`): `flags` were given with a compiled pattern.

**Example usage:**

```python
source = "a\n#region\nx\n#endregion\nb\n#region\ny\n#endregion\n"

keep_between(source, "#region", "#endregion")
# -> '#region\nx\n#endregion\n#region\ny\n#endregion'      two parts, joined by "\n"

keep_between(source, "#region", "#endregion", separator="\n---\n")
# -> '#region\nx\n#endregion\n---\n#region\ny\n#endregion'

keep_between(source, "#region", "#endregion", include_markers=False)
# -> '\nx\n\n\ny\n'      the markers are gone; the line breaks around the content are part of it

keep_between("<body>hi</body>", "<body>", "</body>", include_markers=False)     # -> 'hi'
keep_between("A 1 B A 2 B", "a", "b", flags=re.IGNORECASE)                       # -> 'A 1 B\nA 2 B'
keep_between("a (b) c", "(", ")", include_markers=False)                         # -> 'b'    markers are literals: no escaping

keep_between("#region\nx\n", "#region", "#endregion")      # -> ''    a start without an end is not a part
keep_between("S1 S2 E", "S", "E")                          # -> 'S1 S2 E'   the first start marker wins; the part runs to the first end marker after it
keep_between("a", "a", re.compile("b"), flags=re.I)        # raises ParamError (TEXT_PATTERN_FLAGS_CONFLICT)
```

**Under the hood:**

```python
@validate_call
def keep_between(text: str, start: Pattern, end: Pattern, *, include_markers: bool = True,
                 flags: int = 0, separator: str = "\n") -> str:
    start_pattern = compile_pattern(start, flags)
    end_pattern = compile_pattern(end, flags)

    parts, position = [], 0
    while position <= len(text):
        opening = start_pattern.search(text, position)
        if opening is None:
            break
        closing = end_pattern.search(text, opening.end())     # the first end marker AFTER the start marker
        if closing is None:
            break                                              # a start without an end ends the search
        if include_markers:
            parts.append(text[opening.start():closing.end()])
        else:
            parts.append(text[opening.end():closing.start()])
        position = max(closing.end(), opening.start() + 1)    # always at least one step forward

    return separator.join(parts)
```

Two searches instead of one combined regex: gluing the markers into `(start)(.*?)(end)` would use
only the **source** of a compiled marker and silently lose its flags. Searching for the start and then
for the end keeps each marker exactly as given, and a lookbehind in the end marker still sees the text
before it. **Parts do not overlap**: the search for the next start continues after the end marker.
Nothing here works line by line, so a marker may span lines.

[▲ Back to top](#-table-of-contents)

---

## Errors of this package

These functions raise `ParamError` cards of [`simplibs-exception`](https://pypi.org/project/simplibs-exception/);
the package defines no exceptions of its own. The card's `label` names the offending parameter and
its `value` is what was given.

| Error name                    | Wraps        | Raised by                                                   | Fix                                                                    |
|-------------------------------|--------------|-------------------------------------------------------------|------------------------------------------------------------------------|
| `TEXT_LINE_RANGE_INVALID`     | `ValueError` | `keep_line_range`                                           | Swap the values, or use `end=None` to keep everything from the start line on |
| `TEXT_PATTERN_COMPILE_FAILED` | `ValueError` | `keep_matches`, `keep_lines_matching`, `keep_between`       | Check the pattern and the flags; pass plain text as a `str` to search it literally |
| `TEXT_PATTERN_FLAGS_CONFLICT` | `ValueError` | `keep_matches`, `keep_lines_matching`, `keep_between`       | Put the flags into `re.compile(...)` or `RegexPattern(tree, flags=...)` instead of passing `flags=`        |

An argument of the wrong type is a `ValidationError` from `@validate_call` and never reaches these.

[▲ Back to top](#-table-of-contents)
