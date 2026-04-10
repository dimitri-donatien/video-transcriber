import os
import tempfile
import subprocess
from pathlib import Path
import imageio_ffmpeg


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

        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

        command = [
            ffmpeg_exe,
            "-y",
            "-i", str(self.video_path.resolve()),
            "-vn",
            "-acodec", "pcm_s16le",
            "-ar", "16000",
            "-ac", "1",
            output_path
        ]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"Erreur FFmpeg :\n{result.stderr.decode('utf-8', errors='ignore')}"
            )

        return output_path
