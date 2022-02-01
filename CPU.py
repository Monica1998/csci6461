import PC
import GR
import IndexRegister
import MAR
import MBR
import IR
import IAR
import Memory

#TODO: enforce memory constraints on all registers, PC, etc
#TODO: Fill in decoder()
#TODO: fetch contents in memory using operand data, and mode(direct, indirect)
#implement functions to write instructions to memory, unclear what the address should be

class CPU:

    def __init__(self,memsize=2048):
        self.PC = PC(0)
        self.GR = [GR() for i in range(3)]
        self.IndexRegister = IndexRegister(0)
        self.MAR = MAR()
        self.MBR = MBR()
        self.IR = IR()
        self.IAR = IAR()
        self.Memory = Memory(memsize)
    
    #generator for each cycle 
    def cycle(self):
        self.MAR.set_addr(self.PC.get_addr())
        self.PC.increment_addr() #points to next instruction 
        yield 
        addr = self.MAR.get_addr()
        self.MBR.set_word(self.Memory.words[addr])
        yield 
        self.IR.set_instruction(self.MBR.get_word())
        yield 
        opcode, operand, index_register, mode, general_register = self.IR.decode()
        yield 
        self.IAR.set_addr(operand)
        yield 
        self.MAR.set_addr(self.IAR.get_addr())
        yield 
        word = self.Memory.words[self.MAR.get_addr()]
        self.MBR.set_word(word) #is this an instruction? 
        yield 
        #Execution phase...


#Upon start up...instantiate all the components to be empty, allowing for user to set everything

#after setting everything... 
# optional read IPL.tx (to show all LD and ST addressing modes)
 # single step walk through or run 
# 
