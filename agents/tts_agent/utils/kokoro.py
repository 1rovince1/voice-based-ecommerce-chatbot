# !pip install -q kokoro>=0.9.4 soundfile
# !apt-get -qq -y install espeak-ng > /dev/null 2>&1
from kokoro import KPipeline
# from IPython.display import display, Audio
# import soundfile as sf
import sounddevice as sd
# import torch
import numpy as np
pipeline = KPipeline(lang_code='a')

def kokoro_tts(
        text_to_convert: str,
        kokoro_voice: str = "af_heart"
):
    # text = '''
    # [Kokoro](/kˈOkəɹO/) is an open-weight TTS model with 82 million parameters. Despite its lightweight architecture, it delivers comparable quality to larger models while being significantly faster and more cost-efficient. With Apache-licensed weights, [Kokoro](/kˈOkəɹO/) can be deployed anywhere from production environments to personal projects.
    # '''
    # all_audio = []

    generator = pipeline(text_to_convert, voice=kokoro_voice)

    output_stream = sd.OutputStream(samplerate=24000, channels=1)
    output_stream.start()
    for i, (gs, ps, audio) in enumerate(generator):
        print(i, gs, ps)
        # display(Audio(data=audio, rate=24000, autoplay=i==0))
        # sf.write(f'{i}.wav', audio, 24000)

        # all_audio.append(audio)
        output_stream.write(audio)
    
    # sd.play(np.concatenate(all_audio), 24000)
    # sd.wait()
    # return np.concatenate(all_audio), 24000
    output_stream.stop()
    output_stream.close()

# import asyncio
# asyncio.run(kokoro_model('''
#     [Kokoro](/kˈOkəɹO/) is an open-weight TTS model with 82 million parameters. Despite its lightweight architecture, it delivers comparable quality to larger models while being significantly faster and more cost-efficient. With Apache-licensed weights, [Kokoro](/kˈOkəɹO/) can be deployed anywhere from production environments to personal projects.
#     '''))