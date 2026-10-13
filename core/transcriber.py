
import os
import requests
import whisper
from pydub import AudioSegment

SARVAM_PIECE_SECONDS = 25
WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

SARVAM_STT_URL = "https://api.sarvam.ai/speech-to-text"
SARVAM_MODEL = "saaras:v4"

_model = None


def load_model():
    """Load Whisper only when it is needed."""
    global _model

    if _model is None:
        print(f"Loading Whisper model: {WHISPER_MODEL} ...")
        _model = whisper.load_model(WHISPER_MODEL)
        print("Whisper model loaded.")

    return _model


def transcribe_chunk_whisper(chunk_path: str) -> str:
    """Transcribe an audio chunk using Whisper."""
    model = load_model()

    result = model.transcribe(
        chunk_path,
        fp16=False
    )

    return result["text"].strip()


def transcribe_chunk_sarvam(chunk_path: str) -> str:
    """Transcribe Hindi audio using Sarvam AI."""
    if not SARVAM_API_KEY:
        raise RuntimeError(
            "SARVAM_API_KEY is missing. Check your .env file."
        )

    audio = AudioSegment.from_file(chunk_path)
    piece_ms = SARVAM_PIECE_SECONDS * 1000
    transcripts = []

    total_pieces = (
        len(audio) + piece_ms - 1
    ) // piece_ms

    for i, start in enumerate(range(0, len(audio), piece_ms)):
        piece = audio[start:start + piece_ms]
        piece_path = f"{chunk_path}_sarvam_{i}.wav"

        try:
            # Export this piece as WAV.
            piece.export(piece_path, format="wav")

            headers = {
                "api-subscription-key": SARVAM_API_KEY
            }

            data = {
                "model": SARVAM_MODEL,
                "mode": "transcribe",
                "language_code": "hi-IN"
            }

            print(
                f"Sarvam Hindi transcription "
                f"{i + 1}/{total_pieces}..."
            )

            with open(piece_path, "rb") as audio_file:
                files = {
                    "file": (
                        os.path.basename(piece_path),
                        audio_file,
                        "audio/wav"
                    )
                }

                response = requests.post(
                    SARVAM_STT_URL,
                    headers=headers,
                    files=files,
                    data=data,
                    timeout=120
                )

            if not response.ok:
                print(f"Sarvam API error: {response.status_code}")
                print(response.text)

            response.raise_for_status()

            result = response.json()
            transcript = result.get("transcript", "").strip()

            if transcript:
                transcripts.append(transcript)
            else:
                print(
                    f"Warning: Sarvam returned empty text "
                    f"for piece {i + 1}."
                )

        finally:
            # Remove the temporary WAV file.
            if os.path.exists(piece_path):
                os.remove(piece_path)

    return " ".join(transcripts).strip()


def transcribe_chunk(
    chunk_path: str,
    language: str = "english"
) -> str:
    """Choose the transcription engine based on language."""
    language = language.lower().strip()

    if language in ("hindi", "hinglish", "sarvam"):
        return transcribe_chunk_sarvam(chunk_path)

    return transcribe_chunk_whisper(chunk_path)


def transcribe_all(
    chunks: list,
    language: str = "english"
) -> str:
    """Transcribe all audio chunks and combine their text."""
    if not chunks:
        return ""

    language = language.lower().strip()

    if language in ("hindi", "hinglish", "sarvam"):
        engine = "Sarvam AI (Hindi)"
    else:
        engine = "Whisper (English)"

    print(f"Using {engine} for transcription.")

    transcripts = []

    for i, chunk in enumerate(chunks):
        print(
            f"Transcribing chunk {i + 1}/{len(chunks)}..."
        )

        text = transcribe_chunk(
            chunk,
            language=language
        )

        if text:
            transcripts.append(text)

    print("Transcription complete.")

    return " ".join(transcripts).strip()
