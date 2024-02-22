from random import randint
import subprocess

IP=["10.1.3.10",
"10.1.3.11",
"10.1.3.12",
"10.1.3.13",
"10.1.3.14",
"10.1.3.15",
"10.1.3.16",
"10.1.3.17",
"10.1.3.18",
"10.1.3.19",
"10.1.3.20",
"10.1.3.21",
"10.1.3.22"]

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
