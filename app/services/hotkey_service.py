from pynput import keyboard

from app.services.playback_service import PlaybackService


class HotkeyService:
    """
    Registers global keyboard shortcuts for music actions only.
    """

    def __init__(self, playback_service: PlaybackService) -> None:
        """
        Initialize hotkey service.

        Args:
            playback_service: Shared playback service instance.
        """
        self.playback_service = playback_service

    def run(self) -> None:
        """
        Start listening for global hotkeys.
        """
        with keyboard.GlobalHotKeys(self._bindings()) as listener:
            listener.join()

    def _bindings(self) -> dict[str, callable]:
        """
        Define hotkey mappings for music only.
        """
        return {
            "<shift>+1": lambda: self.playback_service.play_playlist("Somber Journey"),
            "<shift>+2": lambda: self.playback_service.play_playlist("Hopeful Dawn"),
            "<shift>+q": self.playback_service.skip,
            "<shift>+w": self.playback_service.stop,
        }