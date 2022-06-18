import struct
import math
from utils import pretty

# the format of the double precision floating point described at
# https://en.wikipedia.org/wiki/Double-precision_floating-point_format

FLOAT64_SIGN_PRECISION = 1
FLOAT64_EXPONENT_PRECISION = 11
FLOAT64_FRACTION_PRECISION = 52
EXPONENT_BIAS = 1023


def float_to_bin(value):
    """
    :param value float value to be transformed to integer with the same binary representation
    :returns integer representation of the passed value with the same binary representation
    """
    return struct.unpack(">Q", struct.pack(">d", value))[0]


def disassemble_float(float_number):
    int_representation = float_to_bin(float_number)

    sign = int_representation >> 63
    exponent = int_representation >> FLOAT64_FRACTION_PRECISION & 0x07FF
    fraction = int_representation & 0x00_0f_ff_ff_ff_ff_ff_ff

    return sign, exponent, fraction


def exec_fraction(fraction, exponent):
    if 0 == exponent:
        return 0, 0
    if 0 == fraction:
        return 1, 0

    numerators = []
    initial_value = 1 << FLOAT64_FRACTION_PRECISION - 1
    for i in range(0, FLOAT64_FRACTION_PRECISION):
        dig = fraction & (initial_value >> i)
        if dig:
            numerators.append(2 << i)
    # the last numerator is the biggest one, so it must be a common multiple for all previous values
    common_multiple = numerators[-1]
    updated_numerators = [common_multiple / x for x in numerators]
    # adding of the common_multiple here is for
    # sum + 1, as 1 is presented as (common_multiple/common_multiple) - numerator is added to sum_all_numerators,
    # whereas denominator is used to evaluate the denominator of the fraction
    sum_all_numerators = sum(updated_numerators) + common_multiple
    denominator = math.log2(common_multiple)

    return sum_all_numerators, denominator


def calc_exponent(exponent):
    if 0 == exponent:
        return 0
    num_exponent = 0
    for i in range(0, int(math.log2(exponent)) + 1):
        dig = exponent & (1 << i)
        if dig:
            num_exponent += 1 << i
    num_exponent -= EXPONENT_BIAS
    return num_exponent


def build_float_as_int(sign, exponent, fraction):
    return (sign << 63) | (exponent << FLOAT64_FRACTION_PRECISION) | fraction


def bits_to_float(int_value):
    return struct.unpack('!d', struct.pack('!Q', int_value))[0]


def is_finite(exponent, fraction):
    is_nan = exponent == 0x7ff and fraction == 0x0008_0000_0000_0000
    is_inf = exponent == 0x7ff and fraction == 0
    return not (is_inf or is_nan)


def build_float(sign, exponent, fraction):
    if not is_finite(exponent, fraction):
        # can't get nan via multiplication.
        # inf is possible when fraction != 0, actually
        return bits_to_float(build_float_as_int(sign, exponent, fraction))

    s = -1 if sign else 1

    fraction_numerator, fraction_denominator = exec_fraction(fraction, exponent)

    exp = calc_exponent(exponent)
    finish_shift = exp - fraction_denominator
    return s * 2.0 ** finish_shift * fraction_numerator


if __name__ == "__main__":
    number = 12.00000
    sign, exponent, fraction = disassemble_float(number)
    value = build_float(sign, exponent, fraction)
    print(value)
