from pathlib import Path

class SpecPathPolicy:
    """
    Normaliza caminhos gerados por IA para a estrutura oficial do Jarvis DevSpec.
    """

    SPEC_FILE_ALIASES = {
        "requirements.md": "01-requirements.md",
        "question.md": "02-questions.md",
        "questions.md": "02-questions.md",
        "refinement.md": "02-questions.md",
        "decisions.md": "03-decisions.md",
        "decision.md": "03-decisions.md",
        "acceptance.md": "04-acceptance-criteria.md",
        "acceptance-criteria.md": "04-acceptance-criteria.md",
        "criteria.md": "04-acceptance-criteria.md",
        "technical-design.md": "05-technical-design.md",
        "design.md": "05-technical-design.md",
        "tasks.md": "06-tasks.md",
        "task.md": "06-tasks.md",
        "test-plan.md": "07-test-plan.md",
        "tests.md": "07-test-plan.md",
        "validation-report.md": "08-validation-report.md",
        "validation.md": "08-validation-report.md",
        "changelog.md": "09-changelog.md",
    }

    OFFICIAL_SPEC_FILES = [
        "01-requirements.md",
        "02-questions.md",
        "03-decisions.md",
        "04-acceptance-criteria.md",
        "05-technical-design.md",
        "06-tasks.md",
        "07-test-plan.md",
        "08-validation-report.md",
        "09-changelog.md",
    ]

    def normalize(self, relative_path: str) -> tuple[str, str | None]:
        original = relative_path.strip().replace("\\", "/").strip("/")
        path = Path(original)
        parts = list(path.parts)

        if not parts:
            return relative_path, None

        filename = parts[-1]
        lower_filename = filename.lower()

        if lower_filename not in self.SPEC_FILE_ALIASES:
            return relative_path, None

        official_name = self.SPEC_FILE_ALIASES[lower_filename]

        if len(parts) >= 4 and parts[0] == ".jarvis" and parts[1] == "specs":
            parts[-1] = official_name
            normalized = str(Path(*parts))
            return normalized, f"Normalizado: {relative_path} -> {normalized}"

        return relative_path, None

    def official_files_hint(self, feature_slug: str) -> str:
        base = f".jarvis/specs/{feature_slug}"
        lines = [f"- `{base}/{name}`" for name in self.OFFICIAL_SPEC_FILES]
        return "\n".join(lines)
