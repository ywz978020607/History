from matplotlib import pyplot as plt  
import numpy as np  
from mpl_toolkits.mplot3d import Axes3D  
  
fig = plt.figure()  
ax = Axes3D(fig)  
X = np.arange(-2, 2, 0.1)  
Y = np.arange(-2, 2, 0.1)  
X, Y = np.meshgrid(X, Y)  
Z = X**2 + Y**2  
  
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow')  
plt.show() 
