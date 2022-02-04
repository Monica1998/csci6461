from converter import decimal_to_binary
class GeneralRegister:
    def __init__(self,val=0):
        self.val = val

    def get_val(self):
        return self.val

    def set_val(self,val):
        self.val = val


#For testing purposes
def main():
    g1 = GeneralRegister(5);
    print(g1.get_val())
    g1.set_val(3)
    print(g1.val)
    print(g1.get_val())


if __name__== '__main__':
    main()