import os
def AddNetwork(SSID, password):
  lines = [
    'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev',
    'update_config=1',
    'country=GB',
    '\n',
    'network={',
    '\tssid="{}"'.format(SSID),
    '\tpsk="{}"'.format(password),
    '\tkey_mgmt=WPA-PSK',
    '}'
  ]

  config = '\n'.join(lines)
  
  wifiFile = open("/etc/wpa_supplicant/wpa_supplicant.conf", "w")
  wifiFile.write(config)

def CheckNetwork():
  wifiFile = open("/etc/wpa_supplicant/wpa_supplicant.conf", "r")
  for line in wifiFile:
      if line =="network={\n":
          return True
  return False
  
if not CheckNetwork():
    AddNetwork("SSID","password")
    os.system("wpa_cli -i wlan0 reconfigure")
    #need to check whether an internet connection has been established by pinging a website after a set time. Otherwise try again asking for a different QR code.
    #if connection fails then clear the file.
else:
    print("Config already added")
    
