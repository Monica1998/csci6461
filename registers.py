from converter import binary_string_to_decimal, decimal_to_binary


#parent register class with getters and setters
class Register:

    def __init__(self, val=0):
        self.val = val

    def set_val(self, val):
        self.val = val

    def get_val(self):
        return self.val

#Memory Address Register to hold memory address
class MAR(Register):
    pass


#Memory Buffer Register to hold data to/from memory
class MBR(Register):
    pass

#Memory Fault Register
class MFR(Register):
    pass

#Instruction Register to get, set, and decode instructions 
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
        bits = decimal_to_binary(self.instruction)
        s = 0
        opcode = binary_string_to_decimal(bits[s:s+6])
        s += 6
        general_register = binary_string_to_decimal(bits[s:s+2])
        s += 2
        index_register = binary_string_to_decimal(bits[s:s+2])
        s += 2
        mode = binary_string_to_decimal(bits[s:s+1])
        s += 1
        operand = binary_string_to_decimal(bits[s:s+5])
        #opcode = self.instruction % 2 ** 6
        #operand = self.instruction // 2 ** 11
        #index_register = (self.instruction // 2 ** 8) % 2 ** 2
        #mode = (self.instruction // 2 ** 10) % 2 ** 1
        #general_register = (self.instruction // 2 ** 6) % 2 ** 2
        return opcode, operand, index_register, mode, general_register

class IndexRegister(Register):
    pass


class GeneralRegister(Register):
    pass

#for testing purposes
def main():
    m = MAR()
    print(m.get_val())


if __name__ == '__main__':
    main()
