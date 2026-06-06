from dataclasses import dataclass
from pathlib import Path
import re

@dataclass(frozen=True)
class ProposedFile:
    relative_path: str
    content: str

class ImplementationParser:
    # Supported:
    # ```file path=src/Foo.java
    # content
    # ```
    FILE_BLOCK_RE = re.compile(
        r"```file\s+path=(?P<path>[^\n\r]+)\r?\n(?P<content>.*?)```",
        re.DOTALL | re.IGNORECASE,
    )

    def parse_files(self, text: str) -> list[ProposedFile]:
        files: list[ProposedFile] = []

        for match in self.FILE_BLOCK_RE.finditer(text):
            rel_path = match.group("path").strip().strip('"').strip("'")
            content = match.group("content")

            if content.startswith("\n"):
                content = content[1:]

            files.append(ProposedFile(relative_path=rel_path, content=content.rstrip() + "\n"))

        return files

class ImplementationApplier:
    BLOCKED_PARTS = {"..", ".git", ".venv", "venv", "__pycache__"}
    BLOCKED_EXTENSIONS = {".exe", ".dll", ".bat", ".cmd", ".ps1", ".pfx", ".pem", ".key"}

    def __init__(self, file_tool):
        self.file_tool = file_tool

    def validate_relative_path(self, relative_path: str) -> tuple[bool, str]:
        path = Path(relative_path)

        if path.is_absolute():
            return False, "Caminho absoluto não é permitido."

        if any(part in self.BLOCKED_PARTS for part in path.parts):
            return False, f"Caminho bloqueado: {relative_path}"

        if path.suffix.lower() in self.BLOCKED_EXTENSIONS:
            return False, f"Extensão bloqueada: {path.suffix}"

        if not path.parts:
            return False, "Caminho vazio."

        return True, "OK"

    def apply(self, project_path: Path, proposed_files: list[ProposedFile]) -> list[str]:
        results: list[str] = []

        for proposed in proposed_files:
            ok, reason = self.validate_relative_path(proposed.relative_path)
            if not ok:
                results.append(f"BLOQUEADO: {proposed.relative_path} - {reason}")
                continue

            target = project_path / proposed.relative_path
            self.file_tool.write_text(target, proposed.content)
            results.append(f"APLICADO: {target}")

        return results
