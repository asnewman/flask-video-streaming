import os

class WifiConnect:
    @staticmethod
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
      wifiFile.close()
    
    @staticmethod
    def CheckNetwork():
      wifiFile = open("/etc/wpa_supplicant/wpa_supplicant.conf", "r")
      for line in wifiFile:
          if line =="network={\n":
              return True
      return False
      

        
