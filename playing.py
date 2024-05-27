import cv2
import numpy as np
import pyautogui
import time
import tensorflow as tf
import logging

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Laden Sie das trainierte Modell
model = tf.keras.models.load_model("dqn_game_model")
logging.info("Trainiertes Modell dqn_game_model geladen")

# Mapping der Aktionen
key_mapping = ['w', 'a', 's', 'd', 'q', 'e', 'r']
action_to_key = {i: key for i, key in enumerate(key_mapping)}

def preprocess_frame(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (128, 128))  # Muss mit dem Modell-Eingabeformat übereinstimmen
    frame = frame.astype(np.float32) / 255.0  # Normalisieren
    return np.expand_dims(frame, axis=0)

def press_key(key):
    pyautogui.keyDown(key)
    time.sleep(0.1)
    pyautogui.keyUp(key)
    logging.info(f"Taste {key} gedrückt")

# Hauptschleife zur Steuerung des Spiels
try:
    logging.info("Starte Spielsteuerung durch das Modell")
    while True:
        # Screenshot des aktuellen Spielzustands
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)

        # Vorverarbeiten des Frames
        processed_frame = preprocess_frame(frame)

        # Vorhersage der nächsten Aktion durch das Modell
        prediction = model.predict(processed_frame)
        action = np.argmax(prediction[0])
        key = action_to_key[action]

        # Aktion im Spiel ausführen
        press_key(key)

        # Fügen Sie hier eine Bedingung hinzu, um die Schleife zu beenden, z.B. durch Drücken einer Taste
except KeyboardInterrupt:
    logging.info("Spielsteuerung beendet.")