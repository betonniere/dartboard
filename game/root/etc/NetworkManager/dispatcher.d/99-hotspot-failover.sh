#!/bin/bash
# Copyright (C) Yannick Le Roux.
# This file is part of Dartboard.

INTERFACE=$1
ACTION=$2

HOTSPOT_NAME="HotspotDartboard"
CLIENT_NAME="WifiClient"
GPIO_PIN=21

# Sécurité : Si NetworkManager est en plein boot initial, on ignore les événements prématurés
if [ "$ACTION" = "down" ] && [ "$CONNECTIVITY_STATE" = "UNKNOWN" ]; then
    exit 0
fi

/usr/bin/touch /run/dartboard_boot_1

case "$ACTION" in
    down|pre-down|unavailable|connectivity-change|hostname)
        /usr/bin/touch /run/dartboard_boot_2

        # 1. Lecture numérique du GPIO (Priorité absolue)
        pinctrl set "$GPIO_PIN" ip pu
        GPIO_LEVEL=$(pinctrl lev "$GPIO_PIN" 2>/dev/null)

        if [ "$GPIO_LEVEL" = "0" ]; then
            /usr/bin/touch /run/dartboard_boot_3
            echo "[Dispatcher] GPIO $GPIO_PIN à 0. Mode Hotspot forcé."
            nmcli con up id "$HOTSPOT_NAME" >/dev/null 2>&1 &
            exit 0
        fi

        # 2. Temporisation pour laisser le temps à l'autoconnect d'essayer au boot
        sleep 5

        # On vérifie si une connexion Wi-Fi est actuellement active (peu importe le nom de l'interface)
        # nmcli -t -f DEVICE,STATE d grep uniquement les connexions au statut 'connecté'
        if ! nmcli -t -f TYPE,STATE device | grep -q "wifi:connected"; then
            /usr/bin/touch /run/dartboard_boot_4
            echo "[Dispatcher] Aucun Wi-Fi actif détecté. Activation du Hotspot."
            nmcli con up id "$HOTSPOT_NAME" >/dev/null 2>&1 &
        fi

        /usr/bin/touch /run/dartboard_boot_5
        ;;

    up)
        # Si une interface Wi-Fi vient de monter proprement sur le client, on coupe le hotspot
        if [ "$INTERFACE" = "wlan0" ]; then
            CONNECTION_UUID=$3
            if [ "$CONNECTION_UUID" != "$(nmcli -g UUID con show id "$HOTSPOT_NAME" 2>/dev/null)" ]; then
                echo "[Dispatcher] Connexion établie ailleurs. Fermeture du Hotspot."
                nmcli con down id "$HOTSPOT_NAME" >/dev/null 2>&1 &
            fi
        fi
        ;;
esac
