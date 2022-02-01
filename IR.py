class IR:
    instruction = None
    def __init__(self, instruction=None):
        self.instruction = instruction
    
    def set_instruction(self,instruction):
        self.instruction = instruction

    # def get_instruction(self, instruction):
    #     return self.instructions

    #returns opcode, operand, registers to use, indirect/direct mode, etc
    def decode(self):

        #process self.instruciton
        opcode = 0
        operand = 0
        index_register = 0
        mode = 0
        general_register = 0
        return opcode, operand, index_register, mode, general_register
