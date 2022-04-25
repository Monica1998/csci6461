from audioop import mul
import multiprocessing
from Fetch import run
import time
from CPU_pipeline import CPU


def main():
    
    #init buffers
    IF_ID = multiprocessing.Queue()
    ID_EXE = multiprocessing.Queue()
    EXE_MEM = multiprocessing.Queue()
    MEM_WB = multiprocessing.Queue()

    code = multiprocessing.Value('i', 0)

    class MyManager(BaseManager):
        pass

    MyManager.register('CPU', CPU)    
    with MyManager() as manager:
        cpu = manager.CPU()
        p1 = multiprocessing.Process(target=cpu.fetch, args=(IF_ID,))
        p2 = multiprocessing.Process(target=cpu.decode, args=(IF_ID, ID_EXE,))
        p3 = multiprocessing.Process(target=cpu.execute, args=(ID_EXE, EXE_MEM,))
        p4 = multiprocessing.Process(target=cpu.mem, args=(EXE_MEM, MEM_WB,))
        p5 = multiprocessing.Process(target=cpu.wb, args=(MEM_WB,))

        p1.start()
        p2.start()
        p3.start()
        p4.start()
        p5.start()

        p1.join()
        p2.join()
        p3.join()
        p4.join()
        p5.join()

        
if __name__ == '__main__':
    main()