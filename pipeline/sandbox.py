from multiprocessing.managers import BaseManager
import sys
sys.path.append('/Users/vishesh.javangula@ibm.com/Documents/Computer_Architecture/proj_1_4641')
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



class MyManager(BaseManager):
    pass

MyManager.register('CPU', CPU)

def run(m):
    print('setting id')
    m.set_id(-3)

if __name__ == '__main__':
    with MyManager() as manager:
        cpu = manager.CPU()
        #cpu.GRs[0].set_val(5)
        print(cpu.memsize)
        