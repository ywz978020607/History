import nrf24l01use

nrf=nrf24l01use.NRF24L01(spi=2,csn='Y5',ce='Y4')

while True:
	print(nrf.slave())
	
# import nrf24l01use

# nrf=nrf24l01use.NRF24L01(spi=2,csn='Y5',ce='Y4')
# i=0
# while True:
	# nrf.master(i)
	# i+=1