#!/usr/bin/python
import os
import commands
import sys
import re
import operator


def split_line(l):
    tokens = re.split('\s+', l)
    return tokens

def archivos():
    from subprocess import call, PIPE, Popen
    memtotal = 0
    #call("clear")
    proceso = Popen(['free', '-m'], stdout=PIPE, stderr=PIPE)
    memoria = proceso.stdout.readlines()
    for linea in memoria:
        tokens = split_line(linea)
        if tokens[0] == "Mem:":
            memtotal = tokens[1]
        #linea2=linea.lstrip()
    proceso.stdout.close()
    return memtotal

def total_libre():
    from subprocess import call, PIPE, Popen
    memtotal = 0
    #call("clear")
    proceso = Popen(['free', '-m'], stdout = PIPE, stderr = PIPE)
    memoria = proceso.stdout.readlines()
    for linea in memoria:
        tokens = split_line(linea)
        #print tokens
        if tokens[0] == "Mem:":
            total_l = float(tokens[3]) + float(tokens[6])
    porcentaje = (total_l * 100 ) / float(archivos())
    proceso.stdout.close()
    print("% RAM LIBRE")
    print ("%.2f" % porcentaje)

def checkmem():
    total = commands.getoutput('free -m|grep Mem:|tr -s "'" "'" |cut -d "'" "'" -f 2')
    return total

def top_five():
    from subprocess import call, PIPE, Popen
    p1 = Popen(["ps", "aux", "--sort", "pmem"], stdout=PIPE)
    p2 = Popen(["tail", "-5"], stdin=p1.stdout, stdout=PIPE)
    p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    complete = p2.communicate()[0]
    topcinco = complete.splitlines()
    print("TOP 5 PROCESOS QUE CONSUMEN RAM")
    print("user    PID   %Mem  Process")
    for x in topcinco:
        top5 = split_line(x)
        print(top5[0] + " " + top5[1] + " " + top5[3] + " " + top5[10])

def disk_performance(device):
    #print(device)
    from subprocess import PIPE, Popen
    disco_perf = Popen(["hdparm", "-tT", device], stdout = PIPE, stderr = PIPE)
    disco_perf2 = Popen(["grep", "Timing"], stdin=disco_perf.stdout, stdout=PIPE)
    disco_perf.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    output = disco_perf2.communicate()[0]
    disk = output.splitlines()
    print("CACHE READS")
    for y in disk:
        x = split_line(y)
        if x[2] == "cached":
            print(x[10] + " MB/sec")
        else:
            print("BUFFERED")
            print(x[11] + " MB/sec")

mem = checkmem()
#call("clear")


def load_average():
    from subprocess import call, PIPE, Popen
    l1 = Popen(['uptime'], stdout = PIPE, stderr = PIPE)
    la = l1.stdout.readlines()
    print("LOAD AVERAGE")
    for x in la:
        loadavg = split_line(x)
        if loadavg[7] == "average:":
            print(loadavg[8].strip(",") + " " + loadavg[9].strip(",") + " " + loadavg[10].strip(","))
        #print(loadavg[10].strip(","))

def total_swap():
    from subprocess import call, PIPE, Popen
    swaptotal = 0
    #call("clear")
    proceso = Popen(['free', '-m'], stdout = PIPE, stderr = PIPE)
    memoria = proceso.stdout.readlines()
    for linea in memoria:
        tokens = split_line(linea)
        #print tokens
        if tokens[0] == "Swap:":
            #print(tokens[4])
            pswap = (float(tokens[3]) * 100) / float(tokens[1])
    #porcentaje = (total_l * 100 ) / float(archivos())
    proceso.stdout.close()
    print("% SWAP LIBRE")
    print ("%.2f" % pswap)

disk_performance(sys.argv[1])
archivos()
total_libre()

from subprocess import call, PIPE, Popen
p1 = Popen(["sar", "1", "2"], stdout=PIPE)
p2 = Popen(["grep", "Ave"], stdin=p1.stdout, stdout=PIPE)
p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
output = p2.communicate()[0]
tokens = split_line(output)
#print output
print("promedio % procesador libre")
print tokens[7]
p2.stdout.close()

#from subprocess import call, PIPE, Popen
p1 = Popen(["sar", "-w", "1", "2"], stdout=PIPE)
p2 = Popen(["grep", "Ave"], stdin=p1.stdout, stdout=PIPE)
p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
output = p2.communicate()[0]
tokens = split_line(output)
#print output
print("PROMEDIO CONTEXT SWITCH")
print tokens[2]


top_five()
load_average()
total_swap()
