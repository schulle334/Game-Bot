import json
import cv2
import numpy as np
import logging

# Logging konfigurieren
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Laden der Ereignisse
with open("events.json", "r") as f:
    events = json.load(f)
logging.info("Ereignisse aus events.json geladen")

# Laden des Videos
cap = cv2.VideoCapture("gameplay.avi")
frames = []
timestamps = []

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break
    frames.append(cv2.resize(frame, (128, 128)))  # Frames auf 128x128 verkleinern
    timestamps.append(cap.get(cv2.CAP_PROP_POS_MSEC) / 1000)  # Zeitstempel in Sekunden
logging.info("Frames aus gameplay.avi geladen und vorverarbeitet")
cap.release()

# Synchronisieren der Ereignisse mit den Frames
synchronized_data = []
frame_idx = 0

for event in events:
    if event[0] == 'frame':
        frame_idx += 1
    else:
        while frame_idx < len(timestamps) and timestamps[frame_idx] < event[2]:
            frame_idx += 1
        if frame_idx < len(frames):
            synchronized_data.append((frames[frame_idx], event))

logging.info("Ereignisse mit Frames synchronisiert")

# Beispielhafte Verarbeitung der synchronisierten Daten
X = []
y = []

key_mapping = {
    'w': 0,
    'a': 1,
    's': 2,
    'd': 3,
    'q': 4,
    'e': 5,
    'r': 6,
    # Fügen Sie hier weitere Tasten hinzu, die Sie erfassen möchten
}

for frame, event in synchronized_data:
    if event[0] == 'key_press' and event[1] in key_mapping:
        X.append(frame)
        y.append(key_mapping[event[1]])  # Das Ziel ist die zugehörige Aktion (Taste)

X = np.array(X)
y = np.array(y)

logging.info(f"Daten für das Training vorbereitet: X shape: {X.shape}, y shape: {y.shape}")

# Beispielmodelltraining
import tensorflow as tf
from tensorflow.keras import layers

def create_model(input_shape):
    model = tf.keras.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D((2, 2)),
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D((2, 2)),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(len(key_mapping), activation='softmax')  # Anzahl der möglichen Aktionen
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    return model

input_shape = (128, 128, 3)  # Beispielhafte Eingabegröße
model = create_model(input_shape)

logging.info("Starte Modelltraining")
model.fit(X, y, epochs=10)

# Speichern des Modells
model.save("dqn_game_model")
logging.info("Modell als dqn_game_model gespeichert")