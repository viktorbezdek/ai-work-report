import json
from datetime import datetime
from typing import List, Set

from pynput import keyboard

try:
    from AppKit import NSWorkspace
    from Quartz import (CGWindowListCopyWindowInfo, kCGNullWindowID,
                        kCGWindowListOptionOnScreenOnly)

except ImportError:
    print("AppKit or Quartz not found. Please install PyObjC using: pip install pyobjc")
    raise

def get_focused_window_title() -> str:
    curr_app = NSWorkspace.sharedWorkspace().frontmostApplication()
    curr_pid = NSWorkspace.sharedWorkspace().activeApplication(
    )['NSApplicationProcessIdentifier']
    curr_app_name = curr_app.localizedName()
    options = kCGWindowListOptionOnScreenOnly
    windowList = CGWindowListCopyWindowInfo(options, kCGNullWindowID)
    for window in windowList:
        pid = window['kCGWindowOwnerPID']
        windowNumber = window['kCGWindowNumber']
        ownerName = window['kCGWindowOwnerName']
        geometry = window['kCGWindowBounds']
        windowTitle = window.get('kCGWindowName', u'Unknown')
        if curr_pid == pid:
            return "%s - %s" % (ownerName, windowTitle.encode(
                'ascii', 'ignore'))

def key_events_to_text(key_names: List[str]) -> str:
    text = []
    shift_pressed = False
    for key_name in key_names:
        if key_name == 'shift':
            shift_pressed = True
            continue

        if shift_pressed:
            if key_name.isalpha():
                text.append(key_name.upper())
            elif key_name.isdigit():
                shift_mapping = {
                    '0': ')',
                    '1': '!',
                    '2': '@',
                    '3': '#',
                    '4': '$',
                    '5': '%',
                    '6': '^',
                    '7': '&',
                    '8': '*',
                    '9': '(',
                }
                text.append(shift_mapping.get(key_name, key_name))
            else:
                special_shift_mapping = {
                    '-': '_',
                    '=': '+',
                    '[': '{',
                    ']': '}',
                    '\\': '|',
                    ';': ':',
                    "'": '"',
                    ',': '<',
                    '.': '>',
                    '/': '?',
                }
                text.append(special_shift_mapping.get(key_name, key_name))
            shift_pressed = False
        else:
            if key_name == 'space':
                text.append(' ')
            elif key_name == 'enter':
                text.append('\n')
            elif key_name == 'backspace':
                if text:
                    text.pop()
            elif key_name == 'tab':
                text.append('\t')
            elif key_name.isalnum() or key_name in ['-', '=', '[', ']', '\\', ';', "'", ',', '.', '/']:
                text.append(key_name)
            else:
                pass  # Ignore other key events

    return ''.join(text)

def save_events_to_file(keys: List[str], start_time: str, end_time: str, window_title: str, file_name: str = 'keyboard_events.jsonl'):
    event_data = {
        'timeStart': start_time,
        'timeEnd': end_time,
        'keys': key_events_to_text(keys),
        'windowTitle': window_title,
    }

    with open(file_name, 'a') as f:
        f.write(json.dumps(event_data) + '\n')

"""
When a key is pressed, if the focused window has changed, save the previous window's events to a
file, and then reset the keys pressed and the focus start time.
:param key: The key that was pressed
"""
def on_press(key):
    global focused_window_title, keys_pressed, focus_start_time

    current_window_title = get_focused_window_title()

    if current_window_title != focused_window_title:
        focus_end_time = datetime.now().strftime('%H:%M:%S %Y-%m-%d')
        save_events_to_file(keys_pressed, focus_start_time, focus_end_time, focused_window_title)
        keys_pressed = list()
        focus_start_time = focus_end_time

    key_name = (str(key) if hasattr(key, 'char') else key.name).replace("'", "")
    print(key_name)
    keys_pressed.append(key_name)
    focused_window_title = current_window_title

def on_release(key):
    pass

focused_window_title = get_focused_window_title()
keys_pressed = set()
focus_start_time = datetime.now().strftime('%H:%M:%S %Y-%m-%d')

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
