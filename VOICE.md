# Modo Voz do Jarvis

## Modos disponíveis

A partir da v0.3.1, o Jarvis pode iniciar em modo texto ou voz.

### Terminal sempre

```powershell
jarvis --text
```

### Voz

```powershell
jarvis --voice
```

### Sem parâmetro

```powershell
jarvis
```

Nesse caso, ele usa o valor do `.env`:

```env
JARVIS_VOICE_ENABLED=false
```

Recomendação: deixe `false` por padrão e use `jarvis --voice` quando quiser falar com ele.

## Instalação do modo voz

```powershell
pip install -e ".[voice]"
```

Se o PyAudio falhar no Windows:

```powershell
pip install pipwin
pipwin install pyaudio
pip install -e ".[voice]"
```

## Configuração

```env
JARVIS_VOICE_ENABLED=false
JARVIS_VOICE_LANGUAGE=pt-BR
JARVIS_TTS_ENABLED=true
JARVIS_TTS_RATE=185
JARVIS_TTS_VOLUME=1.0
JARVIS_WAKE_WORD=jarvis
JARVIS_LISTEN_TIMEOUT=5
JARVIS_PHRASE_TIME_LIMIT=12
```

## Comandos de voz

```text
Jarvis, ajuda
Jarvis, abra o VS Code
Jarvis, abrir Google Chrome
Jarvis, Chrome
Jarvis, sair
```

## Voz sem resposta falada

```powershell
jarvis --voice --no-tts
```

Isso permite ditar comandos, mas o Jarvis responde só no terminal.

## Fallback automático

Se o `.env` estiver com `JARVIS_VOICE_ENABLED=true`, mas as dependências de voz não estiverem instaladas, o Jarvis não quebra mais. Ele mostra o erro e continua em modo terminal.

## Observações

- O reconhecimento usa SpeechRecognition com Google Speech Recognition.
- Precisa de internet para reconhecer voz nesse modo inicial.
- A leitura usa pyttsx3, que funciona localmente usando as vozes do Windows.
