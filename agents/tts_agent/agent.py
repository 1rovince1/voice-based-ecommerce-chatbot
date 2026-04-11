import logging
import asyncio

from agents.tts_agent.utils.kokoro import kokoro_tts_stream
from services.audio_io.speaker import play_audio_stream

logger = logging.getLogger(__name__)


async def tts_agent(text: str):
    logger.info("TTS agent...")

    audio_stream = await asyncio.to_thread(
        kokoro_tts_stream,
        text_to_convert=text
    )
    await asyncio.to_thread(
        play_audio_stream,
        audio_stream=audio_stream,
        sample_rate=24000,
        num_channels=1,
        data_type="float32"
    )