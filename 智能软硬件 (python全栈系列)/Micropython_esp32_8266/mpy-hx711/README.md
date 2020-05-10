# micropython-hx711
Micropython driver for the HX711 24-Bit Analog-to-Digital Converter

Latest version supports:
- retrieving data from the channel 'A' with gain 128 and 64, 
the channel 'B' with gain 32 in a raw form and a form 
converted from the two's complement.
- sending "power off" sequence to switch device to the power-saving mode.
- sending "power on" sequence with the gain saved before the "power off".
- checking if the device is ready for the data retrieval.

#### Example for the ESP8266:
D_OUT pin is connected to the GPIO 5<br/>
PD_SCK pin is connected to the GPIO 4<br/>
Using internal HX711 oscillator, so ESP8266's frequency is set to 160000000
 
```
>>> from machine import freq
>>> freq(160000000)
>>> 
>>> from hx711 import HX711
>>> 
>>> driver = HX711(d_out=5, pd_sck=4)
>>> driver
HX711 on channel A, gain=128
>>> driver.read()
74342
>>> 
>>> driver.channel=HX711.CHANNEL_A_64
>>> driver.channel
('A', 64)
>>> driver.read()
36328
>>> 
>>> driver.power_off()
```