
import os
import re
from pathlib import Path

from pydub import AudioSegment
from yt_dlp import YoutubeDL


# Store downloaded files and converted audio in the project directory.
BASE_DIR = Path(__file__).resolve().parent.parent
DOWNLOAD_DIR = BASE_DIR / "downloads"
PROCESSED_DIR = BASE_DIR / "processed"

DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def download_youtube_audio(url: str) -> str:
    """
    Download audio from a YouTube URL.
    Returns the downloaded file's local path.
    """
    options = {
        "format": "bestaudio/best",
        "outtmpl": str(DOWNLOAD_DIR / "%(id)s.%(ext)s"),
        "noplaylist": True,
        "quiet": False,
        "no_warnings": False,
    }

    try:
        with YoutubeDL(options) as ydl:
            info = ydl.extract_info(url, download=True)
            downloaded_path = Path(ydl.prepare_filename(info))

        if not downloaded_path.is_file():
            # Find the downloaded file if its extension differs.
            matches = list(DOWNLOAD_DIR.glob(f"{info['id']}.*"))
            if not matches:
                raise FileNotFoundError(
                    "YouTube audio downloaded, but the file was not found."
                )
            downloaded_path = matches[0]

        return str(downloaded_path)

    except Exception as exc:
        raise RuntimeError(
            f"Failed to download YouTube audio: {exc}"
        ) from exc


def convert_to_wav(input_path: str) -> str:
    """
    Convert a local audio/video file into a WAV audio file.
    Requires FFmpeg to be installed and available on PATH.
    """
    source_path = Path(input_path).expanduser().resolve()

    if not source_path.is_file():
        raise FileNotFoundError(
            f"Input file does not exist: {source_path}"
        )

    wav_path = PROCESSED_DIR / f"{source_path.stem}.wav"

    try:
        audio = AudioSegment.from_file(str(source_path))
        audio.export(str(wav_path), format="wav")
        return str(wav_path)

    except Exception as exc:
        raise RuntimeError(
            f"Could not convert '{source_path.name}' to WAV. "
            f"Check that FFmpeg is installed and available on PATH. "
            f"Details: {exc}"
        ) from exc


def split_audio(
    wav_path: str,
    chunk_length_ms: int = 60_000,
    overlap_ms: int = 2_000,
) -> list:
    """
    Split WAV audio into chunks.

    Defaults:
        chunk_length_ms = 60 seconds
        overlap_ms = 2 seconds

    Returns a list of paths to the chunk files.
    """
    if chunk_length_ms <= 0:
        raise ValueError("chunk_length_ms must be greater than zero.")

    if overlap_ms < 0 or overlap_ms >= chunk_length_ms:
        raise ValueError(
            "overlap_ms must be non-negative and smaller than chunk_length_ms."
        )

    source_path = Path(wav_path).resolve()

    if not source_path.is_file():
        raise FileNotFoundError(f"WAV file not found: {source_path}")

    try:
        audio = AudioSegment.from_wav(str(source_path))
    except Exception as exc:
        raise RuntimeError(f"Could not read WAV file: {exc}") from exc

    chunks = []
    step_ms = chunk_length_ms - overlap_ms
    start_ms = 0
    chunk_number = 1

    while start_ms < len(audio):
        end_ms = min(start_ms + chunk_length_ms, len(audio))
        chunk = audio[start_ms:end_ms]

        chunk_path = PROCESSED_DIR / (
            f"{source_path.stem}_chunk_{chunk_number:03d}.wav"
        )

        chunk.export(str(chunk_path), format="wav")
        chunks.append(str(chunk_path))

        start_ms += step_ms
        chunk_number += 1

    if not chunks:
        raise RuntimeError("No audio chunks were generated.")

    return chunks


def process_input(source: str) -> list:
    """
    Process either a YouTube URL or a local audio/video file.

    Returns:
        A list of WAV chunk file paths for the transcription module.
    """
    if not source or not source.strip():
        raise ValueError("Please provide a YouTube URL or a local file path.")

    source = source.strip()

    if source.lower().startswith(("https://", "http://")):
        # Download YouTube audio before passing it to Pydub.
        input_path = download_youtube_audio(source)
    else:
        # Treat the input as a local file path.
        input_path = str(Path(source).expanduser().resolve())

    wav_path = convert_to_wav(input_path)

    # Keep the chunks compatible with the transcription pipeline.
    chunks = split_audio(wav_path)

    return chunks
