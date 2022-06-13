def pretty(str_value, num_digits=-1):
    if not type(str_value) is str:
        raise Exception("str_value in the method pretty must be of type 'str'")
    HEX_PREFIX = "0x"
    if str_value.startswith("0b"):
        pure_bits = str_value[len("0b"): len(str_value)]
        binary_len = len(str_value) - len("0b")
        last_part_len = binary_len % 4
        out_str = pure_bits[0:last_part_len]
        if num_digits != -1 and len(pure_bits) < num_digits:
            out_str = "0" * (num_digits - len(pure_bits)) + out_str
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
