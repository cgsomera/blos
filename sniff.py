#! /usr/bin/env python
from scapy.all import *
#import basico
import commands
import pdb

def limpia():
    z = 0
    arch = open("captura.cap", "w")
    arch.close()

def packet_sniff(pkt):
    arch = open("captura.cap", "a")
    #print("TEST")
    if IP in pkt:
        x = pkt[IP][IP].len
        z = pkt[IP][IP].sport
        c = str(pkt[IP][IP].dst)
        x = str(x)
        z = str(z)
        #print (x)
        a = str(c + "|" + z + "|" + x + "\n")
        #print a
        arch.write(a)
	return
        arch.close


def sniff_read():
    eje_linea = commands.getoutput('> commandpid.txt')
    from subprocess import PIPE, Popen
    lista=[""]
    unicos = commands.getoutput('> unicos.txt')
    arch = open("captura.cap", "r")
    archl = arch.readlines()
    for i in archl:
        j = i.split('|')
        p = j[0]
        x = j[1]
        t = "\"" + str(p) + '|' + str(x) + "\""
        #print t #--- imprime dupla ip puerto
        unicos = commands.getoutput('echo ' + t + ' >> unicos.txt')
    #print unicos
    unicosc = commands.getoutput('cat unicos.txt| sort | uniq > unicosc.txt')
    unicofile = open("unicosc.txt", "r")
    unicoline = unicofile.readlines()
    #print("abrir archivo de unicos")
    #pdb.set_trace()
    for a in unicoline:
        h = 0
        g = a.split('|')
        f = int(g[1])
        #print(f)#------imprime los puertos
        for s in archl:
            d = s.split('|')
            #print d   #imprime los tres elementos
            if f == int(d[1]):
                h += int(d[2])
            #print(h)#----------------ok
        p = (str(g[0]) + '|' + str(g[1]).rstrip('\n') + '|' + str(h))
        #print p
        o = ":" + str(g[1]).rstrip('\n') # Genera el numero de puerto
        #print o
        procesos = Popen(['lsof', '-i', o], stdout = PIPE, stderr = PIPE)
        proc_comm = procesos.stdout.readlines()
        for linea in proc_comm:
            linea_s = linea.split()
            #print linea_s ###### imprime la liena de lsof separada
            if linea_s[0] != "COMMAND":
                linea_tf = linea_s[0] + "|" + linea_s[1]
                #print(linea_tf) ### imprime los comandos y su PID
                #pdb.set_trace()
                eje_linea = commands.getoutput('echo \"' + linea_tf + '\" >> commandpid.txt')
    arch.close()
    eje_linea = commands.getoutput('cat commandpid.txt| sort | uniq > commandpid2.txt')
    eje = commands.getoutput('cat commandpid2.txt')
    print eje
    unicofile.close()

#def obt_procesos():

limpia()
#def principal():
a = sniff(iface = "wlan0", prn = packet_sniff, count = 10) # pasar por argumento NIC
sniff_read()
#basico.total_libre()
