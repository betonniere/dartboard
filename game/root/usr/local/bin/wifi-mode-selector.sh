#!/bin/bash

INTERFACE="wlan0"
GAME_PROFILE="HotspotDartboard"
GPIO_PIN=21

logger "hotspot-switch: Initialisation"

# Unblock the Wi-Fi interface and wait for it to be available
rfkill unblock wifi
nmcli radio wifi on

nmcli device set "$INTERFACE" managed yes

for i in {1..15}; do
    if ip link show "$INTERFACE" &>/dev/null; then break; fi
    sleep 1
done

# Configure the GPIO pin and read its state
pinctrl set "$GPIO_PIN" ip pu
GPIO_STATE=$(pinctrl get "$GPIO_PIN" | grep -o "lo")

if [ "$GPIO_STATE" == "lo" ]; then
  logger "hotspot-switch: Activation HOTSPOT"

  nmcli connection up "$GAME_PROFILE"

else
  logger "hotspot-switch: Activation CLIENT"

  nmcli connection down "$GAME_PROFILE" 2>/dev/null || true
  nmcli device wifi rescan >/dev/null 2>&1 || true
  nmcli device connect "$INTERFACE" >/dev/null 2>&1 || true
fi
