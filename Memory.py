from converter import hex_to_decimal
class Memory:
    def __init__(self,size=2048):
        self.size = size
        self.words = [0 for i in range(size)] #index is memory location 
    
    def read_mem(self,file):
        with open(file, 'r') as f:
            addr, val = f.readline().split(' ')
            #convert hex to interger and store at this index, the value should be integer? 
            addr = hex_to_decimal(addr)
            val = hex_to_decimal(val)
            self.words[addr] = val

