from audioop import mul
import multiprocessing
from Fetch import run
import time
import sys
sys.path.append('/Users/vishesh.javangula@ibm.com/Documents/Computer_Architecture/proj_1_4641')
from CPU_pipeline import CPU
from multiprocessing.managers import BaseManager


 #init buffers
IF_ID = multiprocessing.Queue()
ID_EXE = multiprocessing.Queue()
EXE_MEM = multiprocessing.Queue()
MEM_WB = multiprocessing.Queue()

code = multiprocessing.Value('i', 0) #shared code stop all proccesses

class MyManager(BaseManager):
    pass

def main():
    
    MyManager.register('CPU', CPU)    
    with MyManager() as manager:
        cpu = manager.CPU()
        print(cpu.Memory)
        # p1 = multiprocessing.Process(target=cpu.fetch, args=(IF_ID,code, ))
        # p2 = multiprocessing.Process(target=cpu.decode, args=(IF_ID, ID_EXE,code, ))
        # p3 = multiprocessing.Process(target=cpu.execute, args=(ID_EXE, EXE_MEM,code, ))
        # p4 = multiprocessing.Process(target=cpu.mem, args=(EXE_MEM, MEM_WB,code, ))
        # p5 = multiprocessing.Process(target=cpu.wb, args=(MEM_WB,code, ))

        # p1.start()
        # p2.start()
        # p3.start()
        # p4.start()
        # p5.start()

        # #blocks until all processes exit
        # p1.join()
        # p2.join()
        # p3.join()
        # p4.join()
        # p5.join()


if __name__ == '__main__':
    main()