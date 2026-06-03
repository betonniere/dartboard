
# 1. Prérequis

sudo systemctl disable hostapd dnsmasq nodogsplash

# 2. Création des profils réseaux

## HotspotDartboard

sudo nmcli con add type wifi ifname wlan0 mode ap con-name HotspotDartboard ssid "Dartboard-Club"

sudo nmcli con modify HotspotDartboard 802-11-wireless.band bg
sudo nmcli con modify HotspotDartboard 802-11-wireless-security.key-mgmt wpa-psk
sudo nmcli con modify HotspotDartboard 802-11-wireless-security.proto rsn
sudo nmcli con modify HotspotDartboard 802-11-wireless-security.psk "changeme"
sudo nmcli con modify HotspotDartboard connection.autoconnect no
sudo nmcli con modify HotspotDartboard ipv4.method shared
sudo nmcli con modify HotspotDartboard ipv4.addresses 10.3.141.1/24
sudo nmcli con modify HotspotDartboard ipv6.method disabled

## WifiClient

sudo nmcli con add type wifi ifname wlan0 con-name WifiClient ssid "Votre-Box-Suisse"

sudo nmcli con modify WifiClient wifi-sec.key-mgmt wpa-psk wifi-sec.psk "VotreMotDePasse"
sudo nmcli con modify WifiClient connection.autoconnect yes
sudo nmcli con modify WifiClient ipv4.dhcp-timeout 5
