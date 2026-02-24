#!/bin/bash

INTERFACE="wlan0"
STATIC_IP="10.3.141.1/24"

GPIO_PIN=21
pinctrl set $GPIO_PIN ip pu
GPIO_STATE=$(gpioget $(gpiofind GPIO$GPIO_PIN))

if [ "$GPIO_STATE" -eq 0 ]; then
  systemctl mask wpa_supplicant 2>/dev/null
  systemctl stop wpa_supplicant 2>/dev/null
  systemctl mask NetworkManager 2>/dev/null
  systemctl stop NetworkManager 2>/dev/null

  /usr/sbin/iw dev "$INTERFACE" set power_save off 2>/dev/null

  rfkill unblock wifi

  echo "----> 0"
  for i in {1..5}; do
    [ -d "/sys/class/net/$INTERFACE" ] && break
    sleep 1
  done

  ip addr flush dev "$INTERFACE"
  ip link set "$INTERFACE" up
  ip addr add "$STATIC_IP" dev "$INTERFACE"
  sleep 2

  echo "----> 1"
  systemctl start hostapd --no-block
  echo "----> 2"
  systemctl start dnsmasq --no-block
  echo "----> 3"
  systemctl start nodogsplash --no-block
  echo "----> 4"
else
  systemctl stop nodogsplash 2>/dev/null
  systemctl stop dnsmasq     2>/dev/null
  systemctl stop hostapd     2>/dev/null

  ip addr flush dev "$INTERFACE"

  systemctl unmask wpa_supplicant
  systemctl start wpa_supplicant
  systemctl unmask NetworkManager
  systemctl start NetworkManager
fi
