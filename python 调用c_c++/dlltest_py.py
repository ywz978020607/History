from ctypes import *
#dll = cdll.LoadLibrary('dlltest.dll')  #c
# dll = cdll.LoadLibrary('dlltest2.dll')  #cpp

#.so
dll = CDLL("./dlltest2.so")

a=dll.Double(123)
print(type(a))
print(a)

f1 = 3.5
f2 = 5.6
##若非int，必须声明类型
dll.floatAdd.argtypes=[c_float,c_float]
dll.floatAdd.restype = c_float
b = dll.floatAdd(c_float(f1),c_float(f2))
print(type(b))
print(b)


##若非int，必须声明类型
dll.doubleAdd.argtypes=[c_double,c_double]
dll.doubleAdd.restype = c_double
b = dll.doubleAdd(c_double(f1),c_double(f2))
print(type(b))
print(b)

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


#numpy
pyarray = [1,2,3,4,5,6,7,8]

pyarray = np.array(pyarray,dtype=c_double)  #c_double在numpy里自动变float64

carray = (c_double*len(pyarray))(*pyarray)
dll.double_selfadd1.restype = POINTER(c_double)
result=dll.double_selfadd1(carray,len(pyarray))
print(result[0])