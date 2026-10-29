# 🎀 `logic/decorate` — Add to or Reshape the Text

The `decorate` package holds the functions that **dress a text for its reader** without changing
what it says: numbers in the margin, an indent, a safe length, a line width. Where `remove` and
`keep` decide *which* parts of a text stay, these four change how the whole of it looks.

```python
from simplibs.text import add_line_numbers, indent, truncate, wrap
```

Every function takes the **text first** and returns a **new text**; none of them touches a file.
Each is wrapped in `@validate_call`, so an argument of the wrong type is rejected with a
`ValidationError` before the body runs. Each has an [action](../README_TEXT_ACTIONS.md#decorate)
counterpart for pipelines.

## What each one does to the lines

| Function           | Touches …                                   | Leaves alone …                                       |
|--------------------|---------------------------------------------|------------------------------------------------------|
| `add_line_numbers` | **every** line, blank ones too              | the text of the lines                                |
| `indent`           | every **non-blank** line                    | blank lines — no line is made of spaces only         |
| `truncate`         | the end of the text (lines first, then characters) | everything before the cut                      |
| `wrap`             | only lines **longer than** the width        | lines that fit — every character, tabs included      |

## A note on lines

* Only `"\n"` separates lines — `read_text` of `simplibs-file` already hands over that ending.
* **The final newline is remembered** by `add_line_numbers`, `indent` and `wrap`: a text that ended
  with `"\n"` still does, one that did not still does not. `truncate` is the exception on purpose:
  a shortened text ends with its marker (or with the cut), never with the original's newline.
* **Nothing to do, nothing changed.** `indent` with an empty prefix, `truncate` of a text that
  already fits and `wrap` of text with no long line return the very same text.

## A note on keyword-only options

`add_line_numbers` and `truncate` take **everything after the text** as keyword-only arguments, so a
call reads as what it does: `truncate(text, max_lines=40)`, never `truncate(text, 40)`. `wrap` keeps
`width` positional (`wrap(text, 72)`) and `indent` keeps `prefix` positional (`indent(text, 2)`) —
they have one obvious thing to say.

---

## 🧭 Table of Contents

* [`add_line_numbers`](#add_line_numbers)
* [`indent`](#indent)
* [`truncate`](#truncate)
* [`wrap`](#wrap)
* [Errors of this package](#errors-of-this-package)

[⬅️ Back to main README](../../README.md#-logicdecorate--add-to-or-reshape-the-text)

---

### `add_line_numbers`

Puts a number in front of every line, so a reader (or a model) can say "line 42" and mean the same
line.

**Parameters:**

* `text` (*str*): The text.
* `start` (*int_non_negative*, keyword-only, default `1`): The number of the first line. `1` is the
  way editors count; `0` is allowed for the programmer's count.
* `template` (*str*, keyword-only, default `"{number:>{width}}: {line}"`): A `str.format` template
  with exactly the fields `{number}`, `{line}` and `{width}`. The default right-aligns the numbers
  so the text stays in one column. A literal brace is written `{{` or `}}`.
* `width` (*int_positive | None*, keyword-only, default `None`): The width of the number field;
  `None` means as many digits as the **last** number has.

**Returns:**

* `str`: The numbered lines; an empty text stays empty.

**Raises:**

* `ParamError` (`TEXT_TEMPLATE_INVALID`): The template cannot be filled in (an unknown field, an
  unclosed brace, a positional field such as `{0}`).

**Example usage:**

```python
add_line_numbers("a\nb\nc\n")                          # -> '1: a\n2: b\n3: c\n'
add_line_numbers("a\nb\nc\n", start=0)                 # -> '0: a\n1: b\n2: c\n'
add_line_numbers("a\nb", start=99)                     # -> ' 99: a\n100: b'     the width fits the last number (3 digits)
add_line_numbers("a\nb\n", width=4)                    # -> '   1: a\n   2: b\n'
add_line_numbers("a\n\nb\n", template="{number}| {line}")      # -> '1| a\n2| \n3| b\n'    the blank line is numbered too
add_line_numbers("a\nb\n", template="{number:03d} {line}")     # -> '001 a\n002 b\n'
add_line_numbers("a{x}\n")                             # -> '1: a{x}\n'     braces inside the TEXT are safe
add_line_numbers("")                                   # -> ''
add_line_numbers("a", template="{x}")                  # raises ParamError (TEXT_TEMPLATE_INVALID)
```

**Under the hood:**

```python
@validate_call
def add_line_numbers(text, *, start=1, template="{number:>{width}}: {line}", width=None) -> str:
    try:
        template.format(number=start, line="", width=1)         # try the template once: a mistake is reported even for a short text
    except (KeyError, IndexError, ValueError, AttributeError) as caught_exc:
        raise_invalid_template_error(template, caught_exc)

    lines, has_end = split_lines(text)
    field_width = width or len(str(start + max(len(lines) - 1, 0)))

    numbered = [template.format(number=start + i, line=line, width=field_width)
                for i, line in enumerate(lines)]
    return join_lines(numbered, has_end)
```

The line is a **value** given to `format`, not part of the template, so braces inside the text can
never break it. Blank lines are numbered too, because the numbers must match the lines of the
original. The trial `format` call turns a typo in the template into a card that names the problem,
instead of an error from the middle of a loop.

[▲ Back to top](#-table-of-contents)

---

### `indent`

Puts a prefix in front of every non-blank line — a function body into a class, a snippet into a
Markdown list, a quoted text behind `"> "`. The opposite of
[`dedent`](README_TEXT_REMOVE.md#dedent).

**Parameters:**

* `text` (*str*): The text.
* `prefix` (*str | int_non_negative*, default `"    "`): The text to put in front, or a **number of
  spaces**. `indent(text, 2)` is two spaces; `indent(text, "> ")` is a quote mark.

**Returns:**

* `str`: The indented text; blank lines are left as they are. The same text if there is nothing to
  add (`""` or `0`).

**Example usage:**

```python
indent("a\n\nb\n")                  # -> '    a\n\n    b\n'      the blank line stays empty
indent("a\n  \nb\n", 2)             # -> '  a\n  \n  b\n'        a whitespace-only line is blank too: left untouched
indent("a\nb", "> ")                # -> '> a\n> b'
indent("a\nb\n", 0)                 # -> 'a\nb\n'                nothing to add: the very same text

dedent(indent("def f():\n    x\n\n    y\n"))   # -> 'def f():\n    x\n\n    y\n'   reversible for ordinary content
```

**Under the hood:**

```python
@validate_call
def indent(text: str, prefix: str | int_non_negative = "    ") -> str:
    if isinstance(prefix, int):
        prefix = " " * prefix                         # a number means that many spaces
    if prefix == "":
        return text                                   # nothing to add — the very same text back

    lines, has_end = split_lines(text)
    indented = [line if is_blank(line) else prefix + line for line in lines]
    return join_lines(indented, has_end)
```

Blank lines are skipped so that no line ends up made of spaces only; that is also what keeps the step
reversible — `dedent(indent(text))` gives back the text for ordinary content.

[▲ Back to top](#-table-of-contents)

---

### `truncate`

Shortens a text to a number of lines and / or characters **and says so** — keeps a long file or a log
from flooding a prompt or a report. The marker tells the reader that something is missing instead of
letting the text just stop.

**Parameters:**

* `text` (*str*): The text.
* `max_lines` (*int_positive | None*, keyword-only, default `None`): The most lines to keep.
* `max_chars` (*int_positive | None*, keyword-only, default `None`): The most characters to keep,
  counted **after** `max_lines` was applied, so it is a hard ceiling on what remains.
* `marker` (*str*, keyword-only, default `"… (truncated)"`): A line added after a shortened text.
  It is **not** counted into `max_chars`. `""` cuts silently.

At least one of `max_lines` and `max_chars` is required; both may be given.

**Returns:**

* `str`: The shortened text followed by the marker on its own line; the same text if it already
  fits.

**Raises:**

* `ParamError` (`TEXT_TRUNCATE_LIMIT_MISSING`): Neither `max_lines` nor `max_chars` was given.

**Example usage:**

```python
truncate("1\n2\n3\n4\n5\n", max_lines=2)               # -> '1\n2\n… (truncated)'
truncate("abcdefghij", max_chars=4)                    # -> 'abcd\n… (truncated)'    may cut in the middle of a word
truncate("abc\ndefg\nhij\n", max_lines=2, max_chars=5) # -> 'abc\nd\n… (truncated)'  lines first, then characters
truncate("1\n2\n3\n", max_lines=2, marker="[...]")     # -> '1\n2\n[...]'
truncate("1\n2\n3\n", max_lines=2, marker="")          # -> '1\n2'                   cut silently
truncate("1\n2\n3\n", max_lines=3)                     # -> '1\n2\n3\n'              it fits: the very same text back
truncate("abc\n", max_chars=3)                       # -> 'abc\n… (truncated)'    the final newline counts, so nothing visible is missing but the marker is added
truncate("abc\n", max_chars=4)                       # -> 'abc\n'                 …and with one more character it fits
truncate("a long text")                                # raises ParamError (TEXT_TRUNCATE_LIMIT_MISSING)
```

**Under the hood:**

```python
@validate_call
def truncate(text, *, max_lines=None, max_chars=None, marker="… (truncated)") -> str:
    if max_lines is None and max_chars is None:
        raise_missing_limit_error()                   # without a limit there is nothing to truncate to

    shortened, was_cut = text, False
    if max_lines is not None:                         # lines first
        lines, _ = split_lines(text)
        if len(lines) > max_lines:
            shortened, was_cut = "\n".join(lines[:max_lines]), True
    if max_chars is not None and len(shortened) > max_chars:     # then characters
        shortened, was_cut = shortened[:max_chars], True

    if not was_cut:
        return text
    return shortened + ("\n" + marker if marker else "")
```

The marker stands on its own line, so a text cut in the middle of a line still ends with a clean
line. For a clean cut use `max_lines` alone: `max_chars` counts **every** character of the text,
newlines included, and cuts wherever the limit falls. A shortened text never ends with the original's
final newline — the marker (or the cut) is the end.

**A final newline counts.** `max_chars` counts the whole text, final newline included. A text whose
content is exactly `max_chars` long and ends with a newline is cut by that newline and gets the marker,
although nothing visible is missing.

[▲ Back to top](#-table-of-contents)

---

### `wrap`

Wraps the lines that are longer than a width, keeping each line's indentation — makes prose and
comments fit without ruining the structure.

**Parameters:**

* `text` (*str*): The text.
* `width` (*int_positive*, default `80`): The longest allowed line.
* `break_long_words` (*bool*, keyword-only, default `False`): Split a single word that is longer
  than the line. By default such a word (a URL) stays whole on its own line: better a long line than
  a broken link.

**Returns:**

* `str`: The text with long lines wrapped; lines that fit are untouched, so the same text comes back
  if there is no long line.

**Example usage:**

```python
wrap("one two three four five six", 12)               # -> 'one two\nthree four\nfive six'
wrap("    one two three four five six", 16)            # -> '    one two\n    three four\n    five six'    every new line keeps the indentation
wrap("see https://example.com/a/very/long/path ok", 10)
# -> 'see\nhttps://example.com/a/very/long/path\nok'    the long word stays whole
wrap("see https://example.com/a/very/long/path ok", 10, break_long_words=True)
# -> 'see https:\n//example.\ncom/a/very\n/long/path\nok'
wrap("my-kebab-case-name is long", 10)                 # -> 'my-kebab-case-name\nis long'        no breaking at hyphens
wrap("a very long first line here\n\nsecond\n", 10)    # -> 'a very\nlong first\nline here\n\nsecond\n'   blank lines and short lines stay
```

**Under the hood:**

```python
@validate_call
def wrap(text: str, width: int_positive = 80, *, break_long_words: bool = False) -> str:
    lines, has_end = split_lines(text)
    wrapped = []
    for line in lines:
        if len(line) <= width or is_blank(line):
            wrapped.append(line)                      # a line that fits (or is blank) is not touched at all
            continue
        lead = line[:len(line) - len(line.lstrip())]  # the continuation lines get the same indentation
        wrapped.append(textwrap.fill(line.strip(), width=width,
                                     initial_indent=lead, subsequent_indent=lead,
                                     break_long_words=break_long_words, break_on_hyphens=False,
                                     expand_tabs=False, replace_whitespace=False))
    if wrapped == lines:
        return text
    return join_lines(wrapped, has_end)
```

Only an overlong line is rebuilt, and even then tabs and whitespace inside it are not touched
(`expand_tabs` and `replace_whitespace` are off). Words break **only at whitespace**: `textwrap` would
split `kebab-case-name` at its hyphens by default, which in code and identifiers changes meaning. A
**tab counts as one character**, so a line indented with tabs is measured shorter than it looks.

[▲ Back to top](#-table-of-contents)

---

## Errors of this package

These functions raise `ParamError` cards of [`simplibs-exception`](https://pypi.org/project/simplibs-exception/);
the package defines no exceptions of its own. The card's `label` names the offending parameter and
its `value` is what was given.

| Error name                    | Wraps        | Raised by          | Fix                                                                               |
|-------------------------------|--------------|--------------------|-----------------------------------------------------------------------------------|
| `TEXT_TEMPLATE_INVALID`       | `ValueError` | `add_line_numbers` | Use only `{number}`, `{line}` and `{width}`, e.g. `'{number:>{width}}: {line}'`; write a literal brace as `{{` or `}}` |
| `TEXT_TRUNCATE_LIMIT_MISSING` | `ValueError` | `truncate`         | Pass `max_lines=...`, `max_chars=...`, or both                                    |

`indent` and `wrap` define no errors of their own. An argument of the wrong type — a zero `width`, a
negative `max_lines` — is a `ValidationError` from `@validate_call` and never reaches these.

[▲ Back to top](#-table-of-contents)
