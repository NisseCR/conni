from pynput import keyboard


def on_hotkey():
    print("Hotkey pressed!")


with keyboard.GlobalHotKeys({
    "<shift>+1": on_hotkey,
    "<shift>+q": on_hotkey,
}) as listener:
    print("Listening...")
    listener.join()