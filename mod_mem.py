from converter import binary_string_to_hex, hex_to_binary, hex_to_decimal, decimal_to_binary
from collections import OrderedDict

#Memory class to read in IPL.txt. Using Dictionary to hold (address, instruction) pairs
class Memory:
    def __init__(self, size=2048):
        self.size = size
        self.words = OrderedDict()  # index is memory location
        # self.instructions = dict()
        # self.data = dict()
        self.start = 0

    def read_mem(self, fileName):
        with open(fileName, 'r') as f:
            lines = f.readlines()
            if len(lines) > self.size:
                return 'Memory file too large'  # is this right? or should I only consider the valid instructions
            for line in lines:
                if line.startswith('#'):
                    continue
                addr, val = line.split(' ')[:2]
                # convert hex to interger and store at this index, the value should be integer?
                addr = hex_to_decimal(addr)
                val = hex_to_decimal(val)
                addr += 7
                val += 7

                # if val >= 2**6: #we assumed the address space is the integer space
                #     self.instructions[addr] = val
                # else:
                #     self.data[addr] = val
                self.words[addr] = val


def hex2complement(number):
    hexadecimal_result = format(number, "03X")
    return hexadecimal_result.zfill(4) # .zfill(n) adds leading 0's if the integer has less digits than n

# for testing purposes
def main():
    m = Memory()
    m.read_mem('Program2.txt')
    with open('Program2_mod.txt' ,'a') as f:
        for addr, val in m.words.items():
            addr_h = hex2complement(addr)
            val_h = hex2complement(val)
            f.write(str(addr_h) + ' ' + str(val_h) + '\n')

    print(len(m.words))


if __name__ == '__main__':
    main()

