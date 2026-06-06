# Jarvis DevSpec MVP

Assistente local inspirado no J.A.R.V.I.S., focado em desenvolvimento orientado por especificações.

## Versão atual

v0.4.0

## Funcionalidades

- Conversar via terminal.
- Iniciar explicitamente em modo terminal com `jarvis --text`.
- Iniciar explicitamente em modo voz com `jarvis --voice`.
- Fallback automático para terminal quando dependências de voz faltarem.
- Criar estrutura `.jarvis/` dentro de projetos.
- Criar nova SPEC de funcionalidade.
- Gerar perguntas de refinamento via IA.
- Gerar design técnico via IA.
- Gerar tasks via IA.
- Implementar task por task via IA.
- Aplicar arquivos propostos com blocos estruturados.
- Gerar relatório de implementação.
- Rodar validações configuráveis com `/spec validate`.
- Atualizar `08-validation-report.md`.
- Abrir programas no Windows por comandos permitidos.
- Rodar comandos locais somente com confirmação.
- Usar provider `fake`, `openai` ou `anthropic`.

## Instalação

```powershell
cd E:\Repositories\jarvis-devspec-mvp
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
```

Para voz:

```powershell
pip install -e ".[voice]"
```

Para tudo:

```powershell
pip install -e ".[all]"
```

## Formas de iniciar

Modo terminal:

```powershell
jarvis --text
```

Modo voz:

```powershell
jarvis --voice
```

Modo voz sem resposta falada:

```powershell
jarvis --voice --no-tts
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
/spec validate E:\Repositories\meu-projeto registro-inconsistencias-wiki
/open vscode
/open chrome
/run E:\Repositories\meu-projeto mvn test
/exit
```

## Validation Engine

Ao rodar:

```text
/spec validate E:\Repositories\meu-projeto registro-inconsistencias-wiki
```

o Jarvis cria, se ainda não existir:

```text
.jarvis/validation.toml
```

Configuração padrão:

```toml
[[commands]]
name = "Python compileall"
command = "python -m compileall src"
timeout_seconds = 180
```

Você pode ajustar para Java/Spring Boot:

```toml
[[commands]]
name = "Maven tests"
command = "mvn test"
timeout_seconds = 300

[[commands]]
name = "Maven package"
command = "mvn clean package -DskipTests"
timeout_seconds = 300
```

Para frontend:

```toml
[[commands]]
name = "NPM test"
command = "npm test"
timeout_seconds = 300

[[commands]]
name = "NPM build"
command = "npm run build"
timeout_seconds = 300
```

Para Python:

```toml
[[commands]]
name = "Pytest"
command = "pytest"
timeout_seconds = 300

[[commands]]
name = "Ruff"
command = "ruff check ."
timeout_seconds = 180
```

O relatório é salvo em:

```text
.jarvis/specs/<feature>/08-validation-report.md
```

## Como o Jarvis aplica arquivos

A IA precisa retornar blocos assim:

```text
```file path=src/main/java/br/com/exemplo/Cliente.java
conteúdo completo do arquivo
```
```

O Jarvis só aplica arquivos com caminhos relativos ao projeto.

## Roadmap

### v0.5
- Melhorar TTS/STT.
- Melhorar prompts de implementação.
- Criar modo diff antes de aplicar arquivos.

### v1.0
- Fluxo completo:
  ideia -> spec -> design -> tasks -> implementação -> testes -> validação.
