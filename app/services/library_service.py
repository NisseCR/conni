from __future__ import annotations

from pathlib import Path

from app.models.media import AmbienceFolderItem, AmbienceTrackItem, PlaylistItem


AUDIO_EXTENSIONS = {".mp3", ".wav", ".ogg", ".flac", ".m4a"}
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
THUMBNAIL_NAMES = {"cover", "folder"}


class LibraryService:
    """
    Scans the local media folders and exposes them to the API/UI.
    """

    def __init__(self, music_dir: str = "media/music", ambience_dir: str = "media/ambience") -> None:
        """
        Initialize the library service.

        Args:
            music_dir: Folder containing playlist folders.
            ambience_dir: Folder containing ambience folders.
        """
        self.music_dir = Path(music_dir)
        self.ambience_dir = Path(ambience_dir)

    def list_playlists(self) -> list[PlaylistItem]:
        """
        Discover music playlists from subfolders.
        """
        playlists: list[PlaylistItem] = []

        if not self.music_dir.exists():
            return playlists

        for folder in sorted(self.music_dir.iterdir()):
            if folder.is_dir():
                playlists.append(
                    PlaylistItem(
                        title=folder.name,
                        path=f"music/{folder.name}",
                        thumbnail=self._find_thumbnail(folder, base_prefix=f"music/{folder.name}"),
                    )
                )

        return playlists

    def list_ambience(self) -> list[AmbienceFolderItem]:
        """
        Discover ambience collections from subfolders.
        """
        ambience: list[AmbienceFolderItem] = []

        if not self.ambience_dir.exists():
            return ambience

        for folder in sorted(self.ambience_dir.iterdir()):
            if not folder.is_dir():
                continue

            tracks = self._collect_audio_files(folder)
            if not tracks:
                continue

            base_prefix = f"ambience/{folder.name}"
            ambience.append(
                AmbienceFolderItem(
                    title=folder.name,
                    path=base_prefix,
                    thumbnail=self._find_thumbnail(folder, base_prefix=base_prefix),
                    tracks=[
                        AmbienceTrackItem(
                            title=track.stem,
                            path=f"{base_prefix}/{track.name}",
                        )
                        for track in tracks
                    ],
                )
            )

        return ambience

    def get_ambience_folder(self, folder_name: str) -> AmbienceFolderItem | None:
        """
        Return a single ambience folder by name.
        """
        folder = self.ambience_dir / folder_name
        if not folder.exists() or not folder.is_dir():
            return None

        tracks = self._collect_audio_files(folder)
        if not tracks:
            return None

        base_prefix = f"ambience/{folder.name}"
        return AmbienceFolderItem(
            title=folder.name,
            path=base_prefix,
            thumbnail=self._find_thumbnail(folder, base_prefix=base_prefix),
            tracks=[
                AmbienceTrackItem(
                    title=track.stem,
                    path=f"{base_prefix}/{track.name}",
                )
                for track in tracks
            ],
        )

    def scan(self) -> dict:
        """
        Return the full library snapshot.
        """
        return {
            "playlists": [item.model_dump() for item in self.list_playlists()],
            "ambience": [item.model_dump() for item in self.list_ambience()],
        }

    def _collect_audio_files(self, folder: Path) -> list[Path]:
        """
        Collect audio files from a folder in alphabetical order.

        Explicitly excludes thumbnail files such as cover.jpg/folder.png.
        """
        return sorted(
            [
                p
                for p in folder.iterdir()
                if (
                    p.is_file()
                    and p.suffix.lower() in AUDIO_EXTENSIONS
                    and p.stem.lower() not in THUMBNAIL_NAMES
                )
            ]
        )

    def _find_thumbnail(self, folder: Path, base_prefix: str) -> str | None:
        """
        Find a thumbnail image for a playlist or ambience folder.
        """
        candidates = ["cover.jpg", "cover.jpeg", "cover.png", "cover.webp", "folder.jpg", "folder.png"]

        for name in candidates:
            candidate = folder / name
            if candidate.exists():
                return f"{base_prefix}/{candidate.name}"

        for file_path in sorted(folder.iterdir()):
            if file_path.is_file() and file_path.suffix.lower() in IMAGE_EXTENSIONS:
                return f"{base_prefix}/{file_path.name}"

        return None