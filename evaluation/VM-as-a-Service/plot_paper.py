import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("./cpu_usage_1024/CPUUsage_statistics.csv")
df = df.iloc[1:]

df2 = pd.read_csv("./ram_usage_1024/RAMUsage_statistics.csv")
df2 = df2.iloc[1:]

x_label = df.columns[0]
y_label = df.columns[1]
std_label = df.columns[2]

x2_label = df2.columns[0]
y2_label = df2.columns[1]
std2_label = df2.columns[2]

plt.plot(df[x_label], df[y_label], linestyle='-', color='b', label="CPU Usage")
plt.plot(df2[x2_label], df2[y2_label], linestyle='-', color='r', label="RAM Usage")

z = 1.96
n = 15
err = []
err2 = []

std = df[std_label].to_numpy()
std2 = df2[std2_label].to_numpy()

for elem in std:
    x = (abs(elem/np.sqrt(n)))*z
    err.append(x)

for elem in std2:
    x = (abs(elem/np.sqrt(n)))*z
    err2.append(x)

errp = []
errn = []
mean = df[y_label].to_numpy()

print(err2)

errp2 = []
errn2 = []
mean2 = df2[y2_label].to_numpy()

for i in range(len(err)):
    errp.append(mean[i] + err[i])
    errn.append(mean[i] - err[i])

for i in range(len(err2)):
    errp2.append(mean2[i] + err2[i])
    errn2.append(mean2[i] - err2[i])


plt.plot(df2[x_label], errp2, color='r', alpha=0.20, label = 'upper and lower bound, I.C. 95%')
plt.plot(df2[x_label], errn2, color='r', alpha=0.20, label = '')

plt.plot(df[x_label], errp, color='b', alpha=0.20, label = 'upper and lower bound, I.C. 95%')
plt.plot(df[x_label], errn, color='b', alpha=0.20, label = '')

plt.fill_between(df2[x_label], errp2, errn2, color="r", alpha=0.15)
plt.fill_between(df[x_label], errp, errn, color="b", alpha=0.15)

plt.title("CPU and RAM Usage in Honeyfarm Deployments (1 GB RAM per VM)")
plt.xlim(1,11)
plt.ylim(0,100)
plt.xlabel("Number of VMs")
plt.ylabel("% of Usage")
plt.grid(True)
plt.legend()
plt.savefig("test.pdf",bbox_inches='tight')
plt.show()



