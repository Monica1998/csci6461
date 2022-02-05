class Register:

    def __init__(self, val=0):
        self.val = val

    def set_val(self, val):
        self.val = val

    def get_val(self):
        return self.val


class MAR(Register):
    pass


class MBR(Register):
    pass


class MFR(Register):
    pass


class IR():

    def __init__(self, instruction=None):
        self.instruction = instruction

    def set_instruction(self, val):
        self.instruction = val

    def get_instruction(self):
        return self.instruction

    def decode(self):
        # instruction = hex_to_decimal(self.instruction)
        # process self.instruciton
        opcode = self.instruction % 2 ** 6
        operand = self.instruction // 2 ** 11
        index_register = (self.instruction // 2 ** 8) % 2 ** 2
        mode = (self.instruction // 2 ** 10) % 2 ** 1
        general_register = (self.instruction // 2 ** 6) % 2 ** 2
        return opcode, operand, index_register, mode, general_register


class IndexRegister(Register):
    pass


class GeneralRegister(Register):
    pass


def main():
    m = MAR()
    print(m.get_val())


if __name__ == '__main__':
    main()
