# Jarvis DevSpec MVP

Assistente local inspirado no J.A.R.V.I.S., focado em desenvolvimento orientado por especificações.

## Versão atual

v0.2.2

## Funcionalidades

- Conversar via terminal.
- Modo voz opcional.
- Leitura das respostas em voz alta.
- Criar estrutura `.jarvis/` dentro de projetos.
- Criar nova SPEC de funcionalidade.
- Gerar perguntas de refinamento via IA.
- Gerar design técnico via IA.
- Gerar tasks via IA.
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

## Uso

```bash
jarvis
```

Ou:

```bash
python -m jarvis.app
```

## Comandos de texto

```text
/help
/spec init E:\Repositories\meu-projeto
/spec new E:\Repositories\meu-projeto registro-inconsistencias-wiki
/spec list E:\Repositories\meu-projeto
/spec refine E:\Repositories\meu-projeto registro-inconsistencias-wiki
/spec design E:\Repositories\meu-projeto registro-inconsistencias-wiki
/spec tasks E:\Repositories\meu-projeto registro-inconsistencias-wiki
/open vscode
/open chrome
/run E:\Repositories\meu-projeto mvn test
/exit
```

## Comandos de voz

```text
Jarvis, ajuda
Jarvis, abra o VS Code
Jarvis, abrir Google Chrome
Jarvis, sair
```

Você também pode ditar comandos completos, mas caminhos Windows longos podem ser difíceis para o reconhecimento de fala.

## Fluxo recomendado para Specs

```text
1. /spec init <projeto>
2. Edite .jarvis/project-context.md
3. Edite .jarvis/architecture.md
4. /spec new <projeto> <feature>
5. Edite 01-requirements.md com a ideia inicial
6. /spec refine <projeto> <feature>
7. Responda as perguntas no arquivo 02-questions.md
8. Ajuste 04-acceptance-criteria.md
9. /spec design <projeto> <feature>
10. /spec tasks <projeto> <feature>
```

## Roadmap

### v0.3
- Implementar task por task.
- Gerar patches/arquivos de código.
- Relatar arquivos alterados.

### v0.4
- Validation engine.
- Rodar testes/build/lint configuráveis.
- Atualizar validation-report.md.

### v1.0
- Fluxo completo:
  ideia -> spec -> design -> tasks -> implementação -> testes -> validação.


## Correções da v0.2.2

- Melhor normalização de comandos de voz.
- Suporte a "abra", "abrir", "abre", "inicie", "execute".
- Suporte a aliases como "vs code", "visual studio code" e "google chrome".
- Correção para reconhecimentos comuns como "Chaves sair".
- TTS mais robusto após a primeira fala.
