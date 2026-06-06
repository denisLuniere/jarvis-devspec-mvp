from datetime import datetime
from pathlib import Path
import subprocess
import sys
import textwrap

from .base import LLMProvider

class ManualProvider(LLMProvider):
    """
    Provider manual para usar ChatGPT Plus sem API.

    Fluxo:
    1. Jarvis cria um prompt em .jarvis/manual/outbox.
    2. Usuário cola o prompt no ChatGPT Plus.
    3. Usuário copia a resposta.
    4. Usuário cola a resposta no terminal até <<<END>>>.
    """

    def __init__(self, base_dir: Path | None = None, open_prompt: bool = True, editor: str = "notepad"):
        self.base_dir = base_dir or Path.cwd()
        self.open_prompt = open_prompt
        self.editor = editor

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        manual_dir = self.base_dir / ".jarvis" / "manual"
        outbox_dir = manual_dir / "outbox"
        inbox_dir = manual_dir / "inbox"
        outbox_dir.mkdir(parents=True, exist_ok=True)
        inbox_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        prompt_path = outbox_dir / f"prompt-{timestamp}.md"
        response_path = inbox_dir / f"response-{timestamp}.md"

        prompt_content = self._build_prompt_file(system_prompt, user_prompt)
        prompt_path.write_text(prompt_content, encoding="utf-8")

        print("\nJarvis Manual Provider")
        print("======================")
        print(f"Prompt gerado em: {prompt_path}")
        print("")
        print("Passos:")
        print("1. Abra o arquivo de prompt.")
        print("2. Copie todo o conteúdo.")
        print("3. Cole no ChatGPT Plus.")
        print("4. Copie a resposta do ChatGPT.")
        print("5. Cole aqui no terminal.")
        print("6. Finalize com uma linha contendo apenas: <<<END>>>")
        print("")

        if self.open_prompt:
            self._open_file(prompt_path)

        print("Cole a resposta abaixo:")
        response = self._read_multiline_until_end()
        response_path.write_text(response, encoding="utf-8")

        print(f"Resposta salva em: {response_path}")
        return response

    def _build_prompt_file(self, system_prompt: str, user_prompt: str) -> str:
        return textwrap.dedent(f"""
        # Prompt para ChatGPT Plus

        Copie todo este conteúdo e cole no ChatGPT.

        ## Instruções do sistema

        {system_prompt.strip()}

        ## Pedido do usuário / tarefa do Jarvis

        {user_prompt.strip()}

        ## Regras importantes para responder

        - Responda apenas com o conteúdo necessário para o Jarvis processar.
        - Quando a tarefa for implementar arquivos, use obrigatoriamente blocos neste formato:

        ```file path=caminho/relativo/ao/projeto.ext
        conteúdo completo do arquivo
        ```

        - Não use caminhos absolutos.
        - Não use `..` no caminho.
        - Ao final, inclua "Validações sugeridas", se aplicável.
        """).strip() + "\n"

    def _read_multiline_until_end(self) -> str:
        lines: list[str] = []

        while True:
            try:
                line = input()
            except EOFError:
                break

            if line.strip() == "<<<END>>>":
                break

            lines.append(line)

        return "\n".join(lines).strip() + "\n"

    def _open_file(self, path: Path) -> None:
        try:
            if sys.platform.startswith("win"):
                if self.editor:
                    subprocess.Popen([self.editor, str(path)], shell=False)
                else:
                    subprocess.Popen(["notepad", str(path)], shell=False)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(path)])
            else:
                subprocess.Popen(["xdg-open", str(path)])
        except Exception as exc:
            print(f"Aviso: não consegui abrir o prompt automaticamente: {exc}")
