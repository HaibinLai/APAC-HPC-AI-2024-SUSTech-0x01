import matplotlib.pyplot as plt

y=[41.883,41.050,41.487,41.504]
x=["openmpi","hmpi-1.1.1","hmpi-1.2.0","hmpi-1.3.1.spc001"]
x_pos = range(len(x))  
  
plt.bar(x_pos, y)  
  
# 设置x轴的刻度标签为原始的x值  
plt.xticks(x_pos, x,fontsize=6)  
for i, count in enumerate(y):  
    plt.text(i, count, str(count), ha='center', va='bottom')
plt.ylabel('steps/s') 
plt.title("core=128")
plt.savefig('mpi_change.png') 