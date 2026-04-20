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
        """
        self.backend = backend
        self.state = PlaybackState(max_ambience_layers=max_ambience_layers)

    def start_playlist(self, playlist_name: str) -> None:
        """
        Start a playlist and update state.
        """
        self.state.current_playlist = playlist_name
        self.state.current_track_index = 0
        self.state.is_music_playing = True
        self.backend.play_playlist(playlist_name, fade_ms=self.state.music_crossfade_ms)
        self.state.current_track_title = self.backend.get_current_track_title()

    def switch_playlist(self, playlist_name: str) -> None:
        """
        Switch playlists and update state.
        """
        self.state.current_playlist = playlist_name
        self.state.current_track_index = 0
        self.state.is_music_playing = True
        self.backend.switch_playlist(playlist_name, fade_ms=self.state.music_crossfade_ms)
        self.state.current_track_title = self.backend.get_current_track_title()

    def skip_track(self) -> None:
        """
        Skip to the next track in the current playlist.
        """
        self.state.current_track_index += 1
        self.backend.skip_track(fade_ms=self.state.music_crossfade_ms)
        self.state.current_track_title = self.backend.get_current_track_title()

    def advance_track(self) -> None:
        """
        Advance to the next track naturally, without a manual fade transition.
        """
        self.state.current_track_index += 1
        self.backend.advance_track()
        self.state.current_track_title = self.backend.get_current_track_title()

    def stop_music(self) -> None:
        """
        Stop music playback.
        """
        self.state.is_music_playing = False
        self.backend.stop_music(fade_ms=self.state.music_crossfade_ms)
        self.state.current_track_title = None

    def toggle_ambience(self, name: str, path: str) -> bool:
        """
        Toggle an ambience layer on or off.
        """
        existing = next((layer for layer in self.state.active_ambience if layer.name == name), None)
        if existing is not None:
            self.state.active_ambience = [
                layer for layer in self.state.active_ambience if layer.name != name
            ]
            self.backend.stop_ambience(name, fade_ms=self.state.ambience_crossfade_ms)
            return False

        if len(self.state.active_ambience) >= self.state.max_ambience_layers:
            return False

        self.state.active_ambience.append(AmbienceLayer(name=name, path=path))
        self.backend.start_ambience(name, path, fade_ms=self.state.ambience_crossfade_ms)
        return True

    def clear_ambience(self) -> None:
        """
        Remove all active ambience layers.
        """
        self.state.active_ambience.clear()
        self.backend.stop_all_ambience(fade_ms=self.state.ambience_crossfade_ms)

    def set_master_volume(self, volume: float) -> None:
        """
        Set master volume.
        """
        self.state.master_volume = self._clamp(volume)
        self.backend.set_master_volume(self.state.master_volume)

    def set_music_volume(self, volume: float) -> None:
        """
        Set music volume.
        """
        self.state.music_volume = self._clamp(volume)
        self.backend.set_music_volume(self.state.music_volume)

    def set_ambience_volume(self, volume: float) -> None:
        """
        Set ambience volume for the global ambience level.
        """
        self.state.ambience_volume = self._clamp(volume)
        self.backend.set_ambience_volume(self.state.ambience_volume)

    def set_ambience_layer_volume(self, layer_name: str, volume: float) -> None:
        """
        Set volume for a single active ambience layer.
        """
        layer = next((item for item in self.state.active_ambience if item.name == layer_name), None)
        if layer is not None:
            layer.volume = self._clamp(volume)
            self.backend.set_ambience_layer_volume(layer_name, layer.volume)

    def _clamp(self, value: float) -> float:
        """
        Clamp a value to the 0.0 to 1.0 range.
        """
        return max(0.0, min(1.0, value))