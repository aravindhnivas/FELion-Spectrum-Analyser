#!/usr/bin/python3

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
        if line.find("#mass")>=0:
            tmp = line[5:].split(":")
            tmp.append(":")
            tmp = tmp[0].strip()+tmp[-1]+tmp[1].strip()
            mass_values.append(tmp)
        
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
        plt.plot(time, d['mass_#{}'.format(i)], label = mass_values[i])


    #Error bar calculations:
    iterations = [int(i.split(":")[-1]) for i in mass_values]
    start = False
    no_of_times = 0
    raw_datas = []

    f = open(filename, "r")
    for line in f:
        if not line[0]=="#" and not line == "\n":
            line.strip()
            tmp = line.split()
            if tmp[0]=="ALL:":
                start = True
                continue
            if start:
                no_of_times += 1
                raw_datas.append(line.strip())
            total = int(no_of_times/sum(iterations))    
    f.close()

    values = []
    for datas in raw_datas:
        values.append(datas.split())
    values = [[float(i) for i in values[0]] for j in values]

    all_datas = []
    for j in range(sum(iterations)):
        i = j*total
        all_datas.append(values[i:i+total])

    samples = {}
    for i in range(no_of_mass):
        samples["mass_sample_{}".format(i)] = []

    k,l = 0, -1
    for i in iterations:
        l += 1
        for j in range(i):
            samples["mass_sample_{}".format(l)].append(all_datas[k])
            k += 1

    plt.grid(True)
    plt.xlabel("Time (ms)")
    plt.ylabel("Ion Counts")
    plt.legend()
    plt.title(filename)
    plt.savefig(filename+".png")
    plt.show()
    plt.close()