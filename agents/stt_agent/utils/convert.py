import logging

import whisper
import numpy as np


logger = logging.getLogger(__name__)


stt_model = whisper.load_model("base.en")


def speech_to_text(audio_np_array: np.ndarray):
    if not audio_np_array:
        logger.info("No audio bytes")
        return None
    
    logger.info("Transcribing...")
    transcription_response = stt_model.transcribe(audio=audio_np_array)

    return transcription_response["text"]