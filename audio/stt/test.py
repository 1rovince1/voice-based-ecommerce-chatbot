import logging
from utils.logger_config import setup_logging
setup_logging()
from io import BytesIO
import numpy as np

from scipy.io.wavfile import write

from audio.stt.record import record_with_vad
from audio.stt.convert import speech_to_text

logger = logging.getLogger(__name__)


logger.info("REcoding")


recorded_frames = record_with_vad()
with open('./audio/stt/test.txt', 'w') as f:
    f.write(str(recorded_frames))
# audio_np = np.concatenate(recorded_frames, axis=0)
# audio_bytes = BytesIO()
# write(audio_bytes, 16000, np.array(recorded_frames))
# write("./audio/stt/temp.wav", 16000, (np.array(recorded_frames)))
# converted_audio = speech_to_text(audio_bytes.getvalue())
converted_audio = speech_to_text(np.concatenate(recorded_frames, axis=0).squeeze())

print(f"Converted audio: {converted_audio}")

# print(type(recorded_frames))
# print(recorded_frames)