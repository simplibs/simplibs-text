import simplibs.text as text_package
import simplibs.text.actions as actions_package
import simplibs.text.presets as presets_package

ANNOTATIONS = {"LineNumber", "Pattern", "Replacement", "UnicodeForm"}
RECIPES = {"cleanup_whitespace", "compact"}
FUNCTIONS = {
    "add_line_numbers", "dedent", "indent", "keep_ascii", "keep_between", "keep_line_range",
    "keep_lines_matching", "keep_matches", "map_lines", "normalize_unicode", "remove_diacritics",
    "remove_empty_lines", "remove_lines_matching", "remove_matches", "remove_non_alphanumeric",
    "remove_punctuation", "remove_spans", "remove_symbols", "replace_matches", "replace_punctuation",
    "split_words", "squeeze_blank_lines", "strip_trailing_spaces", "to_camel_case", "to_kebab_case",
    "to_pascal_case", "to_snake_case", "trim_blank_edges", "truncate", "wrap",
}


def _action_name(function_name: str) -> str:
    return "".join(part.capitalize() for part in function_name.split("_"))


def test_the_root_exports_exactly_the_annotations_the_functions_and_the_recipes() -> None:
    """A name that disappears or sneaks in is noticed."""
    assert set(text_package.__all__) == ANNOTATIONS | FUNCTIONS | RECIPES


def test_the_root_exports_no_name_twice() -> None:
    """One entry per name."""
    assert len(text_package.__all__) == len(set(text_package.__all__))


def test_every_root_name_can_be_imported_from_the_root() -> None:
    """`__all__` lists only what is really there."""
    for name in text_package.__all__:
        assert hasattr(text_package, name), name


def test_every_root_function_is_documented() -> None:
    """A docstring on each public function."""
    for name in FUNCTIONS | RECIPES:
        assert getattr(text_package, name).__doc__, name


def test_actions_and_presets_are_not_exported_from_the_root() -> None:
    """They live in their own folders, as in `file` and `path`."""
    for name in actions_package.__all__ + presets_package.__all__:
        assert not hasattr(text_package, name), name


def test_the_actions_package_has_one_action_for_every_function_except_the_recipes() -> None:
    """Thirty functions, thirty actions, named in CamelCase."""
    assert set(actions_package.__all__) == {_action_name(name) for name in FUNCTIONS}
    assert len(actions_package.__all__) == 30


def test_every_action_is_exported_under_its_own_name() -> None:
    """The class carries the name it is imported by."""
    for name in actions_package.__all__:
        assert getattr(actions_package, name).__name__ == name


def test_the_presets_package_has_one_chain_for_every_recipe() -> None:
    """`CLEANUP_WHITESPACE` and `COMPACT` stand beside the two recipe functions."""
    assert set(presets_package.__all__) == {name.upper() for name in RECIPES}
