from multiprocessing.managers import BaseManager
import sys
import multiprocessing
from CPU import CPU
class MathsClass:
    def __init__(self):
        self.id = 0
    def add(self, x, y):
        return x + y
    def mul(self, x, y):
        return x * y
    def set_id(self,id):
        self.id = id
    def get_id(self):
        return self.id

class Test:

    def __init__(self):
        self.MathsClass = MathsClass()
    
    def set_id(self, id):
        self.MathsClass.id = id
    
    def get_id(self):
        return self.MathsClass.id

class MyManager(BaseManager):
    pass

MyManager.register('Test', Test)

def run(m):
    print('setting id')
    m.set_id(-3)

if __name__ == '__main__':
    with MyManager() as manager:
        test = manager.Test()
        p = multiprocessing.Process(target = test.set_id, args=(-4,))
        p.start()
        p.join()
        print(test.get_id())
        #cpu.GRs[0].set_val(5)
     
        