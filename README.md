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
