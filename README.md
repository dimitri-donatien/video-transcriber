## Utilisation

# Transcription simple
python main.py transcribe video.mp4

# Avec un meilleur modèle, en français, sortie SRT
python main.py transcribe video.mp4 -m medium -l fr -f srt -o subtitles.srt

# Traduire en anglais
python main.py transcribe video.mp4 --translate -f txt -o transcript_en.txt

# Format JSON complet
python main.py transcribe video.mp4 -f json -o result.json

# Voir les modèles disponibles
python main.py models

## Exemple de sortie

```
╭─────────────────────────────────────────╮
│            Video Transcriber            │
│  🎬 Transcription de video.mp4          │
│  Modèle : base | Format : txt | Langue : auto │
╰─────────────────────────────────────────╯
✔ Audio extrait avec succès.
✔ Modèle base chargé.
✔ Transcription terminée (langue détectée : fr, durée : 142.3s)

──────────────────────────────────────────
Bonjour et bienvenue dans cette vidéo...

```

| Modèle | RAM | Vitesse | Précision |
|--------|-----|---------|-----------|
| tiny | ~1GB | ⚡⚡⚡⚡⚡ | ⭐⭐ |
| base | ~1GB | ⚡⚡⚡⚡ | ⭐⭐⭐ |
| small | ~2GB | ⚡⚡⚡ | ⭐⭐⭐⭐ |
| medium | ~5GB | ⚡⚡ | ⭐⭐⭐⭐⭐ |
| large | ~10GB | ⚡ | ⭐⭐⭐⭐⭐ |

💡 Pour démarrer : base est parfait. Pour des vidéos professionnelles, utilise medium ou large.