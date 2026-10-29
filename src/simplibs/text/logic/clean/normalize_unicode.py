import unicodedata
from simplibs.validate import validate_call
# Outers
from ...annotations import UnicodeForm


@validate_call
def normalize_unicode(
    text: str,
    form: UnicodeForm = "NFC",
) -> str:
    """Write every character in one Unicode normalization form.

    Args:
        text: The text.
        form: `"NFC"`, `"NFD"`, `"NFKC"` or `"NFKD"` (see `UnicodeForm`).

    Returns:
        The normalized text; the same text if it already was.
    """

    # 1. The standard library does the work
    normalized = unicodedata.normalize(form, text)

    # 2. Already in this form — the very same text back
    return text if normalized == text else normalized


_DESIGN_NOTES = """
# normalize_unicode — One Spelling per Letter

## Purpose
`é` can be one character or two (`e` + accent). They look the same and are not
equal, so search, comparison and file names go wrong. Normalizing first makes
them equal. `NFC` is the safe default; `NFKC` also folds look-alikes such as
`ﬁ` and full-width letters.
"""
