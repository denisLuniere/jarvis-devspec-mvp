from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class WorkflowStep:
    name: str
    path: Path
    exists: bool
    description: str

class SpecWorkflowInspector:
    def inspect(self, project_path: Path, feature_slug: str) -> list[WorkflowStep]:
        jarvis_dir = project_path / ".jarvis"
        spec_dir = jarvis_dir / "specs" / feature_slug

        return [
            WorkflowStep(
                name="project-context",
                path=jarvis_dir / "project-context.md",
                exists=(jarvis_dir / "project-context.md").exists(),
                description="Contexto geral do projeto.",
            ),
            WorkflowStep(
                name="architecture",
                path=jarvis_dir / "architecture.md",
                exists=(jarvis_dir / "architecture.md").exists(),
                description="Arquitetura e padrões técnicos.",
            ),
            WorkflowStep(
                name="standards",
                path=jarvis_dir / "standards.md",
                exists=(jarvis_dir / "standards.md").exists(),
                description="Padrões de código, testes e commits.",
            ),
            WorkflowStep(
                name="requirements",
                path=spec_dir / "01-requirements.md",
                exists=(spec_dir / "01-requirements.md").exists(),
                description="Requisitos da funcionalidade.",
            ),
            WorkflowStep(
                name="questions",
                path=spec_dir / "02-questions.md",
                exists=(spec_dir / "02-questions.md").exists(),
                description="Perguntas de refinamento.",
            ),
            WorkflowStep(
                name="decisions",
                path=spec_dir / "03-decisions.md",
                exists=(spec_dir / "03-decisions.md").exists(),
                description="Decisões aprovadas.",
            ),
            WorkflowStep(
                name="acceptance",
                path=spec_dir / "04-acceptance-criteria.md",
                exists=(spec_dir / "04-acceptance-criteria.md").exists(),
                description="Critérios de aceite.",
            ),
            WorkflowStep(
                name="technical-design",
                path=spec_dir / "05-technical-design.md",
                exists=(spec_dir / "05-technical-design.md").exists(),
                description="Design técnico.",
            ),
            WorkflowStep(
                name="tasks",
                path=spec_dir / "06-tasks.md",
                exists=(spec_dir / "06-tasks.md").exists(),
                description="Plano de tasks.",
            ),
            WorkflowStep(
                name="test-plan",
                path=spec_dir / "07-test-plan.md",
                exists=(spec_dir / "07-test-plan.md").exists(),
                description="Plano de testes.",
            ),
            WorkflowStep(
                name="validation-report",
                path=spec_dir / "08-validation-report.md",
                exists=(spec_dir / "08-validation-report.md").exists(),
                description="Relatório de validação.",
            ),
            WorkflowStep(
                name="validation-config",
                path=jarvis_dir / "validation.toml",
                exists=(jarvis_dir / "validation.toml").exists(),
                description="Configuração dos comandos de validação.",
            ),
        ]

    def render_status(self, project_path: Path, feature_name: str, feature_slug: str) -> str:
        steps = self.inspect(project_path, feature_slug)
        ok_count = sum(1 for step in steps if step.exists)
        missing = [step for step in steps if not step.exists]

        lines = [
            "# Spec Status",
            "",
            f"Projeto: `{project_path}`",
            f"Feature: `{feature_name}`",
            "",
            f"Arquivos encontrados: {ok_count}/{len(steps)}",
            "",
            "| Status | Item | Caminho | Descrição |",
            "|---|---|---|---|",
        ]

        for step in steps:
            marker = "OK" if step.exists else "PENDENTE"
            lines.append(f"| {marker} | {step.name} | `{step.path}` | {step.description} |")

        lines.append("")
        lines.append("## Próximo passo sugerido")
        lines.append("")

        if not (project_path / ".jarvis").exists():
            lines.append(f"Execute: `/spec init {project_path}`")
        elif not (project_path / ".jarvis" / "specs" / feature_slug).exists():
            lines.append(f"Execute: `/spec new {project_path} {feature_name}`")
        elif missing:
            lines.append("Complete os arquivos pendentes ou rode os comandos de geração apropriados.")
            lines.append("")
            lines.append(f"- Refinar: `/spec refine {project_path} {feature_name}`")
            lines.append(f"- Design: `/spec design {project_path} {feature_name}`")
            lines.append(f"- Tasks: `/spec tasks {project_path} {feature_name}`")
            lines.append(f"- Validar: `/spec validate {project_path} {feature_name}`")
        else:
            lines.append("Estrutura pronta. Você pode implementar ou validar.")
            lines.append("")
            lines.append(f"- Implementar: `/spec implement {project_path} {feature_name} <task>`")
            lines.append(f"- Validar: `/spec validate {project_path} {feature_name}`")

        return "\n".join(lines)
