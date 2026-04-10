import json
from datetime import timedelta


class Formatter:
    """Formate le résultat de la transcription."""

    def __init__(self, result: dict):
        self.result = result

    def format(self, fmt: str) -> str:
        methods = {
            "txt":  self._to_txt,
            "srt":  self._to_srt,
            "vtt":  self._to_vtt,
            "json": self._to_json,
        }
        if fmt not in methods:
            raise ValueError(f"Format inconnu : {fmt}")
        return methods[fmt]()

    def _to_txt(self) -> str:
        return self.result.get("text", "").strip()

    def _to_json(self) -> str:
        return json.dumps(self.result, ensure_ascii=False, indent=2)

    def _to_srt(self) -> str:
        lines = []
        for i, seg in enumerate(self.result.get("segments", []), start=1):
            start = self._fmt_time_srt(seg["start"])
            end   = self._fmt_time_srt(seg["end"])
            text  = seg["text"].strip()
            lines.append(f"{i}\n{start} --> {end}\n{text}\n")
        return "\n".join(lines)

    def _to_vtt(self) -> str:
        lines = ["WEBVTT\n"]
        for seg in self.result.get("segments", []):
            start = self._fmt_time_vtt(seg["start"])
            end   = self._fmt_time_vtt(seg["end"])
            text  = seg["text"].strip()
            lines.append(f"{start} --> {end}\n{text}\n")
        return "\n".join(lines)

    @staticmethod
    def _fmt_time_srt(seconds: float) -> str:
        td = timedelta(seconds=seconds)
        total = int(td.total_seconds())
        ms = int((td.total_seconds() - total) * 1000)
        h, r = divmod(total, 3600)
        m, s = divmod(r, 60)
        return f"{h:02}:{m:02}:{s:02},{ms:03}"

    @staticmethod
    def _fmt_time_vtt(seconds: float) -> str:
        td = timedelta(seconds=seconds)
        total = int(td.total_seconds())
        ms = int((td.total_seconds() - total) * 1000)
        h, r = divmod(total, 3600)
        m, s = divmod(r, 60)
        return f"{h:02}:{m:02}:{s:02}.{ms:03}"
