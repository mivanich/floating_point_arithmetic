import utils
import math


def split_float_point(float_number):
    int_representation = utils.get_bits32(float_number)

    sign = (0x80_00_00_00 & int_representation) >> 31
    exponent = (0x7f_80_00_00 & int_representation) >> 23
    fraction = int_representation & 0x00_7f_ff_ff

    # print("sign\t\t", utils.pretty(bin(sign)))
    # print("exponent\t", utils.pretty(bin(exponent), 8))
    # print("fraction\t", utils.pretty(bin(fraction), 23))

    return sign, exponent, fraction


def normalize(int_value, num_bits):
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


def exec_fraction2(fraction):
    normalized_fraction = normalize(fraction, 23)
    fraction_parts = []
    for i in range(0, len(normalized_fraction)):
        dig = normalized_fraction[i]
        if "1" == dig:
            fraction_parts.append(2 ** (i + 1))
    # print(fraction_parts)

    max = fraction_parts[-1]
    updated_fractions = [max / x for x in fraction_parts]
    sum_all_elems = sum(updated_fractions) + max
    shift = math.log2(max)
    # print("sum", sum_all_elems, shift)

    return sum_all_elems, shift


def exec_fraction(fraction):
    normalized_fraction = normalize(fraction, 23)
    num_fraction = 0.0
    fraction_parts = []
    for i in range(0, len(normalized_fraction)):
        dig = normalized_fraction[i]
        if "1" == dig:
            num_fraction += 2 ** (-(i + 1))
            # print("1 /", 2 ** (i + 1), end= ' + ')
            fraction_parts.append(2 ** (i + 1))

    # print("\nfraction:", num_fraction)
    # print(fraction_parts)

    num_fraction += 1
    return num_fraction


def calc_exponent(exponent):
    normalized_exponent = normalize(exponent, 8)
    num_exponent = 0
    for i in range(0, len(normalized_exponent)):
        dig = normalized_exponent[7 - i]
        if "1" == dig:
            num_exponent += 2 ** i
    num_exponent -= 127
    return num_exponent


def compile_float(sign, exponent, fraction):
    s = -1 if sign else 1
    whole_fraction, shift = exec_fraction2(fraction)
    exp = calc_exponent(exponent)
    finish_shift = exp - shift
    value = s * 2 ** finish_shift * whole_fraction
    return value


if __name__ == "__main__":
    original = 123.0
    s, exp, m = split_float_point(original)
    compiled = compile_float(s, exp, m)
    print("combiled value is", compiled, "| original == compiled:", original == compiled)
