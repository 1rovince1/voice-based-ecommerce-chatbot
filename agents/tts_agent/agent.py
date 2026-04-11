import logging
import asyncio

# import sounddevice as sd

from agents.tts_agent.utils.kokoro import kokoro_tts_stream

logger = logging.getLogger(__name__)


async def tts_agent(text: str):
    logger.info("TTS agent...")
    # converted_audio, sample_rate = await asyncio.to_thread(
    #     kokoro_model,
    #     text
    # )

    # sd.play(data=converted_audio, samplerate=sample_rate)
    # sd.wait()

    await asyncio.to_thread(
        kokoro_tts_stream,
        text
    )

    # return converted_audio