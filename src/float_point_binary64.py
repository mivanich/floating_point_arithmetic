import struct
import math
from utils import pretty

FLOAT64_SIGN_PRECISION = 1
FLOAT64_EXPONENT_PRECISION = 11
FLOAT64_FRACTION_PRECISION = 52


def float_to_bin(value):
    return struct.unpack(">Q", struct.pack(">d", value))[0]


def split_float_point(float_number):
    int_representation = float_to_bin(float_number)

    sign = (0x80_00_00_00_00_00_00_00 & int_representation) >> 63
    exponent = (0x7f_f0_00_00_00_00_00_00 & int_representation) >> 52
    fraction = int_representation & 0x0f_ff_ff_ff_ff_ff_ff

    print("sign\t\t", pretty(bin(sign)))
    print("exponent\t", pretty(bin(exponent), FLOAT64_EXPONENT_PRECISION))
    print("fraction\t", pretty(bin(fraction), FLOAT64_FRACTION_PRECISION))

    return sign, exponent, fraction


def to_binary_str(int_value, num_bits):
    BIN_PREFIX = "0b"
    str_value = bin(int_value)
    if not str_value.startswith(BIN_PREFIX):
        raise Exception("The string", str_value, "has wrong format: it doesn't start from 0b")

    prefix_len = len(BIN_PREFIX)
    normalized = str_value[prefix_len:len(str_value)]
    if len(normalized) < num_bits:
        short = num_bits - len(normalized)
        normalized = ("0" * short) + normalized
    return normalized


def exec_fraction(fraction):
    binary_str = to_binary_str(fraction, FLOAT64_FRACTION_PRECISION)
    fraction_parts = []
    for i in range(0, len(binary_str)):
        dig = binary_str[i]
        if "1" == dig:
            fraction_parts.append(2 ** (i + 1))
    max = fraction_parts[-1]
    updated_fractions = [max / x for x in fraction_parts]
    sum_all_elems = sum(updated_fractions) + max
    shift = math.log2(max)

    return sum_all_elems, shift


def calc_exponent(exponent):
    binary_str = to_binary_str(exponent, FLOAT64_EXPONENT_PRECISION)
    num_exponent = 0
    for i in range(0, len(binary_str)):
        dig = binary_str[FLOAT64_EXPONENT_PRECISION - i - 1]
        if "1" == dig:
            num_exponent += 2 ** i
    num_exponent -= 1023
    return num_exponent


def build_float(sign, exponent, fraction):
    s = -1 if sign else 1
    fraction_numerator, fraction_denominator = exec_fraction(fraction)

    exp = calc_exponent(exponent)
    finish_shift = exp - fraction_denominator
    return s * 2 ** finish_shift * fraction_numerator


if __name__ == "__main__":
    number = 12.00000
    sign, exponent, fraction = split_float_point(number)
    value = build_float(sign, exponent, fraction)
    print(value)
