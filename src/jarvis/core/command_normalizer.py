import re
import unicodedata

APP_ALIASES = {
    "vscode": "vscode",
    "vs code": "vscode",
    "visual studio code": "vscode",
    "code": "vscode",
    "google chrome": "chrome",
    "chrome": "chrome",
    "crome": "chrome",
    "edge": "edge",
    "microsoft edge": "edge",
    "bloco de notas": "notepad",
    "notepad": "notepad",
    "explorador": "explorer",
    "explorer": "explorer",
    "terminal": "terminal",
    "windows terminal": "terminal",
}

EXIT_WORDS = {
    "sair",
    "encerrar",
    "fechar",
    "parar",
    "desligar",
    "tchau",
    "até mais",
    "ate mais",
}

HELP_WORDS = {
    "ajuda",
    "help",
    "comandos",
    "listar comandos",
    "mostre os comandos",
}

def strip_accents(value: str) -> str:
    normalized = unicodedata.normalize("NFD", value)
    return "".join(char for char in normalized if unicodedata.category(char) != "Mn")

def normalize_spaces(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()

def normalize_text(value: str) -> str:
    value = strip_accents(value.lower())
    value = value.replace(",", " ").replace(".", " ").replace(";", " ")
    value = normalize_spaces(value)
    return value

def remove_wake_word(value: str, wake_word: str = "jarvis") -> str:
    normalized = normalize_text(value)
    wake = normalize_text(wake_word)

    # Reconhecimentos comuns errados para "Jarvis" em pt-BR.
    wake_aliases = {wake, "jarves", "jarvis", "chaves", "javis", "charles"}

    for alias in wake_aliases:
        if normalized == alias:
            return ""
        if normalized.startswith(alias + " "):
            return normalized[len(alias):].strip()

    return normalized

def app_alias_to_key(app_text: str) -> str:
    app_text = normalize_text(app_text)

    # Remove duplicações comuns do STT: "google chrome chrome"
    tokens = app_text.split()
    deduped = []
    for token in tokens:
        if not deduped or deduped[-1] != token:
            deduped.append(token)
    app_text = " ".join(deduped)

    # Match direto.
    if app_text in APP_ALIASES:
        return APP_ALIASES[app_text]

    # Match por contenção, do alias mais longo para o mais curto.
    for alias in sorted(APP_ALIASES, key=len, reverse=True):
        if alias in app_text:
            return APP_ALIASES[alias]

    return app_text

def normalize_voice_command(text: str, wake_word: str = "jarvis") -> str:
    command = remove_wake_word(text, wake_word=wake_word)

    if not command:
        return ""

    if command in EXIT_WORDS:
        return "/exit"

    if command in HELP_WORDS:
        return "/help"

    open_prefixes = [
        "abrir ",
        "abra ",
        "abre ",
        "abrir o ",
        "abrir a ",
        "abra o ",
        "abra a ",
        "abre o ",
        "abre a ",
        "iniciar ",
        "inicie ",
        "executar ",
        "execute ",
    ]

    for prefix in open_prefixes:
        if command.startswith(prefix):
            app_text = command[len(prefix):].strip()
            return f"/open {app_alias_to_key(app_text)}"

    # Permite que a pessoa fale "vs code" diretamente.
    app_key = app_alias_to_key(command)
    if app_key in {"vscode", "chrome", "edge", "notepad", "explorer", "terminal"}:
        return f"/open {app_key}"

    return text.strip()
