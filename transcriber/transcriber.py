import os
import shutil
import imageio_ffmpeg
import whisper


class VideoTranscriber:
    """Transcrit un fichier audio avec Whisper."""

    def __init__(self, model_name: str = "base"):
        self.model_name = model_name
        self.model = None
        self._setup_ffmpeg()

    def _setup_ffmpeg(self):
        """Assure que ffmpeg est accessible via le PATH pour Whisper."""
        ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
        ffmpeg_dir = os.path.dirname(ffmpeg_exe)

        # Injecte dans le PATH
        os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")

        # Crée un alias ffmpeg.exe si le binaire a un autre nom (ex: ffmpeg-win64.exe)
        ffmpeg_name = os.path.basename(ffmpeg_exe)
        if ffmpeg_name != "ffmpeg.exe":
            target = os.path.join(ffmpeg_dir, "ffmpeg.exe")
            if not os.path.exists(target):
                shutil.copy2(ffmpeg_exe, target)

    def load_model(self):
        self.model = whisper.load_model(self.model_name)
        return self

    def transcribe(self, audio_path: str, language: str = None, translate: bool = False) -> dict:
        if self.model is None:
            raise RuntimeError("Modèle non chargé. Appelez load_model() d'abord.")

        audio_path = str(os.path.abspath(audio_path))

        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Fichier audio introuvable : {audio_path}")

        options = {
            "task": "translate" if translate else "transcribe",
            "fp16": False,
        }
        if language and language != "auto":
            options["language"] = language

        result = self.model.transcribe(audio_path, **options, verbose=False)
        return result
