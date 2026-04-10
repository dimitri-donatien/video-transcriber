import os
import imageio_ffmpeg

_ffmpeg_dir = os.path.dirname(imageio_ffmpeg.get_ffmpeg_exe())
os.environ["PATH"] = _ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
os.environ["IMAGEIO_FFMPEG_EXE"] = imageio_ffmpeg.get_ffmpeg_exe()

import click
import sys
from pathlib import Path
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from transcriber.extractor import AudioExtractor
from transcriber.transcriber import VideoTranscriber
from transcriber.formatter import Formatter

console = Console()

MODELS = ["tiny", "base", "small", "medium", "large"]
FORMATS = ["txt", "srt", "vtt", "json"]
LANGUAGES = ["fr", "en", "es", "de", "it", "pt", "nl", "pl", "ru", "zh", "ja", "auto"]

@click.group()
def cli():
    """🎬 Video Transcriber - Transcription vidéo avec Whisper"""
    pass

@cli.command()
@click.argument("video", type=click.Path(exists=True))
@click.option("-m", "--model", default="base", type=click.Choice(MODELS), help="Modèle Whisper")
@click.option("-l", "--language", default="auto", type=click.Choice(LANGUAGES), help="Langue de la vidéo")
@click.option("-f", "--format", "output_format", default="txt", type=click.Choice(FORMATS), help="Format de sortie")
@click.option("-o", "--output", default=None, help="Fichier de sortie")
@click.option("--translate", is_flag=True, default=False, help="Traduire en anglais")
def transcribe(video, model, language, output_format, output, translate):
    """Transcrit une vidéo en texte."""

    console.print(Panel(
        f"[bold cyan]🎬 Transcription de {video}[/bold cyan]\n"
        f"Modèle : {model} | Format : {output_format} | Langue : {language}",
        title="Video Transcriber",
        border_style="cyan"
    ))

    audio_tmp = None

    try:
        # Étape 1 : Extraction audio
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Extraction de l'audio...", total=None)
            extractor = AudioExtractor(video)
            audio_tmp = extractor.extract()
            progress.update(task, description="✔ Audio extrait.")

        # Étape 2 : Chargement du modèle
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task(f"Chargement du modèle {model}...", total=None)
            transcriber = VideoTranscriber(model_name=model)
            transcriber.load_model()
            progress.update(task, description=f"✔ Modèle {model} chargé.")

        # Étape 3 : Transcription
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task(f"Transcription avec le modèle {model}...", total=None)
            lang = None if language == "auto" else language
            result = transcriber.transcribe(audio_tmp, language=lang, translate=translate)
            progress.update(task, description="✔ Transcription terminée.")

        # Étape 4 : Formatage
        formatter = Formatter(result)
        content = formatter.format(output_format)

        # Étape 5 : Sortie
        if output:
            Path(output).write_text(content, encoding="utf-8")
            console.print(f"\n[bold green]✔ Fichier sauvegardé : {output}[/bold green]")
        else:
            console.print("\n[bold yellow]--- Transcription ---[/bold yellow]")
            console.print(content)

        if "language" in result:
            console.print(f"\n[dim]Langue détectée : {result['language']}[/dim]")

    except FileNotFoundError as e:
        console.print(f"\n[bold red]✘ Fichier introuvable : {e}[/bold red]")
        sys.exit(1)
    except ValueError as e:
        console.print(f"\n[bold red]✘ Erreur : {e}[/bold red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]✘ Erreur : {e}[/bold red]")
        sys.exit(1)
    finally:
        if audio_tmp and os.path.exists(audio_tmp):
            os.remove(audio_tmp)

@cli.command()
def models():
    """Affiche les modèles Whisper disponibles."""
    table = Table(title="Modèles Whisper disponibles")
    table.add_column("Modèle", style="cyan")
    table.add_column("Taille", style="magenta")
    table.add_column("Vitesse", style="green")
    table.add_column("Précision", style="yellow")

    table.add_row("tiny",   "~75 MB",  "⚡⚡⚡⚡⚡", "⭐")
    table.add_row("base",   "~145 MB", "⚡⚡⚡⚡",  "⭐⭐")
    table.add_row("small",  "~465 MB", "⚡⚡⚡",   "⭐⭐⭐")
    table.add_row("medium", "~1.5 GB", "⚡⚡",    "⭐⭐⭐⭐")
    table.add_row("large",  "~3 GB",   "⚡",     "⭐⭐⭐⭐⭐")

    console.print(table)
    console.print("\n[dim]Utilise -m <modèle> pour choisir, ex: python main.py transcribe video.mp4 -m small[/dim]")

if __name__ == "__main__":
    cli()
