import os
import imageio_ffmpeg
import whisper


class VideoTranscriber:
    """Transcrit un fichier audio avec Whisper."""

    def __init__(self, model_name: str = "base"):
        self.model_name = model_name
        self.model = None
        # Chemin vers le binaire FFmpeg
        self.ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    def load_model(self):
        self.model = whisper.load_model(self.model_name)
        return self

    def transcribe(self, audio_path: str, language: str = None, translate: bool = False) -> dict:
        if self.model is None:
            raise RuntimeError("Modèle non chargé. Appelez load_model() d'abord.")

        options = {
            "task": "translate" if translate else "transcribe",
            "fp16": False,
        }
        if language and language != "auto":
            options["language"] = language

        # Indique explicitement à Whisper où est FFmpeg
        result = self.model.transcribe(
            audio_path,
            **options,
            verbose=False,
        )
        return result
