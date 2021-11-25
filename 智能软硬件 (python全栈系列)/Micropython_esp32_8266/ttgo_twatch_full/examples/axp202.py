from machine import I2C
from machine import Pin
import axp202
import time

i2c = I2C(scl=22, sda=21)
print(i2c)
pmu = axp202.PMU(i2c)
pmu.enablePower(axp202.AXP202_LDO2)
pmu.setLDO2Voltage(3300)
bl = Pin(12, Pin.OUT)
bl.value(1)

'''
enable axp202 adc 
'''
pmu.enableADC(axp202.AXP202_ADC1,axp202.AXP202_BATT_VOL_ADC1)
pmu.enableADC(axp202.AXP202_ADC1, axp202.AXP202_BATT_CUR_ADC1)
pmu.enableADC(axp202.AXP202_ADC1, axp202.AXP202_VBUS_VOL_ADC1)
pmu.enableADC(axp202.AXP202_ADC1, axp202.AXP202_VBUS_CUR_ADC1)


while True:
  if pmu.isVBUSPlug():
    vbus = pmu.getVbusVoltage()
    cbus = pmu.getVbusCurrent()
    print("vbus is connect VBUS is {} mV Current is {} mA".format( vbus , cbus))

  if pmu.isBatteryConnect():
    vbatt = pmu.getBattVoltage()
    percent = pmu.getBattPercentage()
    print("battery percent is {}% battery is {} mV".format(percent , vbatt))
  time.sleep(1)