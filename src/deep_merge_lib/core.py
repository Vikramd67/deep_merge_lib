"""Core deep-merge implementation with explicit list and null rules.

Design decisions (stated plainly so the tests can assert them):

* Only ``Mapping`` inputs are accepted. Anything else raises ``MergeError``.
  This keeps the contract small and avoids guessing how sequences or scalars
  should combine.
* Nested mappings are merged recursively.
* Lists are replaced by the incoming list, not concatenated. Concatenation
  is lossy for ordered data and makes it impossible to intentionally shrink a
  list; replacement is the least surprising rule.
* ``None`` is treated as an explicit value, not as a deletion marker. A key
  present with value ``None`` in the override wins over any value in the base.
  Deletion is therefore not supported by this library; callers who need it
  should drop the key before merging.
* The function is pure: neither input mapping is mutated. New mappings are
  built for every level that changes, and unchanged subtrees are shared by
  reference. Sharing is safe because the result is never mutated internally.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any


class MergeError(TypeError):
    """Raised when deep_merge is given something that is not a mapping."""


_MISSING = object()


def deep_merge(base: Mapping, override: Mapping) -> dict:
    """Return a new mapping with ``override`` merged into ``base``.

    Args:
        base: The mapping that supplies defaults.
        override: The mapping whose values take precedence.

    Returns:
        A plain ``dict``. Values that exist only in ``base`` are preserved.
        Nested mappings are merged recursively. Lists and all other non-mapping
        values from ``override`` replace the value from ``base``. ``None`` in
        ``override`` is a normal value and replaces whatever was in ``base``.

    Raises:
        MergeError: If either argument is not a ``Mapping``.
    """
    if not isinstance(base, Mapping):
        raise MergeError(f"base must be a mapping, got {type(base).__name__}")
    if not isinstance(override, Mapping):
        raise MergeError(f"override must be a mapping, got {type(override).__name__}")

    result = dict(base)
    for key, override_value in override.items():
        base_value = result.get(key, _MISSING)
        if base_value is _MISSING:
            result[key] = override_value
            continue
        if isinstance(base_value, Mapping) and isinstance(override_value, Mapping):
            result[key] = deep_merge(base_value, override_value)
        else:
            # Lists, scalars, and None all take the override value. This is the
            # single rule that makes the behaviour predictable.
            result[key] = override_value
    return result
