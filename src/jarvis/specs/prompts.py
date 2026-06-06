def build_refine_prompt(context: str, feature_name: str, requirements: str, questions: str) -> str:
    return f"""
Você deve refinar a especificação de uma funcionalidade.

Tarefa:
Gere perguntas de refinamento objetivas para completar a SPEC antes de qualquer implementação.

Funcionalidade:
{feature_name}

Contexto do projeto:
{context}

Requirements atuais:
{requirements}

Questions atuais:
{questions}

Formato esperado:
# Perguntas de Refinamento

- [ ] Pergunta 1
- [ ] Pergunta 2

Inclua perguntas sobre objetivo, usuários, campos, regras de negócio, integrações, erros, segurança, logs, testes e critérios de aceite.
"""

def build_design_prompt(context: str, feature_name: str, requirements: str, decisions: str, acceptance: str) -> str:
    return f"""
Você deve gerar o design técnico de uma funcionalidade, respeitando a arquitetura do projeto.

Tarefa:
Gere o design técnico completo.

Funcionalidade:
{feature_name}

Contexto do projeto:
{context}

Requirements:
{requirements}

Decisions:
{decisions}

Acceptance Criteria:
{acceptance}

Formato esperado:
# Technical Design

## Estratégia técnica
## Camadas/arquivos esperados
## Persistência
## Endpoints/Interfaces
## Validações
## Testes necessários
## Riscos técnicos
"""

def build_tasks_prompt(context: str, feature_name: str, requirements: str, design: str, acceptance: str) -> str:
    return f"""
Você deve gerar uma lista de tasks pequenas, sequenciais e implementáveis.

Funcionalidade:
{feature_name}

Contexto do projeto:
{context}

Requirements:
{requirements}

Technical Design:
{design}

Acceptance Criteria:
{acceptance}

Formato esperado:
# Tasks

- [ ] 1. ...
- [ ] 2. ...

As tasks devem ser pequenas, testáveis e respeitar a arquitetura. Inclua tasks de testes e validação.
"""
