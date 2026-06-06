from datetime import datetime
from pathlib import Path
import textwrap
import time

from .base import LLMProvider

class BrowserProvider(LLMProvider):
    """
    Provider experimental para automatizar o ChatGPT Web.

    Importante:
    - Não usa API.
    - Usa uma sessão persistente do Chromium via Playwright.
    - O usuário precisa fazer login manualmente na primeira execução.
    - Pode quebrar se a interface do ChatGPT mudar.
    """

    def __init__(
        self,
        base_dir: Path | None = None,
        url: str = "https://chatgpt.com/",
        profile_dir: Path | None = None,
        headless: bool = False,
        timeout_seconds: int = 240,
        auto_open: bool = True,
        keep_open: bool = True,
    ):
        self.base_dir = base_dir or Path.cwd()
        self.url = url
        self.profile_dir = profile_dir or (self.base_dir / ".jarvis" / "browser-profile")
        if not self.profile_dir.is_absolute():
            self.profile_dir = self.base_dir / self.profile_dir
        self.headless = headless
        self.timeout_seconds = timeout_seconds
        self.auto_open = auto_open
        self.keep_open = keep_open

        self.playwright = None
        self.context = None
        self.page = None

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        prompt = self._build_prompt(system_prompt, user_prompt)
        prompt_path = self._save_prompt(prompt)

        print("\nJarvis Browser Provider")
        print("=======================")
        print(f"Prompt salvo em: {prompt_path}")
        print("Abrindo/controlando ChatGPT Web...")
        print("Na primeira execução, faça login manualmente se necessário.")
        print("")

        try:
            self._ensure_browser()
            self._ensure_ready()
            self._submit_prompt(prompt)
            response = self._wait_and_extract_response()
            self._save_response(response)
            return response
        except Exception as exc:
            self._save_error(exc)
            print(f"Jarvis > Falha na automação do navegador: {exc}")
            print("Jarvis > Fallback manual: copie o prompt salvo, cole no ChatGPT, depois cole a resposta abaixo.")
            print("Jarvis > Finalize com <<<END>>>")
            response = self._read_multiline_until_end()
            self._save_response(response)
            return response
        finally:
            if not self.keep_open:
                self.close()

    def close(self):
        try:
            if self.context:
                self.context.close()
        except Exception:
            pass
        try:
            if self.playwright:
                self.playwright.stop()
        except Exception:
            pass
        self.context = None
        self.page = None
        self.playwright = None

    def _ensure_browser(self):
        if self.page:
            return

        try:
            from playwright.sync_api import sync_playwright
        except ImportError as exc:
            raise RuntimeError('Instale com: pip install -e ".[browser]" e depois rode: python -m playwright install chromium') from exc

        self.profile_dir.mkdir(parents=True, exist_ok=True)

        self.playwright = sync_playwright().start()
        self.context = self.playwright.chromium.launch_persistent_context(
            user_data_dir=str(self.profile_dir),
            headless=self.headless,
            viewport={"width": 1400, "height": 950},
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized",
            ],
        )

        if self.context.pages:
            self.page = self.context.pages[0]
        else:
            self.page = self.context.new_page()

        self.page.goto(self.url, wait_until="domcontentloaded", timeout=60_000)

    def _ensure_ready(self):
        deadline = time.time() + self.timeout_seconds

        while time.time() < deadline:
            if self._find_prompt_box() is not None:
                return

            # Se estiver em tela de login, dá tempo para o usuário autenticar.
            current_url = self.page.url.lower()
            if "auth" in current_url or "login" in current_url:
                print("Jarvis > Login necessário. Faça login no navegador aberto.")
                print("Jarvis > Depois de chegar na tela do chat, pressione Enter aqui...")
                input()
                self.page.goto(self.url, wait_until="domcontentloaded", timeout=60_000)

            time.sleep(2)

        raise TimeoutError("Não encontrei a caixa de prompt do ChatGPT dentro do tempo limite.")

    def _find_prompt_box(self):
        selectors = [
            "#prompt-textarea",
            "textarea[data-testid='prompt-textarea']",
            "textarea",
            "div[contenteditable='true']",
            "[contenteditable='true']",
        ]

        for selector in selectors:
            try:
                locator = self.page.locator(selector)
                count = locator.count()
                if count > 0:
                    item = locator.nth(count - 1)
                    if item.is_visible(timeout=1000):
                        return item
            except Exception:
                continue

        return None

    def _submit_prompt(self, prompt: str):
        box = self._find_prompt_box()
        if box is None:
            raise RuntimeError("Caixa de prompt não encontrada.")

        before_count = self._assistant_message_count()
        self._before_count = before_count

        try:
            import pyperclip
            pyperclip.copy(prompt)
            box.click(timeout=10_000)
            self.page.keyboard.press("Control+V")
        except Exception:
            box.click(timeout=10_000)
            try:
                box.fill(prompt)
            except Exception:
                self.page.keyboard.insert_text(prompt)

        time.sleep(0.5)

        # Tenta clicar no botão de envio.
        send_selectors = [
            "[data-testid='send-button']",
            "button[data-testid='send-button']",
            "button[aria-label*='Send']",
            "button[aria-label*='Enviar']",
            "button:has(svg)",
        ]

        clicked = False
        for selector in send_selectors:
            try:
                loc = self.page.locator(selector)
                count = loc.count()
                if count > 0:
                    btn = loc.nth(count - 1)
                    if btn.is_visible(timeout=1000) and btn.is_enabled(timeout=1000):
                        btn.click(timeout=5000)
                        clicked = True
                        break
            except Exception:
                continue

        if not clicked:
            # Fallback: Enter costuma enviar no ChatGPT web.
            self.page.keyboard.press("Enter")

    def _assistant_message_count(self) -> int:
        selectors = [
            "[data-message-author-role='assistant']",
            "div[data-message-author-role='assistant']",
            "article:has-text('ChatGPT')",
        ]

        for selector in selectors:
            try:
                return self.page.locator(selector).count()
            except Exception:
                continue
        return 0

    def _wait_and_extract_response(self) -> str:
        deadline = time.time() + self.timeout_seconds
        before_count = getattr(self, "_before_count", 0)

        last_text = ""
        stable_ticks = 0

        while time.time() < deadline:
            response = self._extract_last_assistant_text()
            count = self._assistant_message_count()

            if count > before_count and response.strip():
                if response == last_text:
                    stable_ticks += 1
                else:
                    stable_ticks = 0
                    last_text = response

                # Aguarda estabilizar por alguns ciclos e tenta garantir que o botão "stop" sumiu.
                if stable_ticks >= 4 and not self._has_stop_button():
                    return response.strip() + "\n"

            time.sleep(2)

        if last_text.strip():
            return last_text.strip() + "\n"

        raise TimeoutError("Não consegui extrair a resposta do ChatGPT.")

    def _extract_last_assistant_text(self) -> str:
        selectors = [
            "[data-message-author-role='assistant']",
            "div[data-message-author-role='assistant']",
        ]

        for selector in selectors:
            try:
                loc = self.page.locator(selector)
                count = loc.count()
                if count > 0:
                    return loc.nth(count - 1).inner_text(timeout=5000)
            except Exception:
                continue

        return ""

    def _has_stop_button(self) -> bool:
        selectors = [
            "[data-testid='stop-button']",
            "button[aria-label*='Stop']",
            "button[aria-label*='Parar']",
        ]
        for selector in selectors:
            try:
                loc = self.page.locator(selector)
                return loc.count() > 0 and loc.nth(0).is_visible(timeout=500)
            except Exception:
                continue
        return False

    def _build_prompt(self, system_prompt: str, user_prompt: str) -> str:
        return textwrap.dedent(f"""
        Você está atuando como o cérebro externo do Jarvis DevSpec.

        ## Instruções do sistema

        {system_prompt.strip()}

        ## Tarefa

        {user_prompt.strip()}

        ## Regras obrigatórias para a resposta

        - Responda apenas com o conteúdo necessário para o Jarvis processar.
        - Quando a tarefa for implementar arquivos, use obrigatoriamente blocos neste formato:

        ```file path=caminho/relativo/ao/projeto.ext
        conteúdo completo do arquivo
        ```

        - Não use caminhos absolutos.
        - Não use `..` no caminho.
        - Ao final, inclua "Validações sugeridas", se aplicável.
        """).strip()

    def _save_prompt(self, prompt: str) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        outbox = self.base_dir / ".jarvis" / "browser" / "outbox"
        outbox.mkdir(parents=True, exist_ok=True)
        path = outbox / f"prompt-{timestamp}.md"
        path.write_text(prompt + "\n", encoding="utf-8")
        return path

    def _save_response(self, response: str) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        inbox = self.base_dir / ".jarvis" / "browser" / "inbox"
        inbox.mkdir(parents=True, exist_ok=True)
        path = inbox / f"response-{timestamp}.md"
        path.write_text(response, encoding="utf-8")
        return path

    def _save_error(self, exc: Exception) -> Path:
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        errors = self.base_dir / ".jarvis" / "browser" / "errors"
        errors.mkdir(parents=True, exist_ok=True)
        path = errors / f"error-{timestamp}.txt"
        path.write_text(str(exc), encoding="utf-8")
        return path

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
