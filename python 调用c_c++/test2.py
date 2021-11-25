from ctypes import *
import numpy as np
#dll = cdll.LoadLibrary('dlltest.dll')  #c
# dll = cdll.LoadLibrary('dlltest2.dll')  #cpp

#.so
dll = CDLL("./dlltest2.so")


#########
#一维数组
print ("传递并返回一维数组")
INPUT = c_double * 10
data = INPUT()
for i in range(10):
        data[i] = i*2.0
 
dll.double_selfadd1.restype = POINTER(c_double)
result=dll.double_selfadd1(data,len(data))
print('返回值:a[i]+2.0')
for i in range(10):
    print(result[i])

#二维数组，结构体 : https://blog.csdn.net/qq_31342997/article/details/88374804

pyarray = [1,2,3,4,5,6,7,8]

pyarray = np.array(pyarray,dtype=c_double)  #c_double在numpy里自动变float64

carray = (c_double*len(pyarray))(*pyarray)
dll.double_selfadd1.restype = POINTER(c_double)
result=dll.double_selfadd1(carray,len(pyarray))
print(result[0])
np_result = np.ctypeslib.as_array(result,[5])  #转numpy  共享内存
