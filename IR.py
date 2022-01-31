from converter import decimal_to_binary
class IndexRegister:
    def __init__(self,val=0):
        self.val = val

    def get_value(self):
        return decimal_to_binary(self.val)

    def set_value(self,val):
        self.val = val