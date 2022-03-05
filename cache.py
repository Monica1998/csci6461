from math import log

from Memory import Memory
from converter import binary_string_to_decimal,  decimal_to_binary

class Cache:
    def __init__(self, mem_ref,block_size=4,max_size=16): #16 lines, unclear block-size
        self.lines = [] #tuple array: [(tag, block)], block = [(addr, word)]
        self.max_size = max_size
        self.mem = mem_ref
        self.block_size = block_size

    def decode(self,addr):
        """_summary_

        Args:
            addr (int): 12-bit address space
        """
        b_str = decimal_to_binary(addr,12)
        tag = binary_string_to_decimal(b_str[:10])
        blocking_offset = binary_string_to_decimal(b_str[10:])
        return tag, blocking_offset
        
    #read
    def get_word(self,addr):
        """searches for word in cache, if not present, fetches from main memory
        copies it into cache, and returns data to caller. If the cache is full 
        We pop using FIFO and append data to the end 

        Args:
            addr (int): integer denoting memory address of word
        """
        tag, blocking_offset = self.decode(addr)
        #loop through since we don't have an idx, find matching tag
        for t, b in self.lines:
            if t == tag:
                for byte_addr, word in b:
                    if byte_addr == blocking_offset:
                        return word

        #pop if full
        if len(self.lines) == self.max_size:
            self.lines.pop(0)
        
        #get block from main memory
        block_num = addr // self.block_size
        start = block_num * self.block_size
        end = min(start + self.block_size, len(self.mem.words))
        block = [(a % self.block_size,self.mem.words[a]) for a in range(start,end)]
        self.lines.append((tag,block))
        return block[addr % self.block_size][1]

    def set_word(self,addr, new_word):
        """For writing to main memory. First we see if data is present in cache
        if it is we do a write through, else...?

        Args:
            addr (int): memory address of where instruction wants to write
            new_word (int): data to put into that memory address
        """

        #loop through cache to find the matching block (via tag),
        #  then loop to find correct word??  

        tag, offset = self.decode(addr)
        for i, (t, b) in enumerate(self.lines):
            if t == tag:
                for j, (a,word) in enumerate(b): #do we have to loop through this? can this be a dictionary?
                    if a == offset:
                        block  = self.lines[i][1]
                        block[j] = (a,new_word)
                        #write to main mem
                        self.mem.words[addr] = new_word
                        return

        #Write no-allocate
        self.mem.words[addr] = new_word
    
    def clear_cache(self):
        self.lines = []



def main():
   mem = Memory()
   mem.read_mem('IPL.txt')
   print(mem.words[16])
#    c = Cache(mem)

#    #get word test
#    c.get_word(19)

if __name__ == '__main__':
    main()