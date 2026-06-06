# Jarvis DevSpec MVP

Assistente local inspirado no J.A.R.V.I.S., focado em desenvolvimento orientado por especificações.

## Versão atual

v0.5.0

## Principais recursos

- Modo terminal: `jarvis --text`.
- Modo voz: `jarvis --voice`.
- Fluxo guiado de SPEC com `/spec start`.
- Status da feature com `/spec status`.
- Refinamento, design, tasks, implementação e validação.
- Validation Engine com `.jarvis/validation.toml`.
- Aplicação segura de arquivos via blocos `file path=...`.

## Instalação

```powershell
cd E:\Repositories\jarvis-devspec-mvp
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
```

Para tudo:

```powershell
pip install -e ".[all]"
```

## Formas de iniciar

```powershell
jarvis --text
jarvis --voice
jarvis --voice --no-tts
```

## Fluxo recomendado

Agora você pode começar uma feature com um comando só:

```text
/spec start E:\projects\teste-jarvis registro-inconsistencias-wiki
```

Esse comando faz, de forma idempotente:

1. cria `.jarvis/`, se não existir;
2. cria a SPEC da feature, se não existir;
3. cria `.jarvis/validation.toml`, se não existir;
4. mostra o status da estrutura.

Depois siga:

```text
/spec refine E:\projects\teste-jarvis registro-inconsistencias-wiki
/spec design E:\projects\teste-jarvis registro-inconsistencias-wiki
/spec tasks E:\projects\teste-jarvis registro-inconsistencias-wiki
/spec implement E:\projects\teste-jarvis registro-inconsistencias-wiki 5 --preview
/spec implement E:\projects\teste-jarvis registro-inconsistencias-wiki 5
/spec validate E:\projects\teste-jarvis registro-inconsistencias-wiki
```

## Comandos

```text
/help
/spec start E:\projects\teste-jarvis registro-inconsistencias-wiki
/spec status E:\projects\teste-jarvis registro-inconsistencias-wiki
/spec init E:\projects\teste-jarvis
/spec new E:\projects\teste-jarvis registro-inconsistencias-wiki
/spec list E:\projects\teste-jarvis
/spec refine E:\projects\teste-jarvis registro-inconsistencias-wiki
/spec design E:\projects\teste-jarvis registro-inconsistencias-wiki
/spec tasks E:\projects\teste-jarvis registro-inconsistencias-wiki
/spec implement E:\projects\teste-jarvis registro-inconsistencias-wiki 5
/spec implement E:\projects\teste-jarvis registro-inconsistencias-wiki 5 --preview
/spec validate E:\projects\teste-jarvis registro-inconsistencias-wiki
/open vscode
/open chrome
/run E:\projects\teste-jarvis mvn test
/exit
```

## Validation Engine

O arquivo abaixo define as validações:

```text
.jarvis/validation.toml
```

Exemplo Java/Spring:

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

Exemplo Python:

```toml
[[commands]]
name = "Python compileall"
command = "python -m compileall src"
timeout_seconds = 180

[[commands]]
name = "Pytest"
command = "pytest"
timeout_seconds = 300
```

## Roadmap

### v0.6
- Modo diff antes de aplicar arquivos.
- Auto-detecção de stack.
- Sugestão automática de `validation.toml`.
- Melhor suporte a prompts reais com OpenAI/Claude.
