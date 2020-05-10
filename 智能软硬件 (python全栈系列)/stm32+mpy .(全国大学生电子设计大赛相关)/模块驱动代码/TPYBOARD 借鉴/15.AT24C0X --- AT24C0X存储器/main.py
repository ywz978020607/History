import at24c0x

def main():
    at24c=at24c0x.AT24C0x(1)
    at24c.writeAT24C0x(0,'qxw')
    print(at24c.readAT24C0x(0,3))
main()