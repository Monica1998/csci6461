from converter import hex_to_decimal
class Memory:
    def __init__(self,size=2048):
        self.size = size
        self.words = [0 for i in range(size)] #index is memory location 
    
    def read_mem(self,file):
        with open('IPL.txt', 'r') as f:
            lines = f.readlines()
            for line in lines:
                addr, val = line.split(' ')[:2]
            #convert hex to interger and store at this index, the value should be integer? 
                addr = hex_to_decimal(addr)
                val = hex_to_decimal(val)
                print('writing val = {} to addr = {}'.format(val,addr))
                self.words[addr] = val
    


#for testing purposes
def main():
    mem = Memory()
    mem.read_mem('IPL.txt')
    print(mem.words)
    
if __name__ == '__main__':
    main()

