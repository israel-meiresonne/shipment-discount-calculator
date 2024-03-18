import unittest


from module.utils import Helper


class TestHelper(unittest.TestCase):

    def test_check_type_valid_string(self):
        """Test check_type with valid string input."""
        name = "argument_name"
        value = "valid_string"
        class_or_tuple = str
        self.assertTrue(Helper.check_type(name, value, class_or_tuple))

    def test_check_type_valid_integer(self):
        """Test check_type with valid integer input."""
        name = "argument_name"
        value = 42
        class_or_tuple = int
        self.assertTrue(Helper.check_type(name, value, class_or_tuple))

    def test_check_type_valid_tuple_of_types(self):
        """Test check_type with valid tuple of types."""
        name = "argument_name"
        value = 42
        class_or_tuple = int, float
        self.assertTrue(Helper.check_type(name, value, class_or_tuple))

    def test_check_type_invalid_type(self):
        """Test check_type with invalid type."""
        name = "argument_name"
        value = [1, 2, 3]  # List, not the required type
        class_or_tuple = int
        with self.assertRaises(TypeError) as e:
            Helper.check_type(name, value, class_or_tuple)
        self.assertEqual(str(e.exception),
                         f"The {name} must be of type " +
                         f"'{class_or_tuple.__name__}', "
                         f"instead type='{type(value).__name__}'" +
                         f" and {name}='{value}'"
                         )

    def test_check_type_invalid_tuple_of_types(self):
        """Test check_type with invalid type."""
        name = "argument_name"
        value = [1, 2, 3]  # List, not the required type
        class_or_tuple = int, float
        with self.assertRaises(TypeError) as e:
            Helper.check_type(name, value, class_or_tuple)
        class_names = [_class.__name__ for _class in class_or_tuple]
        str_class_names = ', '.join(class_names)
        self.assertEqual(str(e.exception),
                         f"The {name} must be of type " +
                         f"'{str_class_names}', "
                         f"instead type='{type(value).__name__}'" +
                         f" and {name}='{value}'"
                         )

    def test_check_type_valid_subclass(self):
        """Test check_type with a valid subclass of the required type."""
        class MyInt(int):
            pass

        name = "argument_name"
        value = MyInt(10)
        class_or_tuple = int
        self.assertTrue(Helper.check_type(name, value, class_or_tuple))
        # No exception raised, test passes (int is a subclass of int)

    # Test _recursive_get

    def test_recursive_get_valid_path(self):
        """Test _recursive_get returns the value for a valid path."""
        data = {"a": {"b": {"c": 10}}}
        value = Helper._recursive_get(data, ["a", "b", "c"])
        self.assertEqual(value, 10)

    def test_recursive_get_missing_key(self):
        """Test _recursive_get returns None for a missing key."""
        data = {"a": {"b": 5}}
        value = Helper._recursive_get(data, ["a", "c"])
        # self.assertEqual(value, None)
        self.assertIsNone(value)

    def test_recursive_get_non_iterable_data(self):
        """Test _recursive_get return None for non-iterable data."""
        data = 10
        value = Helper._recursive_get(data, ["a"])
        self.assertIsNone(value)

    def test_recursive_get_empty_keys(self):
        """Test _recursive_get returns the data itself for empty keys."""
        data = {"a": 5}
        value = Helper._recursive_get(data, [])
        self.assertEqual(value, data)

    # Test is_iterable

    def test_is_iterable_valid_types(self):
        """Test is_iterable returns True for various iterable types."""
        self.assertTrue(Helper.is_iterable("string"))
        self.assertTrue(Helper.is_iterable([1, 2, 3]))
        self.assertTrue(Helper.is_iterable((1, 2, 3)))
        self.assertTrue(Helper.is_iterable({1: "a", 2: "b"}))
        self.assertTrue(Helper.is_iterable(set(["a", "b"])))

    def test_is_iterable_non_iterable(self):
        """Test is_iterable returns False for non-iterable types."""
        self.assertFalse(Helper.is_iterable(10))
        self.assertFalse(Helper.is_iterable(None))
