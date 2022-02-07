from PC import ProgramCounter as PC
from registers import MAR, MBR, MFR, IR, IndexRegister, GeneralRegister as GR
from Memory import Memory


class CPU:

    def __init__(self, memsize=2048):
        self.PC = PC(0)  # starting addr from IPL.txt
        self.GRs = [GR() for i in range(4)]
        self.IndexRegisters = [IndexRegister(0) for i in range(3)]
        self.MAR = MAR()
        self.MBR = MBR()
        self.MFR = MFR()
        self.IR = IR()
        self.memsize = memsize
        self.Memory = Memory(memsize)

    def reset(self):
        self.PC = PC(0)  # starting addr from IPL.txt
        self.GRs = [GR() for i in range(4)]
        self.IndexRegisters = [IndexRegister(0) for i in range(3)]
        self.MAR = MAR()
        self.MBR = MBR()
        self.MFR = MFR()
        self.IR = IR()
        self.Memory.words = dict.fromkeys((range(self.memsize)), 0)

    def LDR(self, operand, index_register, mode, general_register):
        effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return self.HALT()
        self.MAR.set_val(effective_addr)
        self.MBR.set_val(self.Memory.words[self.MAR.get_val()])
        self.GRs[general_register].set_val(self.MBR.get_val())

    def STR(self, operand, index_register, mode, general_register):
        effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return self.HALT()
        self.MBR.set_val(self.GRs[general_register].get_val())
        self.Memory.words[effective_addr] = self.MBR.get_val()

    def LDA(self, operand, index_register, mode, general_register):
        effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return self.HALT()
        self.GRs[general_register].set_val(effective_addr)

    def LDX(self, operand, index_register, mode, general_register):
        effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return self.HALT()
        self.MBR.set_val(self.Memory.words[effective_addr])
        self.IndexRegisters[index_register - 1].set_val(self.MBR.get_val())

    def STX(self, operand, index_register, mode, general_register):
        effective_addr = self.get_effective_addr(operand, index_register, mode)
        if effective_addr == -1:
            return self.HALT()
        self.MAR.set_val(effective_addr)
        self.MBR.set_val(self.IndexRegisters[index_register - 1].get_val())
        self.Memory.words[self.MAR.get_val()] = self.MBR.get_val()

    def HALT(self):
        return -1

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
            return self.MBR.get_val()
        return 0

    def check_addr(self, addr):
        # Reserved memory location.
        if 0 <= addr < 6:
            self.MFR.set_val(1)
            return False
        # Memory address is beyond the size of memory.
        elif addr >= self.memsize:
            self.MFR.set_val(3)
            return False
        return True

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
        elif opcode == 0:
            return self.HALT()
        # Illegal opcode.
        else:
            self.MFR.set_val(2)
            return self.HALT()

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
        elif opcode == 0:
            return self.HALT()
        # Illegal opcode.
        else:
            self.MFR.set_val(2)
            return self.HALT()


def main():
    cpu = CPU(2048)
    cpu.Memory.read_mem()
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
