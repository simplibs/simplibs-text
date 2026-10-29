from .KeepBetween import KeepBetween
from .KeepLineRange import KeepLineRange
from .KeepLinesMatching import KeepLinesMatching
from .KeepMatches import KeepMatches


_DESIGN_NOTES = """
# Text Actions Keep Sub-Package

## Purpose
Pipeline actions wrapping the keep functions: matches, lines, a range of lines, the part between two markers.

## Internal Components Registry

| Component           | Type   | Description |
| :------------------ | :----- | :---------- |
| `KeepBetween`       | Action | Wraps `keep_between`: keeps the parts between a start marker and an end marker. |
| `KeepLineRange`     | Action | Wraps `keep_line_range`: keeps the lines from `start` to `end`. |
| `KeepLinesMatching` | Action | Wraps `keep_lines_matching`: keeps only the lines that contain a match. |
| `KeepMatches`       | Action | Wraps `keep_matches`: keeps only the matches of a pattern, joined with a separator. |
"""
