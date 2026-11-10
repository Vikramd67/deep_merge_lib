"""Public API for deep_merge_lib.

Exports:
    deep_merge: Merge two mappings with explicit list and null rules.
    MergeError: Raised when inputs are not mappings.
"""

from .core import MergeError, deep_merge

__all__ = ["deep_merge", "MergeError"]
