import machine
import bmp280


i2c = machine.I2C(scl = machine.Pin(23),sda = machine.Pin(22))


'''
confirm your device is present on the bus
it should return [118] for this particular sensor
if this returns nothing, check your wiring
then check the Pin GPIO numbers are correct 
'''

print(i2c.scan())

sensor =  bmp280.BMP280(i2c)
sensor.get()
#returns a list of temp float and barometric pressure int

sensor.getTemp() 
#returns float temp in Celcius 

sensor.getPress()
#returns int pressure in Pascals

sensor.getAltitude()
#returns float calculated altitude in metres
