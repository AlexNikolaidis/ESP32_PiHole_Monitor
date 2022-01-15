import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
if not wlan.isconnected():
    print('connecting to network...')
    # Enter your networks SSID and password
    wlan.connect('SSID', 'PASS')
    while not wlan.isconnected():
        pass
print('network config:', wlan.ifconfig())


