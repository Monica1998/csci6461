from bdb import effective
import sys
sys.path.append('/Users/vishesh.javangula@ibm.com/Documents/Computer_Architecture/proj_1_4641')

from Device import Device
from PC import ProgramCounter as PC
#from converter import decimal_to_binary, binary_string_to_decimal
from registers import MAR, MBR, MFR, CC, IR, IndexRegister, FR, GeneralRegister as GR
from Memory import Memory
from cache import Cache
from converter import *

MAX_VALUE = 65536
MIN_VALUE = 0
OVERFLOW = 0
UNDERFLOW = 1
MAX_WHOLE_FP = int('111111111' + (55 * '0'),2)
MIN_WHOLE_FP = -1 * MAX_WHOLE_FP
MAX_DEC_FP = 5.42101086e-20
MIN_DEC_FP = -1 * MAX_DEC_FP

class CPU:

    # initializes all components, 4 General Registers, 3 Index Registers
    def __init__(self, memsize=2048):
        self.PC = PC(7)  # starting addr from IPL.txt
        self.GRs = [GR() for i in range(4)]
        self.IndexRegisters = [IndexRegister(0) for i in range(3)]
        self.FRs = [FR(0) for i in range(2)]
        self.MAR = MAR()
        self.MBR = MBR()
        self.MFR = MFR()
        self.CC = CC()
        self.IR = IR()
        self.memsize = memsize
        print('creating memory instance')
        self.Memory = Memory(memsize)
        self.Cache = Cache(self.Memory)
        self.Device = Device()
        self.exe_ins = (6, 7, 13, 16, 17, 18, 19, 20, 21, 25, 26, 49, 50, 24, 0)


    def fetch(self, IF_ID, code):
        """Gets PC and pushes it to IF_ID buffer, then increments the PC

        Args:
            IF_ID (Queue): Buffer using Queue data structure to hold instructions fetched from memory
            code (int): shared integer to denote when to stop execution
        """
        while code.value != -1:
            if IF_ID.empty():
                self.MAR.set_val(self.PC.get_addr())
                # cpu.PC.increment_addr()  # points to next instruction
                addr = self.MAR.get_val()
                self.MBR.set_val(self.Memory.words[addr])
                self.IR.set_instruction(self.MBR.get_val()) #end of stage 1
                IF_ID.put(self.IR.get_instruction())
                self.PC.increment_addr()

    def decode(self, IF_ID, ID_EXE, code):
        """Decodes instruction and determines whether to halt. Sends opcode, operand, index registers, mode, general registers
        to ID_EXE buffer

        Args:
            IF_ID (Queue): Buffer that stores the instruction
            ID_EXE (Queue): Buffer to hold decoded instruction
            code (int): shared integer to denote when to stop execution
        """
        while code.value != -1:
            if IF_ID.empty == False and ID_EXE.empty == True:
                IF_ID.get() #its already in the IR
                opcode, operand, index_register, mode, general_register = self.IR.decode() #stage 2
                if opcode == 0:
                    code.value = -1 #halt all processes
                ID_EXE.put((opcode, operand, index_register, mode, general_register))

    def execute(self, ID_EXE, EXE_MEM, code):
        """Pops decoded instruction from ID_EXE buffer, executes instructions that do not require main memory access.
        For those that need main memory access, the effective address is computed. 
        result or effective address along with decoded instruciton is then pushed to EXE_MEM
        
        Args:
            ID_EXE (Queue): holds decoded instruction 
            EXE_MEM (Queue): holds decoded instruction along with result or effective address
            code (int): shared integer to denote when to stop execution
        """
        while code.value != -1:
            if ID_EXE.empty() == False and EXE_MEM.empty() == True:
                opcode, operand, index_register, mode, general_register = ID_EXE.get()
                if opcode in self.exe_ins:
                    res = self.single_step(opcode, operand, index_register, mode, general_register) #will do write-back for these instructions
                    EXE_MEM.put((opcode, operand, index_register, mode, general_register, res))

                else:
                    effective_addr = self.get_effective_addr(opcode, operand, index_register, mode)
                    EXE_MEM.put((opcode, operand, index_register, mode, general_register, effective_addr))

    #TODO: there will likely be conflicts with accessing the MBR, look into locking
    def mem(self, EXE_MEM, MEM_WB, code):
        """Pops decoded instruciton and res/effective address from EXE_MEM. 
        For those instrucitons that need access to main memory, execution is performed here. 
        The result, if not none,  from these instructions are pushed to MEM_WB. 
        For those instructions that already executed, pushes res to MEM_WB buffer. 

        Args:
            EXE_MEM (Queue): holds decoded instruction along with result or effective address
            MEM_WB (Queue): holds result, which is a dictionary of register, register index, and value  
            code (int): shared integer to denote when to stop execution
        """
        while code.value != -1:
            if EXE_MEM.empty() == False and MEM_WB.empty() == True:
                opcode, operand, index_register, mode, general_register, data = EXE_MEM.get()
                if opcode not in self.exe_ins:
                    res = self.single_step(opcode, operand, index_register, mode, general_register, data)
                    if res:
                        MEM_WB.put(res)
                else: #if res is not None
                    MEM_WB.put(data)

    #only for writing to GR, IX, FPR from memory
    def wb(self, MEM_WB, code):
        """Pops res dictionary from MEM_WB and writes the result to the corresponding register

        Args:
            MEM_WB (Queue): holds result, which is a dictionary of register, register index, and value 
            code (int): shared integer to denote when to stop execution
        """
        while code.value != -1:
            if MEM_WB.empty() == False:
                res = MEM_WB.get()
                if res['Register'] == 'General':
                    self.GRs[res['index']].set_val(res['value'])
                if res['Register'] == 'Index':
                    self.IndexRegisters[res['index']].set_val(res['value'])
                if res['Register'] == 'Floating':
                    self.FRs[res['index']].set_val(res['result'])


    # resets all registers and program counter to default values when hitting HALT instruction
    def reset(self):
        self.PC = PC(7)  # starting addr from IPL.txt
        self.GRs = [GR() for i in range(4)]
        self.IndexRegisters = [IndexRegister(0) for i in range(3)]
        self.MAR = MAR()
        self.MBR = MBR()
        self.MFR = MFR()
        self.CC = CC()
        self.IR = IR()
        self.Device = Device()
        self.Memory.words = dict.fromkeys((range(self.memsize)), 0)
        self.Cache.clear_cache()

    # Load data to general register from effective address
    def LDR(self, operand, index_register, general_register, effective_addr):
        if effective_addr == -1:
            return
        self.MAR.set_val(effective_addr)
        self.MBR.set_val(self.Cache.get_word(self.MAR.get_val()))
        #return self.MBR.get_val()
        return {'Register': 'General', 'index': general_register, 'value': self.MBR.get_val()}

        # self.GRs[general_register].set_val(self.MBR.get_val())
        # self.PC.increment_addr()

    # store data from general register to memory
    def STR(self, operand, index_register, mode, general_register, effective_addr):
        if effective_addr == -1:
            return
        self.MBR.set_val(self.GRs[general_register].get_val())
        self.Memory.words[effective_addr] = self.MBR.get_val()
        self.Cache.set_word(effective_addr, self.MBR.get_val())
        #self.PC.increment_addr()
        return
     

    # load effective address into general register
    def LDA(self, operand, index_register, mode, general_register, effective_addr):
        if effective_addr == -1:
            return
        #return effective_addr
        return {'Register': 'General', 'index': general_register, 'value': effective_addr}
        #self.GRs[general_register].set_val(effective_addr)
        #self.PC.increment_addr()

    # load data into index register
    def LDX(self, operand, index_register, mode, general_register, effective_addr):
        if effective_addr == -1:
            return
        #self.MBR.set_val(self.Memory.words[effective_addr])
        self.MBR.set_val(self.Cache.get_word(effective_addr))
        #return self.MBR.get_val()
        return {'Register': 'Index', 'index': index_register-1, 'value': self.MBR.get_val()}
        #self.IndexRegisters[index_register - 1].set_val(self.MBR.get_val())
       # self.PC.increment_addr()

    def LDX_mod(self, operand, index_register, mode, general_register, effective_addr):
        if effective_addr == -1:
            return
        #self.MBR.set_val(self.Memory.words[effective_addr])
        self.MBR.set_val(self.Cache.get_word(effective_addr))
        #return self.MBR.get_val()
        return {'Register': 'Index', 'index': general_register-1, 'value': self.MBR.get_val()}

        # self.IndexRegisters[general_register - 1].set_val(self.MBR.get_val())
        # self.PC.increment_addr()

    def LDFR(self, operand, index_register, mode, floating_register, effective_addr):
        #effective_addr = self.get_effective_addr(operand, 0, 0)


        if effective_addr == -1:
            return
        self.MAR.set_val(effective_addr)
        self.MBR.set_val(self.Cache.get_word(self.MAR.get_val()))
        res1 = self.MBR.get_val()
        res1 = decimal_to_binary(res1)
        res1 = binary_to_floating(res1)

        self.MAR.set_val(effective_addr+1)
        self.MBR.set_val(self.Cache.get_word(self.MAR.get_val()))
        res2 = self.MBR.get_val()
        res2 = decimal_to_binary(res2)
        res2 = binary_to_floating(res2)

        #return self.MBR.get_val()
        return {'Register': 'Floating', 'index': [0,1], 'value': [res1, res2]}

        #self.FRs[floating_register].set_val(self.MBR.get_val())
       # self.PC.increment_addr()

    def STFR(self, operand, index_register, mode, floating_register, effective_addr):
        # effective_addr = self.get_effective_addr(operand, 0, 0)

    

        if effective_addr == -1:
            return

        res = self.FRs[0].get_val()
        res = floating_to_binary(res)
        res = binary_string_to_decimal(res)
        self.MBR.set_val(res)
        self.Cache.set_word(effective_addr, self.MBR.get_val())

        res = self.FRs[1].get_val()
        res = floating_to_binary(res)
        res = binary_string_to_decimal(res)
        self.MBR.set_val(res)
        self.Cache.set_word(effective_addr+1, self.MBR.get_val())

    # store data from index register into memory
    def STX(self, operand, index_register, mode, general_register, effective_addr):
        #effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        self.MAR.set_val(effective_addr)
        self.MBR.set_val(self.IndexRegisters[index_register - 1].get_val())
        #self.Memory.words[self.MAR.get_val()] = self.MBR.get_val()
        self.Cache.set_word(self.MAR.get_val(), self.MBR.get_val())
        #self.PC.increment_addr()

    # Jump if Equal
    def JZ(self, operand, index_register, mode, general_register, effective_addr):
        #effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        self.MAR.set_val(effective_addr)
        if self.GRs[general_register].get_val() == 0:
            self.PC.set_addr(effective_addr)
        # else:
        #     self.PC.increment_addr()

    # Jump If Not Equal
    def JNE(self, operand, index_register, mode, general_register, effective_addr):
        #effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        self.MAR.set_val(effective_addr)
        if self.GRs[general_register].get_val() != 0:
            self.PC.set_addr(effective_addr)
        # else:
        #     self.PC.increment_addr()

    # Jump If Condition Code
    def JCC(self, operand, index_register, mode, cc, effective_addr):
        #effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        self.MAR.set_val(effective_addr)
        bits = decimal_to_binary(self.CC.get_val(), bit=4)
        if bits[cc] == '1':
            self.PC.set_addr(effective_addr)
        # else:
        #     self.PC.increment_addr()

    # Unconditional Jump To Address
    def JMA(self, operand, index_register, mode, general_register, effective_addr):
        #effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        print(effective_addr )
        self.MAR.set_val(effective_addr)
        self.PC.set_addr(effective_addr)

    # Jump and Save Return Address
    def JSR(self, operand, index_register, mode, general_register, effective_addr):
        #effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        self.MAR.set_val(effective_addr)
        result = self.PC.get_addr() + 1
        #self.GRs[3].set_val(result)
        self.PC.set_addr(effective_addr)
        return {'Register': 'General', 'index': 3, 'value': result}
        # R0 should contain pointer to arguments. Argument list should end with -1 (all 1s) value

    # Return From Subroutine w/ return code as Immed portion (optional) stored in the instruction's address Field
    def RFS(self, operand, index_register, mode, general_register):
        #self.GRs[0].set_val(operand)
        temp = self.GRs[3].get_val()
        self.PC.set_addr(temp)
        return {'Register': 'General', 'index': 0, 'value': operand}
        # IX, I fields are ignored

    # Subtract One and Branch
    def SOB(self, operand, index_register, mode, general_register, effective_addr):
       # effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        self.MAR.set_val(effective_addr)
        result = self.GRs[general_register].get_val() - 1
        #self.GRs[general_register].set_val(result)
        if result > 0:
            self.PC.set_addr(effective_addr)
        # else:
        #     self.PC.increment_addr()
        return {'Register': 'General', 'index': general_register, 'value': result}
    # Jump Greater than or equal to
    def JGE(self, operand, index_register, mode, general_register, effective_addr):
        #effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        self.MAR.set_val(effective_addr)
        if self.GRs[general_register].get_val() >= 0:
            self.PC.set_addr(effective_addr)
        # else:
        #     self.PC.increment_addr()

    # Add memory to register.
    def AMR(self, operand, index_register, mode, general_register, effective_addr):
        # immed = operand
        self.CC.set_val(0)
        #effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        self.MAR.set_val(effective_addr)

        # TODO: fetch from cache(self.MAR.get_val())
        #self.MBR.set_val(self.Memory.words[self.MAR.get_val()])
        self.MBR.set_val(self.Cache.get_word(self.MAR.get_val()))

        result = self.GRs[general_register].get_val() + self.MBR.get_val()
        # Check overflow.
        if self.check_cc(result) == OVERFLOW:
            bits = decimal_to_binary(self.CC.get_val(), bit=4)
            bits = '1' + bits[1:]
            self.CC.set_val(binary_string_to_decimal(bits))
        elif self.check_cc(result) == UNDERFLOW:
            bits = decimal_to_binary(self.CC.get_val(), bit=4)
            bits = bits[:1] + '1' + bits[2:]
            self.CC.set_val(binary_string_to_decimal(bits))
        else:
            return {'Register': 'General', 'index': general_register, 'value': result}
            #self.GRs[general_register].set_val(result)
           # {'Register': 'General', 'index': general_register, 'value': result}
       # self.PC.increment_addr()

    # Subtract memory from register.
    def SMR(self, operand, index_register, mode, general_register, effective_addr):
        self.CC.set_val(0)
       # effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        self.MAR.set_val(effective_addr)

        # TODO: fetch from cache(self.MAR.get_val())
        #self.MBR.set_val(self.Memory.words[self.MAR.get_val()])
        self.MBR.set_val(self.Cache.get_word(self.MAR.get_val()))

        result = self.GRs[general_register].get_val() - self.MBR.get_val()
        # Check overflow/underflow.
        if self.check_cc(result) == OVERFLOW:
            bits = decimal_to_binary(self.CC.get_val(), bit=4)
            bits = '1' + bits[1:]
            self.CC.set_val(binary_string_to_decimal(bits))
        elif self.check_cc(result) == UNDERFLOW:
            bits = decimal_to_binary(self.CC.get_val(), bit=4)
            bits = bits[:1] + '1' + bits[2:]
            self.CC.set_val(binary_string_to_decimal(bits))
        else:
            return {'Register': 'General', 'index': general_register, 'value': result}
            #self.GRs[general_register].set_val(result)
           # {'Register': 'General', 'index': general_register, 'value': result}
       # self.PC.increment_addr()

    # Add immediate to register.
    def AIR(self, operand, index_register, mode, general_register, effective_addr):
        # immed = operand
        self.CC.set_val(0)
        if operand == 0:
            self.PC.increment_addr()
            return
        if self.GRs[general_register].get_val() == 0:
            self.GRs[general_register].set_val(operand)
        else:
            result = self.GRs[general_register].get_val() + operand
            # Check overflow/underflow.
            if self.check_cc(result) == OVERFLOW:
                bits = decimal_to_binary(self.CC.get_val(), bit=4)
                bits = '1' + bits[1:]
                self.CC.set_val(binary_string_to_decimal(bits))
            elif self.check_cc(result) == UNDERFLOW:
                bits = decimal_to_binary(self.CC.get_val(), bit=4)
                bits = bits[:1] + '1' + bits[2:]
                self.CC.set_val(binary_string_to_decimal(bits))
            else:
                return {'Register': 'General', 'index': general_register, 'value': result}
               # self.GRs[general_register].set_val(result)
        #self.PC.increment_addr()

    # Subtract immediate from register.
    def SIR(self, operand, index_register, mode, general_register, effective_addr):
        # immed = operand
        self.CC.set_val(0)
        if operand == 0:
            return
        if general_register == 0:
            self.GRs[1].set_val(-1 * operand)
        else:
            result = self.GRs[general_register].get_val() - operand
            # Check overflow/underflow.
            if self.check_cc(result) == OVERFLOW:
                bits = decimal_to_binary(self.CC.get_val(), bit=4)
                bits = '1' + bits[1:]
                self.CC.set_val(binary_string_to_decimal(bits))
            elif self.check_cc(result) == UNDERFLOW:
                bits = decimal_to_binary(self.CC.get_val(), bit=4)
                bits = bits[:1] + '1' + bits[2:]
                self.CC.set_val(binary_string_to_decimal(bits))
            else:
                return {'Register': 'General', 'index': general_register, 'value': result}
               # self.GRs[general_register].set_val(result)
        #self.PC.increment_addr()

    # Multiply register by register.
    def MLT(self, operand, index_register, mode, general_register, effective_addr):
        # rx = general_register, ry = index_register
        self.CC.set_val(0)
        if (general_register != 0 and general_register != 2) or \
                (index_register != 0 and index_register != 2):
            return
        result = self.GRs[general_register].get_val() * self.GRs[index_register].get_val()
        # Check overflow/underflow.
        if self.check_cc(result) == OVERFLOW:
            bits = decimal_to_binary(self.CC.get_val(), bit=4)
            bits = '1' + bits[1:]
            self.CC.set_val(binary_string_to_decimal(bits))
        elif self.check_cc(result) == UNDERFLOW:
            bits = decimal_to_binary(self.CC.get_val(), bit=4)
            bits = bits[:1] + '1' + bits[2:]
            self.CC.set_val(binary_string_to_decimal(bits))
        else:
            # Extract the high order bits.
            self.GRs[general_register].set_val(int(result >> 16))
            # Extract the low order bits.
            self.GRs[general_register + 1].set_val(int(result & 0xFFFF))
        #self.PC.increment_addr()

    # Divide register by register.
    def DVD(self, operand, index_register, mode, general_register):
        # rx = general_register, ry = index_register
        self.CC.set_val(0)
        if (general_register != 0 and general_register != 2) or \
                (index_register != 0 and index_register != 2):
            return
        # Divide by Zero.
        if index_register == 0:
            bits = decimal_to_binary(self.CC.get_val(), bit=4)
            bits = bits[:2] + '1' + bits[3:]
            self.CC.set_val(binary_string_to_decimal(bits))
        else:
            result = self.GRs[general_register].get_val() / self.GRs[index_register].get_val()
            # Check overflow/underflow.
            if self.check_cc(result) == OVERFLOW:
                bits = decimal_to_binary(self.CC.get_val(), bit=4)
                bits = '1' + bits[1:]
                self.CC.set_val(binary_string_to_decimal(bits))
            elif self.check_cc(result) == UNDERFLOW:
                bits = decimal_to_binary(self.CC.get_val(), bit=4)
                bits = bits[:1] + '1' + bits[2:]
                self.CC.set_val(binary_string_to_decimal(bits))
            else:
                remainder = self.GRs[general_register].get_val() % self.GRs[index_register].get_val()
                self.GRs[general_register].set_val(result)
                self.GRs[general_register + 1].set_val(remainder)
       # self.PC.increment_addr()

    # Test the equality of register and register.
    def TRR(self, operand, ry, mode, rx):
        # rx = general_register, ry = index_register
        self.CC.set_val(0)
        if self.GRs[rx].get_val() == self.GRs[ry].get_val():
            bits = decimal_to_binary(self.CC.get_val(), bit=4)
            bits = bits[:3] + '1'
            self.CC.set_val(binary_string_to_decimal(bits))
        else:
            bits = decimal_to_binary(self.CC.get_val(), bit=4)
            bits = bits[:3] + '0'
            self.CC.set_val(binary_string_to_decimal(bits))
        #self.PC.increment_addr()

    # Logical And of register and register
    def AND(self, operand, ry, mode, rx):
        # rx = general_register, ry = index_register
        #return self.GRs[rx].get_val() & self.GRs[ry].get_val()
        #self.GRs[rx].set_val(self.GRs[rx].get_val() & self.GRs[ry].get_val())
        return {'Register': 'General', 'index': rx, 'value': self.GRs[rx].get_val() & self.GRs[ry].get_val()}
       # self.PC.increment_addr()

    # Logical Or of register and register
    def ORR(self, operand, ry, mode, rx, effective_addr):
        # rx = general_register, ry = index_register
        #return self.GRs[rx].get_val() | self.GRs[ry].get_val()
        #self.GRs[rx].set_val(self.GRs[rx].get_val() | self.GRs[ry].get_val())
        return {'Register': 'General', 'index': rx, 'value': self.GRs[rx].get_val() | self.GRs[ry].get_val()}
       # self.PC.increment_addr()

    # Logical Not of register and register
    def NOT(self, operand, ry, mode, rx):
        # rx = general_register
       # return ~self.GRs[rx].get_val()
       # self.GRs[rx].set_val(~self.GRs[rx].get_val())
       return {'Register': 'General', 'index': rx, 'value': ~self.GRs[rx].get_val()}
        #self.PC.increment_addr()

    # Shift register by count
    def SRC(self, operand, index_register, mode, general_register):
        # A_L = index_register 1st bit, L_R = index_register 2nd bit, Count = operand
        A_L = int(decimal_to_binary(index_register, 2)[0])
        L_R = int(decimal_to_binary(index_register, 2)[1])
        if A_L == 0:
            if L_R == 0:
                #return self.GRs[general_register].get_val() >> operand
                return {'Register': 'General', 'index': general_register, 'value': self.GRs[general_register].get_val() >> operand}
                #self.GRs[general_register].set_val(self.GRs[general_register].get_val() >> operand)
            elif L_R == 1:
                #self.GRs[general_register].set_val(self.GRs[general_register].get_val() << operand)
                #return self.GRs[general_register].get_val() << operand
                return {'Register': 'General', 'index': general_register, 'value': self.GRs[general_register].get_val() << operand}
        elif A_L == 1:
            if L_R == 0:
                if self.GRs[general_register].get_val() >= 0:
                    #self.GRs[general_register].set_val(self.rshift(self.GRs[general_register].get_val(), operand))
                   # return self.rshift(self.GRs[general_register].get_val(), operand)
                    return {'Register': 'General', 'index': general_register, 'value': self.rshift(self.GRs[general_register].get_val(), operand)}
                else:
                    tmp = decimal_to_binary(self.rshift(self.GRs[general_register].get_val(), operand))
                    tmp = tmp.replace("1111111111111111", "")
                    #return binary_string_to_decimal(tmp)
                   # self.GRs[general_register].set_val(binary_string_to_decimal(tmp))
                    return {'Register': 'General', 'index': general_register, 'value': binary_string_to_decimal(tmp)}
            elif L_R == 1:
                #self.GRs[general_register].set_val(self.GRs[general_register].get_val() << operand)
                #return self.GRs[general_register].get_val() << operand
                return {'Register': 'General', 'index': general_register, 'value': self.GRs[general_register].get_val() << operand}
        #self.PC.increment_addr()

    # Rotate register by count
    def RRC(self, operand, index_register, mode, general_register):
        # L_R = index_register 2nd bit, Count = operand
        L_R = int(decimal_to_binary(index_register, 2)[1])
        bits = decimal_to_binary(self.GRs[general_register].get_val())
        bits = bits.replace("0000000000000000", "")
        if self.GRs[general_register].get_val() < 0:
            bits = bits.replace("1111111111111111", "")
        if L_R == 1:
            #return binary_string_to_decimal(bits[operand:] + bits[:operand])
           # self.GRs[general_register].set_val(binary_string_to_decimal(bits[operand:] + bits[:operand]))
            return {'Register': 'General', 'index': general_register, 'value': binary_string_to_decimal(bits[operand:] + bits[:operand])}
        elif L_R == 0:
           # return binary_string_to_decimal(bits[len(bits) - operand:] + bits[:len(bits) - operand])
            return {'Register': 'General', 'index': general_register, 'value': binary_string_to_decimal(bits[len(bits) - operand:] + bits[:len(bits) - operand])}
            # self.GRs[general_register].set_val(
            #     binary_string_to_decimal(bits[len(bits) - operand:] + bits[:len(bits) - operand]))
        #self.PC.increment_addr()

    def IN(self, dev_id, index_register, mode, general_register):
        # devid = operand
        if dev_id == 0:  # Console Keyboard
            #return self.Device.get_keyboard()
           # self.GRs[general_register].set_val(self.Device.get_keyboard())
            return {'Register': 'General', 'index': general_register, 'value': self.Device.get_keyboard()}
        elif dev_id == 2:  # Card Reader
            pass
        else:
            pass
       # self.PC.increment_addr()

    def OUT(self, dev_id, index_register, mode, general_register):
        # devid = operand
        if dev_id == 1:  # Console Printer
            self.Device.set_printer(self.GRs[general_register].get_val())
        else:
            pass
       # self.PC.increment_addr()


    def FADD(self, operand, index_register, mode, floating_register, effective_addr):
        #effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        self.MAR.set_val(effective_addr)

        self.MBR.set_val(self.Cache.get_word(self.MAR.get_val()))
        temp = self.MBR.get_val()
        temp = decimal_to_binary(temp)
        temp = binary_to_floating(temp)

        #TODO: Implement error handling for incorrect/out of bounds register
        result = self.FRs[floating_register].get_val() + temp

        # Check overflow.
        if (result > 1 and result > MAX_WHOLE_FP) or (result < -1 and result < MIN_WHOLE_FP):
            bits = decimal_to_binary(self.CC.get_val(), bit=4)
            bits = '1' + bits[1:]
            self.CC.set_val(binary_string_to_decimal(bits))
        #check underflow
        elif (result > 0 and result < MAX_DEC_FP) or (result < 0 and result > MIN_DEC_FP):
            bits = decimal_to_binary(self.CC.get_val(), bit=4)
            bits = bits[:1] + '1' + bits[2:]
            self.CC.set_val(binary_string_to_decimal(bits))
        else:
            #return result
            return {'Register': 'Floating', 'index': floating_register, 'value': result}
           # self.FRs[floating_register].set_val(result)
        #self.PC.increment_addr()

    def FSUB(self, operand, index_register, mode, floating_register, effective_addr):
       # effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        self.MAR.set_val(effective_addr)

        self.MBR.set_val(self.Cache.get_word(self.MAR.get_val()))
        temp = self.MBR.get_val()
        temp = decimal_to_binary(temp)
        temp = binary_to_floating(temp)

        result = self.FRs[floating_register].get_val() - temp

        # Check overflow.
        if (result > 1 and result > MAX_WHOLE_FP) or (result < -1 and result < MIN_WHOLE_FP):
            bits = decimal_to_binary(self.CC.get_val(), bit=4)
            bits = '1' + bits[1:]
            self.CC.set_val(binary_string_to_decimal(bits))
        #check underflow
        elif (result > 0 and result < MAX_DEC_FP) or (result < 0 and result > MIN_DEC_FP):
            bits = decimal_to_binary(self.CC.get_val(), bit=4)
            bits = bits[:1] + '1' + bits[2:]
            self.CC.set_val(binary_string_to_decimal(bits))
        else:
            return {'Register': 'Floating', 'index': floating_register, 'value': result}
            #self.FRs[floating_register].set_val(result)
        #self.PC.increment_addr()


    #NOTE: we assume <16,7> fixed point representation
    def CNVRT(self, operand, index_register, mode, general_register, effective_addr):
        effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        self.MAR.set_val(effective_addr)

        self.MBR.set_val(self.Cache.get_word(self.MAR.get_val()))

        temp = self.MBR.get_val()
        temp = decimal_to_binary(temp)
        
        #get bit from general register
        F = self.GRs[general_register].get_val()
        if F == 0:
            #convert c(EA) to fixed point, storein general_register
            temp = binary_to_floating(temp)
            result = floating_to_fixed(temp, 7)
            if (result > 1 and result > MAX_WHOLE_FP) or (result < -1 and result < MIN_WHOLE_FP):
                bits = decimal_to_binary(self.CC.get_val(), bit=4)
                bits = '1' + bits[1:]
                self.CC.set_val(binary_string_to_decimal(bits))
        #check underflow
            elif (result > 0 and result < MAX_DEC_FP) or (result < 0 and result > MIN_DEC_FP):
                bits = decimal_to_binary(self.CC.get_val(), bit=4)
                bits = bits[:1] + '1' + bits[2:]
                self.CC.set_val(binary_string_to_decimal(bits))
            else:
                #return result
                #self.GRs[general_register].set_val(result)
                return {'Register': 'General', 'index': general_register, 'value': result}
        if F == 1: 
            #concert c(EA) to floating point, store in FR0
            temp = binary_to_fixed(temp)
            result = fixed_to_floating(temp)
            #return result
            return {'Register': 'Floating', 'index': 0, 'value': result}
            #self.FRs[0].set_val(result)
        #self.PC.increment_addr()

    #TODO
    def TRAP(self, trap_code, index_register, mode, general_register):
        if trap_code > 15 or trap_code < 0:
            bits = decimal_to_binary(self.MFR.get_val(), bit=4)
            bits = bits[:2] + '1' + bits[3:]
            self.MFR.set_val(binary_string_to_decimal(bits))

        #Store PC for TRAP
        self.MAR.set_val(2)
        self.MBR.set_val(self.PC.get_addr() + 1)
        self.Cache.set_word(self.MAR.get_val(), self.MBR.get_val())

        #gets address of trap table 
        self.MAR.set_val(0)
        self.MBR.set_val(self.Cache.get_word(self.MAR.get_val()))
        table_addr = self.MBR.get_val()

        #set PC to mapped rountine from trap table
        self.MAR.set_val(trap_code + table_addr)
        self.MBR.set_val(self.Cache.get_word(self.MAR.get_val()))
        routine = self.MBR.get_val()
        self.PC.set_addr(routine)

    def HALT(self):
        return -1

    # determines effective address based off of operand, index register, and mode(direct/indirect)
    def get_effective_addr(self, opcode, operand, index_register, mode):
        if mode == 0:
            if index_register == 0:
                if self.check_addr(operand):
                    return operand
                else:
                    return -1
            else:
                if self.check_addr(operand + self.IndexRegisters[index_register - 1].get_val()):
                    return operand + self.IndexRegisters[index_register - 1].get_val()
                else:
                    return -1
        elif mode == 1:
            if index_register == 0:
                if self.check_addr(operand):
                    self.MAR.set_val(operand)
                    #self.MBR.set_val(self.Memory.words[self.MAR.get_val()])
                    self.MBR.set_val(self.Cache.get_word(self.MAR.get_val()))
                else:
                    return -1
            else:
                if self.check_addr(operand + self.IndexRegisters[index_register - 1].get_val()):
                    self.MAR.set_val(operand + self.IndexRegisters[index_register - 1].get_val())
                    #self.MBR.set_val(self.Memory.words[self.MAR.get_val()])
                    self.MBR.set_val(self.Cache.get_word(self.MAR.get_val()))
                else:
                    return -1
            if self.check_addr(self.MBR.get_val()):
                return self.MBR.get_val()
            else:
                return -1
        return 0

    # validates effective address does not violate memory constraints
    def check_addr(self, addr):
        # Reserved memory location.
        

        if 0 <= addr < 6:
            bits = decimal_to_binary(self.MFR.get_val(), bit=4)
            bits = bits[:3] + '1'
            self.MFR.set_val(binary_string_to_decimal(bits))
            return False
        # Memory address is beyond the size of memory.
        elif addr >= self.memsize:
            bits = decimal_to_binary(self.MFR.get_val(), bit=4)
            bits = '1' + bits[1:]
            self.MFR.set_val(binary_string_to_decimal(bits))
            return False
        return True

    # check overflow and underflow.
    def check_cc(self, num):
        if num >= MAX_VALUE:
            return OVERFLOW
        elif num < MIN_VALUE:
            return UNDERFLOW
        return -1

    def rshift(self, val, n):
        return val >> n if val >= 0 else (val + 0x100000000) >> n


    # function to execute single instruction after being decoded
    def single_step(self, opcode, operand, index_register, mode, general_register, effective_addr=None):
        if self.PC.get_addr() > 9 and self.PC.get_addr() < 126:
            print(self.PC.get_addr())
        if opcode == 1:
            return self.LDR(operand, index_register, mode, general_register, effective_addr)
        elif opcode == 2:
            return self.STR(operand, index_register, mode, general_register, effective_addr)
        elif opcode == 3:
            return self.LDA(operand, index_register, mode, general_register, effective_addr)
        elif opcode == 33:
            return self.LDX_mod(operand, index_register, mode, general_register, effective_addr)
        elif opcode == 34:
            return self.STX(operand, index_register, mode, general_register, effective_addr)
        elif opcode == 4:
            return self.AMR(operand, index_register, mode, general_register, effective_addr)
        elif opcode == 5:
            return self.SMR(operand, index_register, mode, general_register, effective_addr)
        elif opcode == 6:
            return self.AIR(operand, index_register, mode, general_register, effective_addr)
        elif opcode == 7:
            return self.SIR(operand, index_register, mode, general_register, effective_addr)
        elif opcode == 8:
            return self.JZ(operand, index_register, mode, general_register, effective_addr)
        elif opcode == 9:
            return self.JNE(operand, index_register, mode, general_register, effective_addr)
        elif opcode == 10:
            return self.JCC(operand, index_register, mode, general_register, effective_addr)
        elif opcode == 11:
            return self.JMA(operand, index_register, mode, general_register, effective_addr)
        elif opcode == 12:
            return self.JSR(operand, index_register, mode, general_register, effective_addr)
        elif opcode == 13:
            return self.RFS(operand, index_register, mode, general_register)
        elif opcode == 14:
            return self.SOB(operand, index_register, mode, general_register, effective_addr)
        elif opcode == 15:
            return self.JGE(operand, index_register, mode, general_register, effective_addr)
        elif opcode == 16:
            return self.MLT(operand, index_register, mode, general_register, effective_addr)
        elif opcode == 17:
            return self.DVD(operand, index_register, mode, general_register)
        elif opcode == 18:
            return self.TRR(operand, index_register, mode, general_register)
        elif opcode == 19:
            return self.AND(operand, index_register, mode, general_register)
        elif opcode == 20:
            return self.ORR(operand, index_register, mode, general_register)
        elif opcode == 21:
            return self.NOT(operand, index_register, mode, general_register)
        elif opcode == 25:
            return self.SRC(operand, index_register, mode, general_register)
        elif opcode == 26:
            return self.RRC(operand, index_register, mode, general_register)
        elif opcode == 27:
            return self.FADD(operand, index_register, mode, general_register, effective_addr)
        elif opcode == 28:
            return self.FSUB(operand, index_register, mode, general_register, effective_addr)
        elif opcode == 40:
            return self.LDFR(operand, index_register, mode, general_register)
        elif opcode == 41:
            return self.STFR(operand, index_register, mode, general_register)
        elif opcode == 31:
            return self.CNVRT(operand, index_register, mode, general_register, effective_addr)
        elif opcode == 49:
            return self.IN(operand, index_register, mode, general_register)
        elif opcode == 50:
            return self.OUT(operand, index_register, mode, general_register)
        elif opcode == 24:
            return self.TRAP(operand, index_register, mode, general_register)
        elif opcode == 0:
            return self.HALT()
        # Illegal opcode.
        else:
            bits = decimal_to_binary(self.MFR.get_val(), bit=4)
            bits = bits[:1] + '1' + bits[2:]
            self.MFR.set_val(binary_string_to_decimal(bits))
            # return self.HALT()


# for testing purposes
def main():
    cpu = CPU(2048)
    cpu.Memory.read_mem('test_program.txt')
    cpu.GRs[0].set_val(0)
    cpu.FRs[0].set_val(6.2)
    cpu.CNVRT(11, 0, 0, 0)
    cpu.GRs[0].set_val(1)
    cpu.CNVRT(12, 0, 0, 0)
    cpu.LDFR(9, 0, 0, 1)



if __name__ == '__main__':
    main()
