from jarvis.providers.base import LLMProvider

SYSTEM_PROMPT = """
Você é o Jarvis DevSpec, um assistente local para desenvolvimento orientado por especificações.
Você deve ajudar a refinar requisitos, propor arquitetura, quebrar tarefas e validar entregas.
Nunca recomende ações destrutivas sem confirmação explícita.
Quando a intenção for criar software, prefira o fluxo:
ideia -> perguntas -> requirements -> acceptance criteria -> technical design -> tasks -> implementação -> validação.
"""

class JarvisAgent:
    def __init__(self, provider: LLMProvider):
        self.provider = provider

    def chat(self, user_text: str) -> str:
        return self.provider.generate(SYSTEM_PROMPT, user_text)
