# 1. Prérequis
sudo systemctl disable hostapd dnsmasq nodogsplash

# 2. Création du profile HotspotDartboard
sudo nmcli con add type wifi ifname wlan0 mode ap con-name HotspotDartboard ssid "Dartboard-Club"
sudo nmcli con modify HotspotDartboard 802-11-wireless.band bg
sudo nmcli con modify HotspotDartboard 802-11-wireless-security.group ccmp
sudo nmcli con modify HotspotDartboard 802-11-wireless-security.key-mgmt wpa-psk
sudo nmcli con modify HotspotDartboard 802-11-wireless-security.pairwise ccmp
sudo nmcli con modify HotspotDartboard 802-11-wireless-security.proto rsn
sudo nmcli con modify HotspotDartboard 802-11-wireless-security.psk "changeme"
sudo nmcli con modify HotspotDartboard ipv4.method shared
sudo nmcli con modify HotspotDartboard ipv4.addresses 10.3.141.1/24