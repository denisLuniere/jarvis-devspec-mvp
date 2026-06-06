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


        if command.startswith("/spec start "):
            raw = command.replace("/spec start ", "", 1).strip()
            parts = raw.split(" ", 1)
            if len(parts) < 2:
                return "Uso: /spec start <caminho-projeto> <nome-da-feature>"
            return self.spec_engine.start_spec(Path(parts[0]), parts[1])

        if command.startswith("/spec status "):
            raw = command.replace("/spec status ", "", 1).strip()
            parts = raw.split(" ", 1)
            if len(parts) < 2:
                return "Uso: /spec status <caminho-projeto> <nome-da-feature>"
            return self.spec_engine.status_feature(Path(parts[0]), parts[1])

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


        if command.startswith("/spec validate "):
            raw = command.replace("/spec validate ", "", 1).strip()
            parts = raw.split(" ", 1)
            if len(parts) < 2:
                return "Uso: /spec validate <caminho-projeto> <nome-da-feature>"
            return self.spec_engine.validate_feature(Path(parts[0]), parts[1])


        if command.startswith("/spec diff "):
            raw = command.replace("/spec diff ", "", 1).strip()
            parts = raw.rsplit(" ", 1)
            if len(parts) < 2:
                return "Uso: /spec diff <caminho-projeto> <nome-da-feature> <numero-task>"
            project_and_feature = parts[0]
            task_number = parts[1].strip()
            project_feature_parts = project_and_feature.split(" ", 1)
            if len(project_feature_parts) < 2:
                return "Uso: /spec diff <caminho-projeto> <nome-da-feature> <numero-task>"
            return self.spec_engine.implement_task(Path(project_feature_parts[0]), project_feature_parts[1], task_number, apply_changes=False)

        if command.startswith("/spec implement "):
            raw = command.replace("/spec implement ", "", 1).strip()
            apply_changes = True

            if raw.endswith(" --preview"):
                apply_changes = False
                raw = raw.removesuffix(" --preview").strip()

            parts = raw.rsplit(" ", 1)
            if len(parts) < 2:
                return "Uso: /spec implement <caminho-projeto> <nome-da-feature> <numero-task> [--preview]"

            project_and_feature = parts[0]
            task_number = parts[1].strip()

            project_feature_parts = project_and_feature.split(" ", 1)
            if len(project_feature_parts) < 2:
                return "Uso: /spec implement <caminho-projeto> <nome-da-feature> <numero-task> [--preview]"

            project_path = Path(project_feature_parts[0])
            feature_name = project_feature_parts[1]

            return self.spec_engine.implement_task(project_path, feature_name, task_number, apply_changes=apply_changes)

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

/spec start <caminho-projeto> <nome-da-feature>
/spec status <caminho-projeto> <nome-da-feature>
/spec init <caminho-projeto>
/spec new <caminho-projeto> <nome-da-feature>
/spec list <caminho-projeto>
/spec refine <caminho-projeto> <nome-da-feature>
/spec design <caminho-projeto> <nome-da-feature>
/spec tasks <caminho-projeto> <nome-da-feature>
/spec implement <caminho-projeto> <nome-da-feature> <numero-task>
/spec implement <caminho-projeto> <nome-da-feature> <numero-task> --preview
/spec diff <caminho-projeto> <nome-da-feature> <numero-task>
/spec validate <caminho-projeto> <nome-da-feature>
/open vscode
/open chrome
/run <caminho-projeto> <comando>
/help
/exit

Qualquer outro texto será enviado ao provedor de IA configurado.
"""
