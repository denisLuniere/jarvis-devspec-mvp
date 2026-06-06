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

def build_implement_prompt(
    context: str,
    feature_name: str,
    task_number: str,
    requirements: str,
    questions: str,
    decisions: str,
    acceptance: str,
    design: str,
    tasks: str,
) -> str:
    return f"""
Você deve implementar uma task específica de uma SPEC.

Funcionalidade:
{feature_name}

Task solicitada:
{task_number}

Arquivos oficiais da SPEC:
- `.jarvis/specs/{feature_name}/01-requirements.md`
- `.jarvis/specs/{feature_name}/02-questions.md`
- `.jarvis/specs/{feature_name}/03-decisions.md`
- `.jarvis/specs/{feature_name}/04-acceptance-criteria.md`
- `.jarvis/specs/{feature_name}/05-technical-design.md`
- `.jarvis/specs/{feature_name}/06-tasks.md`
- `.jarvis/specs/{feature_name}/07-test-plan.md`
- `.jarvis/specs/{feature_name}/08-validation-report.md`
- `.jarvis/specs/{feature_name}/09-changelog.md`

Não crie arquivos paralelos como `decisions.md`, `requirements.md` ou `tasks.md` dentro da pasta da SPEC. Use sempre os nomes oficiais numerados.

Contexto do projeto:
{context}

Requirements:
{requirements}

Questions:
{questions}

Decisions:
{decisions}

Acceptance Criteria:
{acceptance}

Technical Design:
{design}

Tasks:
{tasks}

CONTRATO OBRIGATÓRIO PARA IMPLEMENTAÇÃO:
A resposta será processada por um parser automático. Para que o Jarvis consiga aplicar ou gerar diff, você DEVE retornar pelo menos um bloco de arquivo no formato exato:

<<<FILE path=caminho/relativo/ao/projeto.ext>>>
conteúdo completo do arquivo aqui
<<<END_FILE>>>

Regras obrigatórias:
1. Implemente somente a task solicitada.
2. Respeite arquitetura, padrões e convenções do projeto.
3. Não apague arquivos.
4. Não altere arquivos fora do escopo da task.
5. O caminho deve ser relativo à raiz do projeto.
5.1. Para alterar decisões da SPEC, use obrigatoriamente `.jarvis/specs/{feature_name}/03-decisions.md`.
6. Não use caminhos absolutos.
7. Não use `..` no caminho.
8. Não use blocos `python`, `java`, `sql`, `markdown` ou similares para arquivos. Prefira marcadores `<<<FILE path=...>>>` e `<<<END_FILE>>>`.
9. Se a task não permitir implementação por falta de contexto, ainda assim crie um arquivo de relatório técnico em `docs/jarvis-blockers/task-{task_number}-blockers.md` usando bloco `file path=...`.
10. Inclua ao final uma seção "Validações sugeridas".

IMPORTANTE:
- Se você não retornar marcador `<<<FILE path=...>>>` ou bloco `file path=...`, o Jarvis considerará que nada foi implementado.
- Para criar SQL, Markdown, Python, Java ou qualquer outro arquivo, coloque o conteúdo dentro de um bloco `file path=...`.

Formato esperado:
# Implementação proposta

## Resumo

## Arquivos propostos

```file path=src/exemplo/Arquivo.ext
conteúdo
```

## Validações sugeridas
- comando ou validação
"""
