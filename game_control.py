from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Controller as KeyboardController

# Initialize controllers
keyboard = KeyboardController()
mouse = MouseController()

# Mapping for keys
def get_keys():
    """
    Returns a list of keys for encoding keyboard keys.
    """
    return ['\t', '\n', '\r', ' ', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '{', '|', '}', '~', 'accept', 'add', 'alt', 'altleft', 'altright', 'apps', 'backspace', 'browserback', 'browserfavorites', 'browserforward', 'browserhome', 'browserrefresh', 'browsersearch', 'browserstop', 'capslock', 'clear', 'convert', 'ctrl', 'ctrlleft', 'ctrlright', 'decimal', 'del', 'delete', 'divide', 'down', 'end', 'enter', 'esc', 'escape', 'execute', 'f1', 'f10', 'f11', 'f12', 'f13', 'f14', 'f15', 'f16', 'f17', 'f18', 'f19', 'f2', 'f20', 'f21', 'f22', 'f23', 'f24', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'final', 'fn', 'hanguel', 'hangul', 'hanja', 'help', 'home', 'insert', 'junja', 'kana', 'kanji', 'launchapp1', 'launchapp2', 'launchmail', 'launchmediaselect', 'left', 'modechange', 'multiply', 'nexttrack', 'nonconvert', 'num0', 'num1', 'num2', 'num3', 'num4', 'num5', 'num6', 'num7', 'num8', 'num9', 'numlock', 'pagedown', 'pageup', 'pause', 'pgdn', 'pgup', 'playpause', 'prevtrack', 'print', 'printscreen', 'prntscrn', 'prtsc', 'prtscr', 'return', 'right', 'scrolllock', 'select', 'separator', 'shift', 'shiftleft', 'shiftright', 'sleep', 'space', 'stop', 'subtract', 'tab', 'up', 'volumedown', 'volumemute', 'volumeup', 'win', 'winleft', 'winright', 'yen', 'command', 'option', 'optionleft', 'optionright']

def get_key(id):
    """
    Retrieves a key from its ID.
    
    Args:
        id (int): ID of the key.
    
    Returns:
        str: Corresponding key.
    """
    keys = get_keys()
    if 0 <= id < len(keys):
        return keys[id]
    else:
        raise ValueError(f"Invalid key ID: {id}")

def get_id(key):
    """
    Retrieves the ID of a key.
    
    Args:
        key (str): The key to retrieve the ID for.
    
    Returns:
        int: The ID of the key.
    """
    keys = get_keys()
    if key in keys:
        return keys.index(key)
    else:
        raise ValueError(f"Invalid key: {key}")

# Mouse actions
def move(x, y):
    """
    Move the mouse to the specified coordinates.
    
    Args:
        x (int): X-coordinate.
        y (int): Y-coordinate.
    """
    mouse.position = (x, y)

def scroll(dx, dy):
    """
    Scroll the mouse.
    
    Args:
        dx (int): Horizontal scroll.
        dy (int): Vertical scroll.
    """
    mouse.scroll(dx, dy)

def click(x, y, button=Button.left):
    """
    Click the mouse at the specified coordinates.
    
    Args:
        x (int): X-coordinate.
        y (int): Y-coordinate.
        button (Button): Mouse button to click.
    """
    move(x, y)
    mouse.click(button)

# Keyboard actions
def press(key):
    """
    Press a key.
    
    Args:
        key (str): Key to press.
    """
    keyboard.press(key)

def release(key):
    """
    Release a key.
    
    Args:
        key (str): Key to release.
    """
    keyboard.release(key)