# 🏪 Gumroad Listing: PromptDoc AI Conversion Assets

This asset file contains the complete, copy-paste ready headlines, category tags, SEO metadata, high-converting product description (in markdown), and the automated post-purchase email sequence for Gumroad.

---

## 🏷️ 1. Listing Meta Details & Settings

Configure these exact settings inside your Gumroad product dashboard for maximum conversions:

* **Product Name:** `PromptDoc AI: 1-Click Codebase Context & Direct Gemini CLI Chat`
* **Short Description (Tagline):** `Stop wasting hours manually copy-pasting code fragments. Scan your workspace, auto-ignore linter/compiler caches, map visual directories, and instantly query your codebase natively from your terminal using Gemini API.`
* **Product Type:** `Digital Product` (Classic)
* **Pricing Model:** `Pay-What-You-Want ($0+)`
  * *Reasoning:* Letting developers download for `$0` removes all entry friction, allowing you to maximize download volume, collect thousands of developer email leads, and build a massive audience for your upcoming product **Sagenta**.
  * *Suggested/Default Price:* Set to `$5.00` (shows as a donation prompt but allows `$0`).
* **Category:** `Software Development / Developer Tools`
* **Tags:** `developer-tools`, `ai`, `artificial-intelligence`, `open-source`, `cli`, `productivity`, `gemini-api`, `devduo`
* **Custom Call to Action Button:** Choose `Get` or `Buy this`

---

## 📄 2. Premium Product Page Description (Copy & Paste)

Paste the following markdown content directly into the rich text/markdown editor on Gumroad:

```markdown
# 🤖 PromptDoc AI: Ultra-Optimized Codebase Packager & CLI Chat

Are you tired of fighting context windows? Spending hours copying 15 different source files into web browsers while debugging? Missing critical files, or blowing up your token limit by accidentally uploading heavy compiled binaries and lock files?

**PromptDoc AI** is an ultra-lightweight, zero-setup Python command-line utility built by developers, for developers. It hooks into your project root, strips out compiler/linter caches, constructs a visual directory hierarchy, and packages a highly optimized markdown context payload directly to your system clipboard and a visible output folder.

And the best part? It comes with **frictionless, zero-setup Gemini CLI Chat integration**. You can query your codebase natively from your console with absolutely no manual setups!

---

### ✨ Core Capabilities

* **⚡ Zero-Setup Interactive Chat:** Just run `promptdoc -a "Your question"`. The tool securely prompts you to paste your free Google AI Studio key once, saves it securely at `~/.promptdoc_key`, and handles all authentication invisibly.
* **📂 Drag-and-Drop Visible Payload:** Automatically outputs a clean codebase package at **`promptdoc_output/prompt_payload.md`** so you can easily drag-and-drop it into Claude, ChatGPT, or Gemini Web App.
* **🛡️ Hardened Ignorers:** Automatically filters out heavy directories (`node_modules`, `venv`, `.git`, `.next`) and standard linter/compiler caches (`.mypy_cache`, `.ruff_cache`, `.pytest_cache`, `.cache`, `.coverage`, `htmlcov`, `.tox`). Strictly respects your project's local `.gitignore` rules.
* **✂️ Smart Token Optimizer:** Identifies and skips non-printable binary streams, and caps text files larger than 500KB with warning placeholders to prevent context blowouts.
* **📂 Visual Directory Tree Mapper:** Generates a premium ASCII map of your active codebase structure up to a custom depth.
* **📋 Clipboard Pipeline Integration:** Automatically copies the fully optimized output markdown payload straight to your clipboard, pre-formatted with instructions prompting the LLM to comprehend your project layout.

---

### 💻 Quick Start in 30 Seconds

```bash
# 1. Clone the repository
git clone https://github.com/your-username/promptDoc.git
cd promptDoc

# 2. Install the package globally
pip install -e .

# 3. Pack your context or ask a question instantly!
promptdoc -a "Explain the codebase structure"
```

---

### 📦 Pay-What-You-Want ($0+)
We packaged this tool out of our internal development pipeline at **DevDuo Innovation** and wanted to release it 100% free to support the developer community. If it saves you hours of copying code, feel free to buy us a coffee! ☕
```

---

## ✉️ 3. Post-Purchase Automated Email Sequence (Lead Nurturing)

Configure this automated workflow email in the Gumroad **Workflows** tab to trigger **1 minute after** a developer downloads PromptDoc AI. This is where we capture their interest for **Sagenta**!

* **Workflow Name:** `PromptDoc Post-Download Welcome & Lead Capture`
* **Trigger:** `Instantly after product is purchased/downloaded`
* **Subject:** `Welcome to PromptDoc AI + Sagenta Private Beta 🚀`
* **Email Body:**

```markdown
Hey!

Thanks for downloading PromptDoc AI! 

This utility was carved out of our team's main pipeline at **DevDuo Innovation**. We got tired of manual copy-pasting while building and testing multi-agent systems, so we built this tool to speed up our workflow and decided to share it for free with the community.

PromptDoc was actually built to support our main upcoming project: **Sagenta**—a localized, multi-agent autonomous framework designed to automate engineering tasks locally on your computer.

If you are interested in watching autonomous coding agent systems work on complex development loops, we would love to have you on our waitlist.

👉 [Join the Sagenta Private Beta Waitlist Here](https://your-waitlist-link.com)

If you have any feedback, bugs, or feature requests for PromptDoc AI, just hit reply to this email. We read and respond to every single message!

Happy coding,

Safwan
Co-founder, DevDuo Innovation
```
