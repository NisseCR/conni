from __future__ import annotations

import logging

from app.audio.audio_backend import AudioBackend


class SimpleAudioBackend(AudioBackend):
    """
    Minimal audio backend placeholder.

    This backend does not play real audio yet.
    It only logs requested actions so the control flow can be tested
    before wiring in a real player library.
    """

    def play_playlist(self, playlist_name: str) -> None:
        """
        Log playlist playback.
        """
        logging.info("Play playlist: %s", playlist_name)

    def skip_track(self) -> None:
        """
        Log track skip.
        """
        logging.info("Skip current track")

    def stop_music(self) -> None:
        """
        Log stopping music playback.
        """
        logging.info("Stop music")

    def start_ambience(self, layer_name: str, path: str) -> None:
        """
        Log ambience playback.
        """
        logging.info("Start ambience layer: %s (%s)", layer_name, path)

    def stop_ambience(self, layer_name: str) -> None:
        """
        Log ambience stop.
        """
        logging.info("Stop ambience layer: %s", layer_name)

    def stop_all_ambience(self) -> None:
        """
        Log stopping all ambience layers.
        """
        logging.info("Stop all ambience layers")
