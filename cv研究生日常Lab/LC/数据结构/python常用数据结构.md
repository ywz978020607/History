# python中的常用数据结构技巧



列表/栈: 原生数组

a=[1,3,4,5]

a.append(6)

a.pop() #退6

也可以实现其他，如左进左出

m.insert(0,-10) #左插入-10

m.pop(0) #退出索引0处(第一个)值  等同于 del m[0]

sorted(m) #返回升序，原数组不变

sorted(m,reverse=True) #返回降序，原数组不变

a.remove(val)

a.index(val) #返回第一个值对应的索引

a.count(val) #数量



队列: collections.deque([])

import collections

a = collections.deque([0,3,5,6])

a.popleft()



字典按值排序

d = {}

d['a']=0

d['b']=1

d['c']=3

sorted(d.items(), key=lambda kv:kv[1])  #升序 返回[('a', 0), ('b', 1), ('c', 3)] 

sorted(d.items(), key=lambda kv:kv[1],reverse=True)  #降序

d.pop('a')  #删除字典中的一项

del d['a'] #删除字典中的一项



## 创建二维数组

matrix = [[0]*cols for i in range(rows)] #切记不能用[ [0] *cols] *rows 



## 字符和ascii转换

ord('b')  #98

chr(98) #'b'