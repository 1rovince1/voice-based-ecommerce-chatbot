import logging

import whisper
import numpy as np


logger = logging.getLogger(__name__)


stt_model = whisper.load_model("base.en")


def speech_to_text(audio_np_array: np.ndarray):
    logger.info("Transcribing...")
    transcription_response = stt_model.transcribe(audio=audio_np_array)

    logger.info(f"Transcribed message: {transcription_response}")
    return transcription_response["text"]