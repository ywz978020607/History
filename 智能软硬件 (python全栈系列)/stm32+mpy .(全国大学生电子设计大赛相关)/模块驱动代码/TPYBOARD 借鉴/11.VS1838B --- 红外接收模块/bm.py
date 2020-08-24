nec_bm=0
def nec_cb(nec, a, c, r):
	global nec_bm
	print(a, c, r)				# Address, Command, Repeat
	nec_bm=c
	
def necbm():
	global nec_bm
	if nec_bm==69:
		nec_bm=0xa0
	elif nec_bm==70:
		nec_bm=0xa1
	elif nec_bm==71:
		nec_bm=0xa2
	elif nec_bm==68:
		nec_bm=0xa3
	elif nec_bm==64:
		nec_bm=0xa4
	elif nec_bm==67:
		nec_bm=0xa5
	elif nec_bm==7:
		nec_bm=0xa6
	elif nec_bm==21:
		nec_bm=0xa7
	elif nec_bm==9:
		nec_bm=0xa8
	elif nec_bm==22:
		nec_bm=0xa9
	elif nec_bm==25:
		nec_bm=0xaa
	elif nec_bm==13:
		nec_bm=0xab
	elif nec_bm==12:
		nec_bm=0xac
	elif nec_bm==24:
		nec_bm=0xad
	elif nec_bm==94:
		nec_bm=0xae
	elif nec_bm==8:
		nec_bm=0xaf
	elif nec_bm==28:
		nec_bm=0xb0
	elif nec_bm==90:
		nec_bm=0xb1
	elif nec_bm==66:
		nec_bm=0xb2
	elif nec_bm==82:
		nec_bm=0xb3
	elif nec_bm==74:
		nec_bm=0xb4
	return nec_bm