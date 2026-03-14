from gtts import gTTS
import os


def speak(text):

    tts = gTTS(text)

    file = "speech.mp3"

    tts.save(file)

    os.system(f"mpg123 {file}")