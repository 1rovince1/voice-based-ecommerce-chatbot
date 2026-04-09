import logging

import sounddevice as sd
import numpy as np


logger = logging.getLogger(__name__)


def record_with_vad(
        sample_rate = 16000, # How many sound snapshots per second
        chunk_size_ms = 50, # How big is each audio piece we check (in ms)
        silence_threshold_rms = 0.02,   # how quiet is silence
        min_silence_duration = 1000 # how long silence means "user stopped talking"
):
    
    recorded_frames = []
    is_recording = False
    silence_counter = 0

    # convert ms to frames/chunks for sounddevice
    chunk_size_frames = int(sample_rate * chunk_size_ms / 1000)
    min_silence_chunks = int(min_silence_duration / chunk_size_ms)

    logger.info("Listening...")
    with sd.InputStream(samplerate=sample_rate, blocksize=chunk_size_frames, channels=1) as stream:
        while(True):
            logger.info("inside while loop...")
            logger.info(is_recording)
            # read a small chunk of audio from the mic
            # this variable is an array of numbers representing the sound
            audio_chunk_np = stream.read(frames=chunk_size_frames)[0]

            # calculate the energy of this audio chunk
            # big RMS = loud sound (maybe speech), small RMS = quiet (maybe silence)
            rms = np.sqrt(np.mean(audio_chunk_np**2))   # this is our VAD's ear
            logger.info(f"RMS: {rms:.6f}")

            if is_recording:
                # if we are already recording
                recorded_frames.append(audio_chunk_np)

                if rms <= silence_threshold_rms: # is it quiet now?
                    silence_counter += 1    # count this chunk
                    if silence_counter >= min_silence_chunks:   # has it been quiet long enough>
                        logger.info("Silence detected, stopping recording...")
                        break
                else:
                    silence_counter = 0 # started talking again, reset the counter

            elif rms > silence_threshold_rms:   # loud enough, trigger recording
                logger.info("Speech detected, starting recording...")
                is_recording = True
                recorded_frames = [audio_chunk_np]  # begin with this frame
                silence_counter = 0

    return recorded_frames
