import matplotlib.pyplot as plt
import os

def timescanplot(filename, location):
    os.chdir(location)
    f = open(filename)

    datas = []
    for line in f:
        if not line[0] == "#" and not line == "\n":
            a = line.split()
            datas.append(a)
            if line.strip() == "ALL:":
                break
    f.close()
    del datas[-1]
    no_of_mass = len(datas[0])-2

    d = {}
    for i in range(no_of_mass):
        d["mass_#{0}".format(i)] = []

    for i in range(len(d)):
        d['mass_#{}'.format(i)] = [j[i+1] for j in datas]
        d['mass_#{}'.format(i)] = [float(j) for j in d['mass_#{}'.format(i)]]

    time = [i[0] for i in datas]
    time = [float(i) for i in time]

    for i in range(no_of_mass):
        plt.scatter(time, d['mass_#{}'.format(i)])
        plt.plot(time, d['mass_#{}'.format(i)], label = "mass_#{}".format(i))
        
    plt.xlabel("Time (ms)")
    plt.ylabel("Ion Counts")
    plt.legend()
    plt.show()
    plt.close()