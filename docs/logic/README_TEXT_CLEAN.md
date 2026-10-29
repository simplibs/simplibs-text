# 🔤 `logic/clean` — The Characters of the Text

The `clean` package holds the functions that work on the **characters** of a text rather than on its
lines or patterns: write them in one Unicode form, take the accents off, keep only ASCII, drop the
punctuation or the symbols, or keep only letters and digits. They prepare text for places that are
picky — search keys, slugs, file names, comparisons, counting words.

```python
from simplibs.text import (
    normalize_unicode, remove_diacritics, keep_ascii,
    remove_punctuation, replace_punctuation, remove_symbols, remove_non_alphanumeric,
)
```

Every function takes the **text first** and returns a **new text**; none of them touches a file.
Each is wrapped in `@validate_call`, so an argument of the wrong type is rejected with a
`ValidationError` before the body runs. Each has an [action](../README_TEXT_ACTIONS.md#clean)
counterpart for pipelines.

## Which function for which job

| You want …                                       | Use                       | `Příliš, žluťoučký kůň! (a+b)` becomes … |
|--------------------------------------------------|---------------------------|-------------------------------------------|
| the same letter always written the same way      | `normalize_unicode`       | the same text, in one form                |
| no accents, letters kept                         | `remove_diacritics`       | `Prilis, zlutoucky kun! (a+b)`            |
| nothing but ASCII                                | `keep_ascii`              | `Pli, luouk k! (a+b)`                     |
| no punctuation                                   | `remove_punctuation`      | `Příliš žluťoučký kůň a+b`                |
| punctuation turned into something else           | `replace_punctuation`     | `Příliš  žluťoučký kůň   a+b `            |
| no symbols (`+ = $ < > ~` and emoji)             | `remove_symbols`          | `Příliš, žluťoučký kůň! (ab)`             |
| letters and digits only                          | `remove_non_alphanumeric` | `Příliš žluťoučký kůň ab`                 |

The functions are **independent and chainable** — `keep_ascii(remove_diacritics(text))` keeps
`Prilis` where `keep_ascii(text)` alone gives `Pli`.

## A note on Unicode doing the deciding

"Is this punctuation?" is answered by the **Unicode database**, not by a hand-made list that always
forgets `„`, `—` or `¿`. Unicode gives every character a general category:

* **Punctuation** (`P…`): `. , ! ? - _ ( ) " « » „ “ — ¿ / # % @` and the like.
* **Symbols** (`S…`): `$ + < = > ^ | ~`, currency signs, math signs and emoji.
* Letters (`L…`), digits (`Nd`) and marks (`M…`) belong to neither.

So `+`, `=`, `$` and `~` are **not** punctuation, and `remove_punctuation("a+b=c $5")` leaves them
alone — use `remove_symbols` for those. And removing symbols from **source code** breaks it, because
`< > = + | ~` are symbols: these two are functions for prose.

## A note on any script

`remove_non_alphanumeric` relies on `str.isalnum`, which knows Czech, Greek and CJK letters and the
digits of other scripts, and it keeps the combining marks that follow a kept letter. `remove_diacritics`
takes only the dedicated **combining-accent blocks**, so the vowel signs of Devanagari or Thai (which
carry the vowels of their scripts) are never damaged.

## A note on nothing to do

A function that finds nothing to change returns the very same text. Most of them are also safe to
run twice; `replace_punctuation` is the exception when the replacement itself contains punctuation
(`"a-b"` with `".."` gives `"a..b"`, and a second run `"a....b"`).

---

## 🧭 Table of Contents

* [`normalize_unicode`](#normalize_unicode)
* [`remove_diacritics`](#remove_diacritics)
* [`keep_ascii`](#keep_ascii)
* [`remove_punctuation`](#remove_punctuation)
* [`replace_punctuation`](#replace_punctuation)
* [`remove_symbols`](#remove_symbols)
* [`remove_non_alphanumeric`](#remove_non_alphanumeric)
* [Errors of this package](#errors-of-this-package)

[⬅️ Back to main README](../../README.md#-logicclean--the-characters-of-the-text)

---

### `normalize_unicode`

Writes every character in one Unicode normalization form. `é` can be **one** character or **two**
(`e` plus a combining accent); they look the same and are not equal, so a search, a comparison or a
file name goes wrong. Normalizing first makes them equal.

**Parameters:**

* `text` (*str*): The text.
* `form` ([*UnicodeForm*](../README_TEXT_ANNOTATIONS.md#unicodeform), default `"NFC"`): One of
  `"NFC"`, `"NFD"`, `"NFKC"`, `"NFKD"`. A typo such as `"nfc"` fails at the signature.
  * `NFC` — composed: `é` is one character. The safe default for storing and comparing.
  * `NFD` — decomposed: `é` is `e` plus an accent.
  * `NFKC` / `NFKD` — the same, and "compatibility" characters also become their plain equivalents
    (`ﬁ` → `fi`, `²` → `2`, a full-width `Ａ` → `A`).

**Returns:**

* `str`: The normalized text; the same text if it already was.

**Example usage:**

```python
decomposed = "e\u0301"                        # 'é' written as two characters
decomposed == "é"                             # -> False
normalize_unicode(decomposed) == "é"          # -> True        now they are equal
len(normalize_unicode("é", "NFD"))            # -> 2
normalize_unicode("\ufb01 ² Ａ", "NFKC")      # -> 'fi 2 A'    look-alikes folded
normalize_unicode("abc")                      # -> 'abc'       the very same text back
```

**Under the hood:**

```python
@validate_call
def normalize_unicode(text: str, form: UnicodeForm = "NFC") -> str:
    normalized = unicodedata.normalize(form, text)
    return text if normalized == text else normalized
```

A thin, validated wrapper over `unicodedata.normalize`; the last line only makes sure that "already
normalized" returns the original object.

[▲ Back to top](#-table-of-contents)

---

### `remove_diacritics`

Removes accents and other diacritical marks from letters: `č` → `c`, `é` → `e`.

**Parameters:**

* `text` (*str*): The text.

**Returns:**

* `str`: The text without diacritics; the same text if there were none.

**Example usage:**

```python
remove_diacritics("příliš žluťoučký kůň")      # -> 'prilis zlutoucky kun'
remove_diacritics("Ångström")                  # -> 'Angstrom'
remove_diacritics("é" + "e\u0301")             # -> 'ee'        both ways of writing an accent are handled
remove_diacritics("łódź Øre đ ß æ")            # -> 'łodz Øre đ ß æ'    ł Ø đ ß æ stay — see below
remove_diacritics("हिन्दी")                     # -> 'हिन्दी'      the vowel signs of other scripts are left alone
remove_diacritics("\u0958")                    # -> '\u0958'     a letter that only looks accented (क़ = क + a nukta) is not touched
```

**Under the hood:**

```python
@validate_call
def remove_diacritics(text: str) -> str:
    if text.isascii():
        return text                                                        # plain ASCII has no accents

    pieces = []
    for char in text:                                                      # one character at a time
        if is_diacritic_mark(char):
            continue                                                       # an accent that stands alone: drop it
        decomposed = unicodedata.normalize("NFD", char)                    # 'é' -> 'e' + accent
        if decomposed != char and any(is_diacritic_mark(part) for part in decomposed):
            char = unicodedata.normalize(
                "NFC", "".join(part for part in decomposed if not is_diacritic_mark(part)))
        pieces.append(char)                                                # any other character is left exactly as it is

    result = "".join(pieces)
    return text if result == text else result
```

`ł`, `ø`, `đ`, `ß` and `æ` are **not** "a letter plus an accent" in Unicode, so they stay. Turning
them into `l`, `o`, `d`, `ss`, `ae` is *transliteration*, a different and language-dependent job.
Only the five combining-accent blocks are taken (U+0300–036F, U+1AB0–1AFF, U+1DC0–1DFF, U+20D0–20FF,
U+FE20–FE2F), not every Unicode "mark" — so the vowel signs of Devanagari and Thai survive.

**Only accented letters are touched.** Each character is looked at on its own, and a character whose
decomposition contains no accent is left exactly as it is, even when Unicode would write it in another
form (the Devanagari `क़` is `क` + a nukta, which is not an accent and is not recomposed by NFC).
Normalizing the whole text first would change such characters and break the promise "the same text if
there were none". Both forms of an accent — `é` as one character, and `e` plus a combining accent —
give `e`.

[▲ Back to top](#-table-of-contents)

---

### `keep_ascii`

Keeps only the ASCII characters (code points 0 to 127) — for places that accept nothing else.

**Parameters:**

* `text` (*str*): The text.

**Returns:**

* `str`: The text without any other character; the same text if it was ASCII only.

**Example usage:**

```python
keep_ascii("Příliš")                           # -> 'Pli'         non-ASCII is removed, not approximated
keep_ascii(remove_diacritics("Příliš"))        # -> 'Prilis'      take the accents off first to keep the letters
keep_ascii("naïve café — ok 😀")               # -> 'nave caf  ok '
keep_ascii("plain text")                       # -> 'plain text'  the very same text back
```

**Under the hood:**

```python
@validate_call
def keep_ascii(text: str) -> str:
    if text.isascii():
        return text                                   # the cheap, common case
    return "".join(char for char in text if char.isascii())
```

Newlines and tabs are ASCII, so the line structure survives. Because characters are **removed**, not
approximated, the spaces around a removed character stay (`'nave caf  ok '`); follow with a
[`replace_matches`](README_TEXT_REPLACE.md#replace_matches) step if that matters.

[▲ Back to top](#-table-of-contents)

---

### `remove_punctuation`

Removes punctuation characters — `. , ! ? - _ ( ) " « »` and everything else Unicode files under
category `P`. Prepares text for counting words or comparing it.

**Parameters:**

* `text` (*str*): The text.

**Returns:**

* `str`: The text without punctuation; the same text if there was none.

**Example usage:**

```python
remove_punctuation("Hi, you! (well-known) «ok» a_b")   # -> 'Hi you wellknown ok ab'    "well-known" is glued together
remove_punctuation("„Ahoj“ — řekl¿")                   # -> 'Ahoj  řekl'
remove_punctuation("a+b=c $5 ~x")                      # -> 'a+b=c $5 ~x'    + = $ ~ are symbols, not punctuation
```

**Under the hood:**

```python
@validate_call
def remove_punctuation(text: str) -> str:
    result = "".join(char for char in text if not has_category(char, "P"))
    return text if result == text else result
```

`has_category` asks `unicodedata.category(char)` and compares its first letter with `"P"`. A removed
hyphen **joins** two words (`well-known` → `wellknown`); to keep words apart use
[`replace_punctuation`](#replace_punctuation).

[▲ Back to top](#-table-of-contents)

---

### `replace_punctuation`

Replaces every punctuation character with a text — a space by default, so words stay apart.

**Parameters:**

* `text` (*str*): The text.
* `replacement` (*str*, default `" "`): What to put in place of **each** punctuation character. Used
  literally — a backslash is just a backslash. `""` removes (the same as `remove_punctuation`).

**Returns:**

* `str`: The changed text; the same text if there was no punctuation.

**Example usage:**

```python
replace_punctuation("well-known, indeed!")     # -> 'well known  indeed '     the words stay apart
replace_punctuation("a--b", "_")               # -> 'a__b'                    two marks, two replacements
replace_punctuation("a, b", "")                # -> 'a b'
replace_punctuation("a-b", "\\1")              # -> 'a\\1b'                   literal: no group reference
```

**Under the hood:**

```python
@validate_call
def replace_punctuation(text: str, replacement: str = " ") -> str:
    result = "".join(replacement if has_category(char, "P") else char for char in text)
    return text if result == text else result
```

Because **every** mark is replaced, `", "` becomes two spaces and `"--"` two replacements. Tidy that
up with [`replace_matches`](README_TEXT_REPLACE.md#replace_matches) or by splitting into words with
[`split_words`](README_TEXT_CASE.md#split_words).

[▲ Back to top](#-table-of-contents)

---

### `remove_symbols`

Removes symbol characters — `$ + < = > ^ | ~`, currency signs, math signs, emoji and the like (Unicode
category `S`). The other half of "special characters": what is not punctuation, not a letter, not a
digit and not whitespace.

**Parameters:**

* `text` (*str*): The text.

**Returns:**

* `str`: The text without symbols; the same text if there were none.

**Example usage:**

```python
remove_symbols("€5 + 3 = 8")                   # -> '5  3  8'
remove_symbols("a<b>c|d~e^f 😀 ok")            # -> 'abcdef  ok'
remove_symbols("Hi, you! (ok) $5")             # -> 'Hi, you! (ok) 5'    punctuation stays
remove_symbols("a\U0001F468\u200d\U0001F469\u200d\U0001F467b")   # -> 'a\u200d\u200db'   a family emoji leaves its invisible joiners behind
```

**Under the hood:**

```python
@validate_call
def remove_symbols(text: str) -> str:
    result = "".join(char for char in text if not has_category(char, "S"))
    return text if result == text else result
```

A function for **prose**. In source code `<`, `>`, `=`, `+`, `|` and `~` are symbols, so removing them
breaks the code.

**Joined emoji.** An emoji made of several parts (a family, a skin tone) is joined by invisible
characters (U+200D, U+FE0F) that are not symbols themselves. They stay behind.

[▲ Back to top](#-table-of-contents)

---

### `remove_non_alphanumeric`

Keeps only letters and digits, of any script, **with the combining marks that belong to them** — the
strictest cleanup: no punctuation, no symbols, no leftovers.

**Parameters:**

* `text` (*str*): The text.
* `keep_whitespace` (*bool*, keyword-only, default `True`): Keep spaces, tabs and newlines, so words
  and lines survive. With `False` the result is one unbroken run — for codes and identifiers.

**Returns:**

* `str`: The text with everything else removed; the same text if there was nothing else.

**Example usage:**

```python
remove_non_alphanumeric("Hello, world! 42\n")                     # -> 'Hello world 42\n'
remove_non_alphanumeric("AB-12 / x", keep_whitespace=False)       # -> 'AB12x'
remove_non_alphanumeric("Příliš, žluťoučký 7!")                   # -> 'Příliš žluťoučký 7'
remove_non_alphanumeric("日本語。テスト！")                         # -> '日本語テスト'
remove_non_alphanumeric("a_b-c")                                  # -> 'abc'      the underscore is punctuation
remove_non_alphanumeric("e\u0301x!")                              # -> 'e\u0301x'  an accent written as a separate character stays with its letter
remove_non_alphanumeric("हिंदी, ok!")                             # -> 'हिंदी ok'   the vowel signs of other scripts stay
remove_non_alphanumeric("\u0301a")                               # -> 'a'        a mark with nothing before it goes
```

**Under the hood:**

```python
@validate_call
def remove_non_alphanumeric(text: str, *, keep_whitespace: bool = True) -> str:
    kept, anchored = [], False            # `anchored`: the previous character was kept as a letter, a digit or a mark
    for char in text:
        if char.isalnum():
            kept.append(char); anchored = True
        elif anchored and has_category(char, "M"):
            kept.append(char)             # a mark right after a kept character still belongs to it
        elif keep_whitespace and char.isspace():
            kept.append(char); anchored = False
        else:
            anchored = False
    result = "".join(kept)
    return text if result == text else result
```

Unlike the two functions above, this one starts from `str.isalnum()` rather than from a Unicode
category. `isalnum()` does not count a vowel sign of Devanagari or Thai, or an accent written as a
separate combining character (`e` + `´`), as "alphanumeric" — yet removing them would destroy the
word. A mark is therefore **kept when the character before it was kept**, and removed together with a
letter that is removed. A mark with nothing before it goes.

[▲ Back to top](#-table-of-contents)

---

## Errors of this package

This package raises **no cards of its own**: every function accepts any text, so there is no
invalid value to report. An argument of the wrong type — or a `form` that is not one of the four
Unicode forms — is a `ValidationError` from `@validate_call` and never reaches the body.

[▲ Back to top](#-table-of-contents)
