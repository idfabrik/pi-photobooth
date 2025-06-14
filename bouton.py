#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import subprocess
import os

PIN_CAPTURE = 22       # Bouton photo
PIN_SHUTDOWN = 18      # Bouton extinction
LED_VERTE = 27         # LED verte (statut)
LED_ROUGE = 17         # LED rouge (flash ou état)

GPIO.setmode(GPIO.BCM)

# Configuration initiale
GPIO.setup(PIN_CAPTURE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_SHUTDOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_VERTE, GPIO.OUT)
GPIO.output(LED_VERTE, GPIO.HIGH)  # Prêt

print("📸 Bouton photo (GPIO22) | ⏻ Bouton arrêt (GPIO18)")

try:
    button_photo_was_pressed = False
    button_shutdown_was_pressed = False

    while True:
        # Détection du bouton photo
        if GPIO.input(PIN_CAPTURE) == GPIO.LOW:
            if not button_photo_was_pressed:
                print("📷 Photo déclenchée")
                GPIO.output(LED_VERTE, GPIO.LOW)  # LED éteinte pendant capture

                # Nettoyer tous les GPIO pour libérer
                GPIO.cleanup()

                # Lancer le script de capture
                subprocess.run(["/home/pi/cab4.sh"])

                # Reconfigurer les GPIO après exécution
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(PIN_CAPTURE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                GPIO.setup(PIN_SHUTDOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                GPIO.setup(LED_VERTE, GPIO.OUT)
                GPIO.output(LED_VERTE, GPIO.HIGH)

                button_photo_was_pressed = True
        else:
            button_photo_was_pressed = False

        # Détection du bouton extinction
        if GPIO.input(PIN_SHUTDOWN) == GPIO.LOW:
            if not button_shutdown_was_pressed:
                print("⚠️  Extinction demandée...")
                GPIO.output(LED_VERTE, GPIO.LOW)
                time.sleep(1)
                os.system("sudo shutdown now")
                button_shutdown_was_pressed = True
        else:
            button_shutdown_was_pressed = False

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nArrêt du script par clavier")
    GPIO.output(LED_VERTE, GPIO.LOW)
    GPIO.cleanup()
