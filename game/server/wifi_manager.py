#!/usr/bin/env python3

import subprocess
import sys
import time

INTERFACE = 'wlan0'
HOTSPOT_PROFILE = 'HotspotDartboard'


# ----------------------------------
def run_nmcli(action, profile=None):
    cmd = ['nmcli']
    if action == 'up':
        cmd += ['connection', 'up', profile, 'ifname', INTERFACE]
    elif action == 'down':
        cmd += ['connection', 'down', profile]
    elif action == 'status':
        cmd += ['-t', '-f', 'DEVICE,STATE', 'device']

    try:
        print(f'Exécution de : {" ".join(cmd)}')
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f'Erreur NetworkManager : {e.stderr}')
        return None


# ----------------------------------
def prepare_wifi():
    # Unblock Wi-Fi et active la radio
    subprocess.run(['rfkill', 'unblock', 'wifi'])
    subprocess.run(['nmcli', 'radio', 'wifi', 'on'])
    subprocess.run(['nmcli', 'device', 'set', INTERFACE, 'managed', 'yes'])

    # Attente que l'interface sorte de l'état 'unavailable'
    for _ in range(10):
        status = run_nmcli('status')
        if status and f'{INTERFACE}:disconnected' in status:
            print(f"     --->> status: {status}")
            break
        time.sleep(1)


# ----------------------------------
def set_hotspot_mode():
    print(f'Activation du Hotspot : {HOTSPOT_PROFILE}...')
    prepare_wifi()

    # On descend le profil au cas où il serait déjà mal activé
    run_nmcli('down', HOTSPOT_PROFILE)
    time.sleep(1)
    if run_nmcli('up', HOTSPOT_PROFILE):
        print('Mode Hotspot activé avec succès.')


# ----------------------------------
def set_client_mode():
    print('Activation du mode Client...')
    prepare_wifi()

    run_nmcli('down', HOTSPOT_PROFILE)
    # Force la recherche et la connexion aux réseaux connus
    subprocess.run(['nmcli', 'device', 'wifi', 'rescan'])
    subprocess.run(['nmcli', 'device', 'connect', INTERFACE])
    print('Mode Client activé.')


# ----------------------------------
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python3 wifi_manager.py [hotspot|client]')
        sys.exit(1)

    mode = sys.argv[1].lower()
    if mode == 'hotspot':
        set_hotspot_mode()
    elif mode == 'client':
        set_client_mode()
    else:
        print('Mode inconnu. Utilisez "hotspot" ou "client".')
