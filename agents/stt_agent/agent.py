import logging
import asyncio

from agents.stt_agent.utils.record import vad_analyzer
from agents.stt_agent.utils.convert import speech_to_text
from services.io.microphone import input_mic_stream

logger = logging.getLogger(__name__)


async def stt_agent():
    logger.info("STT agent...")

    input_chunk_size_ms = 50
    input_sample_rate = 16000
    input_num_channels = 1
    input_data_type = "float32"

    input_audio_stream = await asyncio.to_thread(
        input_mic_stream,
        sample_rate=input_sample_rate,
        num_channels=input_num_channels,
        data_type=input_data_type,
        chunk_size_ms=input_chunk_size_ms
    )
    recorded_frames = await asyncio.to_thread(
        vad_analyzer,
        input_audio_stream=input_audio_stream,
        chunk_size_ms=input_chunk_size_ms
    )
    converted_text = await asyncio.to_thread(
        speech_to_text,
        audio_np_array=recorded_frames
    )

    return converted_text