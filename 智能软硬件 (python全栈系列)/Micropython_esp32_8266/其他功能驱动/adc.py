from machine import ADC,Pin

ad1=ADC(Pin(34))

ad1.atten(ADC.ATTN_11DB)
ad1.width(ADC.WIDTH_12BIT)

print(ad1.read()*3.3/4095)