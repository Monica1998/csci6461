from ast import Str
from bdb import effective
from math import ldexp
from PC import ProgramCounter as PC
from GR import GeneralRegister as GR
from IndexRegister import IndexRegister
from MAR import MAR 
from MBR import MBR
from IR import IR
from Memory import Memory


#TODO: enforce memory constraints on all registers, PC, etc
#implement behavior when using idx register and GR to load/store

class CPU:

    def __init__(self,memsize=2048):
        self.PC = PC(0) #starting addr from IPL.txt
        self.GRs = [GR() for i in range(4)]
        self.IndexRegisters = [IndexRegister(0) for i in range(3)]
        self.MAR = MAR()
        self.MBR = MBR()
        self.IR = IR()
        self.Memory = Memory(memsize)
    
    #TODO: modify to factor in index_register != 0

    def LDR(self,operand, mode, general_register):
        val = None
        if mode == 0:
            self.MAR.set_addr(operand)

        if mode == 1:
            addr = self.Memory.words[operand]
            self.MAR.set_addr(addr)

        self.MBR.set_val(self.Memory.words[self.MAR.get_val()])
        self.GRs[general_register].set_val(self.MBR.get_val())
    
    def STR(self, operand, mode, general_register):
        if mode == 0:
            self.MAR.set_addr(operand)
        if mode == 1:
            addr = self.Memory.words[operand]
            self.MAR.set_addr(addr)

        self.MBR.set_val(self.GRs[general_register].get_val())
        self.Memory[self.MAR.get_addr()] = self.MBR.get_val()
    
    def LDA(self,operand, mode, general_register):
        if mode == 0:
            self.MAR.set_val(operand)

        if mode == 1:
            addr = self.Memory.words[operand]
            self.MAR.set_addr(addr)

        self.MBR.set_val(self.Memory.words[self.MAR.get_val()])
        self.GRs[general_register].set_val(self.MBR.get_val())

    def LDX(self, operand, mode, index_register):
        val = None
        if mode == 0:
            self.MAR.set_addr(index_register)
          
        if mode == 1:
            addr = self.Memory.words[operand]
            self.MAR.set_addr(addr)
           
        self.MBR.set_val(self.Memory.words[self.MAR.get_addr()])
        self.IndexRegisters[index_register].set_val(val)

    def STX(self,operand, mode, index_register):
        if mode == 0:
            self.MAR.set_addr(operand)
        if mode == 1:
            addr = self.Memory[operand]
            self.MAR.set_addr(addr)
        self.MBR.set_val(self.IndexRegisters[index_register].get_val())
        self.Memory[self.MAR.get_addr()] = self.MBR.get_val()
    
    def HALT(self):
        return -1
    
    #TODO: generator for each cycle 
    def step(self):
        self.MAR.set_addr(self.PC.get_addr())
        self.PC.increment_addr() #points to next instruction 
        
        addr = self.MAR.get_addr()
        self.MBR.set_val(self.Memory.words[addr])
       
        self.IR.set_instruction(self.MBR.get_val())
      
        opcode, operand, index_register, mode, general_register = self.IR.decode()
        if opcode == 1:
            self.LDR(operand, mode, general_register)
        elif opcode == 2:
            self.STR(operand, mode, general_register)
        elif opcode == 3: 
            self.LDA(operand, mode, general_register)
        elif opcode == 33:
            self.LDX(operand, mode, index_register)
        elif opcode == 34:
            self.STX(operand, mode, index_register)
        elif opcode == 0:
            return -1
        return 0

def main():
    cpu = CPU(2048)
    cpu.Memory.read_mem()
    cpu.step()

if __name__ == '__main__':
    main()