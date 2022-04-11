class Device:

    def __init__(self):
        self.printer = list()
        self.keyboard = list()

    def set_keyboard(self, val):
        if isinstance(val, str):
            for i in range(len(val)):
                self.keyboard.append(ord(val[i]))
        else:
            self.keyboard.append(val)

    def get_keyboard(self):
        if len(self.keyboard) != 0:
            return self.keyboard.pop(0)

    def set_printer(self, val):
        self.printer.append(val)

    def get_printer(self):
        if len(self.printer) != 0:
            return self.printer.pop(0)

if __name__ == '__main__':
    d = Device()
    d.set_keyboard(5)
    d.set_keyboard('a')
    print(d.get_keyboard())
    print(d.get_keyboard())
