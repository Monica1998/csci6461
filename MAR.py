from PC import ProgramCounter

#stores operand from IAR
class MAR(ProgramCounter):
    def __init__(self,addr=0):
            self.addr = addr
    
    def get_addr(self):
        return self.addr
    
    def set_addr(self,addr):
        self.addr = addr
    