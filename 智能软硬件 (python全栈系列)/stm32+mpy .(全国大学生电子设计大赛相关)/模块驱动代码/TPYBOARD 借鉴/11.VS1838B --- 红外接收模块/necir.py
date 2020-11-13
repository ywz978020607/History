# NEC Infrared capture module for MicroPython board
#
# Connect TL1838 receiver to X4
# (That's a 38kHz IR receiver, as shipped on eBay)
#
# See http://www.sbprojects.com/knowledge/ir/nec.php
#
# 2015-04-27 Initial draft
#    Matt Page / mattmatic@hotmail.com


# Usage:
#    def nec_cb(nec, a, c, r)
#        print(a, c, r)				# Address, Command, Repeat
#
#    from necir import NecIr
#    nec = NecIr()
#    nec.callback(nec_cb)

import pyb

class NecIr:
    def __init__(self, timer=2, channel=4, pin=pyb.Pin.board.X4):
        self._t = pyb.Timer(timer, prescaler=83, period=0x0fffffff)
        self._ic_pin = pin
        self._ic = self._t.channel(channel, pyb.Timer.IC, pin=self._ic_pin, polarity=pyb.Timer.BOTH)
        self._ic_start = 0
        self._ic_width = 0
        self._ic.callback(self._ic_cb)
        self._sr = [0,0,0,0]
        self._rst()
        self._address = 0
        self._command = 0
        self._cb = None
        
    def _rst(self):
        self._sr[0] = 0
        self._sr[1] = 0
        self._sr[2] = 0
        self._sr[3] = 0
        self._sc = 0
        self._sb = 0
        
    def _bit(self, v):
        self._sr[self._sb] = (self._sr[self._sb] >> 1) + v
        self._sc = self._sc + 1
        if (self._sc > 7):
            self._sc = 0
            self._sb = self._sb + 1
            if (self._sb > 3):
                if ((self._sr[0] ^ self._sr[1] ^ self._sr[2] ^ self._sr[3])==0):
                    self._address = self._sr[0]
                    self._command = self._sr[2]
                    if (self._cb):
                        self._cb(self, self._address, self._command, False) # Contains the address & command
                self._rst()
            
    def _ic_cb(self, timer):
        if self._ic_pin.value():
            # Rising edge
            self._ic_start = self._ic.capture()
        else:
            # Falling edge
            icw = self._ic.capture() - self._ic_start & 0x0fffffff
            self._ic_width = icw
            if (icw > 5000):
                # print('[gap]') # gap in transmission
                pass
            elif (icw > 4000):
                #print('IR start')
                self._rst()
            elif (icw > 2000): # Repeat command
                #print('IR repeat')
                if (self._cb):
                    self._cb(self, self._address, self._command, True)
            elif (icw > 1500):
                self._bit(0x80)	# High bit
            else:
                self._bit(0x00) # Low bit
            
        # print(self._ic_start, self._ic_width)
	
    def callback(self, fn):
        self._cb = fn