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
        """
        raise NotImplementedError

    @abstractmethod
    def switch_playlist(self, playlist_name: str, fade_ms: int = 0) -> None:
        """
        Switch to another music playlist with an explicit transition.
        """
        raise NotImplementedError

    @abstractmethod
    def skip_track(self, fade_ms: int = 0) -> None:
        """
        Skip to the next track in the current playlist with an explicit transition.
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
        """
        raise NotImplementedError

    @abstractmethod
    def start_ambience(self, layer_name: str, path: str, fade_ms: int = 0) -> None:
        """
        Start an ambience layer.
        """
        raise NotImplementedError

    @abstractmethod
    def stop_ambience(self, layer_name: str, fade_ms: int = 0) -> None:
        """
        Stop an ambience layer.
        """
        raise NotImplementedError

    @abstractmethod
    def stop_all_ambience(self, fade_ms: int = 0) -> None:
        """
        Stop all active ambience layers.
        """
        raise NotImplementedError

    @abstractmethod
    def set_master_volume(self, volume: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_music_volume(self, volume: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_ambience_volume(self, volume: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def set_ambience_layer_volume(self, layer_name: str, volume: float) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_current_track_title(self) -> str | None:
        """
        Return the currently loaded music track title, if any.
        """
        raise NotImplementedError