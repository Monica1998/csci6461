from converter import decimal_to_binary
class GeneralRegister:
    def __init__(self,val=0):
        self.val = val

    def get_val(self):
        return decimal_to_binary(self.val)

    def get_val(self,val):
        self.val = val