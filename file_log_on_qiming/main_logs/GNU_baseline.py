import matplotlib.pyplot as plt

x=[32,64,128,256,512,1024]
y1=[18.050,34.856,84.520,0,0,0]
y2=[20.143,32.284,41.075,80.173,142.822,] # hmpi 8 259.768
barWidth = 0.2
r1 = range(len(x))  
r2 = [x + barWidth for x in r1] 
centers = [i + barWidth / 2 for i in range(len(x))] 
plt.barh(r1, y1,label="AMD_baseline",height=barWidth)  
plt.barh(r2, y2,label="GNU_baseline",height=barWidth)
for i in range(len(y1)):
    if i in [0, 1, 2]:  # 修正了这里的条件判断
        plt.text(y1[i], r1[i], str(y1[i]), ha='left', va='center', fontsize=10)  # 调整了字体大小
    plt.text(y2[i], r2[i], str(y2[i]), ha='left', va='center', fontsize=10) 
# 设置x轴的刻度标签为原始的x值  
plt.yticks(centers, x)
plt.xlabel('steps/s')
plt.ylabel('Number of cores')
plt.title('Performance Comparison')  # 可以添加一个标题
plt.legend()  # 确保图例显示