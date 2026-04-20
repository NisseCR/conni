from __future__ import annotations

import threading
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

        self._active_ambience_channels: dict[str, pygame.mixer.Channel] = {}
        self._cached_ambience_sounds: dict[str, pygame.mixer.Sound] = {}

        self._current_playlist: str | None = None
        self._current_track_index: int = 0

        self._preload_ambience_sounds()

    def play_playlist(self, playlist_name: str) -> None:
        """
        Start playing a playlist from the first track.

        Args:
            playlist_name: Playlist folder name.
        """
        with self._lock:
            playlist_folder = self.music_root / playlist_name
            tracks = self._list_audio_files(playlist_folder)
            if not tracks:
                return

            self._current_playlist = playlist_name
            self._current_track_index = 0
            self._play_music_file(tracks[0])

    def skip_track(self) -> None:
        """
        Skip to the next track in the current playlist.
        """
        with self._lock:
            if self._current_playlist is None:
                return

            playlist_folder = self.music_root / self._current_playlist
            tracks = self._list_audio_files(playlist_folder)
            if not tracks:
                return

            self._current_track_index = (self._current_track_index + 1) % len(tracks)
            self._play_music_file(tracks[self._current_track_index])

    def stop_music(self) -> None:
        """
        Stop playlist playback.
        """
        with self._lock:
            pygame.mixer.music.stop()
            self._current_playlist = None
            self._current_track_index = 0

    def start_ambience(self, layer_name: str, path: str) -> None:
        """
        Start looping an ambience file on its own channel.

        Args:
            layer_name: Unique ambience layer name.
            path: Relative path to the audio file under media/.
        """
        with self._lock:
            if layer_name in self._active_ambience_channels:
                self.stop_ambience(layer_name)

            sound = self._cached_ambience_sounds.get(path)
            if sound is None:
                return

            channel = self._get_free_channel()
            if channel is None:
                return

            channel.play(sound, loops=-1)
            self._active_ambience_channels[layer_name] = channel

    def stop_ambience(self, layer_name: str) -> None:
        """
        Stop a specific ambience layer.

        Args:
            layer_name: Unique ambience layer name.
        """
        with self._lock:
            channel = self._active_ambience_channels.pop(layer_name, None)
            if channel is not None:
                channel.stop()

    def stop_all_ambience(self) -> None:
        """
        Stop all currently active ambience layers.
        """
        with self._lock:
            for channel in self._active_ambience_channels.values():
                channel.stop()
            self._active_ambience_channels.clear()

    def _preload_ambience_sounds(self) -> None:
        """
        Load all ambience sounds into memory once.

        This reduces audio hiccups when ambience layers are toggled on later.
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

    def _play_music_file(self, file_path: Path) -> None:
        """
        Load and play a music file.

        Args:
            file_path: Absolute path to the audio file.
        """
        pygame.mixer.music.load(str(file_path))
        pygame.mixer.music.play()

    def _list_audio_files(self, folder: Path) -> list[Path]:
        """
        Return audio files inside a folder in sorted order.

        Args:
            folder: Folder to scan.

        Returns:
            Sorted list of audio file paths.
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

        Returns:
            A free pygame mixer channel, or None if none are available.
        """
        for index in range(pygame.mixer.get_num_channels()):
            channel = pygame.mixer.Channel(index)
            if not channel.get_busy():
                return channel
        return None