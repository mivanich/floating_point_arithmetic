import unittest

from main import pretty_print
from main import normalize

class BinaryParserTests(unittest.TestCase):
    def test_pretty_formatter(self):
        str = pretty_print("0b1010101")
        self.assertEqual('0b101_0101', str)

        str = pretty_print("0b11010101")
        self.assertEqual('0b1101_0101', str)

    def test_normalization(self):
        # str = "0b1010101"
        normalized = normalize(0xff, 8)
        self.assertEqual("11111111", normalized)



if __name__ == "__main__":
    unittest.main()