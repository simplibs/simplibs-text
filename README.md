# ✂️ `simplibs-text`

[![PyPI](https://img.shields.io/pypi/v/simplibs-text)](https://pypi.org/project/simplibs-text/)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![Licence](https://img.shields.io/badge/licence-MIT-green)](https://github.com/simplibs/simplibs-text/blob/main/LICENSE)
[![tests](https://github.com/simplibs/simplibs-text/actions/workflows/tests.yml/badge.svg)](https://github.com/simplibs/simplibs-text/actions)

**One text in, one text out — small steps you can trust, and chain.**

A Python library of small, safe steps that turn one text into another: **remove**, **keep**,
**replace** and **decorate** parts of it, **clean** its characters and **convert** between naming
styles. Every step is a plain function (`str -> str`) and, with no extra code, a pipeline
**action** you can join with `>>`. Text means exactly what it says: a `str` pattern is searched
for **literally**, lines are separated by `"\n"` only, a text with nothing to change comes back
untouched, and a wrong call is a structured card that says what and how to fix it.

```python
from simplibs.text import remove_matches, keep_line_range, add_line_numbers

remove_matches("a.b a.b\nA.B\n", "a.b")        # -> 'A.B\n'          (a str is literal; the line that went blank is gone)
keep_line_range("1\n2\n3\n4\n", 2, 3)           # -> '2\n3\n'         (counted from 1, both ends included)
add_line_numbers("a\nb\nc\n", start=10)         # -> '10: a\n11: b\n12: c\n'
```

> `simplibs-text` is a sister of [`simplibs-file`](https://pypi.org/project/simplibs-file/): that
> library moves **text and bytes** to and from the disk, this one **changes the text** once it is in
> memory. `read_text` hands over text with `"\n"` line endings — exactly what every step here expects. A text with `"\r\n"` endings should be normalized first: for these steps a `"\r"` is ordinary content.

---

## 🧭 The Core Philosophy

The usual way is a `re.sub` here, a `splitlines()` there and a `"\n".join(...)` to put it back:
the pattern `"a.b"` quietly matches `"aXb"`, a replacement `"\1"` is read as a group reference, the
final newline of the file disappears, a comment-only line leaves an empty hole and a bare
`str.splitlines()` cuts the text on characters that are ordinary in a source file.
`simplibs-text` takes those traps seriously:

* **Text is literal by default.** A `str` pattern and a `str` replacement mean exactly themselves.
  Regex enters on purpose — through `re.compile(...)`, a `Regex` tree or a `RegexPattern` from `simplibs-regex` — so
  a stray `.` or `\` is never a surprise.
* **Lines are lines.** Only `"\n"` separates them, and the last newline is remembered: a text that
  ended with one still does, and one that did not still does not.
* **Nothing to do, nothing changed.** A step that finds nothing to change returns the very same
  text, not a look-alike.
* **No holes.** A line that became blank **because of** a removal disappears whole; blank lines
  that were there before stay where they are.
* **Cut where you are told.** `remove_spans` takes plain character ranges, so anything that *finds*
  what to remove in its own way (a regex, a parser, a tokenizer) shares one way of cutting.
* **Honest about what is missing.** `truncate` puts a marker on its own line instead of letting the
  text just stop.
* **Functions first, actions on top.** Every action is a thin wrapper over a function of the same
  name; the logic lives once.
* **Every error is a card.** A wrong call is a `ParamError` from
  [`simplibs-exception`](https://pypi.org/project/simplibs-exception/) with a name starting with
  `TEXT_`, what was given, what was expected and how to fix it.
* **Layers that only look left.** `annotations` ← `logic/_common` ← the `logic/` domains ←
  `recipes` ← `actions` ← `presets` — every layer imports only from those before it, and the
  domains of `logic/` never import each other.

```python
remove_matches("a", re.compile("a"), flags=re.I)   # -> raises: TEXT_PATTERN_FLAGS_CONFLICT — the compiled pattern has its own flags
truncate("a very long text")                       # -> raises: TEXT_TRUNCATE_LIMIT_MISSING — no limit, nothing to truncate to
```

---

## 📦 Installation

```bash
pip install simplibs-text
```

Requires Python 3.11+. Runtime dependencies: [`simplibs-exception`](https://pypi.org/project/simplibs-exception/)
(the error cards), [`simplibs-validate`](https://pypi.org/project/simplibs-validate/)
(`@validate_call` and the checks behind `Annotated`), [`simplibs-actions`](https://pypi.org/project/simplibs-actions/)
(the `Action` classes), [`simplibs-types`](https://pypi.org/project/simplibs-types/) (`int_positive`
and `int_non_negative` for widths and counts) and [`simplibs-regex`](https://pypi.org/project/simplibs-regex/)
(the `Regex` tree and the `RegexPattern` accepted as a pattern).

---

## 🚀 Quick Start in 60 Seconds

### Level 1: Take away, keep, number

```python
from simplibs.text import (
    remove_empty_lines, remove_lines_matching, keep_line_range, keep_between, truncate, add_line_numbers,
)

remove_empty_lines("a\n\n  \nb\n")                       # -> 'a\nb\n'
remove_lines_matching("a\n#b\nc\n", "#")                 # -> 'a\nc\n'
keep_line_range("1\n2\n3\n4\n", 2, 3)                    # -> '2\n3\n'
keep_between("x\n# BEGIN\na\nb\n# END\ny\n", "# BEGIN", "# END")   # -> '# BEGIN\na\nb\n# END'
truncate("1\n2\n3\n4\n5\n", max_lines=2)                 # -> '1\n2\n… (truncated)'
add_line_numbers("a\nb\nc\n", start=10)                  # -> '10: a\n11: b\n12: c\n'
```

### Level 2: Patterns, literal or regex

```python
import re
from simplibs.text import remove_matches, replace_matches, keep_matches

remove_matches("a.b a.b\nA.B\n", "a.b")                  # -> 'A.B\n'          a str is literal
remove_matches("x = 1  # c\n# note\ny = 2\n", re.compile(r"#.*"))   # -> 'x = 1  \ny = 2\n'   the comment-only line is gone, no hole
keep_matches("a1 b22 c333", re.compile(r"\d+"), separator=", ")     # -> '1, 22, 333'

replace_matches("a \\1 b", "\\1", "X")                   # -> 'a X b'         "\1" is two characters, not a group
replace_matches("2026-10-28", re.compile(r"(\d+)-(\d+)-(\d+)"),
                lambda m: f"{m.group(3)}.{m.group(2)}.{m.group(1)}")   # -> '28.10.2026'   groups go through a function
```

### Level 3: Characters and naming styles

```python
from simplibs.text import (
    remove_diacritics, keep_ascii, remove_punctuation, to_snake_case, to_camel_case, split_words,
    cleanup_whitespace, compact,
)

remove_diacritics("příliš žluťoučký")                    # -> 'prilis zlutoucky'
remove_punctuation("Hi, you! (ok)")                      # -> 'Hi you ok'
to_snake_case("MyVarName\n  my-other name")              # -> 'my_var_name\n  my_other_name'   per line, indentation kept
to_camel_case("my var_name")                             # -> 'myVarName'
split_words("HTTPServer2Go")                             # -> ['HTTP', 'Server2', 'Go']

cleanup_whitespace("\n\na  \n\n\n\nb \n\n")              # -> 'a\n\nb\n'      tidy, keep the structure
compact("a  \n\n b\n")                                   # -> 'a\n b\n'       no blank lines at all
```

### Level 4: Actions and ready-made chains

```python
import re
from simplibs.text.actions import RemoveMatches, KeepLineRange, AddLineNumbers, Truncate
from simplibs.text.presets import COMPACT

strip_comments = RemoveMatches(pattern=re.compile(r"#.*")) >> COMPACT
strip_comments("x = 1  # c\n# n\n\ny = 2\n")             # -> 'x = 1\ny = 2\n'

preview = KeepLineRange(start=10, end=60) >> AddLineNumbers(start=10) >> Truncate(max_lines=40)
preview(source_text)                                      # lines 10–60, numbered from 10, at most 40 of them
```

---

## 🛠️ Architecture & Package Structure

```
src/simplibs/text/
├── annotations/          ◄── Named types for signatures (Pattern, Replacement, LineNumber, UnicodeForm)
├── logic/                ◄── The functional core — plain functions, no Action knowledge
│   ├── remove/           ◄── remove_spans, remove_matches, remove_lines_matching, remove_empty_lines, ...
│   ├── keep/             ◄── keep_matches, keep_lines_matching, keep_line_range, keep_between
│   ├── replace/          ◄── replace_matches, map_lines
│   ├── decorate/         ◄── add_line_numbers, indent, truncate, wrap
│   ├── clean/            ◄── normalize_unicode, remove_diacritics, keep_ascii, remove_punctuation, ...
│   ├── case/             ◄── split_words, to_snake_case, to_kebab_case, to_camel_case, to_pascal_case
│   └── recipes/          ◄── cleanup_whitespace, compact (combinations of the functions above)
├── actions/              ◄── Action classes over the functions (domain folder)
│   └── remove/  keep/  replace/  decorate/  clean/  case/
└── presets/              ◄── Ready-made action chains (domain folder) — CLEANUP_WHITESPACE, COMPACT
```

Everything in `logic/` and the annotations is importable straight from `simplibs.text`. `actions` and
`presets` are separate domains, imported through their own folders — a function and an action are
different kinds of thing and should stay visibly different at the import line:

```python
from simplibs.text import remove_matches, keep_line_range, to_snake_case, Pattern   # functions and types
from simplibs.text.actions import RemoveMatches, KeepLineRange, ToSnakeCase          # actions
from simplibs.text.presets import CLEANUP_WHITESPACE, COMPACT                        # ready-made chains
```

---

## 🧹 `logic/remove/` — Take something away

Strip comments, markers and noise, and tidy the whitespace left behind. A match or a span is cut
out; a line that went blank **because of** the cut disappears whole (`drop_emptied_lines=True`),
while blank lines that were already there stay.

| Function                | Description / Parameters                                                                                  |
|-------------------------|-----------------------------------------------------------------------------------------------------------|
| `remove_spans`          | Cuts given character ranges out; overlapping ranges are merged (`text`, `spans`, `drop_emptied_lines=True`). |
| `remove_matches`        | Removes every match of a pattern (`text`, `pattern`, `flags=0`, `drop_emptied_lines=True`).                |
| `remove_lines_matching` | Removes every line that contains a match (`text`, `pattern`, `flags=0`).                                   |
| `remove_empty_lines`    | Removes every empty or whitespace-only line (`text`).                                                      |
| `strip_trailing_spaces` | Removes spaces and tabs from the end of every line (`text`).                                               |
| `squeeze_blank_lines`   | Shortens every run of blank lines (`text`, `max_consecutive=1`).                                           |
| `trim_blank_edges`      | Removes blank lines at the start and at the end (`text`).                                                  |
| `dedent`                | Removes the indentation every non-blank line has in common (`text`).                                       |

➡️ [README_TEXT_REMOVE](https://github.com/simplibs/simplibs-text/blob/main/docs/logic/README_TEXT_REMOVE.md)

---

## 🎯 `logic/keep/` — Keep only a chosen part

The opposite verb: what you name stays, the rest goes. Line numbers are counted from 1, and both
ends of a range are included.

| Function              | Description / Parameters                                                                                  |
|-----------------------|-----------------------------------------------------------------------------------------------------------|
| `keep_matches`        | Keeps only the matches, joined by a separator (`text`, `pattern`, `flags=0`, `separator="\n"`).            |
| `keep_lines_matching` | Keeps only the lines that contain a match (`text`, `pattern`, `flags=0`).                                  |
| `keep_line_range`     | Keeps the lines from `start` to `end`; `end=None` means "to the last line" (`text`, `start=1`, `end=None`). |
| `keep_between`        | Keeps the parts between a start marker and an end marker (`text`, `start`, `end`, `include_markers=True`, `flags=0`, `separator="\n"`). |

➡️ [README_TEXT_KEEP](https://github.com/simplibs/simplibs-text/blob/main/docs/logic/README_TEXT_KEEP.md)

---

## 🔁 `logic/replace/` — Change parts of the text

| Function          | Description / Parameters                                                                                  |
|-------------------|-----------------------------------------------------------------------------------------------------------|
| `replace_matches` | Replaces the matches by a literal text or by a function's result (`text`, `pattern`, `replacement`, `flags=0`, `count=0`). |
| `map_lines`       | Applies a function to every line; it must return a `str` (`text`, `func`).                                 |

➡️ [README_TEXT_REPLACE](https://github.com/simplibs/simplibs-text/blob/main/docs/logic/README_TEXT_REPLACE.md)

---

## 🎀 `logic/decorate/` — Add to or reshape the text

| Function           | Description / Parameters                                                                                   |
|--------------------|------------------------------------------------------------------------------------------------------------|
| `add_line_numbers` | Puts a number in front of every line (`text`, keyword-only: `start=1`, `template="{number:>{width}}: {line}"`, `width=None`). |
| `indent`           | Puts a prefix in front of every non-blank line; a number means that many spaces (`text`, `prefix="    "`).                                   |
| `truncate`         | Shortens to a number of lines and / or characters and says so with a marker (`text`, keyword-only: `max_lines=None`, `max_chars=None`, `marker="… (truncated)"`). |
| `wrap`             | Wraps lines longer than a width, keeping each line's indentation (`text`, `width=80`, `break_long_words=False`). |

➡️ [README_TEXT_DECORATE](https://github.com/simplibs/simplibs-text/blob/main/docs/logic/README_TEXT_DECORATE.md)

---

## 🔤 `logic/clean/` — The characters of the text

Unicode-aware, for any script: letters and digits are what `str.isalnum` says they are, so Czech,
Greek and CJK text behaves as expected.

| Function                  | Description / Parameters                                                                            |
|---------------------------|-----------------------------------------------------------------------------------------------------|
| `normalize_unicode`       | Writes every character in one normalization form (`text`, `form="NFC"`).                             |
| `remove_diacritics`       | Removes accents and other combining marks from letters (`text`).                                     |
| `keep_ascii`              | Keeps only the ASCII characters (`text`).                                                            |
| `remove_punctuation`      | Removes punctuation characters (`text`).                                                             |
| `replace_punctuation`     | Replaces every punctuation character with a text (`text`, `replacement=" "`).                        |
| `remove_symbols`          | Removes symbol characters — currency signs, math signs, emoji (`text`).                              |
| `remove_non_alphanumeric` | Keeps only letters and digits, with the marks that belong to them (`text`, `keep_whitespace=True`).   |

➡️ [README_TEXT_CLEAN](https://github.com/simplibs/simplibs-text/blob/main/docs/logic/README_TEXT_CLEAN.md)

---

## 🐍 `logic/case/` — Naming styles

Each line is converted separately and its indentation is kept; a line without any word is left as it
is. `MyVarName`, `my-var-name` and `my var name` are all the same three words to these functions.

| Function          | Description / Parameters                                                                                  |
|-------------------|-----------------------------------------------------------------------------------------------------------|
| `split_words`     | Splits a text or an identifier into its words; returns a `list[str]` (`text`).                             |
| `to_snake_case`   | Writes every line in `snake_case` (`text`).                                                                |
| `to_kebab_case`   | Writes every line in `kebab-case` (`text`).                                                                |
| `to_camel_case`   | Writes every line in `camelCase` (`text`).                                                                 |
| `to_pascal_case`  | Writes every line in `PascalCase` (`text`).                                                                |

➡️ [README_TEXT_CASE](https://github.com/simplibs/simplibs-text/blob/main/docs/logic/README_TEXT_CASE.md)

---

## 🍳 `logic/recipes/` — Ready-made combinations

The two cleanups people reach for most often. A recipe is the one place in `logic/` that looks
sideways: it **combines** functions of `remove`, so it stands above them.

| Function             | Description / Parameters                                                                                |
|----------------------|---------------------------------------------------------------------------------------------------------|
| `cleanup_whitespace` | Strips line ends, shrinks runs of blank lines to one, trims the edges — the structure stays (`text`).    |
| `compact`            | Strips line ends and removes every blank line — the shortest honest form (`text`).                      |

➡️ [README_TEXT_RECIPES](https://github.com/simplibs/simplibs-text/blob/main/docs/logic/README_TEXT_RECIPES.md)

---

## ⚙️ `actions/` — Pipeline steps

Every function above (except the two recipes) is also an `Action` from
[`simplibs-actions`](https://pypi.org/project/simplibs-actions/): configured once, called with the
**text** as its main input, chainable with `>>`, `&` and `|`, and awaitable through `acall`. The
options of the function become the options of the action: `RemoveMatches(pattern=..., flags=...)`.

There is **one direction only**: the text flows and the pattern, the limit or the prefix is
configuration. (`simplibs-file` offers a second direction for writers because it has two things to
carry; here there is one.) `SplitWords` is the one action whose result is not a text — it ends a
text pipeline.

| Group        | Actions                                                                                                                         |
|--------------|---------------------------------------------------------------------------------------------------------------------------------|
| **remove**   | `RemoveSpans`, `RemoveMatches`, `RemoveLinesMatching`, `RemoveEmptyLines`, `StripTrailingSpaces`, `SqueezeBlankLines`, `TrimBlankEdges`, `Dedent` |
| **keep**     | `KeepMatches`, `KeepLinesMatching`, `KeepLineRange`, `KeepBetween`                                                               |
| **replace**  | `ReplaceMatches`, `MapLines`                                                                                                     |
| **decorate** | `AddLineNumbers`, `Indent`, `Truncate`, `Wrap`                                                                                   |
| **clean**    | `NormalizeUnicode`, `RemoveDiacritics`, `KeepAscii`, `RemovePunctuation`, `ReplacePunctuation`, `RemoveSymbols`, `RemoveNonAlphanumeric` |
| **case**     | `SplitWords`, `ToSnakeCase`, `ToKebabCase`, `ToCamelCase`, `ToPascalCase`                                                        |

➡️ [README_TEXT_ACTIONS](https://github.com/simplibs/simplibs-text/blob/main/docs/README_TEXT_ACTIONS.md)

---

## 🧩 `presets/` — Ready-made chains

The same two recipes as **actions**, built once, for use inside a pipeline.

| Preset               | Chain                                                                              |
|----------------------|------------------------------------------------------------------------------------|
| `CLEANUP_WHITESPACE` | `StripTrailingSpaces() >> SqueezeBlankLines(max_consecutive=1) >> TrimBlankEdges()` |
| `COMPACT`            | `StripTrailingSpaces() >> RemoveEmptyLines()`                                      |

➡️ [README_TEXT_PRESETS](https://github.com/simplibs/simplibs-text/blob/main/docs/README_TEXT_PRESETS.md)

---

## 🏷️ `annotations/` — Types for your signatures

Named types for the signatures of your own functions and wrappers. `Pattern` and `LineNumber` carry
a predicate that `@validate_call` checks; `Replacement` and `UnicodeForm` are plain type aliases.

| Type          | Description                                                                                              |
|---------------|----------------------------------------------------------------------------------------------------------|
| `Pattern`     | What to look for: a literal `str`, a compiled `re.Pattern`, a `Regex` tree or a `RegexPattern`; the empty string is rejected. |
| `Replacement` | What to put in place of a match: a literal `str`, or a function from the `re.Match` to a `str`.            |
| `LineNumber`  | A line number counted from 1; zero, negatives and `bool` are rejected.                                     |
| `UnicodeForm` | One of the four Unicode normalization forms: `"NFC"`, `"NFD"`, `"NFKC"`, `"NFKD"`.                        |

➡️ [README_TEXT_ANNOTATIONS](https://github.com/simplibs/simplibs-text/blob/main/docs/README_TEXT_ANNOTATIONS.md)

---

## ⚠️ Exceptions

The library defines no exceptions of its own. A wrong call is a structured
[`simplibs.exception`](https://pypi.org/project/simplibs-exception/) `ParamError` card with a name
starting with `TEXT_`; the card's `label` names the offending parameter and its `value` is what was
given. An argument of the wrong type — or an empty `str` as a pattern — is a `ValidationError` raised
by `@validate_call` before the function runs.

| Error name                     | Class        | Wraps        | Raised when                                                                  |
|--------------------------------|--------------|--------------|------------------------------------------------------------------------------|
| `TEXT_PATTERN_COMPILE_FAILED`  | `ParamError` | `ValueError` | A pattern or its flags cannot be compiled by `re.compile`                    |
| `TEXT_PATTERN_FLAGS_CONFLICT`  | `ParamError` | `ValueError` | `flags` are given together with an already compiled pattern (`re.Pattern`, `RegexPattern`)             |
| `TEXT_CALLBACK_RESULT_INVALID` | `ParamError` | `TypeError`  | A function given by the caller (`map_lines`, `replace_matches`) returns something other than a `str` |
| `TEXT_SPAN_INVALID`            | `ParamError` | `ValueError` | A span of `remove_spans` does not satisfy `0 <= start <= end <= len(text)`   |
| `TEXT_LINE_RANGE_INVALID`      | `ParamError` | `ValueError` | `keep_line_range` gets an `end` before its `start`                           |
| `TEXT_TRUNCATE_LIMIT_MISSING`  | `ParamError` | `ValueError` | `truncate` gets neither `max_lines` nor `max_chars`                          |
| `TEXT_TEMPLATE_INVALID`        | `ParamError` | `ValueError` | The `template` of `add_line_numbers` cannot be filled in with `{number}`, `{line}` and `{width}` |

Each helper README ends with the errors of its own package.

---

## 🔗 Related libraries

* **[`simplibs-file`](https://pypi.org/project/simplibs-file/)** — text and bytes on disk; `read_text` returns the `"\n"` line endings these steps expect.
* **[`simplibs-regex`](https://pypi.org/project/simplibs-regex/)** — the `Regex` tree and the `RegexPattern` accepted wherever a `Pattern` is; **[`simplibs-patterns`](https://pypi.org/project/simplibs-patterns/)** is its ready-made vocabulary.
* **[`simplibs-actions`](https://pypi.org/project/simplibs-actions/)** — the `Action` abstraction and containers behind `simplibs.text.actions`.
* **[`simplibs-rules`](https://pypi.org/project/simplibs-rules/)** — conditions over text and any other value; combine them with the actions through `guard` and `branch` instead of putting a condition inside a step.
* **[`simplibs-validate`](https://pypi.org/project/simplibs-validate/)** — `@validate_call`, which validates every argument here.
* **[`simplibs-exception`](https://pypi.org/project/simplibs-exception/)** — the structured exception cards.

---

## ☯️ About simplibs

All libraries in the **simplibs** (Simple Libraries) ecosystem share a common
engineering philosophy:

* **Dyslexia-friendly:**
We actively minimize cognitive load. Code is atomized into small, self-contained units,
files are named directly after the logical task they perform, and explanations describe
*why* something is designed, not just *what* it is.
* **Programmer's Zen:**
Nothing should be missing, and nothing should be superfluous. We value clean execution
paths and robust, understandable code architectures over rushed, messy feature sets.
* **Defensive Style:**
We actively anticipate edge cases and failure modes so that only safe operational paths
remain. Our code is built to degrade gracefully rather than crash unexpectedly.
* **Minimalism:**
Find the most direct path to the goal in as few operational steps as possible without
taking shortcuts on safety, readability, or completeness.
* **Code as Craft:**
Code should be pleasant to look at, readable at a glance, and evoke structural harmony.
We treat software engineering as a precision trade.

---

### 🤝 Contributing & Community

This is an **open-source project** built with love and care. We strongly believe in
community collaboration and welcome any feedback, bug reports, or feature ideas!

* **Want to contribute?** Feel free to open an Issue or submit a Pull Request.
* **Want to get in touch?** If you'd like to discuss the project further, collaborate,
  or just say hello, feel free to open a GitHub Issue or start a Discussion.

---

### 📝 License

This library is released under the **MIT License**. Build great things!

---
