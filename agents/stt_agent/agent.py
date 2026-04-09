import logging
import numpy as np

from agents.stt_agent.utils.record import record_with_vad
from agents.stt_agent.utils.convert import speech_to_text

logger = logging.getLogger(__name__)


async def stt_agent():
    logger.debug("STT agent...")
    recorded_frames = record_with_vad()
    converted_text = speech_to_text(np.concatenate(recorded_frames, axis=0).squeeze())

    return converted_text