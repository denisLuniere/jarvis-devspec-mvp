from dataclasses import dataclass
from pathlib import Path
import difflib
import re

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
    FILE_BLOCK_RE = re.compile(r"```file\s+path=(?P<path>[^\n\r]+)\r?\n(?P<content>.*?)```", re.DOTALL | re.IGNORECASE)
    def parse_files(self, text: str) -> list[ProposedFile]:
        files=[]
        for m in self.FILE_BLOCK_RE.finditer(text):
            rel=m.group('path').strip().strip('"').strip("'")
            content=m.group('content')
            if content.startswith('\n'): content=content[1:]
            files.append(ProposedFile(rel, content.rstrip()+"\n"))
        return files

class ImplementationApplier:
    BLOCKED_PARTS={"..", ".git", ".venv", "venv", "__pycache__"}
    BLOCKED_EXTENSIONS={".exe", ".dll", ".bat", ".cmd", ".ps1", ".pfx", ".pem", ".key"}
    def __init__(self, file_tool): self.file_tool=file_tool
    def validate_relative_path(self, relative_path: str) -> tuple[bool,str]:
        path=Path(relative_path)
        if path.is_absolute(): return False, "Caminho absoluto não é permitido."
        if any(part in self.BLOCKED_PARTS for part in path.parts): return False, f"Caminho bloqueado: {relative_path}"
        if path.suffix.lower() in self.BLOCKED_EXTENSIONS: return False, f"Extensão bloqueada: {path.suffix}"
        if not path.parts: return False, "Caminho vazio."
        return True, "OK"
    def build_diffs(self, project_path: Path, proposed_files: list[ProposedFile]) -> list[FileDiff]:
        diffs=[]
        for proposed in proposed_files:
            ok, reason = self.validate_relative_path(proposed.relative_path)
            if not ok:
                diffs.append(FileDiff(proposed.relative_path, False, f"BLOQUEADO: {reason}")); continue
            target=project_path/proposed.relative_path
            self.file_tool.guard.require_allowed_path(target.parent)
            exists=target.exists(); old_text=""
            if exists:
                try: old_text=target.read_text(encoding='utf-8')
                except UnicodeDecodeError:
                    diffs.append(FileDiff(proposed.relative_path, True, "BLOQUEADO: arquivo existente não parece ser texto UTF-8.")); continue
            old_lines=old_text.splitlines(keepends=True); new_lines=proposed.content.splitlines(keepends=True)
            if exists:
                diff="".join(difflib.unified_diff(old_lines,new_lines,fromfile=f"a/{proposed.relative_path}",tofile=f"b/{proposed.relative_path}",lineterm="")) or "SEM ALTERAÇÕES: conteúdo proposto é igual ao arquivo atual."
            else:
                diff="".join(difflib.unified_diff([],new_lines,fromfile="/dev/null",tofile=f"b/{proposed.relative_path}",lineterm=""))
            diffs.append(FileDiff(proposed.relative_path, exists, diff))
        return diffs
    def apply(self, project_path: Path, proposed_files: list[ProposedFile]) -> list[str]:
        results=[]
        for proposed in proposed_files:
            ok, reason = self.validate_relative_path(proposed.relative_path)
            if not ok:
                results.append(f"BLOQUEADO: {proposed.relative_path} - {reason}"); continue
            target=project_path/proposed.relative_path
            self.file_tool.write_text(target, proposed.content)
            results.append(f"APLICADO: {target}")
        return results
