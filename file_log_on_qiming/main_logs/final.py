import matplotlib.pyplot as plt
import numpy as np
x=[32,64,128,258,512]
y1=[20.143,32.284,41.075,80.173,142.822] #baseline
y2=[15.96,20.17,42.14,80.36,144.54] #opt
p1=[i/y1[0] for i in y1]
p2=[i/y1[0] for i in y2]
barWidth = 0.2
r1 = range(len(x))  
r2 = [x + barWidth for x in r1] 
centers = [i + barWidth / 2 for i in range(len(x))] 
plt.bar(r1, p1,label="kunpeng 920 baseline",width=barWidth)
plt.bar(r2, p2,label="kunpeng 920 opt",width=barWidth)
for i in range(len(p1)):  
    plt.text(r1[i], p1[i], f"{p1[i]:.2f}", ha='center', va='bottom',fontsize=6) 
    plt.text(r2[i], p2[i], f"{p2[i]:.2f}", ha='center', va='bottom',fontsize=6)
# 设置x轴的刻度标签为原始的x值  
plt.xticks(centers, x) 
plt.xlabel('Number of cores')  
plt.ylabel('Speed Up')
plt.legend(loc="best")
plt.savefig('final2.png') 
