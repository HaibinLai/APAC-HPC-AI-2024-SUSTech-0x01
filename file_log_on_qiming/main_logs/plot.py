import matplotlib.pyplot as plt

rate=[15.55,2.16,2.07,80.22]
label=["MPI_ALLreduce","MPI_Isend","MPI_Irecv","others"]
color = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
plt.pie(rate, labels=label, colors=color, autopct='%1.1f%%', startangle=140)  
plt.axis('equal') 
plt.title("Top Waiting MPI calls")
plt.savefig('MPI_base.png') 

# outer_rate=[26.63,61.64,7.87,3.86]
# outer_label=["Retiring","Backend Bound","Frontend Bound","Bad Speculation"]
# outer_color = ['gold', 'yellowgreen', 'lightcoral', 'lightskyblue']
# inner_rate=[36.17,25.48]
# inner_label=["Memory Bound","Core Bound"]
# inner_color = ['gold','lightskyblue']
# fig, ax = plt.subplots()
# ax.pie(outer_rate, labels=outer_label, colors=outer_color, autopct='%1.1f%%', startangle=140)  
# ax.set_title("Top-down")
# inner_ax = fig.add_axes([0.6,0.1,0.2,0.2], frameon=True)  # [left, bottom, width, height]  
# inner_ax.pie(inner_rate, labels=inner_label, colors=inner_color, autopct='%1.1f%%', startangle=140) 
# plt.axis('equal') 
# plt.savefig('Top-down_opt.png') 