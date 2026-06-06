from pathlib import Path
from jarvis.specs.spec_engine import SpecEngine
from jarvis.tools.program_tool import ProgramTool
from jarvis.tools.shell_tool import ShellTool

class CommandRouter:
    def __init__(
        self,
        spec_engine: SpecEngine,
        program_tool: ProgramTool,
        shell_tool: ShellTool,
    ):
        self.spec_engine = spec_engine
        self.program_tool = program_tool
        self.shell_tool = shell_tool

    def route(self, text: str) -> str | None:
        command = text.strip()

        if command in {"/help", "help", "ajuda"}:
            return self.help()

        if command.startswith("/spec init "):
            project_path = Path(command.replace("/spec init ", "", 1).strip())
            return self.spec_engine.init_project(project_path)

        if command.startswith("/spec list "):
            project_path = Path(command.replace("/spec list ", "", 1).strip())
            return self.spec_engine.list_specs(project_path)

        if command.startswith("/spec new "):
            raw = command.replace("/spec new ", "", 1).strip()
            parts = raw.split(" ", 1)
            if len(parts) < 2:
                return "Uso: /spec new <caminho-projeto> <nome-da-feature>"
            return self.spec_engine.new_spec(Path(parts[0]), parts[1])

        if command.startswith("/spec refine "):
            raw = command.replace("/spec refine ", "", 1).strip()
            parts = raw.split(" ", 1)
            if len(parts) < 2:
                return "Uso: /spec refine <caminho-projeto> <nome-da-feature>"
            return self.spec_engine.refine_spec(Path(parts[0]), parts[1])

        if command.startswith("/spec design "):
            raw = command.replace("/spec design ", "", 1).strip()
            parts = raw.split(" ", 1)
            if len(parts) < 2:
                return "Uso: /spec design <caminho-projeto> <nome-da-feature>"
            return self.spec_engine.generate_design(Path(parts[0]), parts[1])

        if command.startswith("/spec tasks "):
            raw = command.replace("/spec tasks ", "", 1).strip()
            parts = raw.split(" ", 1)
            if len(parts) < 2:
                return "Uso: /spec tasks <caminho-projeto> <nome-da-feature>"
            return self.spec_engine.generate_tasks(Path(parts[0]), parts[1])

        if command.startswith("/open "):
            app_name = command.replace("/open ", "", 1)
            return self.program_tool.open(app_name)

        if command.startswith("/run "):
            raw = command.replace("/run ", "", 1).strip()
            parts = raw.split(" ", 1)
            if len(parts) < 2:
                return "Uso: /run <caminho-projeto> <comando>"
            return self.shell_tool.run(Path(parts[0]), parts[1])

        return None

    def help(self) -> str:
        return """Comandos disponíveis:

/spec init <caminho-projeto>
/spec new <caminho-projeto> <nome-da-feature>
/spec list <caminho-projeto>
/spec refine <caminho-projeto> <nome-da-feature>
/spec design <caminho-projeto> <nome-da-feature>
/spec tasks <caminho-projeto> <nome-da-feature>
/open vscode
/open chrome
/run <caminho-projeto> <comando>
/help
/exit

Qualquer outro texto será enviado ao provedor de IA configurado.
"""
