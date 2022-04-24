from converter import binary_string_to_decimal, binary_string_to_hex, decimal_to_binary, hex_to_binary, hex_to_decimal


opdict = {
    0: 'HLT',
    24: 'TRAP',
    1: 'LDR',
    2: 'STR',
    3: 'LDA',
    33: 'LDX',
    34: 'STX',
    8: 'JZ',
    9: 'JNE',
    10: 'JCC',
    11: 'JMA',
    12: 'JSR',
    13: 'RFS',
    14: 'SOB',
    15: 'JGE',
    4: 'AMR',
    5: 'SMR',
    6: 'AIR',
    7: 'SIR',
    16: 'MLT',
    17: 'DVD',
    18: 'TRR',
    19: 'AND',
    20: 'ORR',
    21: 'NOT',
    25: 'SRC',
    26: 'RRC',
    49: 'IN',
    50: 'OUT',
    51: 'CHK',
    27: 'FADD',
    28: 'FSUB',
    29: 'VADD',
    30: 'VSUB',
    31: 'CNVRT',
    40: 'LDFR',
    41: 'STFR'
}

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

#Condition Code to set when arithmetic/logical operations are executed.
class CC(Register):
    pass


#floating point registers, should be 2, each 16-bit in length
class FR(Register):
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
        print('instruction : {}'.format(bits))
        print('opcode = {}, operand = {}, index register = {}, mode = {}, general register = {}'.format(opdict[opcode], operand, index_register, mode, general_register))
        return opcode, operand, index_register, mode, general_register

class IndexRegister(Register):
    pass


class GeneralRegister(Register):
    pass

#for testing purposes
def main():
    ir = IR()
    # with open('Program2.txt', 'r') as f:
    #         lines = f.readlines()
    #         for line in lines:
    #             if line.startswith('#'):
    #                 continue
    #             addr, word = line.split(' ')[:2]
    #             word = hex_to_decimal(word)
    #             ir.set_instruction(word)
    #             ir.decode()
    ir.set_instruction(11042)
    ir.decode()


                


if __name__ == '__main__':
    main()
