# Roadmap do Jarvis DevSpec

## v0.1
- CLI.
- SPEC init.
- SPEC new.
- Segurança básica.

## v0.2
- Refinamento.
- Design.
- Tasks.

## v0.3
- Implementação por task.
- Preview.
- Aplicação segura de arquivos.

## v0.4
- Validation Engine.
- `.jarvis/validation.toml`.

## v0.5
- `/spec start`.
- `/spec status`.

## v0.6
- `/spec diff`.
- Diff real no relatório.

## v0.7
- `JARVIS_PROVIDER=manual`.

## v0.8
Concluído.

- `JARVIS_PROVIDER=browser`.
- Automação experimental do ChatGPT Web com Playwright.
- Sessão persistente em `.jarvis/browser-profile`.
- Fallback automático para modo manual.
- Registro de prompts, respostas e erros.

## Próximas versões

### v0.9
- Robustez do browser provider.
- Reautenticação guiada.
- Melhor extração de resposta.
- Confirmação interativa antes de aplicar arquivos.


## v0.8.1
Concluído neste pacote.

- Logs detalhados no Browser Provider.
- Validação se o prompt foi enviado.
- Timeout curto para detectar falha de envio.
- `JARVIS_BROWSER_SUBMIT_MODE=enter|button`.
- `JARVIS_BROWSER_SEND_CHECK_SECONDS`.
- Fallback manual em caso de envio não detectado.


## v0.8.2
Concluído neste pacote.

- Contrato mais forte para respostas de implementação.
- Segunda tentativa automática quando a resposta não contém blocos `file path=...`.
- Prompt do browser provider reforçado para `/spec diff` e `/spec implement`.
- Fallback para arquivo de bloqueio quando não houver contexto suficiente.


## v0.8.3
Concluído neste pacote.

- Corrige método ausente `_build_missing_file_blocks_correction_prompt`.
- Mantém segunda tentativa automática para respostas sem blocos `file path=...`.
- Evita quebra total caso a tentativa de correção falhe.


## v0.8.4
Concluído neste pacote.

- Parser aceita marcadores browser-safe:
  `<<<FILE path=...>>>` e `<<<END_FILE>>>`.
- Prompts de implementação passam a preferir marcadores.
- Browser Provider fica menos dependente de cercas Markdown.
- Formato antigo ```file path=...``` continua aceito.


## v0.8.5
Concluído neste pacote.

- Prompt lista arquivos oficiais numerados da SPEC.
- Normalização automática de aliases:
  `decisions.md` -> `03-decisions.md`.
- Diff mostra nota de normalização quando ocorrer.
- Aplicação usa caminho normalizado.
