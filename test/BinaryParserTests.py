import unittest

from utils import pretty
from float_point_binary32 import normalize


class BinaryParserTests(unittest.TestCase):
    def test_pretty_formatter(self):
        pretty_value = pretty("0b1010101")
        self.assertEqual('101_0101', pretty_value)

        pretty_value = pretty("0b11010101")
        self.assertEqual('1101_0101', pretty_value)

    def test_normalization(self):
        normalized = normalize(0xff, 8)
        self.assertEqual("11111111", normalized)

        normalized = normalize(0x01, 8)
        self.assertEqual("00000001", normalized)

        normalized = normalize(0xa3, 8)
        self.assertEqual("10100011", normalized)

        normalized = normalize(0x10, 8)
        self.assertEqual("00010000", normalized)


if __name__ == "__main__":
    unittest.main()