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
        Start a playlist.
        """
        self.mixer.start_playlist(playlist_name)

    def switch_playlist(self, playlist_name: str) -> None:
        """
        Switch to another playlist.
        """
        self.mixer.switch_playlist(playlist_name)

    def skip(self) -> None:
        """
        Skip the current track.
        """
        self.mixer.skip_track()

    def stop(self) -> None:
        """
        Stop music playback.
        """
        self.mixer.stop_music()

    def add_ambience(self, name: str, path: str, volume: float = 1.0) -> bool:
        """
        Add an ambience layer.
        """
        return self.mixer.add_ambience(name, path, volume)

    def remove_ambience(self, name: str) -> bool:
        """
        Remove an ambience layer.
        """
        return self.mixer.remove_ambience(name)

    def clear_ambience(self) -> None:
        """
        Remove all ambience layers.
        """
        self.mixer.clear_ambience()