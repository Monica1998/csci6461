from Device import Device
from PC import ProgramCounter as PC
from converter import decimal_to_binary, binary_string_to_decimal
from registers import MAR, MBR, MFR, CC, IR, IndexRegister, GeneralRegister as GR
from Memory import Memory
from cache import Cache

MAX_VALUE = 65536
MIN_VALUE = 0
OVERFLOW = 0
UNDERFLOW = 1


class CPU:

    # initializes all components, 4 General Registers, 3 Index Registers
    def __init__(self, memsize=2048):
        self.PC = PC(0)  # starting addr from IPL.txt
        self.GRs = [GR() for i in range(4)]
        self.IndexRegisters = [IndexRegister(0) for i in range(3)]
        self.MAR = MAR()
        self.MBR = MBR()
        self.MFR = MFR()
        self.CC = CC()
        self.IR = IR()
        self.memsize = memsize
        self.Memory = Memory(memsize)
        self.Cache = Cache(self.Memory)
        self.Device = Device()

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
    def LDR(self, operand, index_register, mode, general_register):
        effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        self.MAR.set_val(effective_addr)
        self.MBR.set_val(self.Cache.get_word(self.MAR.get_val()))
        self.GRs[general_register].set_val(self.MBR.get_val())
        self.PC.increment_addr()

    # store data from general register to memory
    def STR(self, operand, index_register, mode, general_register):
        effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        self.MBR.set_val(self.GRs[general_register].get_val())
        #self.Memory.words[effective_addr] = self.MBR.get_val()
        self.Cache.set_word(effective_addr, self.MBR.get_val())
        self.PC.increment_addr()

    # load effective address into general register
    def LDA(self, operand, index_register, mode, general_register):
        effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        self.GRs[general_register].set_val(effective_addr)
        self.PC.increment_addr()

    # load data into index register
    def LDX(self, operand, index_register, mode, general_register):
        effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        #self.MBR.set_val(self.Memory.words[effective_addr])
        self.MBR.set_val(self.Cache.get_word(effective_addr))
        self.IndexRegisters[index_register - 1].set_val(self.MBR.get_val())
        self.PC.increment_addr()

    # store data from index register into memory
    def STX(self, operand, index_register, mode, general_register):
        effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        self.MAR.set_val(effective_addr)
        self.MBR.set_val(self.IndexRegisters[index_register - 1].get_val())
        #self.Memory.words[self.MAR.get_val()] = self.MBR.get_val()
        self.Cache.set_word(self.MAR.get_val(), self.MBR.get_val())
        self.PC.increment_addr()

    # Jump if Equal
    def JZ(self, operand, index_register, mode, general_register):
        effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        self.MAR.set_val(effective_addr)
        if self.GRs[general_register].get_val() == 0:
            self.PC.set_addr(effective_addr)
        else:
            self.PC.increment_addr()

    # Jump If Not Equal
    def JNE(self, operand, index_register, mode, general_register):
        effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        self.MAR.set_val(effective_addr)
        if self.GRs[general_register].get_val() != 0:
            self.PC.set_addr(effective_addr)
        else:
            self.PC.increment_addr()

    # Jump If Condition Code
    def JCC(self, operand, index_register, mode, cc):
        effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        self.MAR.set_val(effective_addr)
        bits = decimal_to_binary(self.CC.get_val(), bit=4)
        if bits[cc] == '1':
            self.PC.set_addr(effective_addr)
        else:
            self.PC.increment_addr()

    # Unconditional Jump To Address
    def JMA(self, operand, index_register, mode, general_register):
        effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        self.MAR.set_val(effective_addr)
        self.PC.set_addr(effective_addr)

    # Jump and Save Return Address
    def JSR(self, operand, index_register, mode, general_register):
        effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        self.MAR.set_val(effective_addr)
        result = self.PC.get_addr() + 1
        self.GRs[3].set_val(result)
        self.PC.set_addr(effective_addr)
        # R0 should contain pointer to arguments. Argument list should end with -1 (all 1s) value

    # Return From Subroutine w/ return code as Immed portion (optional) stored in the instruction's address Field
    def RFS(self, operand, index_register, mode, general_register):
        self.GRs[0].set_val(operand)
        temp = self.GRs[3].get_val()
        self.PC.set_addr(temp)
        # IX, I fields are ignored

    # Subtract One and Branch
    def SOB(self, operand, index_register, mode, general_register):
        effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        self.MAR.set_val(effective_addr)
        result = self.GRs[general_register].get_val() - 1
        self.GRs[general_register].set_val(result)
        if self.GRs[general_register].get_val() > 0:
            self.PC.set_addr(effective_addr)
        else:
            self.PC.increment_addr()

    # Jump Greater than or equal to
    def JGE(self, operand, index_register, mode, general_register):
        effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        self.MAR.set_val(effective_addr)
        if self.GRs[general_register].get_val() >= 0:
            self.PC.set_addr(effective_addr)
        else:
            self.PC.increment_addr()

    # Add memory to register.
    def AMR(self, operand, index_register, mode, general_register):
        # immed = operand
        self.CC.set_val(0)
        effective_addr = self.get_effective_addr(operand, index_register, mode)
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
            self.GRs[general_register].set_val(result)
        self.PC.increment_addr()

    # Subtract memory from register.
    def SMR(self, operand, index_register, mode, general_register):
        self.CC.set_val(0)
        effective_addr = self.get_effective_addr(operand, index_register, mode)
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
            self.GRs[general_register].set_val(result)
        self.PC.increment_addr()

    # Add immediate to register.
    def AIR(self, operand, index_register, mode, general_register):
        # immed = operand
        self.CC.set_val(0)
        if operand == 0:
            return
        if general_register == 0:
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
                self.GRs[general_register].set_val(result)
        self.PC.increment_addr()

    # Subtract immediate from register.
    def SIR(self, operand, index_register, mode, general_register):
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
                self.GRs[general_register].set_val(result)
        self.PC.increment_addr()

    # Multiply register by register.
    def MLT(self, operand, index_register, mode, general_register):
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
        self.PC.increment_addr()

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
        self.PC.increment_addr()

    # Test the equality of register and register.
    def TRR(self, operand, ry, mode, rx):
        # rx = general_register, ry = index_register
        self.CC.set_val(0)
        if self.GRs[rx] == self.GRs[ry]:
            bits = decimal_to_binary(self.CC.get_val(), bit=4)
            bits = bits[:3] + '1'
            self.CC.set_val(binary_string_to_decimal(bits))
        else:
            bits = decimal_to_binary(self.CC.get_val(), bit=4)
            bits = bits[:3] + '0'
            self.CC.set_val(binary_string_to_decimal(bits))
        self.PC.increment_addr()

    # Logical And of register and register
    def AND(self, operand, ry, mode, rx):
        # rx = general_register, ry = index_register
        self.GRs[rx].set_val(self.GRs[rx].get_val() & self.GRs[ry].get_val())
        self.PC.increment_addr()

    # Logical Or of register and register
    def ORR(self, operand, ry, mode, rx):
        # rx = general_register, ry = index_register
        self.GRs[rx].set_val(self.GRs[rx].get_val() | self.GRs[ry].get_val())
        self.PC.increment_addr()

    # Logical Not of register and register
    def NOT(self, operand, ry, mode, rx):
        # rx = general_register
        self.GRs[rx].set_val(~self.GRs[rx].get_val())
        self.PC.increment_addr()

    # Shift register by count
    def SRC(self, operand, index_register, mode, general_register):
        # A_L = index_register 1st bit, L_R = index_register 2nd bit, Count = operand
        A_L = int(decimal_to_binary(index_register, 2)[0])
        L_R = int(decimal_to_binary(index_register, 2)[1])
        if A_L == 0:
            if L_R == 0:
                self.GRs[general_register].set_val(self.GRs[general_register].get_val() >> operand)
            elif L_R == 1:
                self.GRs[general_register].set_val(self.GRs[general_register].get_val() << operand)
        elif A_L == 1:
            if L_R == 0:
                if self.GRs[general_register].get_val() >= 0:
                    self.GRs[general_register].set_val(self.rshift(self.GRs[general_register].get_val(), operand))
                else:
                    tmp = decimal_to_binary(self.rshift(self.GRs[general_register].get_val(), operand))
                    tmp = tmp.replace("1111111111111111", "")
                    self.GRs[general_register].set_val(binary_string_to_decimal(tmp))
            elif L_R == 1:
                self.GRs[general_register].set_val(self.GRs[general_register].get_val() << operand)
        self.PC.increment_addr()

    # Rotate register by count
    def RRC(self, operand, index_register, mode, general_register):
        # L_R = index_register 2nd bit, Count = operand
        L_R = int(decimal_to_binary(index_register, 2)[1])
        bits = decimal_to_binary(self.GRs[general_register].get_val())
        bits = bits.replace("0000000000000000", "")
        if self.GRs[general_register].get_val() < 0:
            bits = bits.replace("1111111111111111", "")
        if L_R == 1:
            self.GRs[general_register].set_val(binary_string_to_decimal(bits[operand:] + bits[:operand]))
        elif L_R == 0:
            self.GRs[general_register].set_val(
                binary_string_to_decimal(bits[len(bits) - operand:] + bits[:len(bits) - operand]))
        self.PC.increment_addr()

    def IN(self, dev_id, index_register, mode, general_register):
        # devid = operand
        if dev_id == 0:  # Console Keyboard
            self.GRs[general_register].set_val(self.Device.get_keyboard())
        elif dev_id == 2:  # Card Reader
            pass
        else:
            pass
        self.PC.increment_addr()

    def OUT(self, dev_id, index_register, mode, general_register):
        # devid = operand
        if dev_id == 1:  # Console Printer
            self.Device.set_printer(self.GRs[general_register].get_val())
        else:
            pass
        self.PC.increment_addr()

    def TRAP(self, operand, index_register, mode, trap_code):
        if trap_code > 15 or trap_code < 0:
            bits = decimal_to_binary(self.MFR.get_val(), bit=4)
            bits = bits[:2] + '1' + bits[3:]
            self.MFR.set_val(binary_string_to_decimal(bits))

        self.MAR.set_val(2)
        self.MBR.set_val(self.PC.get_addr() + 1)
        self.Cache.set_word(self.MAR.get_val(), self.MBR.get_val())

        self.MAR.set_val(0)
        self.MBR.set_val(self.Cache.get_word(self.MAR.get_val()))
        table_addr = self.MBR.get_val()

        self.MAR.set_val(trap_code + table_addr)
        self.MBR.set_val(self.Cache.get_word(self.MAR.get_val()))
        routine = self.MBR.get_val()
        self.PC.set_addr(routine)

    def HALT(self):
        return -1

    # determines effective address based off of operand, index register, and mode(direct/indirect)
    def get_effective_addr(self, operand, index_register, mode):
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

    # executes one instruction by fetching instruction address from Program Counter
    def step(self):
        self.MAR.set_val(self.PC.get_addr())
        self.PC.increment_addr()  # points to next instruction

        addr = self.MAR.get_val()
        #self.MBR.set_val(self.Memory.words[addr])
        self.MBR.set_val(self.Cache.get_word(addr))

        self.IR.set_instruction(self.MBR.get_val())

        opcode, operand, index_register, mode, general_register = self.IR.decode()

        if opcode == 1:
            return self.LDR(operand, index_register, mode, general_register)
        elif opcode == 2:
            return self.STR(operand, index_register, mode, general_register)
        elif opcode == 3:
            return self.LDA(operand, index_register, mode, general_register)
        elif opcode == 33:
            return self.LDX(operand, index_register, mode, general_register)
        elif opcode == 34:
            return self.STX(operand, index_register, mode, general_register)
        elif opcode == 4:
            return self.AMR(operand, index_register, mode, general_register)
        elif opcode == 5:
            return self.SMR(operand, index_register, mode, general_register)
        elif opcode == 6:
            return self.AIR(operand, index_register, mode, general_register)
        elif opcode == 7:
            return self.SIR(operand, index_register, mode, general_register)
        elif opcode == 8:
            return self.JZ(operand, index_register, mode, general_register)
        elif opcode == 9:
            return self.JNE(operand, index_register, mode, general_register)
        elif opcode == 10:
            return self.JCC(operand, index_register, mode, general_register)
        elif opcode == 11:
            return self.JMA(operand, index_register, mode, general_register)
        elif opcode == 12:
            return self.JSR(operand, index_register, mode, general_register)
        elif opcode == 13:
            return self.RFS(operand, index_register, mode, general_register)
        elif opcode == 14:
            return self.SOB(operand, index_register, mode, general_register)
        elif opcode == 15:
            return self.JGE(operand, index_register, mode, general_register)
        elif opcode == 16:
            return self.MLT(operand, index_register, mode, general_register)
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
        elif opcode == 49:
            return self.IN(operand, index_register, mode, general_register)
        elif opcode == 50:
            return self.OUT(operand, index_register, mode, general_register)
        elif opcode == 0:
            return self.HALT()
        # Illegal opcode.
        else:
            bits = decimal_to_binary(self.MFR.get_val(), bit=4)
            bits = bits[:1] + '1' + bits[2:]
            self.MFR.set_val(binary_string_to_decimal(bits))
            # return self.HALT()

    # function to execute single instruction after being decoded
    def single_step(self, opcode, operand, index_register, mode, general_register):
        if opcode == 1:
            return self.LDR(operand, index_register, mode, general_register)
        elif opcode == 2:
            return self.STR(operand, index_register, mode, general_register)
        elif opcode == 3:
            return self.LDA(operand, index_register, mode, general_register)
        elif opcode == 33:
            return self.LDX(operand, index_register, mode, general_register)
        elif opcode == 34:
            return self.STX(operand, index_register, mode, general_register)
        elif opcode == 4:
            return self.AMR(operand, index_register, mode, general_register)
        elif opcode == 5:
            return self.SMR(operand, index_register, mode, general_register)
        elif opcode == 6:
            return self.AIR(operand, index_register, mode, general_register)
        elif opcode == 7:
            return self.SIR(operand, index_register, mode, general_register)
        elif opcode == 8:
            return self.JZ(operand, index_register, mode, general_register)
        elif opcode == 9:
            return self.JNE(operand, index_register, mode, general_register)
        elif opcode == 10:
            return self.JCC(operand, index_register, mode, general_register)
        elif opcode == 11:
            return self.JMA(operand, index_register, mode, general_register)
        elif opcode == 12:
            return self.JSR(operand, index_register, mode, general_register)
        elif opcode == 13:
            return self.RFS(operand, index_register, mode, general_register)
        elif opcode == 14:
            return self.SOB(operand, index_register, mode, general_register)
        elif opcode == 15:
            return self.JGE(operand, index_register, mode, general_register)
        elif opcode == 16:
            return self.MLT(operand, index_register, mode, general_register)
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
        elif opcode == 49:
            return self.IN(operand, index_register, mode, general_register)
        elif opcode == 50:
            return self.OUT(operand, index_register, mode, general_register)
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
    cpu.Memory.read_mem('IPL_part2.txt')
    cpu.step()
    cpu.step()
    cpu.step()
    cpu.step()
    cpu.step()
    cpu.step()
    cpu.step()
    cpu.step()
    cpu.step()
    cpu.step()
    cpu.step()
    cpu.step()
    cpu.step()


if __name__ == '__main__':
    main()
