from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import subprocess
import tomllib

from jarvis.core.safety import SafetyGuard

@dataclass(frozen=True)
class ValidationCommand:
    name: str
    command: str
    timeout_seconds: int = 180

@dataclass(frozen=True)
class ValidationResult:
    name: str
    command: str
    return_code: int
    stdout: str
    stderr: str
    duration_label: str

    @property
    def success(self) -> bool:
        return self.return_code == 0

class ValidationEngine:
    DEFAULT_CONFIG = """# Jarvis validation configuration

# Cada item em [[commands]] representa uma validação executável.
# Ajuste conforme seu projeto.

[[commands]]
name = "Python compileall"
command = "python -m compileall src"
timeout_seconds = 180
"""

    def __init__(self, guard: SafetyGuard):
        self.guard = guard

    def ensure_config(self, project_path: Path) -> Path:
        config_path = project_path / ".jarvis" / "validation.toml"
        self.guard.require_allowed_path(config_path.parent)

        if not config_path.exists():
            config_path.parent.mkdir(parents=True, exist_ok=True)
            config_path.write_text(self.DEFAULT_CONFIG, encoding="utf-8")

        return config_path

    def load_commands(self, project_path: Path) -> list[ValidationCommand]:
        config_path = self.ensure_config(project_path)
        raw = tomllib.loads(config_path.read_text(encoding="utf-8"))
        commands = []

        for item in raw.get("commands", []):
            name = str(item.get("name", "Validação sem nome")).strip()
            command = str(item.get("command", "")).strip()
            timeout_seconds = int(item.get("timeout_seconds", 180))

            if not command:
                continue

            commands.append(
                ValidationCommand(
                    name=name,
                    command=command,
                    timeout_seconds=timeout_seconds,
                )
            )

        return commands

    def run(self, project_path: Path) -> tuple[Path, list[ValidationResult]]:
        self.guard.require_allowed_path(project_path)
        commands = self.load_commands(project_path)

        results: list[ValidationResult] = []
        for validation in commands:
            start = datetime.now()

            ok, reason = self.guard.validate_command(validation.command)
            if not ok:
                results.append(
                    ValidationResult(
                        name=validation.name,
                        command=validation.command,
                        return_code=999,
                        stdout="",
                        stderr=reason,
                        duration_label="0s",
                    )
                )
                continue

            try:
                proc = subprocess.run(
                    validation.command,
                    cwd=project_path,
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=validation.timeout_seconds,
                )
                end = datetime.now()
                duration = max(0, int((end - start).total_seconds()))

                results.append(
                    ValidationResult(
                        name=validation.name,
                        command=validation.command,
                        return_code=proc.returncode,
                        stdout=proc.stdout.strip(),
                        stderr=proc.stderr.strip(),
                        duration_label=f"{duration}s",
                    )
                )
            except subprocess.TimeoutExpired as exc:
                results.append(
                    ValidationResult(
                        name=validation.name,
                        command=validation.command,
                        return_code=124,
                        stdout=(exc.stdout or "").strip() if isinstance(exc.stdout, str) else "",
                        stderr=f"Timeout após {validation.timeout_seconds}s.",
                        duration_label=f">{validation.timeout_seconds}s",
                    )
                )
            except Exception as exc:
                results.append(
                    ValidationResult(
                        name=validation.name,
                        command=validation.command,
                        return_code=1,
                        stdout="",
                        stderr=f"Erro ao executar validação: {exc}",
                        duration_label="0s",
                    )
                )

        config_path = project_path / ".jarvis" / "validation.toml"
        return config_path, results

    def build_report(self, feature_name: str, config_path: Path, results: list[ValidationResult]) -> str:
        now = datetime.now().isoformat(timespec="seconds")
        success_count = sum(1 for item in results if item.success)
        fail_count = len(results) - success_count
        status = "APROVADO" if results and fail_count == 0 else "REPROVADO" if results else "SEM VALIDACOES"

        table = "\n".join(
            f"| {item.name} | `{item.command}` | {item.return_code} | {'OK' if item.success else 'FALHOU'} | {item.duration_label} |"
            for item in results
        ) or "| Nenhuma | - | - | - | - |"

        details = []
        for item in results:
            details.append(f"## {item.name}\n")
            details.append(f"Comando:\n\n```bash\n{item.command}\n```\n")
            details.append(f"Resultado: {'OK' if item.success else 'FALHOU'} | Código: {item.return_code} | Duração: {item.duration_label}\n")

            if item.stdout:
                details.append("STDOUT:\n\n```text\n" + self._truncate(item.stdout) + "\n```\n")
            if item.stderr:
                details.append("STDERR:\n\n```text\n" + self._truncate(item.stderr) + "\n```\n")

        return f"""# Validation Report: {feature_name}

Gerado em: {now}

## Status

{status}

## Configuração usada

`{config_path}`

## Resumo

- Total de validações: {len(results)}
- Sucesso: {success_count}
- Falha: {fail_count}

## Validações executadas

| Validação | Comando | Código | Resultado | Duração |
|---|---|---:|---|---|
{table}

## Detalhes

{chr(10).join(details)}

## Próximas ações

- Corrigir falhas, se existirem.
- Rodar `/spec validate` novamente.
- Revisar o diff no Git antes do commit.
"""

    def _truncate(self, value: str, max_chars: int = 7000) -> str:
        if len(value) <= max_chars:
            return value
        return value[:max_chars] + "\n... saída truncada ..."
