import os
import numpy as np
from time import sleep
from PIL import ImageGrab
from game_control import get_id
from get_dataset import save_img
from multiprocessing import Process
from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyListener
import logging
from tensorflow.keras.models import model_from_json
from skimage.transform import resize

# Configure logging
logging.basicConfig(level=logging.INFO)

def get_screenshot():
    """
    Capture a screenshot, resize it, and normalize pixel values.

    Returns:
        np.array: Processed screenshot.
    """
    img = ImageGrab.grab()
    img = np.array(img)[:, :, :3]  # Get first 3 channels (RGB)
    img = resize(img, (150, 150, 3), anti_aliasing=True).astype('float32') / 255.0
    return img

def save_event_keyboard(data_path, event, key):
    """
    Save keyboard event along with a screenshot.

    Args:
        data_path (str): Path to save data.
        event (int): Event type (press/release).
        key: Key event information.
    """
    key = get_id(key)
    event_path = os.path.join(data_path, f'-1,-1,{event},{key}')
    screenshot = get_screenshot()
    save_img(event_path, screenshot)

def save_event_mouse(data_path, x, y):
    """
    Save mouse event along with a screenshot.

    Args:
        data_path (str): Path to save data.
        x (int): X coordinate of mouse.
        y (int): Y coordinate of mouse.
    """
    event_path = os.path.join(data_path, f'{x},{y},0,0')
    screenshot = get_screenshot()
    save_img(event_path, screenshot)

def listen_mouse():
    """
    Start listening for mouse events.
    """
    data_path = 'Data/Train_Data/Mouse'
    os.makedirs(data_path, exist_ok=True)

    def on_click(x, y, button, pressed):
        logging.info(f'Mouse clicked at ({x}, {y})')
        save_event_mouse(data_path, x, y)

    def on_scroll(x, y, dx, dy):
        pass

    def on_move(x, y):
        pass

    with MouseListener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
        listener.join()

def listen_keyboard():
    """
    Start listening for keyboard events.
    """
    data_path = 'Data/Train_Data/Keyboard'
    os.makedirs(data_path, exist_ok=True)

    def on_press(key):
        logging.info(f'Key pressed: {key}')
        save_event_keyboard(data_path, 1, key)

    def on_release(key):
        logging.info(f'Key released: {key}')
        save_event_keyboard(data_path, 2, key)

    with KeyListener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def main():
    """
    Main function to start the dataset creation process.
    """
    dataset_path = 'Data/Train_Data/'
    os.makedirs(dataset_path, exist_ok=True)

    # Start listening to mouse events in a new process
    Process(target=listen_mouse).start()
    listen_keyboard()

if __name__ == '__main__':
    main()