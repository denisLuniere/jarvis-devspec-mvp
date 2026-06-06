from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        raise NotImplementedError

class FakeProvider(LLMProvider):
    def generate(self, system_prompt: str, user_prompt: str) -> str:
        lower_prompt = user_prompt.lower()

        if "gere perguntas de refinamento" in lower_prompt or "refinar a especificação" in lower_prompt:
            return """# Perguntas de Refinamento

- [ ] Qual é o objetivo principal da funcionalidade?
- [ ] Quem será o usuário principal?
- [ ] Quais campos ou dados são obrigatórios?
- [ ] Quais regras de negócio precisam ser respeitadas?
- [ ] Quais cenários de erro devem ser tratados?
- [ ] Existe integração com banco, API, fila, Databricks ou outro sistema?
- [ ] Quais critérios indicam que a funcionalidade foi concluída com sucesso?
"""

        if "gere o design técnico" in lower_prompt:
            return """# Technical Design

## Estratégia técnica

Implementar a funcionalidade respeitando a arquitetura definida em `.jarvis/architecture.md`.

## Camadas sugeridas

- Interface/Controller/Notebook/Job: receber entrada e expor a funcionalidade.
- Service/Use Case: concentrar regras de negócio.
- Repository/Gateway: acessar dados externos ou persistência.
- DTO/Model: padronizar entrada e saída.
- Tests: validar regras e cenários de erro.

## Validações

- Validar campos obrigatórios.
- Validar regras de negócio.
- Tratar erros conhecidos.
- Registrar logs quando aplicável.

## Riscos técnicos

- Especificação incompleta.
- Dependências externas não mapeadas.
- Testes insuficientes.
"""

        if "gere uma lista de tasks" in lower_prompt:
            return """# Tasks

- [ ] 1. Revisar requisitos e perguntas respondidas.
- [ ] 2. Atualizar critérios de aceite.
- [ ] 3. Definir modelo de dados/DTOs.
- [ ] 4. Implementar camada de domínio ou validação.
- [ ] 5. Implementar service/use case.
- [ ] 6. Implementar interface de entrada.
- [ ] 7. Criar testes unitários.
- [ ] 8. Criar testes de integração, se aplicável.
- [ ] 9. Rodar build/testes/lint.
- [ ] 10. Atualizar relatório de validação.
"""

        return (
            "Sou o Jarvis DevSpec MVP em modo local/fake. "
            "Para respostas inteligentes reais, configure JARVIS_PROVIDER=openai ou anthropic no .env."
        )
