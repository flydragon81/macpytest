#main.py
import multiprocessing
import time
import numpy as np
from func import writeln
from calc import calc
import scipy.io as sio

def func1(x):
    calc()
    c1=0
    d1=np.zeros(233,int)
    for i in xrange(5):
        d1[c1]=writeln(1,i)
        c1+=1
        #time.sleep(1)
    sio.savemat('11.mat',{'dd':d1})

def func2(x):
    calc()
    c2=0
    d2=np.zeros(233,int)
    for i in xrange(5):
        d2[c2]=writeln(2,i)
        c2+=1
        #time.sleep(1)
    sio.savemat('22.mat',{'dd':d2})

def func3(x):
    calc()
    c3=0
    d3=np.zeros(233,int)
    for i in xrange(5):
        d3[c3]=writeln(3,i)
        c3+=1
        #time.sleep(1)
    sio.savemat('33.mat',{'dd':d3})

def func4(x):
    calc()
    c4=0
    d4=np.zeros(233,int)
    for i in xrange(5):
        d4[c4]=writeln(4,i)
        c4+=1
        #time.sleep(1)
    sio.savemat('44.mat',{'dd':d4})

if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=4)

    pool.apply_async(func1, (1, ))
    pool.apply_async(func2, (2, ))
    pool.apply_async(func3, (3, ))
    pool.apply_async(func4, (4, ))

    pool.close()
    pool.join()


    print "Sub-process(es) done."

#calc.py
def calc():
    x=233
    for i in xrange(1000000000):
        x=x+1
        x=x-1
#func.py
def writeln(x,y):
     aa=x*10+y
     print(aa)
     return(aa)