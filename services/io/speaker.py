import logging

import sounddevice as sd

logger = logging.getLogger(__name__)


def play_audio_stream(
        audio_stream,
        sample_rate = 24000,
        num_channels = 1,
        data_type = "float32"
):
    logger.info("Speaker stream started...")

    with sd.OutputStream(
        samplerate=sample_rate,
        channels=num_channels,
        dtype=data_type
    ) as output_stream:
        
        for audio_chunk_np in audio_stream:
            output_stream.write(audio_chunk_np)