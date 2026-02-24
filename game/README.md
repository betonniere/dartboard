# 1. Désactiver le boot automatique des services individuels
sudo systemctl disable hostapd dnsmasq nodogsplash wpa_supplicant NetworkManager

# 2. Activer ton nouveau service de sélection
# (Assure-toi d'avoir créé le fichier /etc/systemd/system/wifi-selector.service)
sudo systemctl daemon-reload
sudo systemctl enable wifi-mode-selector.service