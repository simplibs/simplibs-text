# 🔁 `logic/replace` — Change Parts of the Text

The `replace` package holds the two functions that **change a text instead of cutting it**:
`replace_matches` swaps the matches of a pattern for something else, and `map_lines` hands every
line to a function of your own. The second one is the **open door** of the library: when no ready
step fits, `map_lines(text, my_function)` does the job and still takes part in pipelines.

```python
from simplibs.text import replace_matches, map_lines
```

Every function takes the **text first** and returns a **new text**; none of them touches a file.
Each is wrapped in `@validate_call`, so an argument of the wrong type (or an empty `str` as a
[`Pattern`](../README_TEXT_ANNOTATIONS.md#pattern)) is rejected with a `ValidationError` before the
body runs. Each has an [action](../README_TEXT_ACTIONS.md#replace) counterpart for pipelines.

## A note on literal replacements

A `str` replacement is inserted **exactly as written**. `"\1"` and `"\g<name>"` are **not** group
references here — they are ordinary characters — so a stray backslash can never end in
`re.error: bad escape`. When you want a group, or any computed value, pass a **function** instead:
it gets the whole `re.Match`, so named groups and positions are all available (see
[`Replacement`](../README_TEXT_ANNOTATIONS.md#replacement)).

## A note on functions you pass in

Text steps work with text, so a function given to these two must return a `str` on **every path**
(an empty one is fine). Anything else — typically `None` from a function with a forgotten `return`
— is a `ParamError` card (`TEXT_CALLBACK_RESULT_INVALID`) that says where it happened ("line 3",
"the match at 12"), not a crash somewhere inside `re`.

## A note on empty matches

A pattern that can match nothing (`a*`, or `^` with `re.MULTILINE`) matches at positions, and **each of
those matches is replaced**. That is what makes `replace_matches(text, re.compile("^", re.M), "> ")` a
way to prefix every line. Note that `^` with `re.MULTILINE` also matches after a final newline, so a
text ending with `"\n"` gets one more prefix at its very end. [`remove_matches`](README_TEXT_REMOVE.md#remove_matches)
and [`keep_matches`](README_TEXT_KEEP.md#keep_matches) skip empty matches because they have nothing to
cut or keep; replacing is the place where an empty match still means something (insertion).

## A note on removing

Both functions can make a line blank, and **neither removes it**: `replacement=""` leaves an empty
line, and an empty string returned by `map_lines` stays as an empty line. To drop what became empty
use [`remove_matches`](README_TEXT_REMOVE.md#remove_matches) (which removes emptied lines by
default), [`remove_lines_matching`](README_TEXT_REMOVE.md#remove_lines_matching) or
[`remove_empty_lines`](README_TEXT_REMOVE.md#remove_empty_lines).

---

## 🧭 Table of Contents

* [`replace_matches`](#replace_matches)
* [`map_lines`](#map_lines)
* [Errors of this package](#errors-of-this-package)

[⬅️ Back to main README](../../README.md#-logicreplace--change-parts-of-the-text)

---

### `replace_matches`

Replaces the matches of a pattern by a literal text or by the result of a function.

**Parameters:**

* `text` (*str*): The text.
* `pattern` ([*Pattern*](../README_TEXT_ANNOTATIONS.md#pattern)): A literal `str`, a compiled
  `re.Pattern`, a `Regex` tree or a `RegexPattern`. A `str` is searched for **literally**.
* `replacement` ([*Replacement*](../README_TEXT_ANNOTATIONS.md#replacement)): A literal `str`
  (inserted as it is; `""` removes the matches), or a function that gets the `re.Match` and
  returns a `str`.
* `flags` (*int*, keyword-only, default `0`): `re` flags. They work with a `str` literal too. Not
  allowed together with a compiled pattern (`re.Pattern` or `RegexPattern`), which carries its own.
* `count` (*int_non_negative*, keyword-only, default `0`): How many matches to replace, counted from
  the start of the text; `0` means all of them (as in `re.sub`).

**Returns:**

* `str`: The text with the replacements; the same text if nothing matched, and also when every
  replacement turned out to be identical to what it replaced.

**Raises:**

* `ParamError` (`TEXT_PATTERN_COMPILE_FAILED`): The pattern or the flags cannot be compiled.
* `ParamError` (`TEXT_PATTERN_FLAGS_CONFLICT`): `flags` were given with a compiled pattern.
* `ParamError` (`TEXT_CALLBACK_RESULT_INVALID`): The function returned something other than a `str`.

**Example usage:**

```python
replace_matches("a.b aXb", "a.b", "-")              # -> '- aXb'      a str is literal: "a.b" does not match "aXb"
replace_matches("a \\1 b", "\\1", "X")              # -> 'a X b'      "\1" is two characters, not a group
replace_matches("a a a a", "a", "b", count=2)       # -> 'b b a a'    the first two only
replace_matches("Abc ABC", "abc", "-", flags=re.IGNORECASE)   # -> '- -'

# a function: groups, computed values
replace_matches("Hello world", re.compile(r"\w+"), lambda m: m.group(0).upper())   # -> 'HELLO WORLD'
replace_matches("a1b22", re.compile(r"(?P<n>\d+)"), lambda m: "<" + m.group("n") + ">")   # -> 'a<1>b<22>'
replace_matches("2026-10-28", re.compile(r"(\d+)-(\d+)-(\d+)"),
                lambda m: f"{m.group(3)}.{m.group(2)}.{m.group(1)}")                    # -> '28.10.2026'

replace_matches("x\ny\n", "y", "")                   # -> 'x\n\n'      the matches are gone, their line stays (see remove_matches)
replace_matches("a\nb", re.compile("^", re.M), "> ")   # -> '> a\n> b'    an empty match is replaced: a prefix on every line
replace_matches("a\nb\n", re.compile("^", re.M), "> ") # -> '> a\n> b\n> '   …and `^` also matches after the final newline
replace_matches("same", "zzz", "-")                  # -> 'same'       the very same text back
replace_matches("a", "a", lambda m: None)            # raises ParamError (TEXT_CALLBACK_RESULT_INVALID): "... returned NoneType for the match at 0."
```

**Under the hood:**

```python
@validate_call
def replace_matches(text, pattern, replacement, *, flags=0, count=0) -> str:
    compiled = compile_pattern(pattern, flags)

    if isinstance(replacement, str):
        def substitute(match):                        # a text goes in as it is …
            return replacement
    else:
        def substitute(match):                        # … a function is called for every match and checked
            result = replacement(match)
            if not isinstance(result, str):
                raise_invalid_callback_result_error(replacement, result, f"the match at {match.start()}")
            return result

    replaced = compiled.sub(substitute, text, count=count)
    return text if replaced == text else replaced
```

Even a literal `str` goes through a **function** — that is how `re.sub` is kept from interpreting
backslashes in it. The last line returns the original object when nothing changed, so "nothing to
do" really is the very same text.

[▲ Back to top](#-table-of-contents)

---

### `map_lines`

Applies a function to every line.

**Parameters:**

* `text` (*str*): The text.
* `func` (*Callable[[str], str]*): Gets a line **without its newline** and returns the new line. The
  newline is put back by the library, so the function never has to care whether a line was the last
  one.

**Returns:**

* `str`: The text made of the new lines; the same text if no line changed.

**Raises:**

* `ParamError` (`TEXT_CALLBACK_RESULT_INVALID`): The function returned something other than a `str`.

**Example usage:**

```python
map_lines("a\nb\n", str.upper)                         # -> 'A\nB\n'
map_lines("  a\nb", "[{}]".format)                     # -> '[  a]\n[b]'        a method of str works as well as a lambda
map_lines("a\n\nb\n", lambda line: line.strip() or "-")   # -> 'a\n-\nb\n'      blank lines are lines too
map_lines("a\nb\n", lambda line: line + "\n" + line)   # -> 'a\na\nb\nb\n'      a returned "\n" is used as it is: one line becomes two
map_lines("", str.upper)                               # -> ''
map_lines("a\nb\n", lambda line: None if line == "b" else line)   # raises ParamError (TEXT_CALLBACK_RESULT_INVALID): "... returned NoneType for line 2."
```

**Under the hood:**

```python
@validate_call
def map_lines(text: str, func: Callable[[str], str]) -> str:
    lines, has_end = split_lines(text)
    mapped = []
    for number, line in enumerate(lines, start=1):
        result = func(line)
        if not isinstance(result, str):
            raise_invalid_callback_result_error(func, result, f"line {number}")
        mapped.append(result)

    if mapped == lines:
        return text                                   # nothing changed — the very same text back
    return join_lines(mapped, has_end)
```

A returned `str` may contain `"\n"`; it is used as it is, so one line can become several — the
function decides and it is not checked. It is **not** a tool for dropping lines: return `""` and the
line stays as an empty line. Line numbers in the error card are counted from 1, as in an editor.

[▲ Back to top](#-table-of-contents)

---

## Errors of this package

These functions raise `ParamError` cards of [`simplibs-exception`](https://pypi.org/project/simplibs-exception/);
the package defines no exceptions of its own. The card's `label` names the offending parameter (for
the function it is `result of '<function name>'`) and its `value` is what was given.

| Error name                     | Wraps        | Raised by                       | Fix                                                                       |
|--------------------------------|--------------|---------------------------------|---------------------------------------------------------------------------|
| `TEXT_PATTERN_COMPILE_FAILED`  | `ValueError` | `replace_matches`               | Check the pattern and the flags; pass plain text as a `str` to search it literally |
| `TEXT_PATTERN_FLAGS_CONFLICT`  | `ValueError` | `replace_matches`               | Put the flags into `re.compile(...)` or `RegexPattern(tree, flags=...)` instead of passing `flags=`           |
| `TEXT_CALLBACK_RESULT_INVALID` | `TypeError`  | `replace_matches`, `map_lines`  | Return a `str` on every path of the function, including "nothing to change" |

An argument of the wrong type is a `ValidationError` from `@validate_call` and never reaches these.

[▲ Back to top](#-table-of-contents)
