from __future__ import annotations

from app.audio.audio_backend import AudioBackend
from app.models.state import AmbienceLayer, PlaybackState


class MixerService:
    """
    Owns playback state and forwards playback actions to the audio backend.
    """

    def __init__(self, backend: AudioBackend, max_ambience_layers: int = 4) -> None:
        """
        Initialize playback state and backend.

        Args:
            backend: Audio backend implementation.
            max_ambience_layers: Default maximum number of active ambience layers.
        """
        self.backend = backend
        self.state = PlaybackState(max_ambience_layers=max_ambience_layers)

    def start_playlist(self, playlist_name: str) -> None:
        """
        Start a playlist and update state.

        Args:
            playlist_name: Playlist folder name.
        """
        self.state.current_playlist = playlist_name
        self.state.current_track_index = 0
        self.state.is_music_playing = True
        self.backend.play_playlist(playlist_name)

    def switch_playlist(self, playlist_name: str) -> None:
        """
        Switch playlists and update state.

        Args:
            playlist_name: Playlist folder name.
        """
        self.state.current_playlist = playlist_name
        self.state.current_track_index = 0
        self.state.is_music_playing = True
        self.backend.play_playlist(playlist_name)

    def skip_track(self) -> None:
        """
        Skip to the next track in the current playlist.
        """
        self.state.current_track_index += 1
        self.backend.skip_track()

    def stop_music(self) -> None:
        """
        Stop music playback.
        """
        self.state.is_music_playing = False
        self.backend.stop_music()

    def toggle_ambience(self, name: str, path: str) -> bool:
        """
        Toggle an ambience layer on or off.

        Args:
            name: Unique layer name.
            path: Relative path to the ambience file.

        Returns:
            True if added, False if removed or rejected.
        """
        existing = next((layer for layer in self.state.active_ambience if layer.name == name), None)
        if existing is not None:
            self.state.active_ambience = [
                layer for layer in self.state.active_ambience if layer.name != name
            ]
            self.backend.stop_ambience(name)
            return False

        if len(self.state.active_ambience) >= self.state.max_ambience_layers:
            return False

        self.state.active_ambience.append(AmbienceLayer(name=name, path=path))
        self.backend.start_ambience(name, path)
        return True

    def clear_ambience(self) -> None:
        """
        Remove all active ambience layers.
        """
        self.state.active_ambience.clear()
        self.backend.stop_all_ambience()

    def set_master_volume(self, volume: float) -> None:
        """
        Set master volume.
        """
        self.state.master_volume = self._clamp(volume)

    def set_music_volume(self, volume: float) -> None:
        """
        Set music volume.
        """
        self.state.music_volume = self._clamp(volume)

    def set_ambience_volume(self, volume: float) -> None:
        """
        Set ambience volume.
        """
        self.state.ambience_volume = self._clamp(volume)

    def _clamp(self, value: float) -> float:
        """
        Clamp a value to the 0.0 to 1.0 range.
        """
        return max(0.0, min(1.0, value))
