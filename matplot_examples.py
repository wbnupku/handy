# 更多的例子参照 网页https://www.tutorialspoint.com/matplotlib/matplotlib_twin_axes.htm

r“”“
知识点:

  1. 左右都有不同的用y轴，叫做twin axes
  2. 设定图像展示的x, y坐标范围， 参见：https://stackabuse.com/how-to-set-axis-range-xlim-ylim-in-matplotlib
    * 可以用plt.xlim([lower, upper]), 或者ax.set_xlim([lower_upper])
    * y对应的是plt.ylim, ax.set_ylim
     
”“”

# 像矩阵一样画子图， 2行2列（2， 2）的子图
import matplotlib.pyplot as plt
fig,a =  plt.subplots(2,2)
import numpy as np
x = np.arange(1,5)
a[0][0].plot(x,x*x)
a[0][0].set_title('square')
a[0][1].plot(x,np.sqrt(x))
a[0][1].set_title('square root')
a[1][0].plot(x,np.exp(x))
a[1][0].set_title('exp')
a[1][1].plot(x,np.log10(x))
a[1][1].set_title('log')
plt.show()
