import io
import logging

import whisper


logger = logging.getLogger(__name__)


stt_model = whisper.load_model("base.en")


def speech_to_text(audio_bytes: bytes):
    if not audio_bytes:
        logger.info("No audio bytes")
        return None
    
    logger.info("Transcribing...")
    # we need to send this audio as if its a file
    # io.BytesIO helps us treat our 'audio_bytes' like a file in memory
    audio_file_like = io.BytesIO(audio_bytes)
    audio_file_like.name = "input.wav"

    transcription_response = stt_model.transcribe(audio="input.wav")

    return transcription_response["text"]