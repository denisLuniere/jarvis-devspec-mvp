import threading

class TextToSpeech:
    def __init__(self, enabled: bool = True, rate: int = 185, volume: float = 1.0):
        self.enabled = enabled
        self.rate = rate
        self.volume = volume
        self.engine = None
        self._lock = threading.Lock()

        if not enabled:
            return

        self._init_engine()

    def _init_engine(self) -> None:
        try:
            import pyttsx3
        except ImportError as exc:
            raise RuntimeError(
                "Dependência de voz ausente. Instale com: pip install -e .[voice]"
            ) from exc

        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", self.rate)
        self.engine.setProperty("volume", self.volume)

        # Tenta selecionar uma voz em português quando disponível.
        try:
            voices = self.engine.getProperty("voices")
            for voice in voices:
                candidate = f"{voice.name} {voice.id}".lower()
                if "portugu" in candidate or "brazil" in candidate or "brasil" in candidate:
                    self.engine.setProperty("voice", voice.id)
                    break
        except Exception:
            pass

    def speak(self, text: str) -> None:
        if not self.enabled or not text:
            return

        clean_text = self._clean_for_speech(text)
        if not clean_text:
            return

        with self._lock:
            try:
                if self.engine is None:
                    self._init_engine()

                # Evita fila antiga presa.
                try:
                    self.engine.stop()
                except Exception:
                    pass

                self.engine.say(clean_text)
                self.engine.runAndWait()
            except RuntimeError:
                # pyttsx3 no Windows às vezes prende o loop depois de uma fala.
                # Reinicializar resolve em muitos ambientes.
                try:
                    self.engine = None
                    self._init_engine()
                    self.engine.say(clean_text)
                    self.engine.runAndWait()
                except Exception as exc:
                    print(f"Jarvis > Aviso: não consegui falar a resposta: {exc}")
            except Exception as exc:
                print(f"Jarvis > Aviso: não consegui falar a resposta: {exc}")

    def _clean_for_speech(self, text: str) -> str:
        replacements = {
            "#": "",
            "*": "",
            "`": "",
            "|": " ",
            "[": "",
            "]": "",
            "(": "",
            ")": "",
            "_": " ",
            "\\": " barra ",
            "/": " barra ",
        }

        clean = text
        for old, new in replacements.items():
            clean = clean.replace(old, new)

        max_chars = 700
        if len(clean) > max_chars:
            clean = clean[:max_chars] + ". Resposta longa truncada para leitura em voz."

        return clean.strip()
