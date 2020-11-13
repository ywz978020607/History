import esp8266uart

esp = esp8266uart.ESP8266(1, 115200)

print('Testing generic methods')
print('=======================')

print('AT startup...')
if esp.test():
    print('Success!')
else:
    print('Failed!')

#print('Soft-Reset...')
#if esp.reset():
#    print('Success!')
#else:
#    print('Failed!')

print('Another AT startup...')
if esp.test():
    print('Success!')
else:
    print('Failed!')

print()

print('Testing WIFI methods')
print('====================')

wifi_mode = 1
print("Testing get_mode/set_mode of value '%s'(%i)..." % (esp8266uart.WIFI_MODES[wifi_mode], wifi_mode))
esp.set_mode(wifi_mode)
if esp.get_mode() == wifi_mode:
    print('Success!')
else:
    print('Failed!')
    
print('Disconnecting from WLAN...')
if esp.disconnect():
    print('Success!')
else:
    print('Failed!')

print('Disconnecting from WLAN again...')
if esp.disconnect():
    print('Success!')
else:
    print('Failed!')

print('Checking if not connected WLAN...')
if esp.get_accesspoint() == None:
    print('Success!')
else:
    print('Failed!')

print('Scanning for WLANs...')
wlans = esp.list_all_accesspoints()
for wlan in wlans:
    print(wlan)
    print("Scanning for WLAN '%s'..." % (wlan['ssid']))
    for wlan2 in esp.list_accesspoints(wlan['ssid']):
        print(wlan2)

print('Setting access point mode...')
if esp.set_mode(esp8266uart.WIFI_MODES['Access Point + Station']):
    print('Failed!')
else:
    print('Success!')

print('Reading access point configuration')
print(esp.get_accesspoint_config())
print('Listing all stations connected to the module in access point mode...')
print(esp.list_stations())

print('Checking DHCP client and server settings...')
for mode in range(3):
    print(esp.set_dhcp_config(mode, 0))
    print(esp.set_dhcp_config(mode, 1))
    print(esp.set_dhcp_config(mode, True))
    print(esp.set_dhcp_config(mode, False))
try:
    print(esp.set_dhcp_config(0, 2))
except esp8266uart.CommandError:
    print('Obvious error caught!')
try:
    print(esp.set_dhcp_config(4, 1))
except esp8266uart.CommandError:
    print('Obvious error caught!')

print('Setting autoconnect to access point in station mode...')
esp.set_autoconnect(True)
esp.set_autoconnect(False)
esp.set_autoconnect(True)

print('Reading and setting the station IP...')
print(esp.get_station_ip())
esp.set_station_ip('192.168.1.10')
print(esp.get_station_ip())

print('Reading and setting the access point IP...')
print(esp.get_accesspoint_ip())
esp.set_accesspoint_ip('192.168.1.1')
print(esp.get_accesspoint_ip())