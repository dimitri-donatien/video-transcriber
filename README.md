# 🎬 Video Transcriber

Un outil en ligne de commande puissant pour transcrire automatiquement des vidéos et fichiers audio en texte, propulsé par **OpenAI Whisper**.

---

## Fonctionnalités

- 🎥 Support vidéo : MP4, AVI, MKV, MOV, WMV, FLV, WEBM
- 🎵 Support audio : MP3, WAV, M4A, FLAC, OGG, AAC
- 🌍 Détection automatique de la langue ou spécification manuelle
- 📄 Export en plusieurs formats : TXT, JSON, SRT (sous-titres), VTT
- ⚡ Plusieurs modèles Whisper selon tes besoins (rapidité vs précision)
- 🎨 Interface CLI colorée et intuitive avec barre de progression
- 📋 Historique des transcriptions

---

## 📋 Prérequis

- **Python 3.8+**
- **pip**
- **Git**

---

## Note sur FFmpeg

Ce projet utilise **`imageio-ffmpeg`** qui embarque FFmpeg, cependant **une manipulation manuelle est nécessaire** car Whisper appelle `ffmpeg` par son nom court et ne trouve pas le binaire automatiquement.

### Solution requise

Après l'installation des dépendances, tu dois créer une copie du binaire FFmpeg nommée `ffmpeg.exe` :

**Windows :**
```powershell
# Trouve le chemin du binaire imageio-ffmpeg
python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"

# Copie et renomme le binaire (adapte le chemin selon ton environnement)
copy "C:\..\.venv\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe" `
     "C:\..\.venv\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg.exe"
```

**Linux/macOS :**
```bash
# Trouve le chemin du binaire
python -c "import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())"

# Crée un lien symbolique
ln -s /chemin/vers/ffmpeg-linux-x86_64 /chemin/vers/ffmpeg
```

> **Pourquoi ?** Whisper cherche `ffmpeg` dans le PATH système. Le binaire fourni par `imageio-ffmpeg` a un nom versionné (ex: `ffmpeg-win-x86_64-v7.1.exe`) et n'est pas reconnu directement. Le `main.py` ajoute automatiquement le dossier au PATH, mais le fichier `ffmpeg.exe` doit exister avec ce nom exact.

> **Alternative :** Installe FFmpeg directement sur ton système via [ffmpeg.org](https://ffmpeg.org/download.html) pour éviter cette manipulation.

---

## Installation

### 1. Clone le projet

```bash
git clone https://gitlab.com/votre-utilisateur/video-transcriber.git
cd video-transcriber
```

### 2. Crée un environnement virtuel

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/macOS
python -m venv .venv
source .venv/bin/activate
```

### 3. Installe les dépendances

```bash
pip install -r requirements.txt
```

### 4. Configure FFmpeg

Suis les instructions de la section [Note sur FFmpeg](#️-note-sur-ffmpeg) ci-dessus.

---

## Utilisation

### Commande de base

```bash
python main.py transcribe <fichier> [options]
```

### Options disponibles

| Option | Raccourci | Description | Défaut |
|--------|-----------|-------------|--------|
| `--model` | `-m` | Modèle Whisper à utiliser | `base` |
| `--language` | `-l` | Langue de la vidéo (ex: `fr`, `en`) | Auto-détection |
| `--format` | `-f` | Format de sortie (`txt`, `json`, `srt`, `vtt`) | `txt` |
| `--output` | `-o` | Nom du fichier de sortie | Auto-généré |

### Exemples

```bash
# Transcription simple
python main.py transcribe video.mp4

# Avec modèle medium en français
python main.py transcribe video.mp4 -m medium -l fr

# Export en sous-titres SRT
python main.py transcribe video.mp4 -m medium -l fr -f srt -o sous_titres.srt

# Export en JSON avec le modèle large
python main.py transcribe video.mp4 -m large -l fr -f json -o resultat.json

# Export en texte brut
python main.py transcribe video.mp4 -m medium -l fr -f txt -o transcript.txt
```

### Voir l'historique des transcriptions

```bash
python main.py history
```

### Lister les modèles disponibles

```bash
python main.py models
```

---

## Modèles Whisper

| Modèle | Taille | Vitesse | Précision | VRAM requise |
|--------|--------|---------|-----------|--------------|
| `tiny` | 39 MB | ⚡⚡⚡⚡⚡ | ⭐⭐ | ~1 GB |
| `base` | 74 MB | ⚡⚡⚡⚡ | ⭐⭐⭐ | ~1 GB |
| `small` | 244 MB | ⚡⚡⚡ | ⭐⭐⭐⭐ | ~2 GB |
| `medium` | 769 MB | ⚡⚡ | ⭐⭐⭐⭐⭐ | ~5 GB |
| `large` | 1550 MB | ⚡ | ⭐⭐⭐⭐⭐⭐ | ~10 GB |

> 💡 **Recommandation :** Utilise `medium` pour un bon équilibre rapidité/précision. Utilise `large` pour une précision maximale si tu as un GPU puissant.

---

## Structure du projet

```
video-transcriber/
├── main.py                 # Point d'entrée CLI
├── requirements.txt        # Dépendances Python
├── README.md               # Documentation
├── .gitignore              # Fichiers ignorés par Git
└── transcriptions/         # Dossier de sortie (auto-créé)
```

---

## Dépendances

```txt
openai-whisper
click
rich
imageio-ffmpeg
```

---

## Langues supportées

Whisper supporte plus de **90 langues**, dont :

`fr` Français · `en` Anglais · `es` Espagnol · `de` Allemand · `it` Italien · `pt` Portugais · `nl` Néerlandais · `ja` Japonais · `zh` Chinois · `ar` Arabe · `ru` Russe · et bien d'autres...

> Utilise le paramètre `-l <code>` pour spécifier la langue et améliorer la précision.

---

## 🤝 Contribuer

Les contributions sont les bienvenues !

1. Fork le projet
2. Crée ta branche (`git checkout -b feature/ma-fonctionnalite`)
3. Commit tes changements (`git commit -m 'feat: ajout de ma fonctionnalité'`)
4. Push sur la branche (`git push origin feature/ma-fonctionnalite`)
5. Ouvre une Merge Request

---

## 📄 Licence

Ce projet est sous licence **MIT**. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

## Auteur

Fait avec ❤️ par **[dimitri-donatien](https://gitlab.com/dimitri-donatien)**

---