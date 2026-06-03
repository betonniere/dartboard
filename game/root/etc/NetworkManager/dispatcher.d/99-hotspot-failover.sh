#!/bin/bash

INTERFACE="$1"
ACTION="$2"

# On ne cible que l'interface Wi-Fi
if [ "$INTERFACE" != "wlan0" ]; then
    exit 0
fi

HOTSPOT_NAME="HotspotDartboard"
CLIENT_NAME="WifiClient"

case "$ACTION" in
    up)
        # Si le Wi-Fi client vient de se connecter, on s'assure que le Hotspot est éteint
        if [ "$CONNECTION_UUID" != "$(nmcli -g UUID con show id "$HOTSPOT_NAME")" ]; then
            nmcli con down id "$HOTSPOT_NAME" > /dev/null 2>&1
        fi
        ;;
    down)
        # Si la connexion principale tombe ou échoue, on attend un court instant
        # pour laisser à NetworkManager le temps de tenter une reconnexion
        sleep 2

        # On vérifie si wlan0 est actuellement connecté à un réseau
        if ! nmcli device show wlan0 | grep -q "GENERAL.CONNECTION"; then
            echo "Aucun réseau Wi-Fi trouvé. Activation du Hotspot de secours..."
            nmcli con up id "$HOTSPOT_NAME"
        fi
        ;;
esac
