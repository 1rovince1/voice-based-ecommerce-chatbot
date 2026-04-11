import logging
import asyncio

from agents.tts_agent.utils.kokoro import kokoro_tts_stream
from services.io.speaker import play_audio_stream

logger = logging.getLogger(__name__)


async def tts_agent(text: str):
    logger.info("TTS agent...")

    output_sample_rate = 24000
    output_num_channels = 1
    output_data_type = "float32"

    audio_stream = await asyncio.to_thread(
        kokoro_tts_stream,
        text_to_convert=text
    )
    await asyncio.to_thread(
        play_audio_stream,
        audio_stream=audio_stream,
        sample_rate=output_sample_rate,
        num_channels=output_num_channels,
        data_type=output_data_type
    )