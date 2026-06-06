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
- Provider injetado no SpecEngine.
- Prompts específicos para refinamento, design e tasks.

### v0.2.1
Concluído.

- Modo voz opcional.
- Speech-to-text com SpeechRecognition.
- Text-to-speech com pyttsx3.

### v0.2.2
Concluído.

- Normalização melhorada de comandos por voz.
- Correção de aliases: VS Code, Google Chrome, Chrome.
- Correção de variações: abra, abrir, abre, inicie, execute.
- Correção para reconhecimento comum "Chaves sair".
- TTS reinicializa se o pyttsx3 travar depois da primeira fala.

### v0.3
Concluído neste pacote.

- `/spec implement <projeto> <feature> <task-number>`
- `/spec implement <projeto> <feature> <task-number> --preview`
- Geração de proposta de implementação.
- Parser de blocos estruturados `file path=...`.
- Aplicação segura de arquivos.
- Relatório de implementação em `10-implementation`.

## Próximas versões

### v0.4: Validação
- `/spec validate <projeto> <feature>`
- Comandos configuráveis de validação.
- Atualização de `08-validation-report.md`.

### v1.0: DevSpec completo
- Refinar.
- Desenhar.
- Planejar.
- Implementar.
- Validar.
- Documentar.
