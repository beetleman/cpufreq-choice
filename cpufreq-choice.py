#!/usr/bin/env python2

import subprocess as sp
import os
import sys


def  determineNumberOfCPUs():
    # POSIX
    try:
        res = int(os.sysconf('SC_NPROCESSORS_ONLN'))

        if res > 0:
                return res
    except (AttributeError,ValueError):
        pass
    # Python 2.6+
    try:
        import multiprocessing
        return multiprocessing.cpu_count()
    except (ImportError,NotImplementedError):
        pass

def set_governor(g, c):
    def tmp():
        for i in xrange(c):
            sp.call(["cpufreq-set", "-c", str(i), "-g", g])
    return tmp

def set_frequency(f, c):
    def tmp():
        for i in xrange(c):
            sp.call(["cpufreq-set", "-c", str(i), "-f", f])
    return tmp
def get_governor():
    governors_f = sp.Popen("find /sys/devices/system/cpu/ -name scaling_available_governors",
                           shell=True,
                           stdout=sp.PIPE).stdout.read().split()[0]
    with  open(governors_f) as f:
        governors = f.read().replace("userspace", "").split()
    return governors

def get_frequency():
    frequency_steps_f = sp.Popen("find /sys/devices/system/cpu/ -name scaling_available_frequencies",
                                 shell=True,
                                 stdout=sp.PIPE).stdout.read().split()[0]
    
    with  open(frequency_steps_f) as f:
        frequency_steps = f.read().split()
    return frequency_steps


if __name__ == '__main__':
    if os.geteuid() != 0:
        print "You must be root to run this program."
        sys.exit(1)
    #take info about governors and frequency
    #TODO:
    # napisz funkcje do zbierania tego, sprubuj to zrobic poprzez
    # cpufreutils
    
    

    
    cpu_count = determineNumberOfCPUs()
    
    command = []
        
    for g in get_governor():
        command.append([g ,
                       set_governor(g,cpu_count)
                        ])
    for f in get_frequency():
        command.append([str(int(f)/1000.0)+" Mhz",
                        set_frequency(f,cpu_count)
                        ])
                       
    print "Available frequency_steps/cpufreq_governors: "
    for i in xrange(len(command)):
        print "\t%i)" % (i+1), command[i][0]
    print "\tother)", "Quit"
    choice = raw_input("select: ")
    try:
        choice = int(choice)
    except :
        sys.exit()
    
    if choice in xrange(1,len(command)+1):
        command[choice-1][1]() #choice
    else:
        sys.exit()

    

    
