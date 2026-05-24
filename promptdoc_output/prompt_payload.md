================================================================================
PROMPT DOC SYSTEM INSTRUCTION WRAPPER
================================================================================
You are an elite Full-Stack AI Engineer and Software Systems Architect. 
Below is a verified snapshot of a target local codebase workspace. 

### INSTRUCTIONS FOR YOUR ANALYSIS:
1. Carefully inspect the "TARGET WORKSPACE DIRECTORY TREE" to understand how components link together.
2. Read through the "SOURCE FILE REPOSITORY" section where file paths are maps to their raw contents.
3. Treat all code pieces inside the fenced blocks as a singular source of truth.
4. When answering subsequent questions, preserve patterns found in this architecture unless explicitly asked to modify them.

### TARGET WORKSPACE DIRECTORY TREE:
.
├── .gitignore
├── promptdoc.py
├── pyproject.toml
├── README.md
└── test_promptdoc.py

### SOURCE FILE REPOSITORY:
### .gitignore
```text
# PromptDoc AI Ignores
.pytest_cache/
*.egg-info/
.promptdoc.md
.pytest_cache
*.pyc
__pycache__/

```
---

### promptdoc.py
```python
import os
import sys
from pathlib import Path
import fnmatch
import json
import urllib.request
import urllib.error
import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.markdown import Markdown
import pyperclip


app = typer.Typer(help="PromptDoc AI - Project Context Packager")
console = Console()

# Global exclusions as specified in the PRD
GLOBAL_IGNORED_DIRS = {
    ".git", "node_modules", "__pycache__", ".next", ".venv", "venv", "env",
    "dist", "build", "target", ".idea", ".vscode", "promptdoc_output",
    ".mypy_cache", ".ruff_cache", ".pytest_cache", ".sass-cache", ".cache",
    ".coverage", "htmlcov", ".tox", ".ipynb_checkpoints"
}

GLOBAL_IGNORED_FILES = {
    "package-lock.json", "pnpm-lock.yaml", "yarn.lock", ".DS_Store",
    ".promptdoc.md", "prompt_payload.md"
}

GLOBAL_IGNORED_EXTENSIONS = {
    ".exe", ".pyc", ".pyd", ".png", ".jpg", ".jpeg", ".gif", ".ico", ".svg",
    ".mp4", ".zip", ".tar.gz"
}

class IgnoreEngine:
    """
    Engine to intelligently filter out non-source, global, and git-ignored files and directories.
    """
    def __init__(self, root_dir: Path):
        self.root_dir = root_dir.resolve()
        self.gitignore_patterns = []
        self._load_gitignore()

    def _load_gitignore(self):
        gitignore_path = self.root_dir / ".gitignore"
        if not gitignore_path.exists():
            return
        try:
            with open(gitignore_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.rstrip("\r\n").rstrip()
                    if not line or line.startswith("#"):
                        continue
                    
                    is_dir_only = line.endswith("/")
                    pattern = line.rstrip("/")
                    self.gitignore_patterns.append((pattern, is_dir_only))
        except Exception as e:
            console.print(f"[red]Error reading .gitignore: {e}[/red]")

    def _matches_pattern(self, rel_path: Path, pattern: str, is_dir_only: bool, is_dir: bool) -> bool:
        if is_dir_only and not is_dir:
            return False

        rel_str = str(rel_path).replace(os.sep, "/")
        parts = rel_path.parts

        pattern = pattern.replace("\\", "/")

        # 1. Absolute match from root if starts with /
        if pattern.startswith("/"):
            match_pat = pattern.lstrip("/")
            if fnmatch.fnmatchcase(rel_str, match_pat) or fnmatch.fnmatchcase(rel_str, f"{match_pat}/*"):
                return True
        # 2. Match containing / (path-relative but not absolute)
        elif "/" in pattern:
            if (fnmatch.fnmatchcase(rel_str, pattern) or 
                fnmatch.fnmatchcase(rel_str, f"{pattern}/*") or 
                fnmatch.fnmatchcase(rel_str, f"*/{pattern}") or 
                fnmatch.fnmatchcase(rel_str, f"*/{pattern}/*")):
                return True
        # 3. Match name only (anywhere in hierarchy)
        else:
            for part in parts:
                if fnmatch.fnmatchcase(part, pattern):
                    return True
        return False

    def is_ignored(self, path: Path) -> bool:
        try:
            rel_path = path.resolve().relative_to(self.root_dir)
        except ValueError:
            return True

        if rel_path == Path("."):
            return False

        # Traverse hierarchy from root to path to ensure parent directory rules apply
        current_rel = Path(".")
        for part in rel_path.parts:
            current_rel = current_rel / part
            current_full = self.root_dir / current_rel
            
            # Check global hardcoded directories
            if current_rel.name in GLOBAL_IGNORED_DIRS:
                return True

            # Check global files and extensions
            if current_full.is_file():
                if current_rel.name in GLOBAL_IGNORED_FILES:
                    return True
                if current_full.suffix.lower() in GLOBAL_IGNORED_EXTENSIONS:
                    return True

            # Check gitignore rules
            is_dir = current_full.is_dir()
            for pattern, is_dir_only in self.gitignore_patterns:
                if self._matches_pattern(current_rel, pattern, is_dir_only, is_dir):
                    return True

        return False

def build_tree_representation(root_dir: Path, ignore_engine: IgnoreEngine, max_depth: int = 3) -> str:
    """
    Assembles a text-based ASCII visualization of the directory tree hierarchy up to a max depth.
    """
    lines = ["."]
    
    def _walk(dir_path: Path, prefix: str, depth: int):
        if depth > max_depth:
            return
        
        try:
            items = sorted(list(dir_path.iterdir()), key=lambda p: (not p.is_dir(), p.name.lower()))
        except Exception:
            return

        valid_items = [item for item in items if not ignore_engine.is_ignored(item)]
        
        count = len(valid_items)
        for i, item in enumerate(valid_items):
            is_last = (i == count - 1)
            connector = "└── " if is_last else "├── "
            
            display_name = f"{item.name}/" if item.is_dir() else item.name
            lines.append(f"{prefix}{connector}{display_name}")
            
            if item.is_dir():
                next_prefix = prefix + ("    " if is_last else "│   ")
                _walk(item, next_prefix, depth + 1)

    _walk(root_dir, "", 1)
    return "\n".join(lines)

LANGUAGE_MAP = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".tsx": "tsx",
    ".jsx": "jsx",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".md": "markdown",
    ".html": "html",
    ".css": "css",
    ".sh": "bash",
    ".bash": "bash",
    ".go": "go",
    ".rs": "rust",
    ".c": "c",
    ".cpp": "cpp",
    ".h": "cpp",
    ".java": "java",
    ".kt": "kotlin",
    ".toml": "toml",
    ".ini": "ini",
    ".sql": "sql",
}

def get_language_tag(path: Path) -> str:
    """
    Returns the markdown programming language code block tag based on suffix.
    """
    return LANGUAGE_MAP.get(path.suffix.lower(), "text")

def is_binary(file_path: Path) -> bool:
    """
    Preemptive heuristic scanner for binary files.
    """
    try:
        with open(file_path, "rb") as f:
            chunk = f.read(1024)
            if b"\x00" in chunk:
                return True
            # Printable character set heuristic
            text_chars = bytearray({7, 8, 9, 10, 12, 13, 27} | set(range(0x20, 0x100)) - {0x7f})
            non_printable = sum(1 for c in chunk if c not in text_chars)
            if len(chunk) > 0 and non_printable / len(chunk) > 0.30:
                return True
    except Exception:
        return True
    return False

def bundle_files(root_dir: Path, ignore_engine: IgnoreEngine, warnings: list[str]) -> tuple[str, int, int]:
    """
    Scans files, detects languages, filters binary files, checks thresholds, and packages code.
    """
    bundled_content = []
    total_files_packed = 0
    total_bytes_saved = 0

    all_files = []
    try:
        for p in root_dir.rglob("*"):
            if p.is_file() and not ignore_engine.is_ignored(p):
                all_files.append(p)
    except Exception as e:
        warnings.append(f"Error scanning directory tree: {e}")

    # Deterministic alphabetical sorting of relative paths
    all_files.sort(key=lambda p: str(p.relative_to(root_dir)).lower())

    for path in all_files:
        rel_path = path.relative_to(root_dir)
        rel_str = str(rel_path)

        if is_binary(path):
            warnings.append(f"Skipped binary file: {rel_str}")
            continue

        total_files_packed += 1

        try:
            size = path.stat().st_size
        except Exception as e:
            warnings.append(f"Could not read size for {rel_str}: {e}")
            continue

        # Size threshold check (500KB)
        if size > 500 * 1024:
            content_str = "// [PromptDoc Warning: File size exceeds 500KB threshold. Raw code excluded to prevent token window overflow.]"
            warnings.append(f"Excluded large file contents (>500KB): {rel_str}")
            total_bytes_saved += (size - len(content_str))
        else:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content_str = f.read()
            except UnicodeDecodeError:
                warnings.append(f"Unicode decode error (non-UTF-8): {rel_str}")
                total_files_packed -= 1
                continue
            except Exception as e:
                warnings.append(f"Could not read file {rel_str}: {e}")
                total_files_packed -= 1
                continue

        lang = get_language_tag(path)
        
        # Heading 3, fenced code block, exact content, horizontal rule separator
        block = f"### {rel_str}\n"
        block += f"```{lang}\n"
        block += f"{content_str}\n"
        block += "```\n"
        block += "---\n"
        
        bundled_content.append(block)

    return "\n".join(bundled_content), total_files_packed, total_bytes_saved

def call_gemini_api(api_key: str, prompt: str, system_prompt: str, model: str = "gemini-3.5-flash") -> str:
    """
    Direct, zero-dependency HTTP call to the Gemini API using urllib.
    """
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    
    # Combined payload for maximum robustness across all API versions and models
    combined_text = f"{system_prompt}\n\n============================================================\nUSER QUESTION:\n{prompt}"
    
    data = {
        "contents": [
            {
                "parts": [
                    {"text": combined_text}
                ]
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": api_key
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            candidates = res_data.get("candidates", [])
            if candidates:
                content = candidates[0].get("content", {})
                parts = content.get("parts", [])
                if parts:
                    return parts[0].get("text", "")
            return "No response received from Gemini."
    except urllib.error.HTTPError as e:
        try:
            error_body = e.read().decode("utf-8")
            err_json = json.loads(error_body)
            msg = err_json.get("error", {}).get("message", error_body)
            return f"Gemini API Error (HTTP {e.code}): {msg}"
        except Exception:
            return f"Gemini API Error (HTTP {e.code})"
    except Exception as e:
        return f"Error contacting Gemini API: {e}"

SYSTEM_PROMPT_TEMPLATE = """================================================================================
PROMPT DOC SYSTEM INSTRUCTION WRAPPER
================================================================================
You are an elite Full-Stack AI Engineer and Software Systems Architect. 
Below is a verified snapshot of a target local codebase workspace. 

### INSTRUCTIONS FOR YOUR ANALYSIS:
1. Carefully inspect the "TARGET WORKSPACE DIRECTORY TREE" to understand how components link together.
2. Read through the "SOURCE FILE REPOSITORY" section where file paths are maps to their raw contents.
3. Treat all code pieces inside the fenced blocks as a singular source of truth.
4. When answering subsequent questions, preserve patterns found in this architecture unless explicitly asked to modify them.

### TARGET WORKSPACE DIRECTORY TREE:
{tree_data}

### SOURCE FILE REPOSITORY:
{bundled_content}
================================================================================
"""

@app.command()
def main(
    target: Path = typer.Option(
        Path("."),
        "--target",
        "-t",
        help="Target workspace directory to scan",
        exists=True,
        file_okay=False,
        dir_okay=True,
        writable=True,
        resolve_path=True,
    ),
    depth: int = typer.Option(
        3,
        "--depth",
        "-d",
        help="Maximum depth level for the visual directory tree mapping",
    ),
    ask: str = typer.Option(
        None,
        "--ask",
        "-a",
        help="Query Gemini directly with the bundled codebase context",
    ),
    model: str = typer.Option(
        "gemini-3.5-flash",
        "--model",
        "-m",
        help="Gemini LLM model identifier to use",
    ),
    set_key: str = typer.Option(
        None,
        "--set-key",
        "-k",
        help="Configure, update, or clear (pass empty string) your saved Gemini API Key globally",
    ),
):
    """
    Intelligently aggregates project workspace into a clipboard-ready token-optimized Markdown.
    """
    # UX Optimization: Support changing or deleting the saved global API Key
    if set_key is not None:
        key_file_path = Path.home() / ".promptdoc_key"
        cleaned_key = set_key.strip()
        if not cleaned_key:
            if key_file_path.exists():
                try:
                    key_file_path.unlink()
                    console.print("[bold green]✔ Successfully deleted your globally saved Gemini API Key.[/bold green]")
                except Exception as e:
                    console.print(f"[bold red]Error deleting configuration: {e}[/bold red]")
            else:
                console.print("[yellow]No saved Gemini API Key was found to delete.[/yellow]")
        else:
            try:
                key_file_path.write_text(cleaned_key, encoding="utf-8")
                console.print("[bold green]✔ Successfully configured your globally saved Gemini API Key![/bold green]")
            except Exception as e:
                console.print(f"[bold red]Error saving your API Key: {e}[/bold red]")
        raise typer.Exit()

    console.print(Panel(
        "[bold cyan]🤖 PromptDoc AI[/bold cyan] | [dim]Ultra-Optimized Codebase Packager[/dim]",
        subtitle="[dim]v1.0.0[/dim]",
        border_style="cyan",
        expand=False
    ))
    
    warnings = []
    
    with Progress(
        SpinnerColumn("dots12", style="bold cyan"),
        TextColumn("[bold white]{task.description}[/bold white]"),
        console=console,
    ) as progress:
        
        # Phase 1: Scan Root Workspace
        task1 = progress.add_task(description="Scanning workspace rules & .gitignore...", total=1)
        ignore_engine = IgnoreEngine(target)
        progress.update(task1, completed=1)

        # Phase 2: Build tree representation
        task2 = progress.add_task(description="Building visual directory tree...", total=1)
        tree_str = build_tree_representation(target, ignore_engine, max_depth=depth)
        progress.update(task2, completed=1)

        # Phase 3: Pack and bundle files
        task3 = progress.add_task(description="Reading and packing source files...", total=1)
        bundled_str, count, bytes_saved = bundle_files(target, ignore_engine, warnings)
        progress.update(task3, completed=1)

    # Phase 4: Construct system wrapper payload
    payload = SYSTEM_PROMPT_TEMPLATE.format(
        tree_data=tree_str,
        bundled_content=bundled_str
    )

    # Phase 5: Write to local promptdoc_output/prompt_payload.md
    output_dir = target / "promptdoc_output"
    output_file = output_dir / "prompt_payload.md"
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(payload)
        console.print(f"\n[bold green]✔ Workspace packaged successfully![/bold green]")
        console.print(f"👉 [bold white]Visible Markdown Payload:[/bold white] [bold cyan]{output_file}[/bold cyan]")
        console.print(f"   [dim](Drag and drop this .md file directly into Claude, ChatGPT, or Gemini Web App)[/dim]\n")
    except Exception as e:
        console.print(f"[bold red]Error writing local file: {e}[/bold red]")

    # Phase 6: Load payload into system clipboard
    clipboard_success = False
    try:
        pyperclip.copy(payload)
        clipboard_success = True
        console.print("[bold green]✔ Copied prompt payload to your system clipboard![/bold green]\n")
    except Exception as e:
        console.print(
            "[bold yellow]⚠ System clipboard unavailable. Output successfully preserved in visible markdown file.[/bold yellow]\n"
        )

    # Final visual metrics table
    table = Table(
        title="📊 Context Aggregation Statistics",
        title_style="bold cyan",
        show_header=True,
        header_style="bold magenta",
        border_style="dim"
    )
    table.add_column("Metric", style="bold white")
    table.add_column("Value", justify="right", style="cyan")
    
    table.add_row("Total Source Files Bundled", f"{count}")
    table.add_row("Large File Bytes Avoided", f"{bytes_saved:,} bytes" if bytes_saved else "0 bytes")
    table.add_row("Output Folder Created", "promptdoc_output/")
    table.add_row("Visible Markdown File", "prompt_payload.md")
    table.add_row("Clipboard Status", "Copied to Clipboard" if clipboard_success else "Unavailable")
    
    console.print(table)

    # Print Warnings if any
    if warnings:
        console.print("\n[bold yellow]Non-Fatal Warnings / Exclusions:[/bold yellow]")
        for warn in warnings[:10]:
            console.print(f" [yellow]⚠ {warn}[/yellow]")
        if len(warnings) > 10:
            console.print(f" [yellow]⚠ ... and {len(warnings) - 10} more exclusions/warnings capped to prevent terminal clutter[/yellow]")

    # Phase 7: Handle Direct Gemini API Query if specified
    if ask:
        api_key = os.environ.get("GEMINI_API_KEY")
        
        # Load saved key from home config if environment variable is missing
        key_file_path = Path.home() / ".promptdoc_key"
        if not api_key and key_file_path.exists():
            try:
                api_key = key_file_path.read_text(encoding="utf-8").strip()
            except Exception:
                pass
        
        # Interactively guide the user to paste and save their key if still missing
        if not api_key:
            console.print("\n[bold yellow]🔑 Gemini API Key configuration needed![/bold yellow]")
            console.print("[dim]Get a free API key at:[/dim] [bold under cyan]https://aistudio.google.com/[/bold under cyan]")
            
            input_key = typer.prompt(
                "Paste your Gemini API Key",
                hide_input=True
            ).strip()
            
            if not input_key:
                console.print("[bold red]Error: No API key supplied. Aborting direct Q&A session.[/bold red]\n")
                raise typer.Exit(code=1)
            
            api_key = input_key
            
            save_choice = typer.confirm(
                "\nWould you like to save this key locally for future sessions? (Saved in ~/.promptdoc_key)",
                default=True
            )
            if save_choice:
                try:
                    key_file_path.write_text(api_key, encoding="utf-8")
                    console.print("[bold green]✔ API Key successfully saved locally! Future queries will run instantly.[/bold green]\n")
                except Exception as e:
                    console.print(f"[yellow]⚠ Could not write local key file: {e}[/yellow]\n")
        
        response = ""
        with console.status("[bold cyan]Contacting Gemini AI API and analyzing codebase context...[/bold cyan]", spinner="dots"):
            response = call_gemini_api(api_key, ask, payload, model=model)
        
        console.print("\n[bold magenta]==================== GEMINI AI RESPONSE ====================[/bold magenta]\n")
        console.print(Markdown(response))
        console.print("\n[bold magenta]============================================================[/bold magenta]\n")

if __name__ == "__main__":
    app()

```
---

### pyproject.toml
```toml
[build-system]
requires = ["setuptools>=61.0.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "promptdoc-ai"
version = "1.0.0"
description = "Context-packaging utility for software engineers and web-based LLMs"
readme = "README.md"
requires-python = ">=3.10"
license = { text = "MIT" }
dependencies = [
    "typer>=0.9.0",
    "rich>=13.0.0",
    "pyperclip>=1.8.2",
]

[project.scripts]
promptdoc = "promptdoc:app"

[tool.setuptools]
py-modules = ["promptdoc"]

```
---

### README.md
```markdown
# 🚀 PromptDoc AI

> **Intelligently pack your local codebase into clipboard-ready prompts & query Gemini directly from your terminal in 1-click.**

PromptDoc AI is an ultra-lightweight, zero-dependency command-line interface (CLI) utility built for developers who pair program with LLMs (Claude, Gemini, ChatGPT). It crawls your workspace, filters out temporary and compiled assets, builds a visual directory tree, maps language files, and structures everything into a single token-optimized markdown stream directly in your system clipboard.

It also features **Direct Gemini CLI Chat Integration**—enabling you to ask questions about your entire codebase natively from your console with no extra overhead or cloud dashboard copy-pasting.

---

## ✨ Features

- **⚡ Direct Gemini API Integration:** Ask questions about your project directly from the CLI via `promptdoc -a "Your question"`. Answers are streamed and rendered with beautiful markdown formatting.
- **📂 Visual Directory Tree Visualizer:** Constructs an ASCII map representing your active codebase structure up to a custom depth.
- **🛡 Strict Gitignore Parsing:** Respects local `.gitignore` specifications and skips heavy standard paths (`node_modules`, `.git`, `venv`, etc.) automatically.
- **📋 Clipboard Sync Pipeline:** Instantly loads the fully structured markdown system wrapper payload into your clipboard on completion.
- **🎨 Premium Rich UI:** Gorgeous CLI visuals including animated progress spinners, warning panels, and summarized statistics tables.
- **📏 Token Optimization:** Automatically skips binary assets (images, archives) and avoids token blowouts by excluding contents of files larger than 500KB.

---

## 💻 Installation

To install PromptDoc AI globally on your machine, clone this repository and run the setup script:

```bash
# Clone the repository
git clone https://github.com/your-username/promptDoc.git
cd promptDoc

# Install globally in editable mode
pip install -e .
```

---

## 🔑 Quick Start

### 📋 1. Copy & Upload Codebase Context
Run the packager in the root of any repository to aggregate your codebase structure and source files:
```bash
promptdoc
```
* **📋 Clipboard Sync:** The fully structured context wrapper prompt is instantly loaded into your system clipboard on completion.
* **📂 Visible Payload File:** PromptDoc automatically creates a visible folder and saves a standalone file at: **`promptdoc_output/prompt_payload.md`**
  *(Perfect for dragging and dropping directly into web-based interfaces like Claude, ChatGPT, or Gemini Web App!)*

### 💬 2. Direct Codebase Q&A (Zero-Setup Setup!)
PromptDoc makes using Google Gemini incredibly seamless. You don't even need to mess with command line exports!

* **🚀 Interactive Setup:** Simply run your query. If no API key is set, PromptDoc will securely guide you:
  ```bash
  promptdoc -a "Explain how IgnoreEngine works"
  ```
* **🔑 Secure Local Persistence:** Paste your free API key from [Google AI Studio](https://aistudio.google.com/) when prompted. PromptDoc will offer to save it securely at **`~/.promptdoc_key`**.
* **✨ Invisible Authentication:** Once configured, all future Q&A commands will run instantly in one click with **zero additional setup required!**

### 🔧 3. Managing your Saved API Key
If you ever want to change, update, or remove your saved API key globally from your system:

* **To update or set a new key globally:**
  ```bash
  promptdoc --set-key "your_new_gemini_api_key"
  # OR
  promptdoc -k "your_new_gemini_api_key"
  ```
* **To delete/clear your saved key globally:**
  ```bash
  promptdoc --set-key ""
  ```

---

## 🛠 Command Reference

```text
 Usage: promptdoc [OPTIONS]

 Intelligently aggregates project workspace into a clipboard-ready
 token-optimized Markdown.

╭─ Options ────────────────────────────────────────────────────────────────────╮
│ --target              -t      DIRECTORY  Target workspace directory to scan  │
│                                          [default: .]                        │
│ --depth               -d      INTEGER    Maximum depth level for the visual  │
│                                          directory tree mapping              │
│                                          [default: 3]                        │
│ --ask                 -a      TEXT       Query Gemini directly with the      │
│                                          bundled codebase context            │
│ --model               -m      TEXT       Gemini LLM model identifier to use  │
│                                          [default: gemini-3.5-flash]         │
│ --set-key             -k      TEXT       Configure, update, or clear (pass   │
│                                          empty string) your saved Gemini     │
│                                          API Key globally                    │
│ --install-completion                     Install completion for the current  │
│                                          shell.                              │
│ --show-completion                        Show completion for the current     │
│                                          shell, to copy it or customize the  │
│                                          installation.                       │
│ --help                                   Show this message and exit.         │
╰──────────────────────────────────────────────────────────────────────────────╯
```

---

## 🏛 License

PromptDoc AI is released by **DevDuo Innovation** under the MIT License.

```
---

### test_promptdoc.py
```python
import pytest
from pathlib import Path
from promptdoc import (
    IgnoreEngine,
    build_tree_representation,
    get_language_tag,
    is_binary,
    bundle_files,
    call_gemini_api,
)


def test_ignore_engine_global_exclusions(tmp_path):
    # Create files/dirs that should be globally ignored
    git_dir = tmp_path / ".git"
    git_dir.mkdir()
    (git_dir / "config").write_text("dummy", encoding="utf-8")

    node_modules = tmp_path / "node_modules"
    node_modules.mkdir()
    (node_modules / "package.json").write_text("dummy", encoding="utf-8")

    venv_dir = tmp_path / "venv"
    venv_dir.mkdir()
    (venv_dir / "bin" / "python").mkdir(parents=True, exist_ok=True)

    promptdoc_out = tmp_path / "promptdoc_output"
    promptdoc_out.mkdir()
    (promptdoc_out / "prompt_payload.md").write_text("payload", encoding="utf-8")

    normal_dir = tmp_path / "src"
    normal_dir.mkdir()
    normal_file = normal_dir / "main.py"
    normal_file.write_text("print('hello')", encoding="utf-8")

    pyc_file = normal_dir / "main.pyc"
    pyc_file.write_text("binary", encoding="utf-8")

    ignore_engine = IgnoreEngine(tmp_path)
    
    assert ignore_engine.is_ignored(git_dir) is True
    assert ignore_engine.is_ignored(git_dir / "config") is True
    assert ignore_engine.is_ignored(node_modules) is True
    assert ignore_engine.is_ignored(venv_dir) is True
    assert ignore_engine.is_ignored(promptdoc_out) is True
    assert ignore_engine.is_ignored(promptdoc_out / "prompt_payload.md") is True
    assert ignore_engine.is_ignored(pyc_file) is True
    assert ignore_engine.is_ignored(normal_file) is False

def test_ignore_engine_gitignore_patterns(tmp_path):
    # Write .gitignore
    gitignore = tmp_path / ".gitignore"
    gitignore.write_text("""
# This is a comment
*.log
/config
build/
    """, encoding="utf-8")

    # Files to check
    log_file = tmp_path / "app.log"
    log_file.write_text("log", encoding="utf-8")

    nested_log = tmp_path / "src" / "debug.log"
    nested_log.parent.mkdir(exist_ok=True)
    nested_log.write_text("log", encoding="utf-8")

    config_dir = tmp_path / "config"
    config_dir.mkdir()
    config_file = config_dir / "settings.json"
    config_file.write_text("{}", encoding="utf-8")

    nested_config_dir = tmp_path / "src" / "config"
    nested_config_dir.mkdir(exist_ok=True)
    nested_config_file = nested_config_dir / "settings.json"
    nested_config_file.write_text("{}", encoding="utf-8")

    build_dir = tmp_path / "build"
    build_dir.mkdir()
    build_file = build_dir / "output.txt"
    build_file.write_text("output", encoding="utf-8")

    ignore_engine = IgnoreEngine(tmp_path)

    assert ignore_engine.is_ignored(log_file) is True
    assert ignore_engine.is_ignored(nested_log) is True
    assert ignore_engine.is_ignored(config_dir) is True
    assert ignore_engine.is_ignored(config_file) is True
    assert ignore_engine.is_ignored(nested_config_file) is False  # /config only matches root config
    assert ignore_engine.is_ignored(build_file) is True

def test_build_tree_representation(tmp_path):
    # Setup folders
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("print('hello')", encoding="utf-8")
    (tmp_path / "src" / "utils.py").write_text("def run(): pass", encoding="utf-8")
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "settings.json").write_text("{}", encoding="utf-8")
    (tmp_path / "README.md").write_text("Read me", encoding="utf-8")

    ignore_engine = IgnoreEngine(tmp_path)
    tree_str = build_tree_representation(tmp_path, ignore_engine, max_depth=3)

    assert "." in tree_str
    assert "src/" in tree_str
    assert "main.py" in tree_str
    assert "config/" in tree_str
    assert "settings.json" in tree_str
    assert "README.md" in tree_str

def test_get_language_tag():
    assert get_language_tag(Path("main.py")) == "python"
    assert get_language_tag(Path("script.sh")) == "bash"
    assert get_language_tag(Path("config.json")) == "json"
    assert get_language_tag(Path("unknown.xyz")) == "text"

def test_is_binary(tmp_path):
    txt_file = tmp_path / "text.txt"
    txt_file.write_text("Normal printable text", encoding="utf-8")
    
    bin_file = tmp_path / "binary.bin"
    bin_file.write_bytes(b"\x00\x01\x02\x03\x04\x05")

    assert is_binary(txt_file) is False
    assert is_binary(bin_file) is True

def test_bundle_files_and_size_threshold(tmp_path):
    # Normal file
    normal_file = tmp_path / "main.py"
    normal_file.write_text("print('hello')", encoding="utf-8")

    # Large file (> 500KB)
    large_file = tmp_path / "large.txt"
    large_file.write_text("A" * (501 * 1024), encoding="utf-8")

    ignore_engine = IgnoreEngine(tmp_path)
    warnings = []
    bundled_str, count, bytes_saved = bundle_files(tmp_path, ignore_engine, warnings)

    assert count == 2
    assert "### main.py" in bundled_str
    assert "print('hello')" in bundled_str
    assert "### large.txt" in bundled_str
    assert "[PromptDoc Warning: File size exceeds 500KB threshold. Raw code excluded to prevent token window overflow.]" in bundled_str
    assert bytes_saved > 0
    assert any("Excluded large file contents" in w for w in warnings)

def test_call_gemini_api():
    from unittest.mock import patch
    import io
    
    mock_response = io.BytesIO(b'{"candidates": [{"content": {"parts": [{"text": "Mocked response text"}]}}]}')
    with patch("urllib.request.urlopen") as mock_urlopen:
        mock_urlopen.return_value = mock_response
        res = call_gemini_api("dummy_key", "hello", "system instructions")
        assert res == "Mocked response text"


```
---

================================================================================
