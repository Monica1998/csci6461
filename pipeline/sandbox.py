from multiprocessing.managers import BaseManager
import sys
sys.path.append('/Users/vishesh.javangula@ibm.com/Documents/Computer_Architecture/proj_1_4641')
import multiprocessing
from CPU import CPU
import os
import time


def test():
    print('hello world')


class Test:
    def get_id(self):
        print('3')

class MathsClass:
        def __init__(self, id):
            self.test = Test()
            
        
        def show(self):
            self.test.get_id()

        def add(self, x, y):
            #time.sleep(10)
            print(x+y)
            print('current process id = {}'.format(os.getpid()))
            
            return x + y
        def mul(self, x, y,):
            print('current process id = {}'.format(os.getpid()))
            #time.sleep(5)
            print(x*y)
            
            return x * y

class MyManager(BaseManager):
    pass

MyManager.register('Maths', MathsClass)

    #code = multiprocessing.Value('i', 0) #shared code stop all proccesses


def main():



    with MyManager() as manager:
     
        maths = manager.Maths(4)
        procs = []
        p1 = multiprocessing.Process(target=maths.add, args=(1,2,))
        procs.append(p1)
        p2 = multiprocessing.Process(target=maths.mul, args=(3,4,))
        procs.append(p2)
        p1.start()
        print('p1 pid = {}'.format(p1.pid))
        p1.join()
        print('p1 is done')
        time.sleep(10)
        p2.start()
        print('p2 pid = {}'.format(p2.pid))
        
        p1.join()
        p2.join()
        

if __name__ == '__main__':
    main()

    #code = multiprocessing.Value('i', 0) #shared code stop all proccesses

    
        