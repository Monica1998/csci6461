# from math import abs

def hex_to_decimal(hex):
    # do we need to hard code this?
    return int(hex, 16)


def decimal_to_binary(dec, bit=16):
    if bit == 16:
        return '{0:016b}'.format(dec)
    elif bit == 12:
        return '{0:012b}'.format(dec)
    elif bit == 4:
        return '{0:004b}'.format(dec)
    elif bit == 2:
        return '{0:002b}'.format(dec)
    elif bit == 7:
        return '{0:007b}'.format(dec)
    elif bit == 15:
        return '{0:0015b}'.format(dec)

def format_float(result):
    whole, dec = result.split('.')
    if len(whole) == 0:
        #get distance from first 1 bit in dec
        f_idx = dec.find('1')
        #p_idx = result.find('.')
        exp = f_idx + 1
        #get exp-binary represetnation
        exp = decimal_to_binary(exp, 7)
        exp = twos_comp_binary(exp)
        man = dec[f_idx+1:] + '0'* (8 -len(dec[f_idx+1:]))
        
    if len(whole) > 0:
        #get distance from first 1 bit in whole
        exp = len(whole) -1
        #get exp-binary rep
        exp = decimal_to_binary(exp,7)
        #extract mantissa
        man = whole[1:] + dec
        #man = man + '0' * (8 -len(whole[1:]))
    return exp, man

def twos_comp_binary(exp):
    inverse_exp = ''
    for bit in exp:
        if bit == '1':
            inverse_exp += '0'
        if bit == '0':
            inverse_exp += '1'
    temp = int(inverse_exp, 2) + 1
    return decimal_to_binary(temp, len(exp))

def twos_comp(val, bits):
    """compute the 2's complement of int value val"""
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val   


def floating_to_binary(fp):
    sb = '0' if fp >= 0 else '1'
    fp = abs(fp)
    whole = int(fp)
    result = bin(whole).lstrip("0b") + '.' 
    dec = fp - whole
    places = 8 - (len(result) - 2) #remaining places left in mantissa for floating value
    for i in range(places):
        dec *= 2
        if dec >= 1:
            result += str(int(dec))
            dec = dec % int(dec)
        else:
            result += '0'
        # exp = decimal_to_binary(len(man), bit=7) #make sure this is signed
    print(result)
    exp, man = format_float(result)
    return sb + exp + man

def binary_to_floating(b):
    s, exp, man = b[0], b[1:8], b[8:]
    exp = twos_comp(int(exp, 2), 7)
    man = int(man, 2) + (1 << 8)
    res = float(man) / (2**(8-exp))
    if s == '1':
        return -res
    return res
    

def floating_to_fixed(f, e=7):
    res = abs(f) * (2**e)
    res = int(round(res))
    if f < 0:
        res = -1 * res
    return res 

def fixed_to_binary(fi, wlen=15,e=7):
    sb = '1' if fi < 0 else '0'
    fi = abs(fi)
    fi = fi 
    return sb + decimal_to_binary(fi, wlen)

def binary_to_fixed(b):
    res = binary_string_to_decimal(b[1:])
    if b[0] == '1':
        return -1 * res
    return res

def fixed_to_floating(fi, e=7):

    return float(fi) / (2**e)

def hex_to_binary(hex):
    temp = hex_to_decimal(hex)
    return decimal_to_binary(temp)


def binary_string_to_decimal(bin_string):
    return int(bin_string, 2)


def binary_string_to_hex(bin_string):
    return hex(int(bin_string, 2))

if __name__ == '__main__':
    # temp = 5.42101086e-20
    # if 1 > temp:
    #     print('greater than')
    # print(temp)
#     temp = floating_to_binary(0.514)
#     print(temp)
#   #  print(len(temp))
#     print(binary_to_floating(temp))
    temp = fixed_to_binary(1216)
    print(binary_string_to_hex(temp))
    #print(binary_string_to_hex(temp))
    