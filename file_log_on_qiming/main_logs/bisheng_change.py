import matplotlib.pyplot as plt

y=[41.075,41.733,41.549,41.776,41.882,41.427]
x=["GNU","Bisheng-2.1.0","Bisheng-2.4.0","Bisheng-2.5.0","Bisheng-3.1.0","bisheng-4.0.0"]
x_pos = range(len(x))  
  
plt.bar(x_pos, y)  
  
# 设置x轴的刻度标签为原始的x值  
plt.xticks(x_pos, x,rotation=45,fontsize=6)  
for i, count in enumerate(y):  
    plt.text(i, count, str(count), ha='center', va='bottom')
plt.ylabel('steps/s') 
plt.title("core=128")
plt.savefig('bisheng_change.png') 