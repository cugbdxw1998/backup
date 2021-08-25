from random import Random
import matplotlib.pyplot as plt

from random_walk import Randomwalk

#创建一个randomwalk实例
while True:
    rw =Randomwalk()
    rw.fill_walk()
#将所有的点都绘制出来
    plt.style.use('classic')
    fig,ax=plt.subplots()
    ax.scatter(rw.x_values,rw.y_values,s=15)
    plt.show()

    keeprunning =input("make another work?(y/n)")
    if keeprunning == "n":
        break
    





