import matplotlib.pyplot as plt

x=[4,8,16,32]
y1=[37.588,79.362,144.439,240.777]
y2=[37.611,79.810,145.779,235.609]
y3=[38.006,80.035,143.056,242.518]
barWidth = 0.2
r1 = range(len(x))  
r2 = [x + barWidth for x in r1] 
r3 = [x + barWidth for x in r2] 
plt.bar(r1, y1,label="baseline",width=barWidth)  
plt.bar(r2, y2,label="Running MPI with HCOLL",width=barWidth)
plt.bar(r3, y3,label="Running OSHMEM with HCOLL",width=barWidth)

# 设置x轴的刻度标签为原始的x值  
plt.xticks(r2, x) 
plt.xlabel('Number of nodes')  
plt.ylabel('steps/s')
plt.legend(loc="best")
plt.savefig('pic_diff1.png') 