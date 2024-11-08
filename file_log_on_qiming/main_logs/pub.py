import matplotlib.pyplot as plt

x=[2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023]
y=[13,19,22,27,38,39,46,51,55,53,52,41,65]
x_pos = range(len(x))  
  
plt.plot(x_pos, y)  
  
# 设置x轴的刻度标签为原始的x值  
plt.xticks(x_pos, x)  
for i, count in enumerate(y):  
    plt.text(i, count, str(count), ha='center', va='bottom')
plt.xlabel('Year')  
plt.ylabel('Number')
plt.savefig('pub.png') 