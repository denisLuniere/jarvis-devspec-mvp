# Roadmap do Jarvis DevSpec

## Visão

Construir um assistente local capaz de conversar por voz, entender especificações, gerar código dentro da arquitetura definida e validar funcionalidades com segurança.

## Status atual

### v0.1
Concluído.

- CLI.
- SPEC init.
- SPEC new.
- Abertura de programas.
- Shell com confirmação.
- Segurança básica.

### v0.2
Concluído.

- `/spec refine`
- `/spec design`
- `/spec tasks`
- `/spec list`

### v0.3
Concluído.

- `/spec implement <projeto> <feature> <task-number>`
- `/spec implement <projeto> <feature> <task-number> --preview`
- Aplicação segura de arquivos.
- Relatório de implementação.

### v0.3.1
Concluído.

- `jarvis --text`
- `jarvis --voice`
- `jarvis --voice --no-tts`
- Fallback automático para terminal.

### v0.4
Concluído neste pacote.

- `/spec validate <projeto> <feature>`
- `.jarvis/validation.toml`
- Execução de comandos configuráveis.
- Timeout por comando.
- Atualização automática de `08-validation-report.md`.
- Resumo de sucesso/falha.

## Próximas versões

### v0.5
- Modo diff antes de aplicar arquivos.
- Melhorar suporte a voz.
- Melhorar leitura de estrutura do projeto.
- Sugestão automática de comandos de validação conforme stack.

### v1.0
- Refinar.
- Desenhar.
- Planejar.
- Implementar.
- Validar.
- Documentar.
