from __future__ import annotations

from abc import ABC, abstractmethod


class AudioBackend(ABC):
    """
    Abstract audio backend used by the mixer service.

    This keeps the UI and playback logic independent from the
    actual audio implementation.
    """

    @abstractmethod
    def play_playlist(self, playlist_name: str) -> None:
        """
        Start playing a music playlist.

        Args:
            playlist_name: Name of the playlist to start.
        """
        raise NotImplementedError

    @abstractmethod
    def skip_track(self) -> None:
        """
        Skip to the next track in the current playlist.
        """
        raise NotImplementedError

    @abstractmethod
    def stop_music(self) -> None:
        """
        Stop playlist playback.
        """
        raise NotImplementedError

    @abstractmethod
    def start_ambience(self, layer_name: str, path: str) -> None:
        """
        Start an ambience layer.

        Args:
            layer_name: Unique layer name.
            path: Relative path to the audio file.
        """
        raise NotImplementedError

    @abstractmethod
    def stop_ambience(self, layer_name: str) -> None:
        """
        Stop an ambience layer.

        Args:
            layer_name: Unique layer name.
        """
        raise NotImplementedError

    @abstractmethod
    def stop_all_ambience(self) -> None:
        """
        Stop all active ambience layers.
        """
        raise NotImplementedError