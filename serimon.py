#!/usr/bin/env python

import serial
import thread
import time
import npyscreen
import curses
import sys
import argparse

serial_port='/dev/ttyAMA0'
baud_rate=19200

def monitor(port, form):
    while True:
        time.sleep(.3)
        line = port.readline()
        if line:
            form.add_line('>>' + line)
            

class SendText(npyscreen.TitleText):

    def __init__(self, *args, **keywords):
        super(SendText, self).__init__(*args, **keywords)
        self.entry_widget.handlers.update({curses.ascii.NL: self.on_enter,
                                           '^P': self.on_ctrl_z,
                                           '^E': self.on_ctrl_e,
                                           curses.KEY_DOWN:   self.on_key_down,
                                           curses.KEY_UP:     self.on_key_up})
        self.history = []
        self.history_index = -1
     
    def add_history(self, line):
        self.history.append(line)
        self.history_index = len(self.history) - 1

    def on_enter(self, a):
        self.parent.send(self.value)
        self.add_history(self.value)
        self.value = ''
        self.display()
    
    def on_ctrl_z(self, a):
        self.parent.send(self.value, chr(26))
        self.add_history(self.value)
        self.value = ''
        self.display()

    def on_ctrl_e(self, e):
        self.parent.send(self.value, chr(27))
        self.add_history(self.value)
        self.value = ''
        self.display()

        
    def on_key_up(self,a):
        if self.history_index >= 0:
            self.value = self.history[self.history_index]
            self.display()
        if self.history_index > 0:
            self.history_index -= 1
        elif self.history_index < 0:
            self.history_index = len(self.history) - 1
        
    
    def on_key_down(self, a):
        if self.history_index >= 0:
            self.value = self.history[self.history_index]
            self.display()       
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
        elif self.history_index < 0:
            self.history_index = len(self.history) - 1
        
    


class MainForm(npyscreen.Form):
    
    
    def __init__(self, *args, **keywords):
        super(MainForm, self).__init__(*args, **keywords)
        self.t = self.add(SendText, name='Send', value='')
        self.ml = self.add(npyscreen.MultiLineEdit, value = '', editable=False)
        self.out = []

    def send(self, load, terminator='\r'):
        port.write(load + terminator)
        self.add_line('>' + load)

    def add_line(self, line):
        if len(self.out) < 20:
            self.out.append(line)
        else:
            self.out = self.out[1:]
            self.out.append(line)
        
        self.ml.value = '\n'.join(self.out) 
        self.ml.display()
        

class TestApp(npyscreen.NPSApp):

    def __ini__(self, *args, **keywords):
        super(TestApp, self).__init__(*args, **keywords)
        self.handlers.update({'^Z': None})


    def main(self):
        main_form  = MainForm(name = "Serial Monitor",)
        thread.start_new_thread(monitor, (port, main_form))

        main_form.edit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', help='serial port name/path', default=serial_port)    
    parser.add_argument('--rate', help='baud rate', default=baud_rate)
    args = parser.parse_args()
    if args.port:
        serial_port = args.port
    if args.rate:
        baud_rate = args.rate
    port = serial.Serial(serial_port, 19200, timeout=.3)
    App = TestApp()
    App.run()
    port.close()

