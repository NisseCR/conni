from __future__ import annotations

from pynput import keyboard

from app.services.playback_service import PlaybackService


class HotkeyService:
    """
    Registers global keyboard shortcuts for music actions only.
    """

    def __init__(self, playback_service: PlaybackService) -> None:
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

        Returns:
            Dictionary of shortcut strings mapped to callbacks.
        """
        return {
            "<shift>+1": lambda: self.playback_service.switch_playlist("frontier"),
            "<shift>+2": lambda: self.playback_service.switch_playlist("dissonance"),
            "<shift>+q": self.playback_service.skip,
            "<shift>+w": self.playback_service.stop,
        }