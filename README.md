# 🧠 Brain Template

> An AI-first second brain template designed to interface perfectly with Claude and other AI assistants.

## What is this?

This is a **digital brain system** that solves a fundamental problem: **context loss**. Every time you:
- Switch devices
- Open a new AI chat session
- Switch between projects
- Take a break and come back

...you lose context. You have to re-explain everything. **Brain solves this.**

## Philosophy

Your brain is a **living knowledge base** that:
- 📝 Captures project context (what, where, how)
- 🤔 Documents decision history (why X instead of Y)
- 🗺️ Maintains mental maps (how pieces connect)
- ⚙️ Stores configurations and practices
- 💭 Preserves personal reflections

**The goal**: Give AI full context in seconds, maintain continuity across time and space.

## Structure

```
brain/
├── prompt.md              # The heart: loaded by AI every session
├── projects/              # Project documentation
│   └── project-name/
│       └── index.md       # Project overview, status, decisions
├── diary/                 # Daily logs and reflections
│   └── YYYY/
│       ├── YYYY-MM-DD-diary.md
│       └── .highlights.md # Year's top moments
├── todo/                  # Action items with due dates
│   └── YYYY-MM-DD-task-name.md
├── tools/                 # Reusable procedures by product/service
│   └── product-name/
│       └── procedure.md
└── stats/                 # Auto-generated weekly statistics
    └── YYYY-WXX.md
```

## Quick Start

### 1. Clone and Initialize

```bash
# Clone this template
git clone https://github.com/giobi/brain-template.git brain
cd brain

# Initialize your own repository
rm -rf .git
git init
git add .
git commit -m "🧠 Initialize brain"

# Push to your own repo (create it first on GitHub)
git remote add origin https://github.com/YOUR_USERNAME/brain.git
git push -u origin main
```

### 2. Configure `prompt.md`

This is **the most important file**. It's loaded by AI at the start of every session.

Copy `prompt.template.md` to `prompt.md` and fill it with:

```bash
cp prompt.template.md prompt.md
# Edit prompt.md with your information
```

**What to include:**
- Active projects and their status
- Your communication style preferences
- Your working style and practices
- Infrastructure locations and conventions
- Any context AI needs to work with you effectively

### 3. Set Up GitHub Actions (Optional but Recommended)

The template includes two automations:

#### Weekly Stats (Monday 9 AM UTC)
Auto-generates statistics about your brain activity.

**Required secrets:** None

#### Todo Reminders (Daily 8 AM UTC)
Sends Telegram notifications for overdue/due todos.

**Required secrets:**
- `TELEGRAM_BOT_TOKEN`: Your Telegram bot token ([create one](https://t.me/botfather))
- `TELEGRAM_CHAT_ID`: Your Telegram user ID ([get it](https://t.me/userinfobot))

Add secrets in: `Settings → Secrets and variables → Actions → New repository secret`

### 4. Start Using It

#### Create a diary entry:
```bash
# Create today's diary
mkdir -p diary/$(date +%Y)
echo "# $(date +%Y-%m-%d) - Title

## What happened today

...

## Learnings

...

## Next steps

..." > diary/$(date +%Y)/$(date +%Y-%m-%d)-diary.md
```

#### Document a project:
```bash
mkdir -p projects/my-project
echo "# My Project

## Overview
Brief description...

## Status
Current state...

## Tech Stack
- Technology 1
- Technology 2

## Decisions Log
### YYYY-MM-DD: Decision title
Why we chose X over Y...

## Next Steps
- [ ] Task 1
- [ ] Task 2
" > projects/my-project/index.md
```

#### Create a todo:
```bash
echo "---
due_date: 2025-12-31
priority: high
---

# Task Name

## Context
Why this needs to be done...

## Steps
- [ ] Step 1
- [ ] Step 2

## Success Criteria
What done looks like...
" > todo/2025-12-31-task-name.md
```

## How to Use with AI

### At Session Start

Load your brain context:

```
Please read my brain/prompt.md file to understand the context.
```

Or with Claude Code, simply reference files:
```
Check brain/prompt.md for context
```

### During Work

Have AI update your diary:
```
Update my diary for today at brain/diary/2025/2025-10-17-diary.md
```

### At Session End

```
Please update my daily diary with what we accomplished today
```

## Best Practices

### 1. Keep `prompt.md` Current
This is your **living context file**. Update it when:
- Projects change status
- You learn new practices
- Infrastructure changes
- Communication preferences evolve

### 2. Daily Diary Habit
Even 5 minutes at end of day. Capture:
- What you accomplished
- What you learned
- What's blocking you
- What's next

### 3. Document Decisions
When you make a non-trivial decision, document:
- What you decided
- Why (alternatives considered)
- Trade-offs
- Date and context

### 4. Use Todos with Due Dates
Format: `YYYY-MM-DD-descriptive-name.md`
Include due date in frontmatter for automation support.

### 5. Organize Tools by Product
Not by date, by service. Examples:
- `tools/linux/system-health-check.md`
- `tools/docker/debugging-containers.md`
- `tools/newrelic/cost-analysis.md`

## Customization

### Workflow Schedules

Edit `.github/workflows/*.yml` to change:
- Stats generation time (default: Monday 9 AM UTC)
- Todo reminder time (default: Daily 8 AM UTC)

### Directory Structure

Feel free to add directories for your needs:
- `research/` - Research notes
- `meetings/` - Meeting notes
- `learning/` - Learning resources
- `ideas/` - Random ideas

The template is a starting point. Adapt it to your brain! 🧠

## Philosophy & Inspiration

This template is based on:
- **Second Brain methodology** (Building a Second Brain by Tiago Forte)
- **Zettelkasten principles** (interconnected atomic notes)
- **AI-first design** (optimized for AI consumption and generation)
- **Git as continuity layer** (version control for thoughts)

The key insight: **Your brain should be a living document that grows with you and provides instant context to any AI you work with.**

## FAQ

### Why not use Notion/Obsidian/Roam?

You can! This template works alongside them. The advantage of a git-based system:
- ✅ Plain text (future-proof, AI-readable)
- ✅ Version controlled (full history)
- ✅ Scriptable (automate everything)
- ✅ Free (no subscriptions)
- ✅ Private (self-hosted)
- ✅ Cross-platform (works everywhere)

### Should my brain be public or private?

**Recommendation: Keep it private** unless you're comfortable sharing:
- Your project details
- Your daily thoughts
- Your decision-making process
- Personal reflections

Create a public fork if you want to share select parts.

### How often should I commit?

As often as you want! Some practices:
- Commit after each diary entry
- Commit after documenting a decision
- Auto-commit with cron (e.g., every hour if changes exist)

### Can I use this with other AI assistants?

**Absolutely!** The format is AI-agnostic. Just load `prompt.md` at session start with:
- ChatGPT
- GitHub Copilot
- Any other AI assistant that can read files

## Contributing

Found a bug or have a suggestion? [Open an issue](https://github.com/giobi/brain-template/issues)!

## License

MIT License - Use freely, modify as needed, make it yours! 🚀

## Credits

Created by [giobi](https://github.com/giobi) - Inspired by years of context loss frustration.

---

**Ready to build your brain?** Start with `prompt.md` and go from there. 🧠✨
