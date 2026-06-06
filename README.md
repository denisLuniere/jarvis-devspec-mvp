# Jarvis DevSpec MVP

Assistente local inspirado no J.A.R.V.I.S., focado em desenvolvimento orientado por especificações.

## Versão atual

v0.8.0

## Principais recursos

- Provider `browser` experimental para automatizar ChatGPT Web.
- Provider `manual` para usar ChatGPT Plus por copia-e-cola.
- Provider `fake` para testes sem IA real.
- Provider `openai` para API da OpenAI.
- Modo terminal: `jarvis --text`.
- Modo voz: `jarvis --voice`.
- Fluxo guiado de SPEC com `/spec start`.
- Diff, implementação e validação.

## Instalação base

```powershell
cd E:\Repositories\jarvis-devspec-mvp
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e .
```

## Instalação do browser provider

```powershell
pip install -e ".[browser]"
python -m playwright install chromium
```

## Configuração para automação do ChatGPT Web

No `.env`:

```env
JARVIS_PROVIDER=browser
JARVIS_ALLOWED_ROOT=E:\projects
JARVIS_REQUIRE_CONFIRMATION=true

JARVIS_BROWSER_URL=https://chatgpt.com/
JARVIS_BROWSER_PROFILE=.jarvis/browser-profile
JARVIS_BROWSER_HEADLESS=false
JARVIS_BROWSER_TIMEOUT_SECONDS=240
JARVIS_BROWSER_KEEP_OPEN=true

JARVIS_VOICE_ENABLED=false
```

## Como usar

```powershell
jarvis --text
```

Depois:

```text
/spec refine E:\projects\teste-jarvis registro-inconsistencias-wiki
```

Na primeira execução, o navegador abre e você faz login manualmente no ChatGPT. Depois disso, a sessão tende a ficar salva no perfil do Playwright.

## Fallback

Se a automação do browser falhar, o Jarvis cai automaticamente para o modo manual:

```text
Cole a resposta abaixo.
Finalize com <<<END>>>
```

## Fluxo recomendado

```text
/spec start E:\projects\teste-jarvis registro-inconsistencias-wiki
/spec refine E:\projects\teste-jarvis registro-inconsistencias-wiki
/spec design E:\projects\teste-jarvis registro-inconsistencias-wiki
/spec tasks E:\projects\teste-jarvis registro-inconsistencias-wiki
/spec diff E:\projects\teste-jarvis registro-inconsistencias-wiki 5
/spec implement E:\projects\teste-jarvis registro-inconsistencias-wiki 5
/spec validate E:\projects\teste-jarvis registro-inconsistencias-wiki
```

## Arquivos gerados pelo browser provider

```text
.jarvis/browser/outbox
.jarvis/browser/inbox
.jarvis/browser/errors
.jarvis/browser-profile
```

Não suba esses arquivos para o Git.

## Roadmap

### v0.9
- Melhorar detecção de estado do ChatGPT Web.
- Melhorar extração de resposta.
- Adicionar comando para abrir/reautenticar sessão.
- Adicionar confirmação antes de aplicar implementação real.
