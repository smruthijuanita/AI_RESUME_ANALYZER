import speech_recognition as sr


def speech_to_text():

    r = sr.Recognizer()

    with sr.Microphone() as source:

        audio = r.listen(source)

        text = r.recognize_google(audio)

    return text