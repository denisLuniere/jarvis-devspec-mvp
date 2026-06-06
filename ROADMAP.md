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
- Atalhos falados:
  - "Jarvis, ajuda"
  - "Jarvis, abrir vscode"
  - "Jarvis, abrir chrome"
  - "Jarvis, sair"


### v0.2.2
Concluído.

- Normalização melhorada de comandos por voz.
- Correção de aliases: VS Code, Google Chrome, Chrome.
- Correção de variações: abra, abrir, abre, inicie, execute.
- Correção para reconhecimento comum "Chaves sair".
- TTS reinicializa se o pyttsx3 travar depois da primeira fala.

## Próximas versões

### v0.3: Implementação assistida
- `/spec implement <projeto> <feature> <task-number>`
- Leitura de contexto da spec.
- Geração de código por arquivos.
- Aplicação segura de alterações.
- Relatório de arquivos alterados.

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
