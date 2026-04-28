---
name: project
description: "Project-first session management — activate, create, search projects in wiki/"
user-invocable: true
argument-hint: "[name|list|info|search|temp] [question]"
---

# /project — Project Manager

**Every session works on ONE project.** At startup, the user names the project.
This command loads context and activates the project for the session.

## NLP-First

Interprets natural language — no rigid subcommands.

```
/project nexum                          -> activate nexum
/project show me all                    -> list
/project what am I working on           -> info
/project search laravel                 -> search
/project cooking how do I make rice?    -> activate + answer
/project temp                           -> use YYYY-MM-temp
```

---

## Project Structure — RAG-Oriented

**Every project is a folder** with a mandatory `index.md` + separate files for deep dives.

### Templates by type

In `wiki/projects/.templates/`:
- `app.md` — app with codebase (backend, frontend, DB). Includes Design System + Do/Don'ts UI.
- `website.md` — CMS, static site. Includes domains, plugins, email.
- `business.md` — client relationship, quotes, invoices.
- `personal.md` — hobby, tracking, notes.

### Philosophy: Zero Token Waste

**`index.md`** = RAG-friendly executive summary (<500 tokens):
- What the project is (1-2 paragraphs)
- **Folder map** — what each file contains
- Key info (client, status, stack, contacts)
- Permanent Do/Don'ts
- Current status (one line, REPLACED each time)

**Separate files** = on-demand deep dives:
- `quote-xyz.md`, `tech-stack.md`, `decision-history.md`
- `YYYY-MM-DD-event.md` — dated events (deploy, incident, decisions)

### Save Rules

| What | Where it goes | Where it does NOT go |
|------|---------------|---------------------|
| Structural info (stack, access, domains) | `index.md` fixed sections | — |
| Current status | `index.md` — ONE line, REPLACE | Don't append timeline |
| Dated events (crisis, deploy, decisions) | `diary/YYYY/` with project tag | NOT in index.md |
| Issue tracking, changelog | `{project}/issues.md` or `{project}/log.md` | NOT in index.md |
| Do/Don'ts | `index.md` — permanent rules | NOT temporary operational notes |
| Quote/budget details | `{project}/quote-*.md` | Only reference in index |

**Key rule:** Current status = snapshot, not journal. Do/Don'ts = permanent rules, not TODOs.

---

## Intent Detection

```python
args = "$ARGUMENTS".strip()
args_lower = args.lower()

if args_lower == "temp":
    intent = "temp"
elif any(w in args_lower for w in ["list", "show", "all", "let me see", "elenco"]):
    intent = "list"
elif any(w in args_lower for w in ["active", "current", "what", "status", "info"]):
    intent = "info"
elif any(w in args_lower for w in ["search", "find", "look for"]):
    intent = "search"
elif any(w in args_lower for w in ["analyze", "scan", "deep"]):
    intent = "scan"
else:
    parts = args.split(maxsplit=1)
    intent = "activate"
    project_name = parts[0].lower().replace(" ", "-")
    follow_up_question = parts[1] if len(parts) > 1 else None
```

## Project Activation

```python
import glob
from pathlib import Path

project_name = "$ARGUMENTS".strip().split()[0].lower().replace(" ", "-")

# temp shortcut
if project_name == "temp":
    from datetime import datetime
    project_name = datetime.now().strftime("%Y-%m") + "-temp"

project_file = Path(f"wiki/projects/{project_name}/index.md")

# Fuzzy matching if exact match doesn't exist
if not project_file.exists():
    norm = lambda s: ''.join(c for c in s if c.isalnum()).lower()
    matches = [
        (p, Path(p).parent.name)
        for p in glob.glob("wiki/projects/*/index.md")
        if norm(project_name) in norm(Path(p).parent.name)
        or norm(Path(p).parent.name) in norm(project_name)
    ]
    if len(matches) == 1:
        project_file = Path(matches[0][0])
        project_name = matches[0][1]
    elif len(matches) > 1:
        # Show list, ask to be more specific
        pass
```

### Activation Output

```
Project active: {name}

{first paragraph of the project}

Do: ...
Don'ts: ...
Current status: {status section or "No previous status"}
Open TODOs: N
Recent logs: ...

Rule 0: save to wiki/ and diary/ IMMEDIATELY after every action. Not later, not at the end. Now.

Ready. Logs and TODOs for this session -> tag: {name}
```

### New Project (if it doesn't exist)

Conversational interview:
1. Determine the type (App / Website / Business / Personal)
2. Type-specific questions
3. Create `wiki/projects/{name}/index.md` from the right template

## Tmux Integration (optional)

If the `tmux` skill is installed, on activation:

```bash
# Rename current pane
~/.tmux/set-pane-title.sh "{name} / {topic}"

# Rename window and save mapping
CURRENT_WIN=$(tmux display-message -p '#{window_index}')
echo "{name}" > ~/.tmux/window-projects/$CURRENT_WIN
tmux rename-window "{name}"
```

If the window belonged to a different project, notify the user.

## Session Logger (optional)

If a `session-logger` subagent is available, launch it in background:

```
subagent_type: session-logger
prompt: "Session started for project {name}. Log checkpoints every ~15 messages."
run_in_background: true
model: haiku  (or the lightest available model)
```
