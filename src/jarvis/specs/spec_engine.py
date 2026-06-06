from pathlib import Path
from datetime import datetime
from jarvis.tools.file_tool import FileTool
from jarvis.providers.base import LLMProvider
from jarvis.specs.prompts import build_refine_prompt, build_design_prompt, build_tasks_prompt

def slugify(value: str) -> str:
    return (
        value.strip()
        .lower()
        .replace(" ", "-")
        .replace("_", "-")
        .replace("/", "-")
    )

class SpecEngine:
    def __init__(self, file_tool: FileTool, provider: LLMProvider | None = None):
        self.file_tool = file_tool
        self.provider = provider

    def init_project(self, project_path: Path) -> str:
        jarvis_dir = project_path / ".jarvis"
        files = {
            jarvis_dir / "project-context.md": self._project_context_template(),
            jarvis_dir / "architecture.md": self._architecture_template(),
            jarvis_dir / "standards.md": self._standards_template(),
            jarvis_dir / "prompts" / "refine-spec.md": self._refine_prompt_template(),
            jarvis_dir / "prompts" / "implement-task.md": self._implement_prompt_template(),
        }

        results = [self.file_tool.write_text(path, content) for path, content in files.items()]
        return "\n".join(results)

    def new_spec(self, project_path: Path, feature_name: str) -> str:
        feature_slug = slugify(feature_name)
        spec_dir = project_path / ".jarvis" / "specs" / feature_slug
        created_at = datetime.now().isoformat(timespec="seconds")

        files = {
            spec_dir / "01-requirements.md": self._requirements_template(feature_name, created_at),
            spec_dir / "02-questions.md": self._questions_template(feature_name),
            spec_dir / "03-decisions.md": self._decisions_template(feature_name),
            spec_dir / "04-acceptance-criteria.md": self._acceptance_template(feature_name),
            spec_dir / "05-technical-design.md": self._technical_design_template(feature_name),
            spec_dir / "06-tasks.md": self._tasks_template(feature_name),
            spec_dir / "07-test-plan.md": self._test_plan_template(feature_name),
            spec_dir / "08-validation-report.md": self._validation_report_template(feature_name),
            spec_dir / "09-changelog.md": self._changelog_template(feature_name, created_at),
        }

        results = [self.file_tool.write_text(path, content) for path, content in files.items()]
        return "\n".join(results)

    def refine_spec(self, project_path: Path, feature_name: str) -> str:
        self._require_provider()
        spec_dir = self._spec_dir(project_path, feature_name)
        context = self._read_project_context(project_path)
        requirements = self._read_optional(spec_dir / "01-requirements.md")
        questions = self._read_optional(spec_dir / "02-questions.md")

        prompt = build_refine_prompt(context, feature_name, requirements, questions)
        result = self.provider.generate(self._system_prompt(), prompt)

        output_path = spec_dir / "02-questions.md"
        self.file_tool.write_text(output_path, result)
        self._append_changelog(spec_dir, f"Perguntas de refinamento geradas para '{feature_name}'.")
        return f"Refinamento gerado em: {output_path}"

    def generate_design(self, project_path: Path, feature_name: str) -> str:
        self._require_provider()
        spec_dir = self._spec_dir(project_path, feature_name)
        context = self._read_project_context(project_path)
        requirements = self._read_optional(spec_dir / "01-requirements.md")
        decisions = self._read_optional(spec_dir / "03-decisions.md")
        acceptance = self._read_optional(spec_dir / "04-acceptance-criteria.md")

        prompt = build_design_prompt(context, feature_name, requirements, decisions, acceptance)
        result = self.provider.generate(self._system_prompt(), prompt)

        output_path = spec_dir / "05-technical-design.md"
        self.file_tool.write_text(output_path, result)
        self._append_changelog(spec_dir, f"Design técnico gerado para '{feature_name}'.")
        return f"Design técnico gerado em: {output_path}"

    def generate_tasks(self, project_path: Path, feature_name: str) -> str:
        self._require_provider()
        spec_dir = self._spec_dir(project_path, feature_name)
        context = self._read_project_context(project_path)
        requirements = self._read_optional(spec_dir / "01-requirements.md")
        design = self._read_optional(spec_dir / "05-technical-design.md")
        acceptance = self._read_optional(spec_dir / "04-acceptance-criteria.md")

        prompt = build_tasks_prompt(context, feature_name, requirements, design, acceptance)
        result = self.provider.generate(self._system_prompt(), prompt)

        output_path = spec_dir / "06-tasks.md"
        self.file_tool.write_text(output_path, result)
        self._append_changelog(spec_dir, f"Tasks geradas para '{feature_name}'.")
        return f"Tasks geradas em: {output_path}"

    def list_specs(self, project_path: Path) -> str:
        specs_root = project_path / ".jarvis" / "specs"
        self.file_tool.guard.require_allowed_path(specs_root)

        if not specs_root.exists():
            return "Nenhuma pasta de specs encontrada. Rode primeiro: /spec init <caminho-projeto>"

        specs = sorted([p.name for p in specs_root.iterdir() if p.is_dir()])
        if not specs:
            return "Nenhuma spec encontrada."

        return "Specs encontradas:\n" + "\n".join(f"- {name}" for name in specs)

    def _require_provider(self) -> None:
        if self.provider is None:
            raise RuntimeError("Provider de IA não configurado no SpecEngine.")

    def _spec_dir(self, project_path: Path, feature_name: str) -> Path:
        spec_dir = project_path / ".jarvis" / "specs" / slugify(feature_name)
        self.file_tool.guard.require_allowed_path(spec_dir)

        if not spec_dir.exists():
            raise FileNotFoundError(
                f"Spec não encontrada: {spec_dir}\n"
                f"Crie antes com: /spec new {project_path} {feature_name}"
            )

        return spec_dir

    def _read_project_context(self, project_path: Path) -> str:
        parts = []
        for rel in [".jarvis/project-context.md", ".jarvis/architecture.md", ".jarvis/standards.md"]:
            path = project_path / rel
            parts.append(f"\n\n--- {rel} ---\n{self._read_optional(path)}")
        return "".join(parts)

    def _read_optional(self, path: Path) -> str:
        try:
            self.file_tool.guard.require_allowed_path(path)
            if path.exists():
                return path.read_text(encoding="utf-8")
            return ""
        except Exception as exc:
            return f"[Não foi possível ler {path}: {exc}]"

    def _append_changelog(self, spec_dir: Path, message: str) -> None:
        path = spec_dir / "09-changelog.md"
        previous = self._read_optional(path)
        now = datetime.now().isoformat(timespec="seconds")
        new_content = previous.rstrip() + f"\n\n## {now}\n\n- {message}\n"
        self.file_tool.write_text(path, new_content)

    def _system_prompt(self) -> str:
        return """
Você é o Jarvis DevSpec, um assistente de engenharia de software.
Trabalhe com desenvolvimento orientado por especificações.
Não implemente código antes de requisitos, critérios de aceite, design técnico e tasks estarem claros.
Seja objetivo, prático e mantenha rastreabilidade.
"""

    def _project_context_template(self) -> str:
        return """# Project Context

Descreva aqui o contexto do projeto.

## Produto

## Usuários

## Stack

## Domínio

## Restrições

## Integrações
"""

    def _architecture_template(self) -> str:
        return """# Architecture

Defina aqui a arquitetura oficial do projeto.

## Backend

- Controller não deve conter regra de negócio.
- Service concentra regras e orquestração.
- Repository acessa persistência.
- DTOs devem separar entrada e saída.

## Frontend

## Dados / Databricks

## Convenções de pacotes

## Dependências permitidas

## Dependências proibidas
"""

    def _standards_template(self) -> str:
        return """# Standards

## Código

- Código simples, legível e testável.
- Evitar duplicação.
- Métodos pequenos.
- Logs estruturados quando aplicável.

## Testes

- Toda regra de negócio deve ter teste.
- Build não deve quebrar.
- Lint deve ser validado quando existir.

## Commits

- Usar mensagens objetivas.
"""

    def _refine_prompt_template(self) -> str:
        return """# Refine Spec Prompt

Você é um analista técnico-funcional.
Refine a funcionalidade com perguntas objetivas antes de gerar código.
Nunca implemente antes de existir spec, critérios de aceite e design técnico.
"""

    def _implement_prompt_template(self) -> str:
        return """# Implement Task Prompt

Você é um desenvolvedor sênior.
Implemente apenas a task solicitada.
Respeite architecture.md, standards.md, requirements.md e acceptance-criteria.md.
Após implementar, informe arquivos alterados e validações necessárias.
"""

    def _requirements_template(self, feature_name: str, created_at: str) -> str:
        return f"""# Requirements: {feature_name}

Criado em: {created_at}

## Objetivo

Descreva o objetivo da funcionalidade.

## Problema que resolve

## Usuários envolvidos

## Escopo

### Dentro do escopo

### Fora do escopo

## Regras de negócio

1. TBD

## Dados necessários

| Campo | Tipo | Obrigatório | Observação |
|---|---|---:|---|
| TBD | TBD | Sim | TBD |
"""

    def _questions_template(self, feature_name: str) -> str:
        return f"""# Questions: {feature_name}

Use este arquivo para registrar dúvidas antes da implementação.

## Perguntas abertas

- [ ] Qual é o principal fluxo da funcionalidade?
- [ ] Quais campos são obrigatórios?
- [ ] Quais regras precisam ser validadas?
- [ ] Quais integrações são necessárias?
- [ ] Existe impacto em dados existentes?

## Perguntas respondidas
"""

    def _decisions_template(self, feature_name: str) -> str:
        return f"""# Decisions: {feature_name}

Registre decisões aprovadas.

- TBD
"""

    def _acceptance_template(self, feature_name: str) -> str:
        return f"""# Acceptance Criteria: {feature_name}

- [ ] A funcionalidade atende ao objetivo descrito em requirements.md.
- [ ] Regras de negócio foram implementadas.
- [ ] Cenários de erro foram tratados.
- [ ] Testes foram criados ou atualizados.
- [ ] Build e validações locais foram executados.
"""

    def _technical_design_template(self, feature_name: str) -> str:
        return f"""# Technical Design: {feature_name}

## Estratégia técnica

## Arquivos/classes esperados

| Tipo | Nome | Responsabilidade |
|---|---|---|
| TBD | TBD | TBD |

## Persistência

## Endpoints / Interfaces

## Validações

## Riscos técnicos
"""

    def _tasks_template(self, feature_name: str) -> str:
        return f"""# Tasks: {feature_name}

- [ ] 1. Revisar requirements.md
- [ ] 2. Responder questions.md
- [ ] 3. Aprovar acceptance-criteria.md
- [ ] 4. Criar/atualizar design técnico
- [ ] 5. Implementar camada de domínio
- [ ] 6. Implementar camada de aplicação/service
- [ ] 7. Implementar interface/controller/job/notebook
- [ ] 8. Criar testes
- [ ] 9. Rodar validações locais
- [ ] 10. Atualizar validation-report.md
"""

    def _test_plan_template(self, feature_name: str) -> str:
        return f"""# Test Plan: {feature_name}

## Testes unitários

## Testes de integração

## Testes manuais

## Massa de dados

## Comandos de validação

```bash
# Exemplo
mvn test
```
"""

    def _validation_report_template(self, feature_name: str) -> str:
        return f"""# Validation Report: {feature_name}

## Status

PENDENTE

## Validações executadas

| Validação | Resultado | Observação |
|---|---|---|
| TBD | TBD | TBD |

## Problemas encontrados

## Próximas ações
"""

    def _changelog_template(self, feature_name: str, created_at: str) -> str:
        return f"""# Changelog: {feature_name}

## {created_at}

- Spec criada.
"""
