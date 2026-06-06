class SpeechToText:
    def __init__(
        self,
        language: str = "pt-BR",
        timeout: int = 5,
        phrase_time_limit: int = 12,
        wake_word: str = "jarvis",
    ):
        try:
            import speech_recognition as sr
        except ImportError as exc:
            raise RuntimeError(
                "Dependência de voz ausente. Instale com: pip install -e .[voice]"
            ) from exc

        self.sr = sr
        self.language = language
        self.timeout = timeout
        self.phrase_time_limit = phrase_time_limit
        self.wake_word = wake_word.strip().lower()
        self.recognizer = sr.Recognizer()

    def listen_once(self) -> str:
        with self.sr.Microphone() as source:
            print("Jarvis > Ajustando ruído ambiente...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.4)

            print("Jarvis > Ouvindo...")
            audio = self.recognizer.listen(
                source,
                timeout=self.timeout,
                phrase_time_limit=self.phrase_time_limit,
            )

        try:
            text = self.recognizer.recognize_google(audio, language=self.language)
            return text.strip()
        except self.sr.UnknownValueError:
            return ""
        except self.sr.RequestError as exc:
            raise RuntimeError(f"Falha no reconhecimento de voz: {exc}") from exc

    def listen_command(self) -> str:
        return self.listen_once()
