#Program Counter Class to get/set address as well as increment to the next instruction 
class ProgramCounter:
    def __init__(self,addr=0):
        self.addr = addr
    
    def get_addr(self):
        return self.addr
    
    def set_addr(self,addr):
        self.addr = addr
    
    def increment_addr(self):
        self.addr += 1