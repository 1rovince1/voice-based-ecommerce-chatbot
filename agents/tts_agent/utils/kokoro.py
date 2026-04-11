import logging

from kokoro import KPipeline
import numpy as np

logger = logging.getLogger(__name__)


pipeline = KPipeline(lang_code='a')


def kokoro_tts_stream(
        text_to_convert: str,
        kokoro_voice: str = "af_heart"
):
    generator = pipeline(text_to_convert, voice=kokoro_voice)

    for i, (gs, ps, audio_tensor) in enumerate(generator):
        # logger.debug(i, gs, ps)
        audio_np = audio_tensor.cpu().detach().numpy().astype(np.float32)
        
        yield audio_np


def kokoro_tts_batch(
        text_to_convert: str,
        kokoro_voice: str = "af_heart"
):
    generator = pipeline(text_to_convert, voice=kokoro_voice)

    all_audio = []
    for i, (gs, ps, audio_tensor) in enumerate(generator):
        # logger.debug(i, gs, ps)
        audio_np = audio_tensor.cpu().detach().numpy().astype(np.float32)
        all_audio.append(audio_np)
    
    return np.concatenate(all_audio)