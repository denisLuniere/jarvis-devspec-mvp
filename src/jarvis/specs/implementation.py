from dataclasses import dataclass
from pathlib import Path
import difflib
import re
from jarvis.specs.path_policy import SpecPathPolicy

@dataclass(frozen=True)
class ProposedFile:
    relative_path: str
    content: str

@dataclass(frozen=True)
class FileDiff:
    relative_path: str
    exists: bool
    diff_text: str

class ImplementationParser:
    # Supported markdown:
    # ```file path=src/Foo.java
    # content
    # ```
    FILE_BLOCK_RE = re.compile(
        r"```file\s+path=(?P<path>[^\n\r]+)\r?\n(?P<content>.*?)```",
        re.DOTALL | re.IGNORECASE,
    )

    # Supported browser-safe markers:
    # <<<FILE path=src/Foo.java>>>
    # content
    # <<<END_FILE>>>
    MARKER_BLOCK_RE = re.compile(
        r"<<<FILE\s+path=(?P<path>[^>\n\r]+)>>>\r?\n(?P<content>.*?)<<<END_FILE>>>",
        re.DOTALL | re.IGNORECASE,
    )

    def parse_files(self, text: str) -> list[ProposedFile]:
        files: list[ProposedFile] = []
        seen: set[str] = set()

        for match in self.FILE_BLOCK_RE.finditer(text):
            rel_path = match.group("path").strip().strip('"').strip("'")
            content = match.group("content")

            if content.startswith("\n"):
                content = content[1:]

            if rel_path not in seen:
                files.append(ProposedFile(relative_path=rel_path, content=content.rstrip() + "\n"))
                seen.add(rel_path)

        for match in self.MARKER_BLOCK_RE.finditer(text):
            rel_path = match.group("path").strip().strip('"').strip("'")
            content = match.group("content")

            if content.startswith("\n"):
                content = content[1:]

            if rel_path not in seen:
                files.append(ProposedFile(relative_path=rel_path, content=content.rstrip() + "\n"))
                seen.add(rel_path)

        return files

class ImplementationApplier:
    BLOCKED_PARTS = {"..", ".git", ".venv", "venv", "__pycache__"}
    BLOCKED_EXTENSIONS = {".exe", ".dll", ".bat", ".cmd", ".ps1", ".pfx", ".pem", ".key"}

    def __init__(self, file_tool):
        self.file_tool = file_tool
        self.path_policy = SpecPathPolicy()

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

    def build_diffs(self, project_path: Path, proposed_files: list[ProposedFile]) -> list[FileDiff]:
        diffs: list[FileDiff] = []

        for proposed in proposed_files:
            normalized_path, note = self.path_policy.normalize(proposed.relative_path)
            proposed = ProposedFile(relative_path=normalized_path, content=proposed.content)
            ok, reason = self.validate_relative_path(proposed.relative_path)
            if not ok:
                diffs.append(
                    FileDiff(
                        relative_path=proposed.relative_path,
                        exists=False,
                        diff_text=f"BLOQUEADO: {reason}",
                    )
                )
                continue

            target = project_path / proposed.relative_path
            self.file_tool.guard.require_allowed_path(target.parent)

            old_text = ""
            exists = target.exists()
            if exists:
                try:
                    old_text = target.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    diffs.append(
                        FileDiff(
                            relative_path=proposed.relative_path,
                            exists=True,
                            diff_text="BLOQUEADO: arquivo existente não parece ser texto UTF-8.",
                        )
                    )
                    continue

            old_lines = old_text.splitlines(keepends=True)
            new_lines = proposed.content.splitlines(keepends=True)

            diff = "".join(
                difflib.unified_diff(
                    old_lines,
                    new_lines,
                    fromfile=f"a/{proposed.relative_path}",
                    tofile=f"b/{proposed.relative_path}",
                    lineterm="",
                )
            )

            if not diff and exists:
                diff = "SEM ALTERAÇÕES: conteúdo proposto é igual ao arquivo atual."

            if note:
                diff = f"# {note}\n" + diff

            if not exists:
                diff = "".join(
                    difflib.unified_diff(
                        [],
                        new_lines,
                        fromfile="/dev/null",
                        tofile=f"b/{proposed.relative_path}",
                        lineterm="",
                    )
                )

            diffs.append(
                FileDiff(
                    relative_path=proposed.relative_path,
                    exists=exists,
                    diff_text=diff,
                )
            )

        return diffs

    def apply(self, project_path: Path, proposed_files: list[ProposedFile]) -> list[str]:
        results: list[str] = []

        for proposed in proposed_files:
            normalized_path, note = self.path_policy.normalize(proposed.relative_path)
            proposed = ProposedFile(relative_path=normalized_path, content=proposed.content)
            ok, reason = self.validate_relative_path(proposed.relative_path)
            if not ok:
                results.append(f"BLOQUEADO: {proposed.relative_path} - {reason}")
                continue

            target = project_path / proposed.relative_path
            self.file_tool.write_text(target, proposed.content)
            if note:
                results.append(f"APLICADO: {target} ({note})")
            else:
                results.append(f"APLICADO: {target}")

        return results
