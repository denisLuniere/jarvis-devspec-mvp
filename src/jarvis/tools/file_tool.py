from pathlib import Path
from jarvis.core.safety import SafetyGuard

class FileTool:
    def __init__(self, guard: SafetyGuard):
        self.guard = guard

    def write_text(self, path: Path, content: str) -> str:
        self.guard.require_allowed_path(path.parent)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return f"Arquivo criado/atualizado: {path}"

    def read_text(self, path: Path) -> str:
        self.guard.require_allowed_path(path)
        return path.read_text(encoding="utf-8")
