import subprocess as sp
import os
from utils import which


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


class Cpu_backed(object):
    NAME = "Name"
    CMD = "command"
    def cmd_maker(self, **options):
        tmp = [which(self.CMD)]
        for o in options.keys():
            tmp.append('-%s' % (o))
            tmp.append(str(options[o]))
        return tmp

    def __call__(self, c=None, **options):
        cmd =  self.cmd_maker(c=c,**options)
        sp.call(cmd)

    def is_available(self):
        if which(self.CMD):
            return True
        else:
            return False

    def __str__(self):
        return str(self.NAME)

class Cpu_cpupower(Cpu_backed):
    NAME = 'cpupower'
    CMD = 'cpupower'
    def cmd_maker(self, **options):
        tmp = [which(self.CMD)]
        if 'c' in options.keys():
            tmp.extend(["-c",
                        str(options["c"])])
        tmp.append('frequency-set')
        for o in options.keys():
            if o!='c':
                tmp.append('-%s' % (o))
                tmp.append(str(options[o]))

        return tmp

class Cpu_cpufrequtils(Cpu_backed):
    NAME = 'cpufrequtils'
    CMD = 'cpufreq-set'



class Cpu(object):
    _CPUDIRSPATERN = "/sys/devices/system/cpu/cpu%i/cpufreq/"
    BACKEDS = [Cpu_cpupower,Cpu_cpufrequtils]
    def __init__(self, number):
        assert type(number)==type(int())
        assert os.path.exists(self._CPUDIRSPATERN % number)
        self.__cpudir=self._CPUDIRSPATERN % number
        self.cpunumber=number
        self._cmd = self.get_backed()

    def get_backed(self):
        for b in self.BACKEDS:
            backend = b()
            if backend.is_available():
                return backend

    def set_governor(self, gevenor):

        assert gevenor in self.get_governors(), "nie ma takiej polityki!"
        self._cmd(c=self.cpunumber, g=gevenor)

    def set_frequency(self, frequency):

        assert frequency in self.get_frequences(), "nie ma takiej czestotliwosci"
        self._cmd(c=self.cpunumber, f=str(frequency))


    def get_governors(self):
        governors_f = self.__cpudir + "scaling_available_governors"
        with  open(governors_f) as f:
            governors = f.read().split()
        return governors

    def get_frequences(self):
        frequency_f = self.__cpudir + "scaling_available_frequencies"
        with  open(frequency_f) as f:
                frequency = [int(i) for i in f.read().split()]
        return frequency

    def get_frequency_info(self):
        frequency_f = self.__cpudir +  "scaling_cur_freq"
        with  open(frequency_f) as f:
                frequency = int(f.read())
        return frequency

    def get_governor_info(self):
        governors_f = self.__cpudir +  "scaling_governor"
        with  open(governors_f) as f:
                governors = f.read().replace("\n","")
        return governors
