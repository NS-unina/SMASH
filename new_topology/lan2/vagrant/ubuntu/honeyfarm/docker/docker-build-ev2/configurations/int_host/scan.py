from random import randint
import subprocess

IP=["10.2.3.10",
"10.2.3.11",
"10.2.3.12",
"10.2.3.13",
"10.2.3.14",
"10.2.3.15",
"10.2.3.16",
"10.2.3.17",
"10.2.3.18",
"10.2.3.19",
"10.2.3.20",
"10.2.3.21",
"10.2.3.22",
"10.2.3.23",
"10.2.3.24",
"10.2.3.25",
"10.2.3.26",
"10.2.3.27",
"10.2.3.28",
"10.2.3.29",
"10.2.3.30"]

t = []
i = 0
while len(t) < len(IP):
    x = randint(0, len(IP) - 1)
    z = t.count(IP[x])
    if z > 0:
        pass
    else:
        t.append(IP[x])
        arg = IP[x]
        n = str(i)
        subprocess.check_call(['./check.sh', arg, n])
        i = i + 1
