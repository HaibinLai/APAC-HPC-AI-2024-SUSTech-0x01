import matplotlib.pyplot as plt

x=[32,64,128]
y=[18.050,34.856,84.520]
x_pos = range(len(x))  
  
plt.bar(x_pos, y)  
  
# 设置x轴的刻度标签为原始的x值  
plt.xticks(x_pos, x)  
for i, count in enumerate(y):  
    plt.text(i, count, str(count), ha='center', va='bottom')
plt.xlabel('Number of cores')  
plt.ylabel('steps/s')
plt.savefig('AMD-base.png') 