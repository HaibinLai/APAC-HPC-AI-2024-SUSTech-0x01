import matplotlib.pyplot as plt

x=[128,256,512]
y1=[41.075,80.173,142.822]
y2=[41.320,78.593,146.098]
y3=[41.750,80.036,147.342]
y4=[41.761,80.858,147.962]
barWidth = 0.2
r1 = range(len(x))  
r2 = [x + barWidth for x in r1] 
r3 = [x + barWidth for x in r2] 
plt.bar(r1, y1,label="openmpi",width=barWidth)  
plt.bar(r2, y2,label="hmpi",width=barWidth)
plt.bar(r3, y3,label="hmpi_opt",width=barWidth)
for i in range(len(y1)):  
    plt.text(r1[i], y1[i], str(y1[i]), ha='center', va='bottom',fontsize=6) 
    plt.text(r2[i], y2[i], str(y2[i]), ha='center', va='bottom',fontsize=6)  
    plt.text(r3[i], y3[i], str(y3[i]), ha='center', va='bottom',fontsize=6)
# 设置x轴的刻度标签为原始的x值  
plt.xticks(r2, x) 
plt.xlabel('Number of cores')  
plt.ylabel('steps/s')
plt.legend(loc="best")
plt.savefig('hmpi_opt2.png') 
