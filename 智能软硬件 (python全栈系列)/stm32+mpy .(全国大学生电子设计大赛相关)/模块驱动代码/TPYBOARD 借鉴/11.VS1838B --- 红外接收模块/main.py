from necir import NecIr
from bm import necbm
from bm import nec_cb

def main():
	nec = NecIr()
	while True:
		nec.callback(nec_cb)
		if necbm():
			print("bm=",necbm())
			

main()