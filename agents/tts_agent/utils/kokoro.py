import logging

from kokoro import KPipeline
import sounddevice as sd
import numpy as np

logger = logging.getLogger(__name__)


pipeline = KPipeline(lang_code='a')


def kokoro_tts_stream(
        text_to_convert: str,
        kokoro_voice: str = "af_heart"
):
    generator = pipeline(text_to_convert, voice=kokoro_voice)

    with sd.OutputStream(samplerate=24000, channels=1) as output_stream:
        for i, (gs, ps, audio) in enumerate(generator):
            # logger.debug(i, gs, ps)
            output_stream.write(audio)


def kokoro_tts_batch(
        text_to_convert: str,
        kokoro_voice: str = "af_heart"
):
    generator = pipeline(text_to_convert, voice=kokoro_voice)

    all_audio = []
    for i, (gs, ps, audio) in enumerate(generator):
        # logger.debug(i, gs, ps)
        all_audio.append(audio)
    
    sd.play(np.concatenate(all_audio), 24000)
    sd.wait()
    # return np.concatenate(all_audio), 24000