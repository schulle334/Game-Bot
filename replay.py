import cv2
import numpy as np
import pyautogui
from pynput import keyboard, mouse
import time
import json
import logging

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Variablen zur Speicherung der Ereignisse
events = []

# Funktionen zur Verarbeitung der Tastatur- und Mauseingaben
def on_press(key):
    try:
        events.append(('key_press', key.char, time.time()))
        logging.info(f"Tastendruck aufgezeichnet: {key.char}")
    except AttributeError:
        events.append(('key_press', key.name, time.time()))
        logging.info(f"Tastendruck aufgezeichnet: {key.name}")

def on_click(x, y, button, pressed):
    events.append(('mouse_click', x, y, button.name, pressed, time.time()))
    action = "gedrückt" if pressed else "losgelassen"
    logging.info(f"Mausklick aufgezeichnet: ({x}, {y}), Taste: {button.name}, Aktion: {action}")

# Listener für Tastatur und Maus starten
keyboard_listener = keyboard.Listener(on_press=on_press)
mouse_listener = mouse.Listener(on_click=on_click)

keyboard_listener.start()
mouse_listener.start()

# Funktion zur Aufzeichnung des Bildschirms
def record_screen(filename, duration):
    screen_size = pyautogui.size()
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(filename, fourcc, 20.0, (screen_size.width, screen_size.height))

    start_time = time.time()
    while time.time() - start_time < duration:
        img = pyautogui.screenshot()
        frame = np.array(img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        out.write(frame)
        events.append(('frame', time.time()))
        logging.info("Frame aufgezeichnet")

    out.release()

# Aufzeichnung starten
duration = 120  # Dauer der Aufzeichnung in Sekunden
logging.info(f"Starte Bildschirmaufzeichnung für {duration} Sekunden")
record_screen("gameplay.avi", duration)

# Stoppen der Listener nach der Aufzeichnung
keyboard_listener.stop()
mouse_listener.stop()

# Speichern der Ereignisse in einer JSON-Datei
with open("events.json", "w") as f:
    json.dump(events, f)
logging.info("Ereignisse in events.json gespeichert")