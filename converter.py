def hex_to_decimal(hex):
    #do we need to hard code this? 
    return int(hex,16)

def decimal_to_binary(dec):
    return '{0:016b}'.format(dec)

def hex_to_binary(hex):
    temp = hex_to_decimal(hex)
    return decimal_to_binary(temp)