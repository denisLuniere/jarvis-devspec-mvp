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

Regras obrigatórias:
1. Implemente somente a task solicitada.
2. Respeite arquitetura, padrões e convenções do projeto.
3. Não apague arquivos.
4. Não altere arquivos fora do escopo da task.
5. Se não houver informação suficiente, gere apenas um relatório explicando o bloqueio.
6. Quando quiser criar ou alterar arquivos, use exclusivamente blocos neste formato:

```file path=caminho/relativo/ao/projeto.ext
conteúdo completo do arquivo aqui
```

7. O caminho deve ser relativo à raiz do projeto.
8. Não use caminhos absolutos.
9. Não use `..` no caminho.
10. Inclua ao final uma seção "Validações sugeridas".

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
