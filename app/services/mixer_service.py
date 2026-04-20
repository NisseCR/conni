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

    def toggle_ambience(self, name: str, path: str) -> bool:
        """
        Toggle an ambience layer on or off.

        If the layer is already active, it is removed.
        If it is not active, it is added if capacity allows.

        Args:
            name: Ambience folder name.
            path: Ambience folder path.

        Returns:
            True if the layer was added, False if it was removed or rejected.
        """
        existing = next((layer for layer in self.state.active_ambience if layer.name == name), None)
        if existing is not None:
            self.state.active_ambience = [
                layer for layer in self.state.active_ambience if layer.name != name
            ]
            return False

        if len(self.state.active_ambience) >= self.state.max_ambience_layers:
            return False

        self.state.active_ambience.append(
            AmbienceLayer(name=name, path=path)
        )
        return True

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