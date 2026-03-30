# import whisper

# stt_model = whisper.load_model("base")

# import sounddevice as sd

import requests
result = requests.get("https://www.google.com/search?q=google+messages")
print(result.content)