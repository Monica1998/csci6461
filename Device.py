class Device:

    def __init__(self):
        self.printer = 0
        self.keyboard = list()

    def set_keyboard(self, val):
        if isinstance(val,str):
            val = ord(val)
        self.keyboard.append(val)

    def get_keyboard(self):
        if len(self.keyboard) != 0:
            return self.keyboard.pop(0)

    def set_printer(self, val):
        self.printer = val

    def get_printer(self):
        return self.printer

if __name__ == '__main__':
    d = Device()
    d.set_keyboard(5)
    d.set_keyboard('a')
    print(d.get_keyboard())
    print(d.get_keyboard())
