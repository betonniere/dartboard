#!/bin/bash

INTERFACE="wlan0"
NM_PROFILE="HotspotDartboard"
GPIO_PIN=21

# Unblock the Wi-Fi interface and wait for it to be available
rfkill unblock wlan
for i in {1..15}; do
    if [ -d "/sys/class/net/$INTERFACE" ]; then break; fi
    sleep 1
done

# Configure the GPIO pin and read its state
pinctrl set $GPIO_PIN ip pu
GPIO_STATE=$(pinctrl get $GPIO_PIN | grep -o "lo")

# Activate hotspot mode if the GPIO pin is low, otherwise activate client mode
if [ "$GPIO_STATE" == "lo" ]; then
  echo "Hotspot mode activation (Game)"

  nmcli device set $INTERFACE managed yes
  sleep 2

  nmcli connection up "$NM_PROFILE"

  systemctl start nodogsplash

else
  echo "Client mode activation (Maintenance)"

  systemctl stop nodogsplash 2>/dev/null || true

  nmcli connection down "$NM_PROFILE" 2>/dev/null || true
  nmcli device wifi rescan >/dev/null 2>&1 || true
fi
