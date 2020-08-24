######################################
# PID implementation for micropython #
######################################

import utime

# Wrapper class that allows input, output, and setpoint
# to be passed around and modified
class PIDParams:

    # Constructor
    def __init__(self, input, output, setpoint):
        self.input = input
        self.output = output
        self.setpoint = setpoint
        
    
# Controller
class PID:

    # Constants
    SAMPLE_TIME_DEFAULT = 100
    DIRECT = 0
    REVERSE = 1
    OUTPUT_MIN_DEFAULT = 0 # Micropython PWM min
    OUTPUT_MAX_DEFAULT = 1023  # Micropython PWM max
    MANUAL = 0
    AUTOMATIC = 1
    RAW = 0
    FILTERED = 1
    
    # Constructor
    def __init__(self, params, kP, kI, kD, direction = DIRECT, debugEnabled = False):        
        # Set default values
        self.direction = self.DIRECT
        self.kP = 0.0
        self.kI = 0.0
        self.kD = 0.0
        self.inAuto = False
        self.isRaw = True
        self.outputMin = 0
        self.outputMax = 0
        self.pTerm = 0
        self.iTerm = 0
        self.dTerm = 0
        self.history = [0] * 30
        self.lastOutput = 0
        self.computeCount = 0
        self.filterConstant = 0
        
        # Set input values
        self.params = params
        self.debugEnabled = debugEnabled

        # Set output limits
        self.setOutputLimits(self.OUTPUT_MIN_DEFAULT, self.OUTPUT_MAX_DEFAULT)
        
        # Set sample time
        self.sampleTime = self.SAMPLE_TIME_DEFAULT

        # Set direction
        self.setDirection(direction)
        
        # Set tunings
        self.setTunings(kP, kI, kD)

        # Set last time run
        self.lastTime = utime.ticks_diff(utime.ticks_ms(), self.sampleTime)
        
        self.debug("Created")
        self.debug("Sample time " + str(self.sampleTime))
        self.debug("Input " + str(self.params.input))
        self.debug("Output " + str(self.params.output))
        self.debug("Setpoint " + str(self.params.setpoint))
        self.debug("kP " + str(self.kP))
        self.debug("kI " + str(self.kI))
        self.debug("kD " + str(self.kD))
        self.debug("Output min " + str(self.outputMin))
        self.debug("Output max " + str(self.outputMax))
        self.debug("iTerm " + str(self.iTerm))
        self.debug("Last time " + str(self.lastTime))

    # Compute
    def compute(self):
        self.debug("\n###############")
        self.debug("Computing")

        # If not auto, return
        if not self.inAuto:
            self.debug("Return not in auto")
            self.debug("###############\n")
            return False

        now = utime.ticks_ms()
        timeChange = utime.ticks_diff(now, self.lastTime)
        self.debug("Now " + str(now))
        self.debug("Time change " + str(timeChange))

        if timeChange >= self.sampleTime:
            self.computeCount += 1
            
            if self.computeCount == 10:
                for i in range(29, 0, -1):
                    self.history[i] = self.history[i - 1]
                self.history[0] = self.params.input
                self.computeCount = 0

            input = self.params.input
            error = self.params.setpoint - self.params.input
            self.debug("Input " + str(input))
            self.debug("Error " + str(error))

            self.iTerm += (self.kI * error)
            if self.iTerm > self.outputMax:
                self.iTerm = self.outputMax
            elif self.iTerm < self.outputMin:
                self.iTerm = self.outputMin
            self.debug("i Term " + str(self.iTerm))

            dInput = (self.history[0] - self.history[29]) / (5*60);
            self.debug("d Input " + str(dInput))

            self.pTerm = self.kP * error
            self.debug("p Term " + str(self.pTerm))

            self.dTerm = -self.kD * dInput
            self.debug("d Term " + str(self.dTerm))

            output = self.pTerm + self.iTerm + self.dTerm
            if output > self.outputMax:
                output = self.outputMax
            elif output < self.outputMin:
                output = self.outputMin
            if not self.isRaw and self.filterConstant != 0:
                output = self.lastOutput + ((self.sampleTime / 1000) / self.filterConstant) * (output - self.lastOutput)
                
            self.debug("Output " + str(output))
            self.params.output = output
            
            self.lastOutput = output
            self.lastTime = now

            self.debug("###############\n")
            return True

        self.debug("###############\n")
        return False

    # Initialize
    def initialize(self):
        self.debug("Initializing")
        self.initializeHistory()
        self.iTerm = self.params.output
        if self.iTerm > self.outputMax:
            self.iTerm = self.outputMax
        elif self.iTerm < self.outputMin:
            self.iTerm = self.outputMin
            
    # Initialize histor
    def initializeHistory(self):
        self.debug("Initializing history")
        self.history[0] = self.params.input
        for i in range(1, 30):
            self.history[i] = self.history[0]
            
    # Set tunings
    def setTunings(self, kP, kI, kD):
        self.debug("Setting tunings")

        if kP < 0 or kI < 0 or kD < 0:
            return

        sampleTimeInSecs = self.sampleTime / 1000

        self.kP = kP
        self.kI = kI * sampleTimeInSecs
        self.kD = kD * sampleTimeInSecs

        if self.direction == self.REVERSE:
            self.kP = 0 - self.kP
            self.kI = 0 - self.kI
            self.kD = 0 - self.kD

    # Set output limits
    def setOutputLimits(self, minLimit, maxLimit):
        self.debug("Setting output limits")
        self.outputMin = minLimit
        self.outputMax = maxLimit

        if self.inAuto:
            if self.params.output > self.outputMax:
                self.params.output = self.outputMax
            elif self.params.output < self.outputMin:
                self.params.output = self.outputMin
            if self.iTerm > self.outputMax:
                self.iTerm = self.outputMax
            elif self.iTerm < self.outputMin:
                self.iTerm = self.outputMin

    # Set mode
    def setMode(self, mode):
        self.debug("Setting mode")
        newAuto = (mode == self.AUTOMATIC)
        if newAuto != self.inAuto:
            self.debug("Changing mode")
            self.initialize()
        self.inAuto = newAuto

    # Set output type
    def setOutputType(self, outputType):
        self.debug("Setting output type")
        if outputType == self.RAW:
            self.isRaw = True
        elif outputType == self.FILTERED:
            self.isRaw = False
        
    # Set direction
    def setDirection(self, direction):
        self.debug("Setting direction")
        if self.inAuto and direction != self.direction:
            self.debug("Changing direction")
            self.kP = 0 - self.kP
            self.kI = 0 - self.kI
            self.kD = 0 - self.kD
        self.direction = direction

    # Debug
    def debug(self, s):
        if self.debugEnabled:
            print(s)
    
