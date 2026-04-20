from __future__ import annotations

import random
import threading
import time
from pathlib import Path

import pygame

from app.audio.audio_backend import AudioBackend


class PygameAudioBackend(AudioBackend):
    """
    Real-time audio backend built on pygame.

    This backend provides a minimal MVP implementation for music playback
    and looping ambience layers, with cached ambience sounds to reduce
    start-up hiccups.
    """

    def __init__(self, music_root: str = "media/music", ambience_root: str = "media/ambience") -> None:
        """
        Initialize pygame audio and prepare channel management.

        Args:
            music_root: Root folder containing music playlists.
            ambience_root: Root folder containing ambience folders.
        """
        pygame.mixer.init()
        pygame.mixer.set_num_channels(16)

        self.music_root = Path(music_root)
        self.ambience_root = Path(ambience_root)

        self._lock = threading.Lock()
        self._stop_watcher = threading.Event()
        self._manual_transition_until = 0.0

        self._active_ambience_channels: dict[str, pygame.mixer.Channel] = {}
        self._cached_ambience_sounds: dict[str, pygame.mixer.Sound] = {}

        self._current_playlist: str | None = None
        self._shuffled_tracks: list[Path] = []
        self._current_track_index: int = 0

        self._music_volume: float = 1.0
        self._master_volume: float = 1.0
        self._ambience_volume: float = 1.0

        self._preload_ambience_sounds()

    def start_music_watcher(self) -> None:
        """
        Start a background loop that advances the playlist when a track ends.
        """
        while not self._stop_watcher.is_set():
            should_advance = False

            with self._lock:
                has_playlist = bool(self._shuffled_tracks)
                music_busy = pygame.mixer.music.get_busy()
                in_manual_transition = time.monotonic() < self._manual_transition_until

                if has_playlist and not music_busy and not in_manual_transition:
                    should_advance = True

            if should_advance:
                self.advance_track()

            time.sleep(0.2)

    def stop_music_watcher(self) -> None:
        """
        Stop the background watcher loop.
        """
        self._stop_watcher.set()

    def play_playlist(self, playlist_name: str, fade_ms: int = 0) -> None:
        """
        Start playing a shuffled playlist from the first track.

        Args:
            playlist_name: Playlist folder name.
            fade_ms: Fade-in duration in milliseconds.
        """
        with self._lock:
            playlist_folder = self.music_root / playlist_name
            tracks = self._list_audio_files(playlist_folder)
            if not tracks:
                return

            self._current_playlist = playlist_name
            self._shuffled_tracks = tracks[:]
            random.shuffle(self._shuffled_tracks)
            self._current_track_index = 0
            self._play_music_file(self._shuffled_tracks[0], fade_ms=fade_ms)

    def switch_playlist(self, playlist_name: str, fade_ms: int = 0) -> None:
        """
        Switch to another playlist using an explicit fade transition.

        Args:
            playlist_name: Playlist folder name.
            fade_ms: Fade duration in milliseconds.
        """
        with self._lock:
            self._mark_manual_transition(fade_ms)
            self._fade_out_music(fade_ms)

            playlist_folder = self.music_root / playlist_name
            tracks = self._list_audio_files(playlist_folder)
            if not tracks:
                return

            self._current_playlist = playlist_name
            self._shuffled_tracks = tracks[:]
            random.shuffle(self._shuffled_tracks)
            self._current_track_index = 0
            self._play_music_file(self._shuffled_tracks[0], fade_ms=fade_ms)

    def skip_track(self, fade_ms: int = 0) -> None:
        """
        Skip to the next track in the current playlist using an explicit fade transition.

        Args:
            fade_ms: Fade duration in milliseconds.
        """
        with self._lock:
            if not self._shuffled_tracks:
                return

            self._mark_manual_transition(fade_ms)
            self._fade_out_music(fade_ms)
            self._current_track_index = (self._current_track_index + 1) % len(self._shuffled_tracks)
            self._play_music_file(self._shuffled_tracks[self._current_track_index], fade_ms=fade_ms)

    def advance_track(self) -> None:
        """
        Advance to the next track naturally, without a fade transition.
        """
        with self._lock:
            if not self._shuffled_tracks:
                return

            self._current_track_index = (self._current_track_index + 1) % len(self._shuffled_tracks)
            self._play_music_file(self._shuffled_tracks[self._current_track_index], fade_ms=0)

    def stop_music(self, fade_ms: int = 0) -> None:
        """
        Stop playlist playback.

        Args:
            fade_ms: Fade-out duration in milliseconds.
        """
        with self._lock:
            self._mark_manual_transition(fade_ms)
            self._fade_out_music(fade_ms)
            self._current_playlist = None
            self._shuffled_tracks = []
            self._current_track_index = 0

    def start_ambience(self, layer_name: str, path: str, fade_ms: int = 0) -> None:
        """
        Start looping an ambience file on its own channel.

        Args:
            layer_name: Unique ambience layer name.
            path: Relative path to the audio file under media/.
            fade_ms: Fade-in duration in milliseconds.
        """
        with self._lock:
            if layer_name in self._active_ambience_channels:
                self.stop_ambience(layer_name, fade_ms=fade_ms)

            sound = self._cached_ambience_sounds.get(path)
            if sound is None:
                return

            channel = self._get_free_channel()
            if channel is None:
                return

            channel.play(sound, loops=-1, fade_ms=fade_ms)
            channel.set_volume(self._ambience_volume * self._master_volume)
            self._active_ambience_channels[layer_name] = channel

    def stop_ambience(self, layer_name: str, fade_ms: int = 0) -> None:
        """
        Stop a specific ambience layer.

        Args:
            layer_name: Unique ambience layer name.
            fade_ms: Fade-out duration in milliseconds.
        """
        with self._lock:
            channel = self._active_ambience_channels.pop(layer_name, None)
            if channel is not None:
                if fade_ms > 0:
                    channel.fadeout(fade_ms)
                else:
                    channel.stop()

    def stop_all_ambience(self, fade_ms: int = 0) -> None:
        """
        Stop all currently active ambience layers.

        Args:
            fade_ms: Fade-out duration in milliseconds.
        """
        with self._lock:
            for channel in self._active_ambience_channels.values():
                if fade_ms > 0:
                    channel.fadeout(fade_ms)
                else:
                    channel.stop()
            self._active_ambience_channels.clear()

    def set_music_volume(self, volume: float) -> None:
        """
        Set music playback volume.
        """
        with self._lock:
            self._music_volume = self._clamp(volume)
            self._apply_music_volume()

    def set_master_volume(self, volume: float) -> None:
        """
        Set global master volume.
        """
        with self._lock:
            self._master_volume = self._clamp(volume)
            self._apply_music_volume()
            self._apply_ambience_volumes()

    def set_ambience_volume(self, volume: float) -> None:
        """
        Set global ambience volume.
        """
        with self._lock:
            self._ambience_volume = self._clamp(volume)
            self._apply_ambience_volumes()

    def set_ambience_layer_volume(self, layer_name: str, volume: float) -> None:
        """
        Set volume for a single active ambience layer.
        """
        with self._lock:
            channel = self._active_ambience_channels.get(layer_name)
            if channel is not None:
                channel.set_volume(self._ambience_volume * self._master_volume * self._clamp(volume))

    def _apply_music_volume(self) -> None:
        """
        Apply the current music volume to the pygame music channel.
        """
        pygame.mixer.music.set_volume(self._music_volume * self._master_volume)

    def _apply_ambience_volumes(self) -> None:
        """
        Apply the current ambience and master volume to all active ambience channels.
        """
        for layer_name, channel in self._active_ambience_channels.items():
            channel.set_volume(self._ambience_volume * self._master_volume)

    def _mark_manual_transition(self, fade_ms: int) -> None:
        """
        Mark a short grace period during which the watcher must not auto-advance.
        """
        grace_seconds = max(0.5, (fade_ms / 1000.0) + 0.5)
        self._manual_transition_until = time.monotonic() + grace_seconds

    def _fade_out_music(self, fade_ms: int) -> None:
        """
        Fade out currently playing music if a fade duration is provided.
        """
        if fade_ms > 0:
            pygame.mixer.music.fadeout(fade_ms)
        else:
            pygame.mixer.music.stop()

    def _preload_ambience_sounds(self) -> None:
        """
        Load all ambience sounds into memory once.
        """
        if not self.ambience_root.exists():
            return

        audio_extensions = {".mp3", ".ogg", ".wav", ".flac", ".m4a"}

        for folder in self.ambience_root.iterdir():
            if not folder.is_dir():
                continue

            for item in folder.iterdir():
                if (
                    item.is_file()
                    and item.suffix.lower() in audio_extensions
                    and item.stem.lower() not in {"cover", "folder"}
                ):
                    relative_path = f"ambience/{folder.name}/{item.name}"
                    try:
                        self._cached_ambience_sounds[relative_path] = pygame.mixer.Sound(str(item))
                    except pygame.error:
                        continue

    def _play_music_file(self, file_path: Path, fade_ms: int = 0) -> None:
        """
        Load and play a music file.
        """
        pygame.mixer.music.load(str(file_path))
        pygame.mixer.music.play(fade_ms=fade_ms)
        self._apply_music_volume()

    def _list_audio_files(self, folder: Path) -> list[Path]:
        """
        Return audio files inside a folder in sorted order.
        """
        if not folder.exists() or not folder.is_dir():
            return []

        audio_extensions = {".mp3", ".ogg", ".wav", ".flac", ".m4a"}
        return sorted(
            [
                item
                for item in folder.iterdir()
                if item.is_file()
                and item.suffix.lower() in audio_extensions
                and item.stem.lower() not in {"cover", "folder"}
            ]
        )

    def _get_free_channel(self) -> pygame.mixer.Channel | None:
        """
        Find a free mixer channel for ambience playback.
        """
        for index in range(pygame.mixer.get_num_channels()):
            channel = pygame.mixer.Channel(index)
            if not channel.get_busy():
                return channel
        return None

    def _clamp(self, value: float) -> float:
        """
        Clamp a value to the 0.0 to 1.0 range.
        """
        return max(0.0, min(1.0, value))