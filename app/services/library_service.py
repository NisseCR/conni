from __future__ import annotations

from pathlib import Path

from app.models.media import AmbienceItem, PlaylistItem


class LibraryService:
    """
    Scans the local media folders and exposes them to the API/UI.
    """

    def __init__(self, music_dir: str = "media/music", ambience_dir: str = "media/ambience") -> None:
        """
        Initialize the library service.

        Args:
            music_dir: Folder containing playlist folders.
            ambience_dir: Folder containing ambience files.
        """
        self.music_dir = Path(music_dir)
        self.ambience_dir = Path(ambience_dir)

    def list_playlists(self) -> list[PlaylistItem]:
        """
        Discover music playlists from subfolders.

        Returns:
            A list of playlist items.
        """
        playlists: list[PlaylistItem] = []

        if not self.music_dir.exists():
            return playlists

        for folder in sorted(self.music_dir.iterdir()):
            if folder.is_dir():
                playlists.append(
                    PlaylistItem(
                        title=folder.name,
                        path=str(folder),
                        thumbnail=self._find_thumbnail(folder),
                    )
                )

        return playlists

    def list_ambience(self) -> list[AmbienceItem]:
        """
        Discover ambience files.

        Returns:
            A list of ambience items.
        """
        ambience: list[AmbienceItem] = []

        if not self.ambience_dir.exists():
            return ambience

        for file_path in sorted(self.ambience_dir.iterdir()):
            if file_path.is_file():
                ambience.append(
                    AmbienceItem(
                        title=file_path.stem,
                        path=str(file_path),
                        thumbnail=self._find_thumbnail(file_path.parent, file_path.stem),
                    )
                )

        return ambience

    def scan(self) -> dict:
        """
        Return the full library snapshot.

        Returns:
            Dictionary with playlists and ambience.
        """
        return {
            "playlists": [item.model_dump() for item in self.list_playlists()],
            "ambience": [item.model_dump() for item in self.list_ambience()],
        }

    def _find_thumbnail(self, folder: Path, stem: str | None = None) -> str | None:
        """
        Find a thumbnail image for a playlist or ambience item.

        Args:
            folder: Folder to search in.
            stem: Optional file stem for ambience items.

        Returns:
            Thumbnail path if found, otherwise None.
        """
        candidates: list[str] = []
        if stem:
            candidates.extend([f"{stem}.jpg", f"{stem}.jpeg", f"{stem}.png", f"{stem}.webp"])
        candidates.extend(["cover.jpg", "cover.png", "folder.jpg", "folder.png"])

        for name in candidates:
            candidate = folder / name
            if candidate.exists():
                return str(candidate)

        return None