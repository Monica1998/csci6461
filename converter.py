def hex_to_decimal(hex):
    # do we need to hard code this?
    return int(hex, 16)


def decimal_to_binary(dec, bit=16):
    if bit == 16:
        return '{0:016b}'.format(dec)
    elif bit == 12:
        return '{0:012b}'.format(dec)
    elif bit == 5:
        return '{0:005b}'.format(dec)
    elif bit == 4:
        return '{0:004b}'.format(dec)
    elif bit == 2:
        return '{0:002b}'.format(dec)


def hex_to_binary(hex):
    temp = hex_to_decimal(hex)
    return decimal_to_binary(temp)


def binary_string_to_decimal(bin_string):
    return int(bin_string, 2)


def binary_string_to_hex(bin_string):
    return hex(int(bin_string, 2))