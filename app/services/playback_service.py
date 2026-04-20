from __future__ import annotations

from app.services.mixer_service import MixerService


class PlaybackService:
    """
    High-level playback operations used by routes and hotkeys.
    """

    def __init__(self, mixer: MixerService) -> None:
        """
        Initialize playback service.

        Args:
            mixer: Shared mixer service instance.
        """
        self.mixer = mixer

    def play_playlist(self, playlist_name: str) -> None:
        """
        Start a playlist using the explicit transition behavior.
        """
        self.mixer.switch_playlist(playlist_name)

    def switch_playlist(self, playlist_name: str) -> None:
        """
        Switch to another playlist using the explicit transition behavior.
        """
        self.mixer.switch_playlist(playlist_name)

    def skip(self) -> None:
        """
        Skip the current track using the explicit transition behavior.
        """
        self.mixer.skip_track()

    def advance(self) -> None:
        """
        Advance naturally to the next track without a fade.
        """
        self.mixer.advance_track()

    def stop(self) -> None:
        """
        Stop music playback.
        """
        self.mixer.stop_music()

    def toggle_ambience(self, name: str, path: str) -> bool:
        """
        Toggle an ambience layer.
        """
        return self.mixer.toggle_ambience(name, path)

    def clear_ambience(self) -> None:
        """
        Remove all active ambience layers.
        """
        self.mixer.clear_ambience()