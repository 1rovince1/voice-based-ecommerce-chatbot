import logging
import asyncio

import numpy as np

from agents.stt_agent.utils.record import record_with_vad
from agents.stt_agent.utils.convert import speech_to_text

logger = logging.getLogger(__name__)


async def stt_agent():
    logger.info("STT agent...")
    recorded_frames = await asyncio.to_thread(record_with_vad)
    if not recorded_frames:
        return None
    converted_text = await asyncio.to_thread(speech_to_text, np.concatenate(recorded_frames, axis=0).squeeze())

    return converted_text