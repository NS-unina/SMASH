import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("./response_time_2048/ResponseTime_statistics.csv")
df = df.iloc[1:]


x_label = df.columns[0]
y_label = df.columns[1]
std_label = df.columns[2]

plt.plot(df[x_label], df[y_label], linestyle='-', color='b', label="Response Time")



z = 1.96
n = 15
err = []

std = df[std_label].to_numpy()

for elem in std:
    x = (abs(elem/np.sqrt(n)))*z
    err.append(x)

errp = []
errn = []
mean = df[y_label].to_numpy()


for i in range(len(err)):
    errp.append(mean[i] + err[i])
    errn.append(mean[i] - err[i])



plt.plot(df[x_label], errp, color='b', alpha=0.20, label = 'upper and lower bound, I.C. 95%')
plt.plot(df[x_label], errn, color='b', alpha=0.20, label = '')

plt.fill_between(df[x_label], errp, errn, color="b", alpha=0.15)

#plt.title("Response Time in Honeyfarm Deployments (2 GB RAM per VM)")
plt.xlim(1,6)
plt.ylim(0,200)
plt.xlabel("Time (s)")
plt.ylabel("% of Usage")
plt.grid(True)
plt.legend()
plt.savefig("test.pdf",bbox_inches='tight')

plt.show()



