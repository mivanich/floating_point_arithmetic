import struct

number = 123 #7890123456789 # 01234567890


def pretty_print(str_value):
    HEX_PREFIX = "0x"
    if str_value.startswith("0b"):
        binary_len = len(str_value) - len("0b")
        last_part_len = binary_len % 4
        out_str = "0b" + str_value[len("0b"):last_part_len + len("0b")]
        if last_part_len != 0:
            out_str += "_"
        for i in range(last_part_len + len("0b"), len(str_value), 4):
            out_str += str_value[i] + str_value[i + 1] + str_value[i + 2] + str_value[i + 3]
            if i + 4 < len(str_value):
                out_str += "_"
        return out_str
    elif str_value.startswith(HEX_PREFIX):
        if str_value.startswith(HEX_PREFIX):
            binary_len = len(str_value) - len(HEX_PREFIX)
            last_part_len = binary_len % 2
            out_str = HEX_PREFIX + str_value[len(HEX_PREFIX):last_part_len + len(HEX_PREFIX)]
            if last_part_len != 0:
                out_str += "_"
            for i in range(last_part_len + len(HEX_PREFIX), len(str_value), 2):
                out_str += str_value[i] + str_value[i + 1]
                if i + 2 < len(str_value):
                    out_str += "_"
            return out_str
    return str_value


def split_float_point(float_number):
    bites = struct.pack('>f', float_number)
    int_representation = struct.unpack('>l', bites)[0]
    print(pretty_print(hex(int_representation)), " --- ", pretty_print(bin(int_representation)))

    sign = (0x80_00_00_00 & int_representation) >> 31
    exponent = (0x7f_80_00_00 & int_representation) >> 23
    fraction = int_representation & 0x00_7f_ff_ff

    print("sign", hex(sign))
    print("exponent", pretty_print(hex(exponent)))
    print("fraction", pretty_print(bin(fraction)))

    return sign, exponent, fraction


# sign, exponent, fraction = split_float_point(number)


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


def exec_fraction(fraction):
    normalized_fraction = normalize(fraction, 23)
    num_fraction = 0.0
    fraction_parts = []
    for i in range(0, len(normalized_fraction)):
        dig = normalized_fraction[i]
        if "1" == dig:
            num_fraction += 2 ** (-(i + 1))
            # end = ' + ' if i < len(normalized_fraction) else '\n'
            print("1 /", 2 ** (i + 1), end= ' + ')
            fraction_parts.append(2 ** (i + 1))

    print("\nfraction:", num_fraction)
    print(fraction_parts)
    # num_fraction = 1 / num_fraction
    num_fraction += 1
    print()
    print(num_fraction)

    return num_fraction


def calc_exponent(exponent):
    exponent_bin_str = bin(exponent)
    normalized_exponent = exponent_bin_str[2: len(exponent_bin_str)]
    num_exponent = 0
    for i in range(0, len(normalized_exponent)):
        dig = normalized_exponent[7 - i]
        if "1" == dig:
            num_exponent += 2 ** i
    num_exponent -= 127
    print("num_exponent", num_exponent)
    return num_exponent


# value = (2 ** num_exponent) * num_fraction


def get_float_point_value(sign, exponent, fraction):
    s = -1 if sign else 1
    value = s * 2 ** calc_exponent(exponent) * exec_fraction(fraction)
    return value


def sizeof(number):
    bites = struct.pack('>f', number)
    int_repr = struct.unpack('>l', bites)[0]
    num_bites = len(bin(int_repr)) - 2
    return num_bites


print("sizeof:", sizeof(number))
value = get_float_point_value(*split_float_point(number))
print(value)