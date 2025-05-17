sudo vim /etc/modprobe.d/brcmfmac.conf
-->> options brcmfmac roamoff=1 feature_disable=0x282000

sudo update-initramfs -u
sudo reboot