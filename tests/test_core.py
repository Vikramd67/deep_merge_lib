import unittest

from deep_merge_lib import MergeError, deep_merge


class DeepMergeTests(unittest.TestCase):
    def test_scalar_override(self):
        self.assertEqual(deep_merge({"a": 1}, {"a": 2}), {"a": 2})

    def test_base_only_keys_are_preserved(self):
        self.assertEqual(deep_merge({"a": 1, "b": 2}, {"b": 3}), {"a": 1, "b": 3})

    def test_override_only_keys_are_added(self):
        self.assertEqual(deep_merge({"a": 1}, {"b": 2}), {"a": 1, "b": 2})

    def test_nested_mappings_merge_recursively(self):
        base = {"user": {"name": "ada", "roles": ["admin"]}}
        override = {"user": {"roles": ["editor"]}}
        self.assertEqual(
            deep_merge(base, override),
            {"user": {"name": "ada", "roles": ["editor"]}},
        )

    def test_lists_are_replaced_not_concatenated(self):
        self.assertEqual(deep_merge({"xs": [1, 2, 3]}, {"xs": [4]}), {"xs": [4]})

    def test_none_in_override_replaces_existing_value(self):
        self.assertEqual(deep_merge({"a": 1}, {"a": None}), {"a": None})

    def test_none_in_base_is_replaced_by_mapping(self):
        self.assertEqual(deep_merge({"a": None}, {"a": {"b": 1}}), {"a": {"b": 1}})

    def test_mapping_replaced_by_scalar(self):
        self.assertEqual(deep_merge({"a": {"b": 1}}, {"a": 5}), {"a": 5})

    def test_scalar_replaced_by_mapping(self):
        self.assertEqual(deep_merge({"a": 5}, {"a": {"b": 1}}), {"a": {"b": 1}})

    def test_inputs_are_not_mutated(self):
        base = {"a": {"b": 1}, "xs": [1]}
        override = {"a": {"b": 2}, "xs": [2]}
        base_copy = {"a": {"b": 1}, "xs": [1]}
        override_copy = {"a": {"b": 2}, "xs": [2]}
        deep_merge(base, override)
        self.assertEqual(base, base_copy)
        self.assertEqual(override, override_copy)

    def test_empty_override_returns_copy_of_base(self):
        base = {"a": 1}
        result = deep_merge(base, {})
        self.assertEqual(result, base)
        self.assertIsNot(result, base)

    def test_non_mapping_base_raises(self):
        with self.assertRaises(MergeError):
            deep_merge([], {})  # type: ignore[arg-type]

    def test_non_mapping_override_raises(self):
        with self.assertRaises(MergeError):
            deep_merge({}, [])  # type: ignore[arg-type]

    def test_merge_error_is_a_type_error(self):
        # Callers that only catch TypeError should still catch MergeError.
        with self.assertRaises(TypeError):
            deep_merge(None, {})  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
