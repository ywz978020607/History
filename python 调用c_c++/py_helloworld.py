import ctypes
so = ctypes.CDLL("./libhello.so")
so.test()