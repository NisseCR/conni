from pynput import keyboard


class HotkeyService:
    """
    Registers global keyboard shortcuts for music actions only.
    """

    def __init__(self, playback_service) -> None:
        """
        Initialize the hotkey service.

        Args:
            playback_service: Shared playback service instance.
        """
        self.playback_service = playback_service

    def run(self) -> None:
        """
        Start listening for global hotkeys.
        """
        print("Hotkeys enabled.")
        with keyboard.GlobalHotKeys(self._bindings()) as listener:
            listener.join()

    def _bindings(self) -> dict[str, callable]:
        """
        Define hotkey mappings for music only.
        """
        return {
            "<shift>+1": lambda: self._trigger_playlist("frontier"),
            "<shift>+2": lambda: self._trigger_playlist("dissonance"),
            "<shift>+q": self._trigger_skip,
            "<shift>+w": self._trigger_stop,
        }

    def _trigger_playlist(self, playlist_name: str) -> None:
        """
        Trigger playlist playback and print a debug message.
        """
        print(f"Hotkey: play {playlist_name}")
        self.playback_service.play_playlist(playlist_name)

    def _trigger_skip(self) -> None:
        """
        Trigger track skip and print a debug message.
        """
        print("Hotkey: skip")
        self.playback_service.skip()

    def _trigger_stop(self) -> None:
        """
        Trigger stop and print a debug message.
        """
        print("Hotkey: stop")
        self.playback_service.stop()