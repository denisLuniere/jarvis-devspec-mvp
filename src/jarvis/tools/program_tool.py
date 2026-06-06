import subprocess
import sys

class ProgramTool:
    WINDOWS_APPS = {
        "vscode": ["cmd", "/c", "code"],
        "chrome": ["cmd", "/c", "start", "chrome"],
        "edge": ["cmd", "/c", "start", "msedge"],
        "notepad": ["notepad"],
        "explorer": ["explorer"],
        "terminal": ["cmd", "/c", "start", "wt"],
    }

    def open(self, app_name: str) -> str:
        app_key = app_name.strip().lower()
        if sys.platform.startswith("win"):
            command = self.WINDOWS_APPS.get(app_key)
            if not command:
                return f"Programa não permitido ou desconhecido: {app_name}"
            subprocess.Popen(command, shell=False)
            return f"Programa aberto: {app_name}"

        return "Abertura de programas está implementada inicialmente para Windows."
