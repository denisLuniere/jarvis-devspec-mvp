from jarvis.config import JarvisConfig
from .base import FakeProvider, LLMProvider

def build_provider(config: JarvisConfig) -> LLMProvider:
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
