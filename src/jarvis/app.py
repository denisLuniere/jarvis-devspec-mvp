import argparse

from jarvis.config import load_config
from jarvis.providers import build_provider
from jarvis.core.agent import JarvisAgent
from jarvis.core.router import CommandRouter
from jarvis.core.safety import SafetyGuard
from jarvis.core.command_normalizer import normalize_voice_command
from jarvis.tools.file_tool import FileTool
from jarvis.tools.program_tool import ProgramTool
from jarvis.tools.shell_tool import ShellTool
from jarvis.specs.spec_engine import SpecEngine

def parse_args():
    parser = argparse.ArgumentParser(
        prog="jarvis",
        description="Jarvis DevSpec MVP"
    )

    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--voice",
        action="store_true",
        help="Inicia o Jarvis em modo voz, independentemente do .env."
    )
    mode.add_argument(
        "--text",
        action="store_true",
        help="Inicia o Jarvis em modo terminal, independentemente do .env."
    )

    parser.add_argument(
        "--no-tts",
        action="store_true",
        help="No modo voz, escuta comandos mas não fala respostas."
    )

    return parser.parse_args()

def should_enable_voice(config, args) -> bool:
    if args.text:
        return False
    if args.voice:
        return True
    return config.voice_enabled

def build_voice_loop(config, args):
    try:
        from jarvis.voice.stt import SpeechToText
        from jarvis.voice.tts import TextToSpeech
        from jarvis.voice.voice_loop import VoiceLoop

        stt = SpeechToText(
            language=config.voice_language,
            timeout=config.listen_timeout,
            phrase_time_limit=config.phrase_time_limit,
            wake_word=config.wake_word,
        )
        tts = TextToSpeech(
            enabled=(config.tts_enabled and not args.no_tts),
            rate=config.tts_rate,
            volume=config.tts_volume,
        )
        return VoiceLoop(stt, tts), None

    except Exception as exc:
        return None, exc

def build_app(args):
    config = load_config()
    guard = SafetyGuard(config.allowed_root)
    provider = build_provider(config)

    file_tool = FileTool(guard)
    spec_engine = SpecEngine(file_tool, provider=provider)
    program_tool = ProgramTool()
    shell_tool = ShellTool(guard, require_confirmation=config.require_confirmation)

    router = CommandRouter(spec_engine, program_tool, shell_tool)
    agent = JarvisAgent(provider)

    voice_loop = None
    voice_error = None

    if should_enable_voice(config, args):
        voice_loop, voice_error = build_voice_loop(config, args)

    return router, agent, voice_loop, config, voice_error

def print_and_speak(message: str, voice_loop) -> None:
    print(f"Jarvis > {message}\n")
    if voice_loop:
        voice_loop.say(message)

def main():
    args = parse_args()
    router, agent, voice_loop, config, voice_error = build_app(args)

    print("Jarvis DevSpec MVP iniciado.")
    print("Digite /help para comandos ou /exit para sair.")

    if voice_error:
        print("Jarvis > Modo voz solicitado, mas não consegui iniciar a voz.")
        print(f"Jarvis > Motivo: {voice_error}")
        print('Jarvis > Continuando em modo terminal. Para voz, instale: pip install -e ".[voice]"')
        print("Jarvis > Você também pode iniciar direto em terminal com: jarvis --text")

    if voice_loop:
        print(f"Modo voz: ATIVO | idioma={config.voice_language} | wake word='{config.wake_word}'")
        print("Fale comandos como: 'Jarvis, ajuda', 'Jarvis, abra o VS Code' ou 'Jarvis, sair'.")
    else:
        print("Modo terminal: ATIVO")
        print("Para iniciar com voz: jarvis --voice")
    print()

    if voice_loop:
        voice_loop.say("Jarvis iniciado. Modo voz ativo.")

    while True:
        try:
            if voice_loop:
                spoken_text = voice_loop.get_input().strip()
                user_text = normalize_voice_command(spoken_text, wake_word=config.wake_word)
                if spoken_text and user_text != spoken_text:
                    print(f"Jarvis > Comando interpretado: {user_text}")
            else:
                user_text = input("Você > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEncerrando Jarvis.")
            break

        if not user_text:
            continue

        if user_text.lower() in {"/exit", "exit", "sair"}:
            print_and_speak("Até mais.", voice_loop)
            break

        try:
            routed = router.route(user_text)
            if routed is not None:
                print_and_speak(routed, voice_loop)
                continue

            response = agent.chat(user_text)
            print_and_speak(response, voice_loop)
        except Exception as exc:
            print_and_speak(f"Erro: {exc}", voice_loop)

if __name__ == "__main__":
    main()
