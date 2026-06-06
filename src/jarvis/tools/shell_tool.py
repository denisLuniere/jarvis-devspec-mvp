import subprocess
from pathlib import Path
from jarvis.core.safety import SafetyGuard

class ShellTool:
    def __init__(self, guard: SafetyGuard, require_confirmation: bool = True):
        self.guard = guard
        self.require_confirmation = require_confirmation

    def run(self, working_dir: Path, command: str) -> str:
        self.guard.require_allowed_path(working_dir)

        ok, reason = self.guard.validate_command(command)
        if not ok:
            return reason

        if self.require_confirmation:
            answer = input(f"Confirmar execução em {working_dir}?\n$ {command}\nDigite SIM para executar: ")
            if answer.strip().upper() != "SIM":
                return "Execução cancelada."

        result = subprocess.run(
            command,
            cwd=working_dir,
            shell=True,
            capture_output=True,
            text=True,
            timeout=120,
        )

        output = result.stdout.strip()
        error = result.stderr.strip()

        if result.returncode == 0:
            return output or "Comando executado com sucesso."

        return f"Comando falhou com código {result.returncode}.\nSTDOUT:\n{output}\nSTDERR:\n{error}"
