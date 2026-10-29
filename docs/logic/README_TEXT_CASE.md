# 🐍 `logic/case` — Naming Styles

The `case` package holds the functions that **rewrite names**: `my_var_name`, `my-var-name`,
`myVarName` and `MyVarName` are the same three words written four ways. `split_words` takes the words
out of any of them; the four `to_…_case` functions put them together in the style you choose.

```python
from simplibs.text import split_words, to_snake_case, to_kebab_case, to_camel_case, to_pascal_case
```

Every function takes the **text first**; none of them touches a file. Each is wrapped in
`@validate_call`, so an argument of the wrong type is rejected with a `ValidationError` before the
body runs. Each has an [action](../README_TEXT_ACTIONS.md#case) counterpart for pipelines.

## The four styles

| Function         | Style        | `"my var-name"` becomes … | Separator | Letters                                       |
|------------------|--------------|---------------------------|-----------|-----------------------------------------------|
| `to_snake_case`  | `snake_case` | `my_var_name`             | `_`       | all lowercase                                 |
| `to_kebab_case`  | `kebab-case` | `my-var-name`             | `-`       | all lowercase                                 |
| `to_camel_case`  | `camelCase`  | `myVarName`               | none      | first word lowercase, others capitalized      |
| `to_pascal_case` | `PascalCase` | `MyVarName`               | none      | every word capitalized                        |

## How the words are found

`split_words` walks through the characters. Anything that is **not a letter or a digit** separates
words (a space, `_`, `-`, `.`, `'`, a newline…); a **combining mark** (an accent, a vowel sign) is not a
separator but part of the word it follows. Inside a run of letters and digits a **capital** may
start a new word:

| Where                                               | Rule                         | Example                                   |
|-----------------------------------------------------|------------------------------|-------------------------------------------|
| after a lowercase letter or a digit, before a capital | a new word begins            | `fooBar` → `foo`, `Bar`; `v2Beta` → `v2`, `Beta` |
| the last capital of an acronym followed by lowercase  | the acronym ends before it   | `HTMLParser` → `HTML`, `Parser`           |
| between a letter and a digit                          | **no** boundary              | `utf8`, `base64`, `2fa` stay whole        |
| a combining mark                                      | stays with the letter before it | `cafe` + `´` + `Bar` → `café`, `Bar` (the accent is invisible to the rules above); `हिंदी` is one word |
| any other character                                   | separator                    | `don't` → `don`, `t`                      |

Digits belong to the word they stand next to — otherwise `utf8` would become `utf_8` and be
unrecognisable. All of this is Unicode-aware (`isalnum`, `isupper`, `islower`), so `příliš žlutý` and
`PříšerněŽlutý` split as expected; a script without letter case (Chinese) forms one word per run. A text
with accents written as separate characters (as file names from some systems are) gives the same
words as the same text with composed letters.

## A note on lines

The four `to_…_case` functions convert **every line separately** and keep its indentation, so a
list of names stays a list of names and an indented line of code stays where it is (a newline is a
separator for `split_words`, so converting the whole text at once would glue all lines into one
name). A line without any word — blank, or only punctuation — is **kept as it is**. The final
newline is remembered, and a text that is already in the target style comes back as the very same text.

## A note on acronyms and one-letter words

* `to_pascal_case("HTTPServer")` is `HttpServer`: the style capitalizes only the **first letter** of
  each word, so the acronym does not survive. `to_camel_case("HTTPServer")` is `httpServer`.
* `PascalCase` and `camelCase` carry no separators, so they cannot tell a one-letter word followed by
  a capital from an acronym: `AB` may be `A` + `B` or `AB`. A text with such words may therefore
  change once more when it is converted a second time — `to_pascal_case("a b")` gives `AB`, and
  converting that again gives `Ab`. `snake_case` and `kebab-case` keep their separators and do not
  have this problem.

---

## 🧭 Table of Contents

* [`split_words`](#split_words)
* [`to_snake_case`](#to_snake_case)
* [`to_kebab_case`](#to_kebab_case)
* [`to_camel_case`](#to_camel_case)
* [`to_pascal_case`](#to_pascal_case)
* [Errors of this package](#errors-of-this-package)

[⬅️ Back to main README](../../README.md#-logiccase--naming-styles)

---

### `split_words`

Splits a text or an identifier into its words — the common ground of all naming styles. Understands
spaces, `snake_case`, `kebab-case`, `camelCase`, `PascalCase` and acronyms.

**Parameters:**

* `text` (*str*): The text. Unlike the four conversions, it is looked at as **one** piece: a newline
  is just another separator.

**Returns:**

* `list[str]`: The words in their **original** letter case; never an empty word. An empty text, or a
  text with no letter and no digit, gives `[]`.

`split_words` is the one function of the library that does **not** return a text. It is still a fine
pipeline step ([`SplitWords`](../README_TEXT_ACTIONS.md#case) ends a text pipeline), and it is what a
caller with their own style builds on.

**Example usage:**

```python
split_words("my_var-name")          # -> ['my', 'var', 'name']
split_words("myVarName")            # -> ['my', 'Var', 'Name']
split_words("MyVarName")            # -> ['My', 'Var', 'Name']
split_words("my var name")          # -> ['my', 'var', 'name']
split_words("HTMLParser")           # -> ['HTML', 'Parser']
split_words("HTTPServer2Go")        # -> ['HTTP', 'Server2', 'Go']
split_words("v2Beta")               # -> ['v2', 'Beta']
split_words("utf8 base64")          # -> ['utf8', 'base64']
split_words("don't")                # -> ['don', 't']
split_words("příliš žlutý")         # -> ['příliš', 'žlutý']
split_words("PříšerněŽlutý")        # -> ['Příšerně', 'Žlutý']
split_words("日本語 テスト")          # -> ['日本語', 'テスト']
split_words("हिंदी")                 # -> ['हिंदी']          a vowel sign is part of its word
split_words("cafe\u0301Bar")          # -> ['cafe\u0301', 'Bar']   an accent written as a separate character stays in its word
split_words("--")                   # -> []

# your own style, built on the words
"_".join(word.upper() for word in split_words("myVarName"))       # -> 'MY_VAR_NAME'
" ".join(word.capitalize() for word in split_words("my_var_name")) # -> 'My Var Name'
```

**Under the hood:**

```python
@validate_call
def split_words(text: str) -> list[str]:
    words, current = [], []
    for index, char in enumerate(text):
        if is_mark(char):                             # a combining mark belongs to the letter before it
            if current:
                current.append(char)                  # (with no word open, it is dropped)
            continue
        if not char.isalnum():                        # anything but a letter or a digit separates words
            if current:
                words.append("".join(current)); current = []
            continue
        if current and starts_new_word(text, index):  # inside a run a capital may start a new word
            words.append("".join(current)); current = []
        current.append(char)
    if current:
        words.append("".join(current))
    return words
```

`starts_new_word` is the only place that knows where `camelCase` falls apart: it answers `False`
unless the character is a capital, `True` after a lowercase letter or a digit (`fooBar`, `v2Beta`),
and `True` for the last capital of an acronym that is followed by a lowercase letter (`HTMLParser`
splits before `P`). Both neighbours are judged **past any combining marks**, so a word written with
separate accents (`cafe` + `´` + `Bar`) splits where `café` + `Bar` does. `is_mark` is true for the
Unicode categories Mn, Mc and Me — every mark, in any script — unlike `is_diacritic_mark` in
[`clean`](README_TEXT_CLEAN.md), which knows only the accent blocks because `remove_diacritics` must
leave other scripts alone.

[▲ Back to top](#-table-of-contents)

---

### `to_snake_case`

Writes every line of a text in `snake_case`: all words lowercase, joined by `_`.

**Parameters:**

* `text` (*str*): The text; each line is converted separately.

**Returns:**

* `str`: The converted text; the same text if it already was in this style. Running it twice gives
  the same result.

**Example usage:**

```python
to_snake_case("MyVarName\nmy-var-name\n  my var name\n")   # -> 'my_var_name\nmy_var_name\n  my_var_name\n'
to_snake_case("HTTPServer")                                # -> 'http_server'
to_snake_case("user.name")                                 # -> 'user_name'
to_snake_case("x2Y")                                       # -> 'x2_y'      the digit stays with its word
to_snake_case("Příliš Žlutý")                              # -> 'příliš_žlutý'
to_snake_case("  indented_Name")                           # -> '  indented_name'    the indentation stays
to_snake_case("a\n\n---\nb\n")                             # -> 'a\n\n---\nb\n'      lines without a word are kept
```

**Under the hood:**

```python
@validate_call
def to_snake_case(text: str) -> str:
    return convert_lines(text, lambda words: "_".join(word.lower() for word in words))
```

[▲ Back to top](#-table-of-contents)

---

### `to_kebab_case`

Writes every line of a text in `kebab-case`: all words lowercase, joined by `-`.

**Parameters:**

* `text` (*str*): The text; each line is converted separately.

**Returns:**

* `str`: The converted text; the same text if it already was in this style. Running it twice gives
  the same result.

**Example usage:**

```python
to_kebab_case("MyVarName my_var_name")     # -> 'my-var-name-my-var-name'     one line is one name: the space is a separator
to_kebab_case("MyVarName\nmy_var_name")    # -> 'my-var-name\nmy-var-name'    two lines, two names
```

**Under the hood:**

```python
@validate_call
def to_kebab_case(text: str) -> str:
    return convert_lines(text, lambda words: "-".join(word.lower() for word in words))
```

[▲ Back to top](#-table-of-contents)

---

### `to_camel_case`

Writes every line of a text in `camelCase`: the first word lowercase, every other word with a capital
first letter and the rest lowercase.

**Parameters:**

* `text` (*str*): The text; each line is converted separately.

**Returns:**

* `str`: The converted text; the same text if it already was in this style.

**Example usage:**

```python
to_camel_case("my_var_name")               # -> 'myVarName'
to_camel_case("MyVarName")                 # -> 'myVarName'
to_camel_case("HTTPServer")                # -> 'httpServer'       the acronym is not kept (see above)
to_camel_case("item_2_name")               # -> 'item2Name'        a word that is only digits stays as it is
to_camel_case("  my_name\nother name\n")   # -> '  myName\notherName\n'
```

**Under the hood:**

```python
def _join_camel(words: list[str]) -> str:
    first, *rest = words
    return first.lower() + "".join(word[:1].upper() + word[1:].lower() for word in rest)

@validate_call
def to_camel_case(text: str) -> str:
    return convert_lines(text, _join_camel)
```

[▲ Back to top](#-table-of-contents)

---

### `to_pascal_case`

Writes every line of a text in `PascalCase`: every word with a capital first letter and the rest
lowercase.

**Parameters:**

* `text` (*str*): The text; each line is converted separately.

**Returns:**

* `str`: The converted text; the same text if it already was in this style.

**Example usage:**

```python
to_pascal_case("my_var_name")              # -> 'MyVarName'
to_pascal_case("HTTPServer")               # -> 'HttpServer'        only the first letter of a word is a capital
to_snake_case(to_pascal_case("HTTPServer"))   # -> 'http_server'    and back again
to_pascal_case("příliš žlutý")             # -> 'PřílišŽlutý'
to_pascal_case("a b")                      # -> 'AB'                see "one-letter words" above: a second run gives 'Ab'
```

**Under the hood:**

```python
@validate_call
def to_pascal_case(text: str) -> str:
    return convert_lines(text, lambda words: "".join(word[:1].upper() + word[1:].lower() for word in words))
```

[▲ Back to top](#-table-of-contents)

---

## The shared body: `convert_lines`

The four conversions differ only in **how the words are put together**; everything else lives in one
internal function, so they cannot drift apart:

```python
def convert_lines(text: str, join_words: Callable[[list[str]], str]) -> str:
    lines, has_end = split_lines(text)
    converted = []
    for line in lines:
        words = split_words(line)
        if not words:
            converted.append(line)                    # blank, or punctuation only: kept as it is
            continue
        lead = line[:len(line) - len(line.lstrip())]  # the indentation is not part of the name
        converted.append(lead + join_words(words))
    if converted == lines:
        return text                                   # nothing changed — the very same text back
    return join_lines(converted, has_end)
```

---

## Errors of this package

This package raises **no cards of its own**: every function accepts any text, so there is no
invalid value to report. An argument of the wrong type is a `ValidationError` from `@validate_call`
and never reaches the body.

[▲ Back to top](#-table-of-contents)
