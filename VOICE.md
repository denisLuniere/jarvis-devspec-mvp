# Modo Voz do Jarvis

## Instalação

Ative sua venv:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependências de voz:

```powershell
pip install -e .[voice]
```

Se o PyAudio falhar no Windows, tente:

```powershell
pip install pipwin
pipwin install pyaudio
pip install -e .[voice]
```

## Configuração

No `.env`:

```env
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

```powershell
jarvis
```

Com o modo voz ativo, fale:

```text
Jarvis, ajuda
Jarvis, abra o VS Code
Jarvis, abrir VS Code
Jarvis, abrir Google Chrome
Jarvis, Chrome
Jarvis, sair
```

## Melhorias da v0.2.2

- Entende "abra", "abrir", "abre", "inicie", "execute".
- Entende "vs code", "visual studio code", "google chrome".
- Corrige reconhecimentos comuns como "Chaves sair".
- Reinicializa o motor de voz se o pyttsx3 travar após a primeira fala.

## Observações

- O reconhecimento usa SpeechRecognition com Google Speech Recognition.
- Precisa de internet para reconhecer voz nesse modo inicial.
- A leitura usa pyttsx3, que funciona localmente usando as vozes do Windows.
- Se a voz em português não estiver instalada, o Windows pode ler com voz em inglês.
- Para melhor resultado, instale uma voz pt-BR nas configurações de idioma do Windows.
