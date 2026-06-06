from jarvis.voice.stt import SpeechToText
from jarvis.voice.tts import TextToSpeech

class VoiceLoop:
    def __init__(self, stt: SpeechToText, tts: TextToSpeech):
        self.stt = stt
        self.tts = tts

    def get_input(self) -> str:
        text = self.stt.listen_command()
        if text:
            print(f"Você falou > {text}")
        else:
            print("Jarvis > Não consegui entender.")
        return text

    def say(self, text: str) -> None:
        self.tts.speak(text)
