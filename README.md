# deep_merge_lib

Merge nested mappings with explicit rules for lists and nulls.

```python
from deep_merge_lib import deep_merge

base = {"user": {"name": "ada", "roles": ["admin"]}, "active": True}
override = {"user": {"roles": ["editor"]}, "active": None}

merged = deep_merge(base, override)
assert merged == {"user": {"name": "ada", "roles": ["editor"]}, "active": None}
```

## Why this exists

Config layering usually needs two things that plain `dict.update` gets wrong:
recursive merging of nested sections, and a clear answer for lists and
`None`. This library picks one answer for each and documents it, so callers
can reason about the result without reading the implementation.

The trade-off is that lists are **replaced**, not concatenated. Concatenation
looks convenient until you need to remove an item or reorder a list; then it
is impossible to express. Replacement is the only rule that lets an override
shrink a list, and it keeps the merge associative in the sense that the last
override wins. If you need concatenation, do it explicitly before calling
`deep_merge`.

`None` is treated as an ordinary value. An override of `{"a": None}` sets
`a` to `None`; it does not delete the key. Deletion is intentionally not part
of the API, because a deletion marker would need to be a sentinel value that
callers cannot accidentally pass as real data. To delete a key, remove it
from the mapping before merging.

## API

### `deep_merge(base, override) -> dict`

Returns a new `dict`. Nested mappings are merged recursively. Lists and all
other non-mapping values from `override` replace the corresponding value from
`base`. Keys present only in `base` are preserved. Neither input is mutated.

Raises `MergeError` (a subclass of `TypeError`) if either argument is not a
`collections.abc.Mapping`.

### `MergeError`

The exception raised for non-mapping inputs. It subclasses `TypeError` so
existing code that catches `TypeError` around a merge continues to work.

## The awkward edge

Because lists are replaced, merging `{"xs": [1, 2]}` with `{"xs": [3]}`
gives `{"xs": [3]}`, not `{"xs": [1, 2, 3]}`. That is deliberate. The same
applies to tuples and sets: they are values, not mergeable structures.
