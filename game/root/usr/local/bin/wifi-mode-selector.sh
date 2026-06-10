#!/bin/bash
# Copyright (C) Yannick Le Roux.
# This file is part of Dartboard.

INTERFACE="wlan0"
HOTSPOT_NAME="HotspotDartboard"
GPIO_PIN=21

# Attente de l'interface Wi-Fi
while [ ! -d "/sys/class/net/$INTERFACE" ]; do
    sleep 0.5
done

# Activation du Wi-Fi
nmcli radio wifi on

# Assurer que l'interface est gérée par NetworkManager
nmcli device set "$INTERFACE" managed yes

# Attendre que NetworkManager soit prêt à gérer l'interface
WAIT=0
while [ $WAIT -lt 10 ]; do
    STATE=$(nmcli -t -f DEVICE,STATE device | grep "^${INTERFACE}:" | cut -d: -f2)
    if [ "$STATE" != "unmanaged" ] && [ -n "$STATE" ]; then
        break
    fi
    sleep 0.5
    WAIT=$((WAIT + 1))
done

# Détection du mode par lecture du GPIO
pinctrl set "$GPIO_PIN" ip pu
GPIO_LEVEL=$(pinctrl lev "$GPIO_PIN" 2>/dev/null)

if [ "$GPIO_LEVEL" = "0" ]; then
    echo "[Dartboard] GPIO $GPIO_PIN détecté à l'état BAS. Mode Hotspot FORCÉ."
    nmcli con up id "$HOTSPOT_NAME"
    exit 0
fi

# --- Mode Failover classique ---
MAX_ATTEMPTS=8
ATTEMPT=0
CONNECTED=0

while [ $ATTEMPT -lt $MAX_ATTEMPTS ]; do
    # Vérification immédiate de la connectivité Wi-Fi
    if nmcli -t -f TYPE,STATE device | grep -q "wifi:connected"; then
        CONNECTED=1
        break
    fi

    sleep 1
    ATTEMPT=$((ATTEMPT + 1))
done

if [ $CONNECTED -eq 0 ]; then
    echo "[Dartboard] WifiClient introuvable ou échec d'association après ${MAX_ATTEMPTS}s. Bascule sur le Hotspot."
    nmcli con up id "$HOTSPOT_NAME"
else
    echo "[Dartboard] Connexion WifiClient établie avec succès en ${ATTEMPT}s."
fi

exit 0
