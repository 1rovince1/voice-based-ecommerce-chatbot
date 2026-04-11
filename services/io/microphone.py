import logging

import sounddevice as sd

logger = logging.getLogger(__name__)


def input_mic_stream(
        sample_rate = 16000, # How many sound snapshots per second
        num_channels = 1,
        data_type = "float32",
        chunk_size_ms = 50  # How big is each audio piece we check (in ms)
):
    logger.info("Mic stream started...")
    chunk_size_frames = int(sample_rate * chunk_size_ms / 1000)

    with sd.InputStream(
        samplerate=sample_rate,
        channels=num_channels,
        dtype=data_type,
        blocksize=chunk_size_ms
    ) as input_stream:
        
        while True:
            audio_np_chunk = input_stream.read(frames=chunk_size_frames)[0].squeeze()
            yield audio_np_chunk