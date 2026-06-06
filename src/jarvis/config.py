import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class JarvisConfig:
    provider: str = os.getenv("JARVIS_PROVIDER", "fake").lower()
    model: str = os.getenv("JARVIS_MODEL", "gpt-4.1-mini")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    anthropic_api_key: str | None = os.getenv("ANTHROPIC_API_KEY")
    allowed_root: Path = Path(os.getenv("JARVIS_ALLOWED_ROOT", str(Path.home()))).expanduser()
    require_confirmation: bool = os.getenv("JARVIS_REQUIRE_CONFIRMATION", "true").lower() == "true"

    manual_open_prompt: bool = os.getenv("JARVIS_MANUAL_OPEN_PROMPT", "true").lower() == "true"
    manual_editor: str = os.getenv("JARVIS_MANUAL_EDITOR", "notepad")

    browser_url: str = os.getenv("JARVIS_BROWSER_URL", "https://chatgpt.com/")
    browser_profile: Path = Path(os.getenv("JARVIS_BROWSER_PROFILE", ".jarvis/browser-profile")).expanduser()
    browser_headless: bool = os.getenv("JARVIS_BROWSER_HEADLESS", "false").lower() == "true"
    browser_timeout_seconds: int = int(os.getenv("JARVIS_BROWSER_TIMEOUT_SECONDS", "240"))
    browser_auto_open: bool = os.getenv("JARVIS_BROWSER_AUTO_OPEN", "true").lower() == "true"
    browser_keep_open: bool = os.getenv("JARVIS_BROWSER_KEEP_OPEN", "true").lower() == "true"

    voice_enabled: bool = os.getenv("JARVIS_VOICE_ENABLED", "false").lower() == "true"
    voice_language: str = os.getenv("JARVIS_VOICE_LANGUAGE", "pt-BR")
    tts_enabled: bool = os.getenv("JARVIS_TTS_ENABLED", "true").lower() == "true"
    tts_rate: int = int(os.getenv("JARVIS_TTS_RATE", "185"))
    tts_volume: float = float(os.getenv("JARVIS_TTS_VOLUME", "1.0"))
    wake_word: str = os.getenv("JARVIS_WAKE_WORD", "jarvis").strip().lower()
    listen_timeout: int = int(os.getenv("JARVIS_LISTEN_TIMEOUT", "5"))
    phrase_time_limit: int = int(os.getenv("JARVIS_PHRASE_TIME_LIMIT", "12"))

def load_config() -> JarvisConfig:
    return JarvisConfig()
