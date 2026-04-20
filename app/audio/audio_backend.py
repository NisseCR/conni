from __future__ import annotations

from abc import ABC, abstractmethod


class AudioBackend(ABC):
    """
    Abstract audio backend used by the mixer service.

    This keeps the UI and playback logic independent from the
    actual audio implementation.
    """

    @abstractmethod
    def play_playlist(self, playlist_name: str, fade_ms: int = 0) -> None:
        """
        Start playing a music playlist.

        Args:
            playlist_name: Name of the playlist to start.
            fade_ms: Fade-in duration in milliseconds.
        """
        raise NotImplementedError

    @abstractmethod
    def switch_playlist(self, playlist_name: str, fade_ms: int = 0) -> None:
        """
        Switch to another music playlist with an explicit transition.

        Args:
            playlist_name: Name of the next playlist.
            fade_ms: Fade duration in milliseconds.
        """
        raise NotImplementedError

    @abstractmethod
    def skip_track(self, fade_ms: int = 0) -> None:
        """
        Skip to the next track in the current playlist with an explicit transition.

        Args:
            fade_ms: Fade duration in milliseconds.
        """
        raise NotImplementedError

    @abstractmethod
    def advance_track(self) -> None:
        """
        Advance to the next track naturally, without a fade transition.
        """
        raise NotImplementedError

    @abstractmethod
    def stop_music(self, fade_ms: int = 0) -> None:
        """
        Stop playlist playback.

        Args:
            fade_ms: Fade-out duration in milliseconds.
        """
        raise NotImplementedError

    @abstractmethod
    def start_ambience(self, layer_name: str, path: str, fade_ms: int = 0) -> None:
        """
        Start an ambience layer.

        Args:
            layer_name: Unique layer name.
            path: Relative path to the audio file.
            fade_ms: Fade-in duration in milliseconds.
        """
        raise NotImplementedError

    @abstractmethod
    def stop_ambience(self, layer_name: str, fade_ms: int = 0) -> None:
        """
        Stop an ambience layer.

        Args:
            layer_name: Unique layer name.
            fade_ms: Fade-out duration in milliseconds.
        """
        raise NotImplementedError

    @abstractmethod
    def stop_all_ambience(self, fade_ms: int = 0) -> None:
        """
        Stop all active ambience layers.

        Args:
            fade_ms: Fade-out duration in milliseconds.
        """
        raise NotImplementedError