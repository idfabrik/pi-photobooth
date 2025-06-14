#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import subprocess
import os

PIN_CAPTURE = 22       # Bouton photo
PIN_SHUTDOWN = 18      # Bouton extinction
LED = 27               # LED verte

GPIO.setmode(GPIO.BCM)

# Configuration des GPIO
GPIO.setup(PIN_CAPTURE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(PIN_SHUTDOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED, GPIO.OUT)
GPIO.output(LED, GPIO.HIGH)  # LED allumée = prêt

print("📸 Bouton photo (GPIO22) | ⏻ Bouton arrêt (GPIO18)")

try:
    button_photo_was_pressed = False
    button_shutdown_was_pressed = False

    while True:
        # Détection bouton photo
        if GPIO.input(PIN_CAPTURE) == GPIO.LOW:
            if not button_photo_was_pressed:
                print("📷 Photo déclenchée")
                GPIO.output(LED, GPIO.LOW)

                # Nettoyage des GPIO pour permettre leur réutilisation dans cab4.sh
                GPIO.cleanup()

                # Lancement du script photo
                subprocess.run(["/home/pi/cab4.sh"])

                # Reconfig LED et boutons après cab4.sh
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(PIN_CAPTURE, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                GPIO.setup(PIN_SHUTDOWN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                GPIO.setup(LED, GPIO.OUT)
                GPIO.output(LED, GPIO.HIGH)

                button_photo_was_pressed = True
        else:
            button_photo_was_pressed = False

        # Détection bouton extinction
        if GPIO.input(PIN_SHUTDOWN) == GPIO.LOW:
            if not button_shutdown_was_pressed:
                print("⚠️  Extinction demandée...")
                GPIO.output(LED, GPIO.LOW)
                time.sleep(1)
                os.system("sudo shutdown now")
                button_shutdown_was_pressed = True
        else:
            button_shutdown_was_pressed = False

        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nArrêt du script par clavier")
    GPIO.output(LED, GPIO.LOW)
    GPIO.cleanup()

