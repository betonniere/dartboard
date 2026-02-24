#!/bin/bash

HOTSPOT_FILE="/boot/use_hotspot.txt"
INTERFACE="wlan0"
STATIC_IP="10.3.141.1/24"

if [ -f "$HOTSPOT_FILE" ]; then
  # --- Mode Hotspot ---
  # 1. Arrêt du client Wi-Fi pour éviter le conflit sur l'antenne
  systemctl stop wpa_supplicant 2>/dev/null
  systemctl stop NetworkManager 2>/dev/null

  # 2. Nettoyage de l'interface (Supprime les IP fantômes)
  ip addr flush dev "$INTERFACE"
  ip link set "$INTERFACE" up

  # 3. Fixer l'IP avant de lancer les services (L'ordre est crucial)
  ip addr add "$STATIC_IP" dev "$INTERFACE"

  # 4. Lancement des services AP
  systemctl start hostapd
  sleep 2 # Pause pour stabiliser l'interface
  systemctl start dnsmasq
  systemctl start nodogsplash
else
  # --- Mode Client Wi-Fi ---
  # 1. Arrêt des services Hotspot
  systemctl stop nodogsplash dnsmasq hostapd 2>/dev/null

  # 2. Nettoyage de l'interface pour le DHCP de la box
  ip addr flush dev "$INTERFACE"
  ip link set "$INTERFACE" up

  # 3. Relance de la recherche de réseaux Wi-Fi
  systemctl start wpa_supplicant
  systemctl start NetworkManager
fi