import matplotlib.pyplot as plt
x=[64,128,256,512]
y1=[20.573,40.635,79.009,145.345]
y2=[21.329,39.754,79.58,147.028]
barWidth = 0.2
r1 = range(len(x))  
r2 = [x + barWidth for x in r1] 
centers = [i + barWidth / 2 for i in range(len(x))] 
plt.bar(r1, y1,label="O3",width=barWidth)  
plt.bar(r2, y2,label="Ofast",width=barWidth)
for i in range(len(y1)):  
    plt.text(r1[i], y1[i], str(y1[i]), ha='center', va='bottom',fontsize=5.5) 
    plt.text(r2[i], y2[i], str(y2[i]), ha='center', va='bottom',fontsize=5.5)  
# 设置x轴的刻度标签为原始的x值  
plt.xticks(centers, x) 
plt.xlabel('Number of cores')  
plt.ylabel('steps/s')
plt.legend(loc="best")
plt.savefig('build.png') 
# Ofast+mathlib:[142.127]
# O3:[145.321]