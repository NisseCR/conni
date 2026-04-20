from __future__ import annotations

from app.models.state import AmbienceLayer, PlaybackState


class MixerService:
    """
    Owns shared playback state and later will own the real audio engine.
    """

    def __init__(self, max_ambience_layers: int = 4) -> None:
        """
        Initialize playback state.

        Args:
            max_ambience_layers: Default maximum number of active ambience layers.
        """
        self.state = PlaybackState(max_ambience_layers=max_ambience_layers)

    def start_playlist(self, playlist_name: str) -> None:
        """
        Start a playlist.

        Args:
            playlist_name: Playlist to start.
        """
        self.state.current_playlist = playlist_name
        self.state.current_track_index = 0
        self.state.is_music_playing = True

    def switch_playlist(self, playlist_name: str) -> None:
        """
        Switch playlists with a conceptual crossfade.

        Args:
            playlist_name: Next playlist.
        """
        self.state.current_playlist = playlist_name
        self.state.current_track_index = 0
        self.state.is_music_playing = True

    def skip_track(self) -> None:
        """
        Skip the current track.
        """
        self.state.current_track_index += 1

    def stop_music(self) -> None:
        """
        Stop music playback.
        """
        self.state.is_music_playing = False

    def add_ambience(self, name: str, path: str, volume: float = 1.0) -> bool:
        """
        Add a new ambience layer if capacity allows.

        Args:
            name: Ambience name.
            path: File path to the ambience audio.
            volume: Layer volume.

        Returns:
            True if the layer was added, otherwise False.
        """
        if len(self.state.active_ambience) >= self.state.max_ambience_layers:
            return False

        self.state.active_ambience.append(
            AmbienceLayer(name=name, path=path, volume=self._clamp(volume))
        )
        return True

    def remove_ambience(self, name: str) -> bool:
        """
        Remove an active ambience layer by name.

        Args:
            name: Layer name to remove.

        Returns:
            True if removed, otherwise False.
        """
        before = len(self.state.active_ambience)
        self.state.active_ambience = [
            layer for layer in self.state.active_ambience if layer.name != name
        ]
        return len(self.state.active_ambience) != before

    def clear_ambience(self) -> None:
        """
        Remove all active ambience layers.
        """
        self.state.active_ambience.clear()

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