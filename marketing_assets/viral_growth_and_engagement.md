# 🚀 Viral Growth & Developer Engagement Playbook

This document contains highly optimized, copy-pasteable post templates and execution strategies for developer platforms to generate massive organic traffic.

---

## 👽 1. Reddit Strategy & Post Templates

Reddit has a zero-tolerance policy for direct self-promotion. To succeed, frame your posts as **valuable open-source sharing** rather than a sales pitch.

### 📍 Subreddit: `r/python` or `r/SideProject`
* **Title Option A:** `I got tired of copy-pasting source files into Claude/ChatGPT, so I built a zero-dependency CLI packager and Gemini chat tool (Open Source)`
* **Title Option B:** `Show Python: A lightweight CLI tool that visualizes your codebase, respects .gitignore, and lets you query it natively with Gemini`
* **Post Body:**
```markdown
Hey everyone,

Like many of you, I spend a lot of time feeding context from my local codebases into browser LLMs (Claude, ChatGPT, etc.) for quick debugging sessions or structural refactoring.

Doing this manually is incredibly annoying: you have to copy individual files, make sure you don't accidentally copy heavy build directories or lockfiles, and constantly battle context windows.

To solve this, I built **PromptDoc AI**—a lightweight, zero-dependency Python utility. It runs in your terminal, scans your workspace, builds a premium ASCII directory map, respects your `.gitignore` rules, and bundles all source code into a single clipboard-ready (and file-saved) token-optimized Markdown package.

Additionally, to save more time, I added a direct Gemini API ask-connector. You can query your codebase natively from your console with **zero-setup setup** (you paste your Google AI Studio key once, and it persists securely at `~/.promptdoc_key`).

It's 100% open-source and free (Pay-What-You-Want) on Gumroad. I built it purely to solve our team's daily friction, and wanted to share it with the community.

* **GitHub:** [Link to your GitHub]
* **Gumroad (Free Download):** [Link to Gumroad]

I'd love to hear how you guys currently handle codebase context packaging, and what features I should add to the roadmap!
```

---

## 🐦 2. X (Twitter) Launch Thread

Frame your Twitter/X thread as a visual, highly practical showcase. Include a short video, screenshot, or GIF showing the CLI terminal in action.

### 🧵 Tweet 1 (The Hook):
> Feeding codebase context to Claude or ChatGPT manually is a massive waste of time.
>
> You copy 10 files, struggle with formatting, or accidentally paste heavy lockfiles and caches.
>
> We built PromptDoc AI to completely remove this bottleneck.
>
> 1-Click Codebase Context + Direct Gemini CLI Chat. 🧵👇 [Add Screenshot/GIF]

### 🧵 Tweet 2 (The Solution):
> 📂 Runs instantly in your terminal.
> 🛡️ Automatically respects local `.gitignore` rules.
> 🧬 Skips binaries and heavy caches (.mypy_cache, .ruff_cache, node_modules).
> 📋 Automatically builds an ASCII visual directory tree and copies the optimized payload to your clipboard.

### 🧵 Tweet 3 (The CLI Chat Magic):
> It gets better: We built a frictionless Gemini CLI ask-connector.
>
> Run `promptdoc -a "Write a pytest suite for promptdoc.py"`
>
> Streams beautifully styled markdown answers right in your terminal. Zero-setup key configuration, saves securely on first run.

### 🧵 Tweet 4 (Call to Action):
> PromptDoc AI is 100% open-source and free (Pay-What-You-Want) on Gumroad.
>
> Grab it free, star our repo, and give us your feedback!
>
> 📦 Gumroad: [Link to Gumroad]
> 🧬 GitHub: [Link to GitHub]
>
> Formed with love by **@DevDuoInnovation** 🚀

---

## ⚡ 3. Hacker News "Show HN" Submission

Hacker News traffic is highly technical. Keep your description minimal, clean, and focus strictly on utility.

* **Title:** `Show HN: PromptDoc AI – Zero-setup codebase context packer & Gemini CLI chat`
* **Text:**
```text
Hey HN,

While building local agent workflows, our team kept losing time copy-pasting source code into browser-based models for debugging. 

We built PromptDoc AI to run directly at the root workspace, scan all source code, respect .gitignore files, ignore heavy binary and build caches, build an ASCII representation of the tree, and output an optimized markdown package to the clipboard and a local folder.

We also built a direct Gemini terminal connector that stores your credentials securely at ~/.promptdoc_key so you can run queries natively.

It is written in Python, open-source under MIT, and free to download. We'd love to get your feedback on how we can improve the ignore matching engine!

GitHub: https://github.com/your-username/promptDoc
Gumroad: [Link to Gumroad]
```
