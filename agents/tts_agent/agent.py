import logging
import asyncio

import sounddevice as sd

from agents.tts_agent.utils.kokoro import kokoro_tts

logger = logging.getLogger(__name__)


async def tts_agent(text: str):
    logger.info("TTS agent...")
    # converted_audio, sample_rate = await asyncio.to_thread(
    #     kokoro_model,
    #     text
    #     # "Realistic male voice in the 30s age with american accent. Normal pitch, warm timbre, conversational pacing."
    # )

    # sd.play(data=converted_audio, samplerate=sample_rate)
    # sd.wait()

    await asyncio.to_thread(
        kokoro_tts,
        text
        # "Realistic male voice in the 30s age with american accent. Normal pitch, warm timbre, conversational pacing."
    )

    # return converted_audio