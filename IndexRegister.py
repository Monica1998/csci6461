from converter import decimal_to_binary
class IndexRegister:
    def __init__(self,val=0):
        self.val = val

    def get_val(self):
        return decimal_to_binary(self.val)

    def set_val(self,val):
        self.val = val

#For testing purposes
def main():
    ir = IndexRegister(5);
    print(ir.get_val())
    ir.set_val(3)
    print(ir.val)
    print(ir.get_val())
    print(len(ir.get_val()))


if __name__== '__main__':
    main()