import os
import numpy as np
from time import sleep
from PIL import ImageGrab
from game_control import press, release, click, get_key
from predict import predict
from tensorflow.keras.models import model_from_json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def load_model(model_json_path, model_weights_path):
    """
    Load the model architecture and weights from the specified files.

    Args:
        model_json_path (str): Path to the model JSON file.
        model_weights_path (str): Path to the model weights file.

    Returns:
        model: Loaded Keras model.
    """
    logging.info("Loading model...")
    with open(model_json_path, 'r') as model_file:
        model_json = model_file.read()
    model = model_from_json(model_json)
    model.load_weights(model_weights_path)
    logging.info("Model loaded successfully.")
    return model

def get_screenshot():
    """
    Capture a screenshot and convert it to a numpy array.

    Returns:
        np.array: Screenshot as a numpy array.
    """
    img = ImageGrab.grab()
    img_np = np.array(img)
    return img_np

def main():
    """
    Main function to start the AI and perform actions based on predictions.
    """
    # Load model
    model = load_model('Data/Model/model.json', 'Data/Model/weights.h5')

    logging.info("AI started now!")

    while True:
        # Get screenshot
        screen = get_screenshot()
        
        # Get predictions
        Y = predict(model, screen)
        
        if np.array_equal(Y, [0, 0, 0, 0]):
            # No action
            continue
        elif Y[0] == -1 and Y[1] == -1:
            # Only keyboard action
            key = get_key(Y[3])
            if Y[2] == 1:
                # Press key
                logging.info(f"Pressing key: {key}")
                press(key)
            else:
                # Release key
                logging.info(f"Releasing key: {key}")
                release(key)
        elif Y[2] == 0 and Y[3] == 0:
            # Only mouse action
            logging.info(f"Clicking at: ({Y[0]}, {Y[1]})")
            click(Y[0], Y[1])
        else:
            # Mouse and keyboard action
            logging.info(f"Clicking at: ({Y[0]}, {Y[1]}) and handling key: {Y[3]}")
            click(Y[0], Y[1])
            key = get_key(Y[3])
            if Y[2] == 1:
                # Press key
                logging.info(f"Pressing key: {key}")
                press(key)
            else:
                # Release key
                logging.info(f"Releasing key: {key}")
                release(key)

if __name__ == '__main__':
    main()