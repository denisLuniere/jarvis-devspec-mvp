# Browser Provider Experimental

O provider `browser` tenta automatizar o ChatGPT Web usando Playwright.

## Objetivo

Reduzir o copia-e-cola do provider `manual` durante o desenvolvimento do Jarvis, sem usar API paga.

## Instalação

```powershell
cd E:\Repositories\jarvis-devspec-mvp
.\.venv\Scripts\Activate.ps1
pip install -e ".[browser]"
python -m playwright install chromium
```

## Configuração

No `.env`:

```env
JARVIS_PROVIDER=browser
JARVIS_ALLOWED_ROOT=E:\projects

JARVIS_BROWSER_URL=https://chatgpt.com/
JARVIS_BROWSER_PROFILE=.jarvis/browser-profile
JARVIS_BROWSER_HEADLESS=false
JARVIS_BROWSER_TIMEOUT_SECONDS=240
JARVIS_BROWSER_KEEP_OPEN=true
JARVIS_VOICE_ENABLED=false
```

## Primeiro uso

Execute:

```powershell
jarvis --text
```

Rode um comando que precise de IA:

```text
/spec refine E:\projects\teste-jarvis registro-inconsistencias-wiki
```

O navegador abrirá. Se pedir login, faça login manualmente. A sessão ficará salva em:

```text
.jarvis/browser-profile
```

## Limitações

Este provider é experimental.

Ele pode quebrar se:

- a interface do ChatGPT mudar;
- aparecer captcha;
- aparecer etapa de login;
- aparecer modal;
- o seletor da caixa de texto mudar;
- a resposta demorar demais.

Quando falhar, ele cai para o fallback manual: você cola a resposta no terminal e finaliza com `<<<END>>>`.

## Segurança

O Jarvis não armazena sua senha. O login fica na sessão local do navegador Playwright.
Não suba `.jarvis/browser-profile` para o Git.


## Troubleshooting: travou no envio

Se o Jarvis abrir o ChatGPT, mas não conseguir enviar a pergunta, tente trocar o modo de envio no `.env`:

```env
JARVIS_BROWSER_SUBMIT_MODE=button
```

Ou volte para:

```env
JARVIS_BROWSER_SUBMIT_MODE=enter
```

A v0.8.1 valida se o envio começou. Se não detectar envio em `JARVIS_BROWSER_SEND_CHECK_SECONDS`, ele cai para fallback manual.
