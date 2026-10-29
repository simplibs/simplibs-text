import unicodedata
import pytest
from simplibs.text.logic.case import split_words


@pytest.mark.parametrize(
    "text",
    ["my_var_name", "my-var-name", "myVarName", "MyVarName", "my var name", "my_var-name", "MY_VAR_NAME"],
)
def test_split_words_every_naming_style_gives_the_same_words(text) -> None:
    """The common ground of all case conversions (case is kept; this is the words as written)."""
    assert [word.lower() for word in split_words(text)] == ["my", "var", "name"]


@pytest.mark.parametrize(
    "text, expected",
    [
        ("HTMLParser", ["HTML", "Parser"]),
        ("getHTTPResponseCode", ["get", "HTTP", "Response", "Code"]),
        ("HTTPServer2Go", ["HTTP", "Server2", "Go"]),
        ("v2Beta", ["v2", "Beta"]),
        ("utf8", ["utf8"]),
        ("base64Encode", ["base64", "Encode"]),
        ("2fa", ["2fa"]),
        ("md5sum", ["md5sum"]),
        ("ABC", ["ABC"]),
    ],
)
def test_split_words_camel_case_acronyms_and_digits(text, expected) -> None:
    """A digit stays with the word it stands next to, so `utf8` and `md5` stay recognizable."""
    assert split_words(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        ("a__b--c  d", ["a", "b", "c", "d"]),
        ("_a_", ["a"]),
        ("  hello,   world! ", ["hello", "world"]),
        ("a\nb\tc", ["a", "b", "c"]),
        ("don't", ["don", "t"]),
        ("a.b/c", ["a", "b", "c"]),
    ],
)
def test_split_words_anything_that_is_not_a_letter_or_digit_separates(text, expected) -> None:
    """Any number of separators of any kind, at the ends too; no empty words."""
    assert split_words(text) == expected


@pytest.mark.parametrize("text", ["", "---", "   ", "!?_", "\n\n"])
def test_split_words_a_text_without_letters_and_digits_has_no_words(text) -> None:
    """An empty list."""
    assert split_words(text) == []


def test_split_words_the_words_keep_their_original_case() -> None:
    """Nothing is lowercased here."""
    assert split_words("myVar_Name") == ["my", "Var", "Name"]


def test_split_words_returns_a_list() -> None:
    """The one function of this package that does not return a text."""
    assert isinstance(split_words("a b"), list)


@pytest.mark.parametrize(
    "text, expected",
    [
        ("p\u0159\u00edli\u0161 \u017elut\u00fd", ["p\u0159\u00edli\u0161", "\u017elut\u00fd"]),
        ("P\u0159\u00ed\u0161ern\u011b\u017dlut\u00fd", ["P\u0159\u00ed\u0161ern\u011b", "\u017dlut\u00fd"]),
        ("\u4e2d\u6587 \u5b57", ["\u4e2d\u6587", "\u5b57"]),
        ("\u4e2d\u6587abc", ["\u4e2d\u6587abc"]),
        ("\u0939\u093f\u0902\u0926\u0940 \u092d\u093e\u0937\u093e", ["\u0939\u093f\u0902\u0926\u0940", "\u092d\u093e\u0937\u093e"]),
    ],
    ids=["czech", "czech-camel", "chinese", "chinese-with-latin", "hindi"],
)
def test_split_words_other_scripts(text, expected) -> None:
    """Letters of any script; a script without letter case forms one word per run."""
    assert split_words(text) == expected


@pytest.mark.parametrize(
    "text",
    ["P\u0159\u00edli\u0161 \u017elut\u00fd", "caf\u00e9Bar", "P\u0159\u00ed\u0161ern\u011b\u017dlut\u00fd", "HTML\u010cajn\u00edk", "\u00c9X2", "\u0939\u093f\u0902\u0926\u0940 ok"],
)
def test_split_words_composed_and_decomposed_input_give_the_same_words(text) -> None:
    """Accents written as separate combining characters (as some file systems do) do not split words."""
    composed = split_words(unicodedata.normalize("NFC", text))
    decomposed = [unicodedata.normalize("NFC", word) for word in split_words(unicodedata.normalize("NFD", text))]
    assert decomposed == composed


def test_split_words_a_mark_with_no_word_open_is_dropped() -> None:
    """At the start, or after a separator, it has nothing to belong to."""
    assert split_words("\u0301abc") == ["abc"]
    assert split_words("a -\u0301b") == ["a", "b"]


def test_split_words_a_combining_mark_stays_in_the_word() -> None:
    """The word is the letter and its marks."""
    assert split_words("cafe\u0301 bar") == ["cafe\u0301", "bar"]
