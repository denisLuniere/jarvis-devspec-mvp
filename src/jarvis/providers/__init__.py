from pathlib import Path

from jarvis.config import JarvisConfig
from .base import FakeProvider, LLMProvider

def build_provider(config: JarvisConfig) -> LLMProvider:
    if config.provider == "manual":
        from .manual_provider import ManualProvider
        return ManualProvider(
            base_dir=Path.cwd(),
            open_prompt=config.manual_open_prompt,
            editor=config.manual_editor,
        )

    if config.provider == "browser":
        from .browser_provider import BrowserProvider
        return BrowserProvider(
            base_dir=Path.cwd(),
            url=config.browser_url,
            profile_dir=config.browser_profile,
            headless=config.browser_headless,
            timeout_seconds=config.browser_timeout_seconds,
            auto_open=config.browser_auto_open,
            keep_open=config.browser_keep_open,
            submit_mode=config.browser_submit_mode,
            send_check_seconds=config.browser_send_check_seconds,
        )

    if config.provider == "openai":
        if not config.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY não configurada.")
        from .openai_provider import OpenAIProvider
        return OpenAIProvider(api_key=config.openai_api_key, model=config.model)

    if config.provider == "anthropic":
        if not config.anthropic_api_key:
            raise RuntimeError("ANTHROPIC_API_KEY não configurada.")
        from .anthropic_provider import AnthropicProvider
        return AnthropicProvider(api_key=config.anthropic_api_key, model=config.model)

    return FakeProvider()
