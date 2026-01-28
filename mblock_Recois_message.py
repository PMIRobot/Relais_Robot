import cyberpi
import mbot2
import time

# --- Configuration WiFi ---
ssid = " " # Nom du réseau 
pwd = " " # Mot de passe 
topic = "/test_room"

# Initialisation : LED rouge et affichage du statut WiFi
cyberpi.led.on(255, 0, 0, id='all')
cyberpi.display.show_label("WiFi:", 12, 0, 0, 0)

if not cyberpi.wifi.is_connect():
    cyberpi.display.show_label("WiFi: No Connect", 12, 0, 0, 0)
    cyberpi.wifi.connect(ssid, pwd)
    while not cyberpi.wifi.is_connect():
        cyberpi.display.show_label("Connecting..", 12, 0, 20, 1)

# Connexion réussie : LED verte et attente de messages
cyberpi.display.show_label("WiFi: Connected!\n", 12, 0, 0, 0)
cyberpi.display.show_label("Waiting Message...", 12, 0, 20, 1)
cyberpi.led.on(0, 255, 0, id='all')

dernier_message = ""

# Boucle principale : réception et traitement des messages
while True:
    cyberpi.wifi_broadcast.set(topic, "")

    time.sleep(0.2)
    message = cyberpi.wifi_broadcast.get(topic)
    
    # Traiter uniquement les nouveaux messages
    if message and message != dernier_message:
        dernier_message = message
        cyberpi.display.show_label("{}".format(message), 12, 0, 20, 1)
        
        # Commande "Avance !" : avancer pendant 3 secondes
        if message == "Avance !":
            cyberpi.led.on(0, 255, 0, id='all')
            # Avancer continuellement jusqu'à recevoir "Stop!"
            mbot2.drive_speed(60, -60)
            time.sleep(3)
            mbot2.drive_speed(0, 0)
        # Commande "Stop !" : arrêt immédiat
        elif message == "Stop !":
            cyberpi.led.on(255, 0, 0, id='all')
            mbot2.drive_speed(0, 0)
    
    time.sleep(0.1)