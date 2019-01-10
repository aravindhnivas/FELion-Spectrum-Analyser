import matplotlib.pyplot as plt
import os

def timescanplot(filename, location):
    os.chdir(location)
    datas, mass_values, values = [], [], []
    f = open(filename, "r")

    for line in f:
        if not line[0] == "#" and not line == "\n":
            a = line.split()
            datas.append(a)
            if line.strip() == "ALL:":
                del datas[-1]
                break
    no_of_mass = len(datas[0])-2

    f.close()

    f = open(filename, "r")
    for line in f:
        if line.find("#Time")>=0:
            values = line.split()

    for i in range(no_of_mass):
        mass_values.append(values[i+1])
        
    f.close()

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
        plt.plot(time, d['mass_#{}'.format(i)], label = "mass: {}".format(mass_values[i]))

    plt.grid(True)
    plt.xlabel("Time (ms)")
    plt.ylabel("Ion Counts")
    plt.legend()
    plt.title(filename)
    plt.savefig(filename+".png")
    plt.show()
    plt.close()