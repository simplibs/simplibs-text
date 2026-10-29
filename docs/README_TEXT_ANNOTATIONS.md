# 🏷️ `annotations` — Types for Your Signatures

The `annotations` package holds the four types the whole library shares — the exact types the
functions and actions declare for their parameters. They live in `simplibs.text.annotations` and are
also exported from the package root, so **your own functions can accept exactly what this library
accepts**:

```python
from simplibs.text import LineNumber, Pattern, Replacement, UnicodeForm
```

Each is a plain annotation object — no class to instantiate — and works with `simplibs-validate`
(`@validate_call`) and with type checkers.

```python
from simplibs.validate import validate_call
from simplibs.text import Pattern, keep_lines_matching

@validate_call
def count_lines_with(text: str, pattern: Pattern) -> int:
    return len(keep_lines_matching(text, pattern).splitlines())

count_lines_with("a\nb\na\n", "a")            # -> 2
count_lines_with("a\nb\na\n", "")             # raises ValidationError — an empty pattern matches everywhere
```

The same annotations are what the actions use for their constructor options, so a mistake is caught
when the action is **built**, before any text flows through it.

## Three kinds of annotation

| Kind               | Annotations                         | How it decides                                                                |
|--------------------|-------------------------------------|-------------------------------------------------------------------------------|
| **Annotated type** | `Pattern`, `LineNumber`             | `Annotated[base, predicate]` — a base type plus a predicate that checks the **value**. |
| **Type alias**     | `Replacement`                       | A plain `str \| Callable[[re.Match], str]` — only the type is checked; every `str` is fine, even `""`. |
| **Fixed set**      | `UnicodeForm`                       | A `Literal` — only the listed values exist.                                    |

An annotated type is written so that editors and type checkers understand it: to the editor it is
the plain base type (`str | re.Pattern | Regex | RegexPattern`, `int`) and offers the usual hints, while
`@validate_call` reads the predicate from the `Annotated` metadata and checks the **value**. A fixed
set is a `Literal`, so it fails at the signature on a typo (`form="nfc"`) instead of deep inside
`unicodedata`.

## Where each one is used

| Annotation    | Parameter                     | Used by                                                                                                        |
|---------------|-------------------------------|----------------------------------------------------------------------------------------------------------------|
| `Pattern`     | `pattern`, `start`, `end`     | `remove_matches`, `remove_lines_matching`, `keep_matches`, `keep_lines_matching`, `keep_between` (`start`, `end`), `replace_matches` — and their actions |
| `Replacement` | `replacement`                 | `replace_matches` and `ReplaceMatches`                                                                          |
| `LineNumber`  | `start`, `end`                | `keep_line_range` and `KeepLineRange`                                                                           |
| `UnicodeForm` | `form`                        | `normalize_unicode` and `NormalizeUnicode`                                                                      |

> **`add_line_numbers` does not use `LineNumber`.** Its `start` is an `int_non_negative`, because
> `0` is a legitimate first number for the programmer's count, while a `LineNumber` is always at
> least `1`.

---

## 🧭 Table of Contents

**Annotated types**

* [`Pattern`](#pattern)
* [`LineNumber`](#linenumber)

**Type alias**

* [`Replacement`](#replacement)

**Fixed set**

* [`UnicodeForm`](#unicodeform)

[⬅️ Back to main README](../README.md#-annotations--types-for-your-signatures)

---

### `Pattern`

What to **look for**: a literal `str`, a compiled `re.Pattern`, a `Regex` tree or a `RegexPattern`.

**Definition:**

```python
Pattern = Annotated[str | re.Pattern | Regex | RegexPattern, is_pattern]
```

**What each form means:**

* **`str`** — a **literal**. `"a.b"` finds `a.b`, not `a` + any character + `b`. The same rule as
  `Literal` in `simplibs-regex` and `Contains` in `simplibs-rules`, so there is no silent trap in
  `"("` or `"."`.
* **`re.Pattern`** — used as it is, with its own flags. `flags=` is refused with it.
* **`Regex`** — a tree from [`simplibs-regex`](https://pypi.org/project/simplibs-regex/) (and so any
  term from `simplibs-patterns`), rendered with `to_pattern()` and compiled.
* **`RegexPattern`** — the compiled wrapper of `simplibs-regex`. The `re.Pattern` inside it is used as
  it is, with the flags it was built with, so `flags=` is refused with it too.

**Accepts:** `"abc"`, `"a.b"`, `"# TODO"`, `re.compile(r"\d+")`, a `Regex` tree, a `RegexPattern`.

**Rejects:** the empty string `""`, `None`, `bytes` (`b"a"`), numbers.

**Example usage:**

```python
remove_matches(text, "# TODO")                 # fine — a literal
remove_matches(text, re.compile(r"#.*"))       # fine — a regex, on purpose
remove_matches(text, "")                       # raises ValidationError
keep_between(text, "<body>", "</body>")        # fine — start and end are both a Pattern
```

**Why the empty string is refused.** As a literal it matches at every position, so
`remove_matches(text, "")` would "succeed" and change nothing, and `keep_matches` would return a pile
of nothing. Better to fail at the signature.

**Why a `str` is not a regex.** A regex is a program; a `str` from a config file or a user is data.
Making the data literal means a stray `.` or `(` is never a surprise, and regex enters only through
`re.compile(...)`, a `Regex` tree or a `RegexPattern` — visibly, on purpose.

**Flags.** `flags=` belongs to the forms that are not compiled yet (`str`, `Regex`). A `re.Pattern`
and a `RegexPattern` already carry theirs, so `flags=` with them is refused with a
`TEXT_PATTERN_FLAGS_CONFLICT` card instead of being silently ignored.

<details>
<summary>🔍 Under the hood</summary>

```python
def is_pattern(value: str | re.Pattern | Regex | RegexPattern) -> bool:
    # 1. A text is a literal — the empty one would match between every two characters
    if isinstance(value, str):
        return value != ""

    # 2. A compiled pattern, a `Regex` tree and a `RegexPattern` are taken as they are
    return isinstance(value, (re.Pattern, Regex, RegexPattern))
```

The predicate only answers "is this the right kind of thing". Whether a `Regex` tree renders into a
valid pattern is known only after rendering, and that is reported by the library itself with its own
card (`TEXT_PATTERN_COMPILE_FAILED`). A `RegexPattern` built with `lazy=True` is compiled on first use,
so its own card (from `simplibs-regex`) appears then, not here.

</details>

[▲ Back to top](#-table-of-contents)

---

### `LineNumber`

A line number **counted from 1** — the way editors, error messages and `sed` count.

**Definition:**

```python
LineNumber = Annotated[int, is_line_number]
```

**Accepts:** `1`, `2`, `40`, `10_000` — any `int` greater than zero.

**Rejects:** `0`, negative integers, `True` / `False`, `None` (where `None` is not allowed), non-numbers
(`"1"`, `2.0`).

**Example usage:**

```python
keep_line_range(text, 10, 20)                  # fine
keep_line_range(text, 0)                       # raises ValidationError — there is no line 0
KeepLineRange(start=5, end=None)               # fine — `end` may also be None: "to the last line"
```

**Why it cannot be zero.** `0` would be quietly read as "the first line" or as "before the first
line", which is exactly how an off-by-one slips in. It is stopped at the signature instead.

**Why `bool` is rejected.** In Python `True` is an `int` (it equals `1`), but `start=True` is never
what a caller meant.

<details>
<summary>🔍 Under the hood</summary>

```python
def is_line_number(value: int) -> bool:
    # 1. A real integer (a bool is an int in Python, but never what the caller meant)
    if not isinstance(value, int) or isinstance(value, bool):
        return False

    # 2. Lines are counted from 1
    return value > 0
```

</details>

[▲ Back to top](#-table-of-contents)

---

### `Replacement`

What to put **in place of a match**: a literal `str`, or a function from the match to a `str`.

**Definition:**

```python
Replacement = str | Callable[[re.Match], str]
```

**A `str` is literal.** Like `Pattern`, a `str` means itself. `"\1"` and `"\g<n>"` are **not** group
references here — they are ordinary characters — so a stray backslash can never end in
`re.error: bad escape`.

**A function gets the whole `re.Match`**, so named groups, positions and everything else are
available, and must return a `str` (an empty one is fine — that is a removal).

**Example usage:**

```python
replace_matches("a \\1 b", "\\1", "X")                                                  # -> 'a X b'
replace_matches("2026-10-28", re.compile(r"(\d+)-(\d+)-(\d+)"),
                lambda m: f"{m.group(3)}.{m.group(2)}.{m.group(1)}")                    # -> '28.10.2026'
replace_matches("a1b22", re.compile(r"(?P<n>\d+)"), lambda m: "<" + m.group("n") + ">")  # -> 'a<1>b<22>'
replace_matches("a", "a", lambda m: None)      # raises ParamError (TEXT_CALLBACK_RESULT_INVALID) — the function must return a str
```

**Why it is not `Annotated`.** There is nothing to check beyond the type: any `str` is fine,
including `""` — unlike `Pattern`, where the empty string is a mistake. What the function **returns**
is checked at the moment it is called, by the library, with a card that says where it happened.

[▲ Back to top](#-table-of-contents)

---

### `UnicodeForm`

One of the **four Unicode normalization forms**.

**Definition:**

```python
UnicodeForm = Literal["NFC", "NFD", "NFKC", "NFKD"]
```

**Accepts:** `"NFC"`, `"NFD"`, `"NFKC"`, `"NFKD"` — exactly these, in capitals.

**Rejects:** `"nfc"`, `"NFC "`, `"UTF-8"`, anything else.

**The forms:**

| Form   | What it does                                                                                    |
|--------|-------------------------------------------------------------------------------------------------|
| `NFC`  | **Composed**: `é` is one character. The usual form for storing and comparing.                   |
| `NFD`  | **Decomposed**: `é` is `e` plus a combining accent.                                              |
| `NFKC` | Like `NFC`, and "compatibility" characters also become their plain equivalents (`ﬁ` → `fi`, `²` → `2`, a full-width `Ａ` → `A`). |
| `NFKD` | Like `NFD`, with the same compatibility folding.                                                 |

**Example usage:**

```python
normalize_unicode("e\u0301")                   # -> 'é'      the default form is "NFC"
normalize_unicode("\ufb01 ² Ａ", "NFKC")       # -> 'fi 2 A'
normalize_unicode("é", "nfc")                  # raises ValidationError — a typo fails at the signature
```

**Why a `Literal`.** A typo (`"nfc"`, `"NFC "`) fails at the signature, not deep inside
`unicodedata`; and an editor completes the four values for you.

[▲ Back to top](#-table-of-contents)
