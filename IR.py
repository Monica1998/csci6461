from converter import hex_to_decimal
class IR:
    instruction = None
    def __init__(self, instruction=None):
        self.instruction = instruction
    
    def set_instruction(self,instruction):
        self.instruction = instruction

    # def get_instruction(self, instruction):
    #     return self.instructions

    #returns opcode, operand, registers to use, indirect/direct mode, etc
    #values should be integers
    def decode(self):
        #instruction = hex_to_decimal(self.instruction)
        #process self.instruciton
        opcode = self.instruction % 2**6 
        operand = self.instruction // 2**11
        index_register = (self.instruction // 2*8) % 2**2
        mode = (self.instruction // 2**10) % 2**1
        general_register = (self.instruction // 2**6) % 2**2
        return opcode, operand, index_register, mode, general_register


#testing decoder
def main():
    ir = IR('004F')
    print(ir.decode())
if __name__ == '__main__':
    main()