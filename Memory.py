from converter import hex_to_decimal

#Memory class to read in IPL.txt. Using Dictionary to hold (address, instruction) pairs
class Memory:
    def __init__(self, size=2048):
        self.size = size
        self.words = dict.fromkeys((range(self.size)), 0)  # index is memory location
        # self.instructions = dict()
        # self.data = dict()
        self.start = 0

    def read_mem(self, fileName='./IPL.txt'):
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
                # if val >= 2**6: #we assumed the address space is the integer space
                #     self.instructions[addr] = val
                # else:
                #     self.data[addr] = val
                self.words[addr] = val


# for testing purposes
def main():
    print('{0:016b}'.format(6))


if __name__ == '__main__':
    main()


