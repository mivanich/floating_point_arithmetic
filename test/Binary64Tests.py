import unittest, math


from float_point_binary64 import build_float, disassemble_float


class Binary64Tests(unittest.TestCase):
    def test_no_fraction_disassemble(self):
        value = 42.0
        sign, exponent, fraction = disassemble_float(value)
        self.assertEqual(0, sign)
        self.assertEqual(0x404, exponent)
        self.assertEqual(0x5000000000000, fraction)

    def test_no_fraction_assemble(self):
        value = build_float(0, 0x404, 0x5000000000000)
        self.assertEqual(42.0, value)

    def test_no_fraction_negative_disassemble(self):
        value = -42.0
        sign, exponent, fraction = disassemble_float(value)
        self.assertEqual(1, sign)
        self.assertEqual(0x404, exponent)
        self.assertEqual(0x5000000000000, fraction)

    def test_no_fraction_negative_assemble(self):
        value = build_float(1, 0x404, 0x5000000000000)
        self.assertEqual(-42.0, value)

    def test_fraction_disassemble(self):
        value = 0.3
        sign, exponent, fraction = disassemble_float(value)
        self.assertEqual(0, sign)
        self.assertEqual(0x3fd, exponent)
        self.assertEqual(0x3333333333333, fraction)

    def test_fraction_assemble(self):
        value = build_float(0, 0x3fd, 0x3333333333333)
        self.assertEqual(0.3, value)

    def test_fraction_negative_disassemble(self):
        value = -0.3
        sign, exponent, fraction = disassemble_float(value)
        self.assertEqual(1, sign)
        self.assertEqual(0x3fd, exponent)
        self.assertEqual(0x3333333333333, fraction)

    def test_fraction_negative_assemble(self):
        value = build_float(1, 0x3fd, 0x3333333333333)
        self.assertEqual(-0.3, value)

    def test_fraction_disassemble2(self):
        value = 12340.056789
        sign, exponent, fraction = disassemble_float(value)
        self.assertEqual(0, sign)
        self.assertEqual(0x40c, exponent)
        self.assertEqual(0x81a0744dca8e3, fraction)

    def test_fraction_assemble2(self):
        value = build_float(0, 0x40c, 0x81a0744dca8e3)
        self.assertEqual(12340.056789, value)

    def test_fraction_negative_disassemble2(self):
        value = -12340.056789
        sign, exponent, fraction = disassemble_float(value)
        self.assertEqual(1, sign)
        self.assertEqual(0x40c, exponent)
        self.assertEqual(0x81a0744dca8e3, fraction)

    def test_fraction_negative_assemble2(self):
        value = build_float(1, 0x40c, 0x81a0744dca8e3)
        self.assertEqual(-12340.056789, value)

    def test_disassemble_zero(self):
        value = 0
        sign, exponent, fraction = disassemble_float(value)
        self.assertEqual(0, sign)
        self.assertEqual(0, exponent)
        self.assertEqual(0, fraction)

    def test_assemble_zero(self):
        value = build_float(0, 0, 0)
        self.assertEqual(0, value)

    def test_disassemble_negative_zero(self):
        value = -0.0
        sign, exponent, fraction = disassemble_float(value)
        self.assertEqual(1, sign)
        self.assertEqual(0, exponent)
        self.assertEqual(0, fraction)

    def test_assemble_negative_zero(self):
        value = build_float(1, 0, 0)
        self.assertEqual(-0.0, value)

    def test_disassemble_one(self):
        value = 1
        sign, exponent, fraction = disassemble_float(value)
        self.assertEqual(0, sign)
        self.assertEqual(0x3ff, exponent)
        self.assertEqual(0, fraction)

    def test_assemble_one(self):
        value = build_float(0, 0x3ff, 0)
        self.assertEqual(1, value)

    def test_disassemble_negative_one(self):
        value = -1
        sign, exponent, fraction = disassemble_float(value)
        self.assertEqual(1, sign)
        self.assertEqual(0x3ff, exponent)
        self.assertEqual(0, fraction)

    def test_assemble_negative_one(self):
        value = build_float(1, 0x3ff, 0)
        self.assertEqual(-1, value)

    def test_nan(self):
        value = math.nan
        sign, exponent, fraction = disassemble_float(value)
        # print(hex(sign), hex(exponent), hex(fraction))
        self.assertEqual(0, sign)
        self.assertEqual(0x7ff, exponent)
        self.assertEqual(0x0008_0000_0000_0000, fraction)

    def test_assembly_nan(self):
        value = build_float(0, 0x7ff, 0x0008_0000_0000_0000)
        self.assertTrue(math.isnan(value))

    def test_negative_nan(self):
        value = -math.nan
        sign, exponent, fraction = disassemble_float(value)
        # print(hex(sign), hex(exponent), hex(fraction))
        self.assertEqual(1, sign)
        self.assertEqual(0x7ff, exponent)
        self.assertEqual(0x0008_0000_0000_0000, fraction)

    def test_assembly_negative_nan(self):
        value = build_float(1, 0x7ff, 0x0008_0000_0000_0000)
        self.assertTrue(math.isnan(value))

    def test_inf(self):
        value = math.inf
        sign, exponent, fraction = disassemble_float(value)
        # print(hex(sign), hex(exponent), hex(fraction))
        self.assertEqual(0, sign)
        self.assertEqual(0x7ff, exponent)
        self.assertEqual(0, fraction)

    def test_assembly_inf(self):
        value = build_float(0, 0x7ff, 0)
        self.assertTrue(math.isinf(value))

    def test_negative_inf(self):
        value = -math.inf
        sign, exponent, fraction = disassemble_float(value)
        # print(hex(sign), hex(exponent), hex(fraction))
        self.assertEqual(1, sign)
        self.assertEqual(0x7ff, exponent)
        self.assertEqual(0, fraction)

    def test_assembly_negative_inf(self):
        value = build_float(1, 0x7ff, 0)
        self.assertTrue(math.isinf(value))
        self.assertEqual(-math.inf, value)