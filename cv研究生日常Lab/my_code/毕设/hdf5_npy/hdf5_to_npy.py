import h5py
import numpy as np

"PQFLabel_BasketballDrill_832x480_500.npy"
"PQFLabel_BasketballPass_416x240_500_20200312_001345.hdf5"

# check1 = np.load("PQFLabel_BasketballDrill_832x480_500.npy")
# check2 = np.load("PQFLabel_BasketballPass_416x240_500.npy")
#


f = h5py.File("PQFLabel_BasketballPass_416x240_500_20200312_001345.hdf5",'r')   #打开h5文件
# 可以查看所有的主键
shape = f['PQF_label'].shape
data = f['PQF_label'].value

np.save('PQFLabel_BasketballPass_416x240_500.npy',data)

pass

