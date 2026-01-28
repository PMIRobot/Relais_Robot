import cyberpi
import mbot2
import mbuild
import time

# --- Configuration WiFi ---
ssid = " " # Nom du réseau 
pwd = " " # Mot de passe 
topic = "/test_room"

# Initialisation : LED rouge et affichage du statut WiFi
cyberpi.led.on(255, 0, 0, id='all')
cyberpi.wifi.connect(ssid, pwd)

# Attente de la connexion
while not cyberpi.wifi.is_connect():
    cyberpi.display.show_label("Connecting..", 12, 0, 0)

# Connexion réussie : affichage des instructions et LED verte
cyberpi.display.clear()
cyberpi.display.show_label("Connecté !\nA: Lancer\nB: Arréter", 12, 0, 0)
cyberpi.led.on(0, 255, 0, id='all')
cyberpi.wifi_broadcast.set(topic, "")

# Variable d'état pour contrôler le mouvement
is_moving = False 

# Boucle principale
while True:
    # Gestion des boutons pour démarrer/arrêter
    if cyberpi.controller.is_press('a'):
        is_moving = True
        cyberpi.display.clear()
        cyberpi.display.show_label("En marche...", 12, 0, 0)
    
    if cyberpi.controller.is_press('b'):
        is_moving = False
        mbot2.drive_speed(0, 0)
        cyberpi.display.show_label("Manuel Stop", 12, 0, 0)

    # Logique de détection et mouvement si activé
    if is_moving:
        # Lecture du capteur de luminosité (L1)
        # On utilise souvent L1 ou R1 pour la détection de ligne
        luminosite = mbuild.quad_rgb_sensor.get_gray("L1")
       
        # Détection de la ligne noire
        if luminosite < 25:  # Seuil ajusté pour le noir
            # STOP : Arrêt du robot
            mbot2.drive_speed(0, 0)
            cyberpi.led.on(255, 0, 0, id='all')
            cyberpi.display.show_label("NOIR DETECTE", 16, 0, 0)
            
            # Envoyer le message une seule fois
            # Signal WiFi "Avance !"
            cyberpi.wifi_broadcast.set(topic, "Avance !")
            
            # Changement d'état à False pour ne pas boucler indéfiniment
            is_moving = False 
        else:
            # Avancer tant que pas de noir détecté
            mbot2.drive_speed(30, -30)
            cyberpi.wifi_broadcast.set(topic, "Stop !")
    time.sleep(0.1)