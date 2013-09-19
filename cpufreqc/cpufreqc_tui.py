#!/usr/bin/env python2

import urwid
import sys
import os
from libs.cpu import determineNumberOfCPUs
from libs.cpu import Cpu
from libs.cpu import NoBackend


class Ui(object):
    __PALETTE = [('header', 'white', 'black'),
               ('reveal focus', 'black', 'dark cyan', 'standout'),]
    def __init__(self, ):
        rb_list=[]
        sw_list=[]
        self._cpus=[]
        for c in range(determineNumberOfCPUs()):
            try:
                self._cpus.append(Cpu(c))
            except NoBackend:
                sys.stderr.write("You must install cpupower or cpufrequtils\n")
                exit()
        #state stuff:
        state= list(set([cpu.get_governor_info() for cpu in self._cpus]))
        if len(state)!=1:
            state = None
        elif state[0]!='userspace':
            state=state[0]
        else:
            state = list(set([cpu.get_frequency_info() for cpu in self._cpus]))
            if len(state)!=1:
                state=None
            else:
                state=state[0]

        #radiobutton stuff:
        sw_list.append(urwid.Text("Governors:"))
        for g in self._cpus[0].get_governors():
            if g=="userspace":
                continue
            elif g==state:
                sw_list.append(urwid.RadioButton(rb_list,g,
                                                 state=True,
                                                 on_state_change=self.__buttoncallback,
                                                 user_data=g,
                                                 ))
            else:
                sw_list.append(urwid.RadioButton(rb_list,g,
                                                 state=False,
                                                 on_state_change=self.__buttoncallback,
                                                 user_data=g,
                                                 ))
        sw_list.append(urwid.Text("Frequences:"))
        for f in self._cpus[0].get_frequences():
            if g=="userspace":
                continue
            elif f==state:
                sw_list.append(urwid.RadioButton(rb_list,"%i Mhz" % (f/1000),
                                                 state=True,
                                                 on_state_change=self.__buttoncallback,

                                                 ))
            else:
                sw_list.append(urwid.RadioButton(rb_list,"%i Mhz" % (f/1000),
                                                 state=False,
                                                 on_state_change=self.__buttoncallback,
                                                 user_data=f,
                                                 ))

        #urwid stuff:
        content = urwid.SimpleListWalker([
                urwid.AttrMap(w, None, 'reveal focus') for w in sw_list
                ])
        listbox = urwid.ListBox(content)
        self.__cpumonitor = urwid.Text("", wrap='clip')
        head = urwid.AttrMap(self.__cpumonitor, 'header')
        top = urwid.Frame(listbox, head)
        self.__loop = urwid.MainLoop(top, self.__PALETTE,
                                     # input_filter=self.__show_all_input,
                                     unhandled_input=self.__exit_on_cr,
                                     )
    def __watchcpu(self,loop,user_data):
        label=[]
        for c in self._cpus:
            label.append("cpu%i: %iMhz" % (c.cpunumber, c.get_frequency_info()/1000))
        self.__cpumonitor.set_text(' '.join(label))
        self.__loop.set_alarm_in(2.0,self.__watchcpu)

    def run(self):
        self.__loop.set_alarm_in(0.5,self.__watchcpu)
        self.__loop.run()

    def __buttoncallback(self,rbutton, state, *user_data):
        if not state or not user_data:
            return False

        if type(user_data[0])==type(int()):
            functmp=lambda c: c.set_frequency(user_data[0])
        else:
            functmp=lambda c: c.set_governor(user_data[0])
        for c in self._cpus:
            functmp(c)
        return True

    def __exit_on_cr(self, input):
        if input in ['q','Q','esc']:
            raise urwid.ExitMainLoop()

    def __show_all_input(self, input, raw):
        self.__show_key.set_text("Pressed: " + " ".join([
                    unicode(i) for i in input]))
        return input

def main():
    if os.geteuid() != 0:
        print "You must be root to run this program."
        sys.exit(1)
    ui=Ui()
    ui.run()

if __name__ == '__main__':
    main()
