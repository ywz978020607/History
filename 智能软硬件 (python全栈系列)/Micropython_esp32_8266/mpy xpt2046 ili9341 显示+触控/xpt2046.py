# asyncio version
# The MIT License (MIT)
#
# Copyright (c) 2016, 2017 Robert Hammelrath (basic driver)
#               2016 Peter Hinch (asyncio extension)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# Class supporting the resisitve touchpad of TFT LC-displays
#
from time import sleep_ms
from machine import SPI, Pin
# define constants
#
T_GETX  = const(0xd0)  ## 12 bit resolution
T_GETY  = const(0x90)  ## 12 bit resolution
T_GETZ1 = const(0xb8)  ## 8 bit resolution
T_GETZ2 = const(0xc8)  ## 8 bit resolution
#
X_LOW  = const(10)     ## lowest reasonable X value from the touchpad
Y_HIGH = const(4090)   ## highest reasonable Y value

class XPT2046:
#
# Init just sets the PIN's to In / out as required
# async: set True if asynchronous operation intended
# confidence: confidence level - number of consecutive touches with a margin smaller than the given level
#       which the function will sample until it accepts it as a valid touch
# margin: Distance from mean centre at which touches are considered at the same position
# delay: Delay between samples in ms. (n/a if asynchronous)
#
    DEFAULT_CAL = (-3917, -0.127, -3923, -0.1267, -3799, -0.07572, -3738,  -0.07814)

    def __init__(self, spi=None, *, confidence=5, margin=50, delay=10, calibration=None):
        if spi is None:
            raise IOError("The SPI object has to be supplied")
        else:
            self.spi = spi
        self.recv = bytearray(3)
        self.xmit = bytearray(3)
# set default values
        self.ready = False
        self.touched = False
        self.x = 0
        self.y = 0
        self.buf_length = 0
        cal = XPT2046.DEFAULT_CAL if calibration is None else calibration
        self.touch_parameter(confidence, margin, delay, cal)

# set parameters for get_touch()
# res: Resolution in bits of the returned values, default = 10
# confidence: confidence level - number of consecutive touches with a margin smaller than the given level
#       which the function will sample until it accepts it as a valid touch
# margin: Difference from mean centre at which touches are considered at the same position
# delay: Delay between samples in ms.
#
    def touch_parameter(self, confidence=5, margin=50, delay=10, calibration=None):
        confidence = max(min(confidence, 25), 5)
        if confidence != self.buf_length:
            self.buff = [[0,0] for x in range(confidence)]
            self.buf_length = confidence
        self.delay = max(min(delay, 100), 5)
        margin = max(min(margin, 100), 1)
        self.margin = margin * margin # store the square value
        if calibration:
            self.calibration = calibration

# get_touch(): Synchronous use. get a touch value; Parameters:
#
# initital: Wait for a non-touch state before getting a sample.
#           True = Initial wait for a non-touch state
#           False = Do not wait for a release
# wait: Wait for a touch or not?
#       False: Do not wait for a touch and return immediately
#       True: Wait until a touch is pressed.
# raw: Setting whether raw touch coordinates (True) or normalized ones (False) are returned
#      setting the calibration vector to (0, 1, 0, 1, 0, 1, 0, 1) result in a identity mapping
# timeout: Longest time (ms, or None = 1 hr) to wait for a touch or release
#
# Return (x,y) or None
#
    def get_touch(self, *, initial=True, wait=True, raw=False, timeout=None):
        if timeout is None:
            timeout = 3600000 # set timeout to 1 hour
#
        if initial:  ## wait for a non-touch state
            sample = True
            while sample and timeout > 0:
                sample = self.raw_touch()
                sleep_ms(self.delay)
                timeout -= self.delay
            if timeout <= 0: # after timeout, return None
                return None
#
        buff = self.buff
        buf_length = self.buf_length
        buffptr = 0
        nsamples = 0
        while timeout > 0:
            if nsamples == buf_length:
                meanx = sum([c[0] for c in buff]) // buf_length
                meany = sum([c[1] for c in buff]) // buf_length
                dev = sum([(c[0] - meanx)**2 + (c[1] - meany)**2 for c in buff]) / buf_length
                if dev <= self.margin: # got one; compare against the square value
                    if raw:
                        return (meanx, meany)
                    else:
                        return self.do_normalize((meanx, meany))
# get a new value
            sample = self.raw_touch()  # get a touch
            if sample is None:
                if not wait:
                    return None
                nsamples = 0    # Invalidate buff
            else:
                buff[buffptr] = sample # put in buff
                buffptr = (buffptr + 1) % buf_length
                nsamples = min(nsamples + 1, buf_length)
            sleep_ms(self.delay)
            timeout -= self.delay
        return None
#
# do_normalize(touch)
# calculate the screen coordinates from the touch values, using the calibration values
# touch must be the tuple return by get_touch
#
    def do_normalize(self, touch):
        xmul = self.calibration[3] + (self.calibration[1] - self.calibration[3]) * (touch[1] / 4096)
        xadd = self.calibration[2] + (self.calibration[0] - self.calibration[2]) * (touch[1] / 4096)
        ymul = self.calibration[7] + (self.calibration[5] - self.calibration[7]) * (touch[0] / 4096)
        yadd = self.calibration[6] + (self.calibration[4] - self.calibration[6]) * (touch[0] / 4096)
        x = int((touch[0] + xadd) * xmul)
        y = int((touch[1] + yadd) * ymul)
        return (x, y)
#
# raw_touch(tuple)
# raw read touch. Returns (x,y) or None
#
    def raw_touch(self):
        x  = self.touch_talk(T_GETX, 12)
        y  = self.touch_talk(T_GETY, 12)
        if x > X_LOW and y < Y_HIGH:  # touch pressed?
            return (x, y)
        else:
            return None
#
# Send a command to the touch controller and wait for the response
# cmd:  command byte
# bits: expected data size. Reasonable values are 8 and 12
#
    def touch_talk(self, cmd, bits):
        self.xmit[0] = cmd
        self.spi.write_readinto(self.xmit, self.recv)
        return (self.recv[1] * 256 + self.recv[2]) >> (15 - bits)

