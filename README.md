# Jarvis DevSpec MVP

Assistente local inspirado no J.A.R.V.I.S., focado em desenvolvimento orientado por especificações.

## Versão atual

v0.3.0

## Funcionalidades

- Conversar via terminal.
- Modo voz opcional.
- Leitura das respostas em voz alta.
- Criar estrutura `.jarvis/` dentro de projetos.
- Criar nova SPEC de funcionalidade.
- Gerar perguntas de refinamento via IA.
- Gerar design técnico via IA.
- Gerar tasks via IA.
- Implementar task por task via IA.
- Aplicar arquivos propostos com blocos estruturados.
- Gerar relatório de implementação.
- Abrir programas no Windows por comandos permitidos.
- Rodar comandos locais somente com confirmação.
- Usar provider `fake`, `openai` ou `anthropic`.
- Bloquear comandos perigosos básicos.

## Instalação

Requer Python 3.11+.

```bash
cd jarvis-devspec-mvp
python -m venv .venv
.venv\Scripts\activate
pip install -e .
```

Para usar OpenAI:

```bash
pip install -e .[openai]
```

Para usar Claude:

```bash
pip install -e .[anthropic]
```

Para usar voz:

```bash
pip install -e .[voice]
```

## Exemplo de `.env`

```env
JARVIS_PROVIDER=fake
JARVIS_MODEL=gpt-4.1-mini
JARVIS_ALLOWED_ROOT=E:\Repositories
JARVIS_REQUIRE_CONFIRMATION=true

JARVIS_VOICE_ENABLED=true
JARVIS_VOICE_LANGUAGE=pt-BR
JARVIS_TTS_ENABLED=true
JARVIS_TTS_RATE=185
JARVIS_TTS_VOLUME=1.0
JARVIS_WAKE_WORD=jarvis
JARVIS_LISTEN_TIMEOUT=5
JARVIS_PHRASE_TIME_LIMIT=12
```

## Comandos

```text
/help
/spec init E:\Repositories\meu-projeto
/spec new E:\Repositories\meu-projeto registro-inconsistencias-wiki
/spec list E:\Repositories\meu-projeto
/spec refine E:\Repositories\meu-projeto registro-inconsistencias-wiki
/spec design E:\Repositories\meu-projeto registro-inconsistencias-wiki
/spec tasks E:\Repositories\meu-projeto registro-inconsistencias-wiki
/spec implement E:\Repositories\meu-projeto registro-inconsistencias-wiki 5
/spec implement E:\Repositories\meu-projeto registro-inconsistencias-wiki 5 --preview
/open vscode
/open chrome
/run E:\Repositories\meu-projeto mvn test
/exit
```

## Novo fluxo da v0.3

```text
1. /spec init <projeto>
2. Editar .jarvis/project-context.md
3. Editar .jarvis/architecture.md
4. /spec new <projeto> <feature>
5. Editar 01-requirements.md
6. /spec refine <projeto> <feature>
7. Responder 02-questions.md
8. Ajustar 04-acceptance-criteria.md
9. /spec design <projeto> <feature>
10. /spec tasks <projeto> <feature>
11. /spec implement <projeto> <feature> <numero-task> --preview
12. Revisar proposta
13. /spec implement <projeto> <feature> <numero-task>
```

## Como o Jarvis aplica arquivos

A IA precisa retornar blocos assim:

```text
```file path=src/main/java/br/com/exemplo/Cliente.java
conteúdo completo do arquivo
```
```

O Jarvis só aplica arquivos com caminhos relativos ao projeto.

Bloqueios básicos:

- caminhos absolutos;
- caminhos com `..`;
- `.git`;
- `.venv`;
- executáveis e scripts sensíveis como `.exe`, `.bat`, `.cmd`, `.ps1`, `.key`, `.pem`.

## Relatórios

Cada implementação gera arquivos em:

```text
.jarvis/specs/<feature>/10-implementation/
```

Exemplo:

```text
task-5-20260606-153012-proposal.md
task-5-20260606-153012-report.md
```

## Roadmap

### v0.4
- Validation engine.
- Rodar testes/build/lint configuráveis.
- Atualizar validation-report.md.

### v1.0
- Fluxo completo:
  ideia -> spec -> design -> tasks -> implementação -> testes -> validação.
