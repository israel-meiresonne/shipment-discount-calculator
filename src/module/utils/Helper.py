class Helper:
    @staticmethod
    def check_type(name: str, value, class_or_tuple) -> True:
        def check(name: str, value, class_or_tuple) -> None:
            if not isinstance(value, class_or_tuple):
                if isinstance(class_or_tuple, tuple):
                    class_names = [
                        _class.__name__ for _class in class_or_tuple]
                    str_class_names = ', '.join(class_names)
                else:
                    str_class_names = class_or_tuple.__name__
                raise TypeError(
                    f"The {name} must be of type " +
                    f"'{str_class_names}', " +
                    f"instead type='{type(value).__name__}' " +
                    f"and {name}='{value}'"
                )
        check('name', name, str)
        check(name, value, class_or_tuple)
        return True

    @classmethod
    def _recursive_get(cls, data, keys):
        """
        Recursively retrieves a value from a nested dictionary using
        a list of keys.

        Args:
            data: The nested dictionary to search.
            keys: A list of keys representing the path to the desired value.

        Returns:
            The value found at the specified path within the nested dictionary,
            or None if the path doesn't exist.
        """
        if not keys:
            return data
        key = keys[0]
        if cls.is_iterable(data) and (key in data):
            return cls._recursive_get(data[key], keys[1:])
        else:
            return None

    @staticmethod
    def is_iterable(obj) -> bool:
        """
        Checks if a value is iterable using isinstance().

        Args:
            obj: The value to check.

        Returns:
            True if the value is iterable, False otherwise.
        """
        return isinstance(obj, (str, list, tuple, set, dict)) \
            or hasattr(obj, '__iter__')
