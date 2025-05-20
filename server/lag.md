sudo modprobe -r brcmfmac
sudo modprobe brcmfmac feature_disable=0x82000
sudo systemctl restart wpa_supplicant@wlan0.service