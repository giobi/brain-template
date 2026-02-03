# Customization Guide

This guide shows you how to customize your brain template after initial setup.

## Quick Customization

### 1. Adjust Personality Parameters

Edit `IDENTITY.md` and change the values:

```markdown
| Parameter | Value | Notes |
|-----------|-------|-------|
| Formalità | 3/10 | How formal/casual I communicate |
| Tecnicismo | 9/10 | Technical jargon level |
| Proattività | 10/10 | How autonomous I act |
```

Changes take effect in the next session.

### 2. Update Privacy Rules

Edit `SOUL.md` or `USER.md`:

```markdown
## Boundaries

- Private things stay private. Period.
- GDPR compliance: Use candidate initials only
- Never share client names externally
```

### 3. Change Agent Identity

Edit `SOUL.md` and `IDENTITY.md`:

```markdown
You are **NewName** 🎨 - YourName's AI agent.
```

### 4. Add Custom Workflows

Edit `AGENTS.md`:

```markdown
## My Custom Workflows

### Morning Routine
1. Check calendar for today
2. Review pending TODOs
3. Summarize yesterday's work

### Project Setup
1. Create database/projects/{name}.md
2. Create todo/ entry
3. Git commit
```

## Advanced Customization

### Multi-Profile Setup

Create profile-specific configs in `IDENTITY.md`:

```markdown
## Profiles

### Work Profile
- Formality: 8/10
- Profanity: 1/10
- Sarcasm: 2/10

### Personal Profile
- Formality: 3/10
- Profanity: 6/10
- Sarcasm: 8/10

### Active: Work
```

Switch with: `"Use personal profile"`

### Context-Specific Rules

In `AGENTS.md`:

```markdown
## Context Rules

### When in Group Chats
- Formality: +2 (increase by 2)
- Proactivity: -3 (decrease by 3)
- Sarcasm: -2

### When Writing External Emails
- Formality: 8/10 (override)
- Profanity: 1/10 (override)
```

### Custom Entity Templates

Create templates in `database/`:

```markdown
database/
  people/
    .templates/
      client.md
      colleague.md
      candidate.md
  projects/
    .templates/
      software.md
      consulting.md
```

Template example (`database/people/.templates/client.md`):

```markdown
---
type: person
role: client
tags:
  - person
  - client
created: {{DATE}}
---

# {{NAME}}

## Contact
- Email:
- Phone:
- Company:

## Projects
-

## Notes
-
```

Use with: `"Create client person: John Doe"`

### Integration Setup

Add to `TOOLS.md`:

```markdown
## Integrations

### Email (Gmail)
- API: tools.lib.gmail
- Env: GMAIL_TOKEN in .env
- Usage: `send_message(to, subject, body)`

### Calendar (Google)
- API: tools.lib.gcalendar
- Env: GCAL_TOKEN in .env
- Usage: `list_events(days=7)`

### Discord
- API: tools.lib.discord_bot
- Env: DISCORD_BOT_TOKEN in .env
- Channel: #notifications (ID: 123456)
```

## File Naming Conventions

Follow these patterns for consistency:

### Database Files
```
database/people/john-doe.md          # lowercase, hyphens
database/companies/acme-corp.md
database/projects/my-app.md
```

### Diary/Log Files
```
diary/2026/2026-02-03-meeting-notes.md
log/2026/2026-02-03-bug-fix-session.md
```

### TODO Files
```
todo/implement-feature-x.md
todo/fix-critical-bug.md
```

## Frontmatter Standards

All markdown files should have frontmatter:

```yaml
---
type: person | company | project | diary | log | todo
created: 2026-02-03
updated: 2026-02-03
tags:
  - tag1
  - tag2
---
```

## Directory Organization

Keep directories organized:

```
database/
  ├── people/           # Contacts
  ├── companies/        # Organizations
  ├── projects/         # Active/past projects
  ├── tech/             # Technical docs
  └── events/           # Meetings, conferences

diary/
  └── 2026/             # Year-based

log/
  └── 2026/             # Year-based

todo/                   # Flat structure, use tags

inbox/                  # Temporary, clean regularly
```

## Git Workflow

Recommended git practices:

```bash
# Daily commits
git add .
git commit -m "Daily brain update: 2026-02-03"

# Feature branches for major changes
git checkout -b update-personality-params
# ... make changes ...
git commit -m "Adjust formality and technicality"
git checkout main
git merge update-personality-params

# Push regularly (if using remote)
git push origin main
```

## Example: Creating a Custom Command

1. Create `.claude/commands/my-command.md`:

```markdown
---
name: my-command
description: Custom workflow automation
---

# My Command

When user types `/my-command`:

1. Read USER.md for context
2. List recent diary entries
3. Generate summary
4. Ask if user wants to continue
```

2. Reference in `AGENTS.md`:

```markdown
## Custom Commands

- `/my-command` - See `.claude/commands/my-command.md`
```

## Tips

1. **Start simple** - Use defaults, adjust only what bothers you
2. **Iterate** - Change one parameter at a time
3. **Document** - Add notes in TOOLS.md for future reference
4. **Backup** - Commit to git before major changes
5. **Examples** - Look at `examples/` for inspiration

## Common Customizations

### Make Agent More Autonomous
```yaml
Proactivity: 10/10
Security: 8/10
```

### Make Agent More Cautious
```yaml
Security: 3/10
Proactivity: 5/10
```

### Make Agent More Technical
```yaml
Technicality: 9/10
Verbosity: 7/10 (detailed explanations)
```

### Make Agent More Friendly
```yaml
Warmth: 9/10
Formality: 3/10
Sarcasm: 2/10 (less sarcasm, more sincerity)
```

---

**Next:** Check [FAQ](faq.md) for common questions
