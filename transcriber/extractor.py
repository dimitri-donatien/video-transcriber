import os
import tempfile
from pathlib import Path
from moviepy import VideoFileClip


class AudioExtractor:
    """Extrait l'audio d'une vidéo."""

    SUPPORTED_FORMATS = {".mp4", ".avi", ".mkv", ".mov", ".webm", ".flv", ".wmv"}

    def __init__(self, video_path: str):
        self.video_path = Path(video_path)
        self._validate()

    def _validate(self):
        if not self.video_path.exists():
            raise FileNotFoundError(f"Fichier introuvable : {self.video_path}")
        if self.video_path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Format non supporté : {self.video_path.suffix}\n"
                f"Formats acceptés : {', '.join(self.SUPPORTED_FORMATS)}"
            )

    def extract(self, output_path: str = None) -> str:
        if output_path is None:
            tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            output_path = tmp.name
            tmp.close()

        with VideoFileClip(str(self.video_path)) as video:
            if video.audio is None:
                raise ValueError("La vidéo ne contient pas de piste audio.")
            video.audio.write_audiofile(output_path)

        return output_path
