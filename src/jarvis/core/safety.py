from pathlib import Path

class SafetyGuard:
    dangerous_fragments = [
        " rm -rf ",
        " del /f ",
        " format ",
        " shutdown ",
        " reg delete ",
        "remove-item -recurse",
        "drop database",
        "truncate table",
    ]

    def __init__(self, allowed_root: Path):
        self.allowed_root = allowed_root.resolve()

    def is_path_allowed(self, path: Path) -> bool:
        try:
            resolved = path.resolve()
            return resolved == self.allowed_root or self.allowed_root in resolved.parents
        except OSError:
            return False

    def validate_command(self, command: str) -> tuple[bool, str]:
        normalized = f" {command.lower()} "
        for fragment in self.dangerous_fragments:
            if fragment in normalized:
                return False, f"Comando bloqueado por segurança: contém '{fragment.strip()}'."
        return True, "Comando permitido."

    def require_allowed_path(self, path: Path) -> None:
        if not self.is_path_allowed(path):
            raise PermissionError(f"Caminho fora da raiz autorizada: {path}")
