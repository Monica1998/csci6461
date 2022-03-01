from PC import ProgramCounter as PC
from converter import decimal_to_binary, binary_string_to_decimal
from registers import MAR, MBR, MFR, CC, IR, IndexRegister, GeneralRegister as GR
from Memory import Memory

MAX_VALUE = 2147483647
MIN_VALUE = -2147483648
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

    # resets all registers and program counter to default values when hitting HALT instruction
    def reset(self):
        self.PC = PC(0)  # starting addr from IPL.txt
        self.GRs = [GR() for i in range(4)]
        self.IndexRegisters = [IndexRegister(0) for i in range(3)]
        self.MAR = MAR()
        self.MBR = MBR()
        self.MFR = MFR()
        self.CC = CC()
        self.IR = IR()
        self.Memory.words = dict.fromkeys((range(self.memsize)), 0)

    # Load data to general register from effective address
    def LDR(self, operand, index_register, mode, general_register):
        effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        self.MAR.set_val(effective_addr)
        self.MBR.set_val(self.Memory.words[self.MAR.get_val()])
        self.GRs[general_register].set_val(self.MBR.get_val())

    # store data from general register to memory
    def STR(self, operand, index_register, mode, general_register):
        effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        self.MBR.set_val(self.GRs[general_register].get_val())
        self.Memory.words[effective_addr] = self.MBR.get_val()

    # load effective address into general register
    def LDA(self, operand, index_register, mode, general_register):
        effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        self.GRs[general_register].set_val(effective_addr)

    # load data into index register
    def LDX(self, operand, index_register, mode, general_register):
        effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        self.MBR.set_val(self.Memory.words[effective_addr])
        self.IndexRegisters[index_register - 1].set_val(self.MBR.get_val())

    # store data from index register into memory
    def STX(self, operand, index_register, mode, general_register):
        effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        self.MAR.set_val(effective_addr)
        self.MBR.set_val(self.IndexRegisters[index_register - 1].get_val())
        self.Memory.words[self.MAR.get_val()] = self.MBR.get_val()

    # Add memory to register.
    def AMR(self, operand, index_register, mode, general_register):
        # immed = operand
        effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        self.MAR.set_val(effective_addr)

        # TODO: fetch from cache(self.MAR.get_val())
        self.MBR.set_val(self.Memory.words[self.MAR.get_val()])

        result = self.GRs[general_register].get_val() + self.MBR.get_val()
        # Check overflow.
        if MIN_VALUE <= result <= MAX_VALUE:
            self.GRs[general_register].set_val(result)

    # Subtract memory from register.
    def SMR(self, operand, index_register, mode, general_register):
        effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return
        self.MAR.set_val(effective_addr)

        # TODO: fetch from cache(self.MAR.get_val())
        self.MBR.set_val(self.Memory.words[self.MAR.get_val()])

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

    # Add immediate to register.
    def AIR(self, operand, index_register, mode, general_register):
        # immed = operand
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

    # Subtract immediate from register.
    def SIR(self, operand, index_register, mode, general_register):
        # immed = operand
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

    # Multiply register by register.
    def MLT(self, operand, index_register, mode, general_register):
        # rx = general_register, ry = index_register
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

    # Divide register by register.
    def DVD(self, operand, index_register, mode, general_register):
        # rx = general_register, ry = index_register
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

    # Test the equality of register and register.
    def TRR(self, operand, index_register, mode, general_register):
        # rx = general_register, ry = index_register
        if (general_register != 0 and general_register != 2) or \
                (index_register != 0 and index_register != 2):
            return
        if general_register == index_register:
            bits = decimal_to_binary(self.CC.get_val(), bit=4)
            bits = bits[:3] + '1'
            self.CC.set_val(binary_string_to_decimal(bits))
        else:
            bits = decimal_to_binary(self.CC.get_val(), bit=4)
            bits = bits[:3] + '0'
            self.CC.set_val(binary_string_to_decimal(bits))

    # Logical And of register and register
    def AND(self, operand, index_register, mode, general_register):
        # rx = general_register, ry = index_register
        self.GRs[general_register].set_val(general_register & index_register)

    # Logical Or of register and register
    def ORR(self, operand, index_register, mode, general_register):
        # rx = general_register, ry = index_register
        self.GRs[general_register].set_val(general_register | index_register)

    # Logical Not of register and register
    def NOT(self, operand, index_register, mode, general_register):
        # rx = general_register
        self.GRs[general_register].set_val(~general_register)

    # Shift register by count
    def SRC(self, operand, index_register, mode, general_register):
        # A_L = index_register 1st bit, L_R = index_register 2nd bit, Count = operand
        A_L = decimal_to_binary(index_register, 2)[0]
        L_R = decimal_to_binary(index_register, 2)[1]
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

    # Rotate register by count
    def RRC(self, operand, index_register, mode, general_register):
        # L_R = index_register 2nd bit, Count = operand
        L_R = decimal_to_binary(index_register, 2)[1]
        bits = decimal_to_binary(self.GRs[general_register].get_val())
        bits = bits.replace("0000000000000000", "")
        if self.GRs[general_register].get_val() < 0:
            bits = bits.replace("1111111111111111", "")
        if L_R == 1:
            self.GRs[general_register].set_val(binary_string_to_decimal(bits[operand:] + bits[:operand]))
        elif L_R == 0:
            self.GRs[general_register].set_val(binary_string_to_decimal(bits[:len(bits) - operand] + bits[len(bits) - operand:]))


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
                    self.MBR.set_val(self.Memory.words[self.MAR.get_val()])
                else:
                    return -1
            else:
                if self.check_addr(operand + self.IndexRegisters[index_register - 1].get_val()):
                    self.MAR.set_val(operand + self.IndexRegisters[index_register - 1].get_val())
                    self.MBR.set_val(self.Memory.words[self.MAR.get_val()])
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
        if num > MAX_VALUE:
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
        self.MBR.set_val(self.Memory.words[addr])

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
        elif opcode == 0:
            return self.HALT()
        # Illegal opcode.
        else:
            bits = decimal_to_binary(self.MFR.get_val(), bit=4)
            bits = bits[:1] + '1' + bits[2:]
            self.MFR.set_val(binary_string_to_decimal(bits))
            #return self.HALT()

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
        elif opcode == 0:
            return self.HALT()
        # Illegal opcode.
        else:
            bits = decimal_to_binary(self.MFR.get_val(), bit=4)
            bits = bits[:1] + '1' + bits[2:]
            self.MFR.set_val(binary_string_to_decimal(bits))
            #return self.HALT()


# for testing purposes
def main():
    cpu = CPU(2048)
    cpu.Memory.read_mem('IPL.txt')
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
