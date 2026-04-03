# Brain Protocol

Open specification for structured AI agent workspaces.

**Markdown-first, git-versioned, LLM-agnostic, human-readable.**

> The AI model is replaceable. The brain is not.

## What is it

Brain Protocol is a convention — not a framework, not software. It defines how to organize markdown files so any AI agent can read them, write to them, and accumulate knowledge over time.

Your brain is yours: portable, readable, versioned. Works with Claude, Gemini, GPT-4o, Cursor, Aider, or anything that reads files.

## Quick Start

```bash
git clone https://github.com/giobi/brainprotocol.git my-brain
cd my-brain
```

Open with your AI agent. It will read `boot/soul.md` and start the interactive onboarding.

## Structure

```
brain/
├── boot/         ← Identity: who you are, how the AI behaves
├── wiki/         ← Structured entities: people, companies, projects
├── diary/        ← Temporal log: what happened, when, why
├── todo/         ← Open tasks with frontmatter and tags
├── inbox/        ← Staging area for incoming stuff
├── public/       ← Published files, served via web
├── storage/      ← Temporary files, cache, unstructured data
└── .env          ← Credentials (always gitignored)
```

Every `.md` file has YAML frontmatter:

```yaml
---
type: diary
date: '2026-04-03'
project: my-project
tags:
  - meeting
  - decisions
---
```

## Skills

Skills are installable modules: commands, agents, automations, integrations. Install with `/brain install <skill>`. Skills are protocol-level — they work on any brain, with any LLM.

## Compatibility

Works with any AI agent that reads markdown:

- Claude Code (Anthropic)
- Gemini CLI (Google)
- GPT-4o / ChatGPT
- Cursor, Windsurf, Aider
- Codex CLI, Mistral, Llama

## Links

- **Website**: [brainprotocol.it](https://brainprotocol.it)
- **Specification**: [boot/brain.md](boot/brain.md)
- **License**: MIT

---

Brain Protocol v5.1 — [giobi.com](https://giobi.com)

