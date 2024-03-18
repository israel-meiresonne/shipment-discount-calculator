import unittest


from module.enums import Period, Provider, Size


class TestEnums(unittest.TestCase):
    def setUp(self) -> None:
        self.str_enums = (Period, Provider, Size)

    def test_valid_format(self) -> None:
        """Test if all string enums imported:
            - Have their name and value in upper case
            - Have their name matching their value
        """
        for enum in self.str_enums:
            members = dict(enum.__members__)
            for name, value in members.items():
                self.assertTrue(name.upper() == name == value)
