import pytest
from simplibs.exception import ValidationError
from simplibs.text import (
    add_line_numbers, cleanup_whitespace, compact, dedent, indent, keep_ascii, keep_between,
    keep_line_range, keep_lines_matching, keep_matches, map_lines, normalize_unicode,
    remove_diacritics, remove_empty_lines, remove_lines_matching, remove_matches,
    remove_non_alphanumeric, remove_punctuation, remove_spans, remove_symbols, replace_matches,
    replace_punctuation, split_words, squeeze_blank_lines, strip_trailing_spaces, to_camel_case,
    to_kebab_case, to_pascal_case, to_snake_case, trim_blank_edges, truncate, wrap,
)

# The functions and the arguments they need besides the text.
FUNCTIONS = {
    "add_line_numbers": (add_line_numbers, ()),
    "cleanup_whitespace": (cleanup_whitespace, ()),
    "compact": (compact, ()),
    "dedent": (dedent, ()),
    "indent": (indent, ()),
    "keep_ascii": (keep_ascii, ()),
    "keep_between": (keep_between, ("[", "]")),
    "keep_line_range": (keep_line_range, ()),
    "keep_lines_matching": (keep_lines_matching, ("a",)),
    "keep_matches": (keep_matches, ("a",)),
    "map_lines": (map_lines, (str.upper,)),
    "normalize_unicode": (normalize_unicode, ()),
    "remove_diacritics": (remove_diacritics, ()),
    "remove_empty_lines": (remove_empty_lines, ()),
    "remove_lines_matching": (remove_lines_matching, ("a",)),
    "remove_matches": (remove_matches, ("a",)),
    "remove_non_alphanumeric": (remove_non_alphanumeric, ()),
    "remove_punctuation": (remove_punctuation, ()),
    "remove_spans": (remove_spans, ([(0, 1)],)),
    "remove_symbols": (remove_symbols, ()),
    "replace_matches": (replace_matches, ("a", "b")),
    "replace_punctuation": (replace_punctuation, ()),
    "split_words": (split_words, ()),
    "squeeze_blank_lines": (squeeze_blank_lines, ()),
    "strip_trailing_spaces": (strip_trailing_spaces, ()),
    "to_camel_case": (to_camel_case, ()),
    "to_kebab_case": (to_kebab_case, ()),
    "to_pascal_case": (to_pascal_case, ()),
    "to_snake_case": (to_snake_case, ()),
    "trim_blank_edges": (trim_blank_edges, ()),
    "truncate": (truncate, ()),
    "wrap": (wrap, ()),
}


@pytest.mark.parametrize("name", sorted(FUNCTIONS))
@pytest.mark.parametrize("text", [5, None, b"abc", ["a"], 1.5], ids=["int", "None", "bytes", "list", "float"])
def test_every_function_rejects_a_text_that_is_not_a_str(name, text) -> None:
    """The first argument must be a str; anything else is a ValidationError."""
    function, extra = FUNCTIONS[name]
    with pytest.raises(ValidationError):
        function(text, *extra)


BAD_OPTIONS = {
    "add_line_numbers: negative start": lambda: add_line_numbers("a", start=-1),
    "add_line_numbers: zero width": lambda: add_line_numbers("a", width=0),
    "add_line_numbers: template not a str": lambda: add_line_numbers("a", template=5),
    "indent: negative prefix": lambda: indent("a", -1),
    "indent: prefix None": lambda: indent("a", None),
    "keep_between: empty start": lambda: keep_between("a", "", "]"),
    "keep_between: end not a pattern": lambda: keep_between("a", "[", 5),
    "keep_between: include_markers not a bool": lambda: keep_between("a", "[", "]", include_markers="x"),
    "keep_between: separator not a str": lambda: keep_between("a", "[", "]", separator=5),
    "keep_line_range: zero start": lambda: keep_line_range("a", 0),
    "keep_line_range: zero end": lambda: keep_line_range("a", 1, 0),
    "keep_line_range: start not an int": lambda: keep_line_range("a", "x"),
    "keep_lines_matching: empty pattern": lambda: keep_lines_matching("a", ""),
    "keep_lines_matching: flags not an int": lambda: keep_lines_matching("a", "a", flags="x"),
    "keep_matches: empty pattern": lambda: keep_matches("a", ""),
    "keep_matches: pattern not a pattern": lambda: keep_matches("a", 5),
    "keep_matches: separator not a str": lambda: keep_matches("a", "a", separator=5),
    "map_lines: func not callable": lambda: map_lines("a", 5),
    "normalize_unicode: unknown form": lambda: normalize_unicode("a", "nfc"),
    "normalize_unicode: form not a str": lambda: normalize_unicode("a", 5),
    "remove_lines_matching: empty pattern": lambda: remove_lines_matching("a", ""),
    "remove_lines_matching: flags not an int": lambda: remove_lines_matching("a", "a", flags="x"),
    "remove_matches: empty pattern": lambda: remove_matches("a", ""),
    "remove_matches: pattern not a pattern": lambda: remove_matches("a", 5),
    "remove_matches: flags not an int": lambda: remove_matches("a", "a", flags="x"),
    "remove_matches: drop_emptied_lines not a bool": lambda: remove_matches("a", "a", drop_emptied_lines="x"),
    "remove_non_alphanumeric: keep_whitespace not a bool": lambda: remove_non_alphanumeric("a", keep_whitespace="x"),
    "remove_spans: spans not a sequence": lambda: remove_spans("a", 5),
    "remove_spans: span of three": lambda: remove_spans("abc", [(1, 2, 3)]),
    "remove_spans: drop_emptied_lines not a bool": lambda: remove_spans("a", [(0, 1)], drop_emptied_lines="x"),
    "replace_matches: empty pattern": lambda: replace_matches("a", "", "b"),
    "replace_matches: replacement not a str or function": lambda: replace_matches("a", "a", 5),
    "replace_matches: negative count": lambda: replace_matches("a", "a", "b", count=-1),
    "replace_punctuation: replacement not a str": lambda: replace_punctuation("a", 5),
    "squeeze_blank_lines: negative max": lambda: squeeze_blank_lines("a", -1),
    "squeeze_blank_lines: max not an int": lambda: squeeze_blank_lines("a", "x"),
    "truncate: zero max_lines": lambda: truncate("a", max_lines=0),
    "truncate: max_chars not an int": lambda: truncate("a", max_chars="x"),
    "truncate: marker not a str": lambda: truncate("a", max_lines=1, marker=5),
    "wrap: zero width": lambda: wrap("a", 0),
    "wrap: width not an int": lambda: wrap("a", "x"),
    "wrap: break_long_words not a bool": lambda: wrap("a", break_long_words="x"),
}


@pytest.mark.parametrize("name", sorted(BAD_OPTIONS))
def test_every_option_rejects_a_value_of_the_wrong_kind(name) -> None:
    """Wrong type or out-of-range value of an option is a ValidationError, whatever the text."""
    with pytest.raises(ValidationError):
        BAD_OPTIONS[name]()
