# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [0.1.0] - 2026-10-29

### ✨ Added

#### Remove — take something away

* `remove_spans(text, spans, *, drop_emptied_lines=True)` — cuts given `(start, end)` character ranges out of a text; the shared primitive behind every removal and the entry point for anything that finds its own positions (a parser, a tokenizer). Ranges are half-open, may come in any order and are merged when they overlap or touch; empty ranges are ignored
* `remove_matches(text, pattern, *, flags=0, drop_emptied_lines=True)` — removes every match of a pattern; a line that became blank because of the removal disappears whole, blank lines that were already there stay
* `remove_lines_matching(text, pattern, *, flags=0)` — removes every line that contains a match; the pattern is searched in each line separately, so `^` and `$` mean the start and the end of a line
* `remove_empty_lines(text)` — removes every empty or whitespace-only line
* `strip_trailing_spaces(text)` — removes spaces and tabs from the end of every line; other whitespace characters are content
* `squeeze_blank_lines(text, max_consecutive=1)` — shortens every run of blank lines; `0` removes them all
* `trim_blank_edges(text)` — removes blank lines at the start and at the end of a text
* `dedent(text)` — removes the indentation every non-blank line has in common

#### Keep — keep only a chosen part

* `keep_matches(text, pattern, *, flags=0, separator="\n")` — keeps only the matches, joined by a separator; empty matches are skipped
* `keep_lines_matching(text, pattern, *, flags=0)` — keeps only the lines that contain a match; the exact mirror of `remove_lines_matching`
* `keep_line_range(text, start=1, end=None)` — keeps the lines from `start` to `end`, counted from 1 with both ends included; a range past the end of the text is not an error, a range that runs backwards is
* `keep_between(text, start, end, *, include_markers=True, flags=0, separator="\n")` — keeps the parts between a start marker and an end marker; the parts never overlap, a start without an end is not a part

#### Replace — change parts of the text

* `replace_matches(text, pattern, replacement, *, flags=0, count=0)` — replaces the matches by a literal text (`"\1"` is not a group reference) or by the result of a function that gets the `re.Match`; empty matches are replaced too, so `^` with `re.MULTILINE` prefixes every line
* `map_lines(text, func)` — applies a function to every line; the open door for steps the library does not have

#### Decorate — add to or reshape the text

* `add_line_numbers(text, *, start=1, template="{number:>{width}}: {line}", width=None)` — puts a number in front of every line, blank ones included; the template is checked up front
* `indent(text, prefix="    ")` — puts a prefix (a text, or a number of spaces) in front of every non-blank line
* `truncate(text, *, max_lines=None, max_chars=None, marker="… (truncated)")` — shortens a text to a number of lines and / or characters and says so with a marker on its own line; `max_chars` counts the final newline
* `wrap(text, width=80, *, break_long_words=False)` — wraps lines longer than a width, keeping each line's indentation; only lines that are too long are touched, and words break only at whitespace

#### Clean — the characters of the text

* `normalize_unicode(text, form="NFC")` — writes every character in one of the four Unicode normalization forms
* `remove_diacritics(text)` — removes accents from letters, written as one character or as a separate combining mark; a character without an accent is never touched, and the vowel signs of other scripts are left alone
* `keep_ascii(text)` — keeps only the ASCII characters
* `remove_punctuation(text)` — removes punctuation, as Unicode defines it (category `P`)
* `replace_punctuation(text, replacement=" ")` — replaces every punctuation character with a text
* `remove_symbols(text)` — removes symbols (category `S`): currency and math signs, `+ = < > ~`, emoji; the invisible joiners of multi-part emoji (U+200D, U+FE0F) stay behind
* `remove_non_alphanumeric(text, *, keep_whitespace=True)` — keeps only letters and digits of any script, together with the combining marks that follow a kept letter (accents written as separate characters, vowel signs)

#### Case — naming styles

* `split_words(text)` — splits a text or an identifier into its words (spaces, `snake_case`, `kebab-case`, `camelCase`, `PascalCase`, acronyms); returns a `list[str]`; combining marks belong to the word they follow, so decomposed and composed spellings give the same words
* `to_snake_case(text)`, `to_kebab_case(text)`, `to_camel_case(text)`, `to_pascal_case(text)` — convert every line separately, keeping its indentation; a line without any word is left as it is

#### Recipes — ready-made combinations

* `cleanup_whitespace(text)` — strips line ends, shortens runs of blank lines to one and trims the edges; the structure stays
* `compact(text)` — strips line ends and removes every blank line

#### Behaviour shared by all functions

* A `str` pattern or replacement is **literal**; regex enters on purpose through `re.compile(...)`, a `Regex` tree or a `RegexPattern`
* Only `"\n"` separates lines; the final newline of a text is remembered
* A function that finds nothing to change returns the very same text
* Every public function is validated by `@validate_call`

#### Actions — `simplibs.text.actions`

* Thirty actions in six groups, one for every function except the two recipes: `RemoveSpans`, `RemoveMatches`, `RemoveLinesMatching`, `RemoveEmptyLines`, `StripTrailingSpaces`, `SqueezeBlankLines`, `TrimBlankEdges`, `Dedent`; `KeepMatches`, `KeepLinesMatching`, `KeepLineRange`, `KeepBetween`; `ReplaceMatches`, `MapLines`; `AddLineNumbers`, `Indent`, `Truncate`, `Wrap`; `NormalizeUnicode`, `RemoveDiacritics`, `KeepAscii`, `RemovePunctuation`, `ReplacePunctuation`, `RemoveSymbols`, `RemoveNonAlphanumeric`; `SplitWords`, `ToSnakeCase`, `ToKebabCase`, `ToCamelCase`, `ToPascalCase`
* The text is the main input and every other parameter of the function is a keyword-only constructor option
* Chainable with `>>`, `&` and `|`, and awaitable through `acall`
* `SplitWords` is the one action whose result is not a text

#### Presets — `simplibs.text.presets`

* `CLEANUP_WHITESPACE` — `StripTrailingSpaces() >> SqueezeBlankLines(max_consecutive=1) >> TrimBlankEdges()`; the pipeline form of `cleanup_whitespace`
* `COMPACT` — `StripTrailingSpaces() >> RemoveEmptyLines()`; the pipeline form of `compact`

#### Annotations

* `Pattern` — what to look for: a literal `str`, a compiled `re.Pattern`, a `Regex` tree or a `RegexPattern`; the empty string is rejected; `flags=` is refused with an already compiled pattern
* `Replacement` — a literal `str`, or a function from the `re.Match` to a `str`
* `LineNumber` — a line number counted from 1 (rejects zero, negatives and `bool`)
* `UnicodeForm` — `"NFC"`, `"NFD"`, `"NFKC"` or `"NFKD"`

#### Exceptions

* The library defines no exceptions of its own; a wrong call raises `ParamError` from `simplibs-exception`
* Error names: `TEXT_CALLBACK_RESULT_INVALID`, `TEXT_LINE_RANGE_INVALID`, `TEXT_PATTERN_COMPILE_FAILED`, `TEXT_PATTERN_FLAGS_CONFLICT`, `TEXT_SPAN_INVALID`, `TEXT_TEMPLATE_INVALID`, `TEXT_TRUNCATE_LIMIT_MISSING`            <!-- EVERY name from the code, no more, no less -->

#### Package Layout

* `simplibs.text` exports the functions and the four annotations directly; `actions` and `presets` are domain packages with their own `__all__`
* Layers that only look left: `annotations` ← `logic/_common` ← the domains of `logic/` ← `recipes` ← `actions` ← `presets`; the domains of `logic/` never import each other

#### Documentation

* Main `README.md` with a quick start in four levels, the package structure, a quick reference and the table of error names
* Detailed references in `docs/`: `README_TEXT_ANNOTATIONS`, `README_TEXT_ACTIONS` and `README_TEXT_PRESETS`, and under `docs/logic/` `README_TEXT_REMOVE`, `README_TEXT_KEEP`, `README_TEXT_REPLACE`, `README_TEXT_DECORATE`, `README_TEXT_CLEAN`, `README_TEXT_CASE` and `README_TEXT_RECIPES` — one card per function or action, with a view under the hood

#### Dependencies

* `simplibs-exception` — the structured cards behind every error
* `simplibs-validate` — `@validate_call` on the public functions
* `simplibs-actions` — the `Action` classes behind `simplibs.text.actions`
* `simplibs-types` — `int_positive` and `int_non_negative` for widths and counts
* `simplibs-regex` — the `Regex` tree and the `RegexPattern` accepted as a `Pattern`

---

## Legend

* 🔄 **Changed** — modifications to existing functionality
* ✨ **Added** — new features and components
* 🐛 **Fixed** — bug fixes
* 📋 **Improved** — enhancements to existing features
* ⚠️ **Deprecated** — deprecated functionality (not used yet in this project)
* 🗑️ **Removed** — removed functionality (not used yet in this project)
