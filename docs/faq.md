# Frequently Asked Questions

## General

### What is a "brain template"?

A structured system for organizing your knowledge, tasks, and communications with an AI assistant. Think of it as a "second brain" that remembers context across sessions.

### Why use this instead of just chatting with Claude?

Regular chats have no memory across sessions. This template:
- Persists memory through files
- Maintains consistent personality
- Organizes knowledge structurally
- Enables workflows and automation

### Is this only for Claude Code?

No! While designed for Claude Code, it works with any AI assistant that can read markdown files (Codex CLI, Aider, Cursor, etc.)

## Setup

### How long does setup take?

5-10 minutes to answer the 20 onboarding questions. The agent auto-generates all system files.

### Can I skip questions?

Some questions have defaults. Required questions are marked clearly.

### What if I make a mistake during setup?

You can:
1. Edit the generated files directly
2. Delete everything and re-run BOOTSTRAP.md
3. Just update the specific parameter in IDENTITY.md

### Do I need coding knowledge?

No. The onboarding is interactive questions. Customization is editing markdown files (plain text).

## Personality Parameters

### What's the difference between Formality and Warmth?

- **Formality**: Professional distance (casual vs. formal language)
- **Warmth**: Emotional engagement (cold vs. encouraging)

You can be "formal but warm" (professional + encouraging) or "casual but cold" (friendly language + pure function).

### Can I change parameters after setup?

Yes! Edit `IDENTITY.md` anytime. Changes take effect in the next session.

### Can I adjust parameters temporarily?

Yes! During conversation:
- "Be more formal for this email" (temporary)
- "Always be more formal" (update IDENTITY.md)

### What's the recommended Proactivity level?

- **7/10** for most users (proactive but asks for risky operations)
- **10/10** if you want maximum autonomy
- **5/10** if you're learning the system

### Should I set Profanity to 1 for work contexts?

Recommended for professional contexts. You can:
- Set default to 1/10
- Use higher values for personal projects
- Create separate profiles for work/personal

## Privacy & Security

### Is my data shared externally?

No. Everything stays local by default. The agent won't send external messages without permission.

### Can I use this for confidential work?

Yes. Set appropriate privacy rules in USER.md. See the recruiter example for GDPR compliance.

### What about API keys?

Store in `.env` files (gitignored by default). Never commit secrets to git.

### Can multiple people use the same brain?

This template is for **single-user** brains. For multi-user, see the ABChat architecture (enterprise setup).

## Files & Structure

### How do I organize diary entries?

Use **tags** in frontmatter to distinguish content type:

```yaml
tags:
  - diary
  - personal    # for personal reflections
```

```yaml
tags:
  - diary
  - work        # for work notes
  - technical   # for technical logs
```

All entries go in `diary/YYYY/`, organized by year.

### Do I have to use all directories?

No. Use what you need. Empty directories are fine.

### Can I add custom directories?

Yes! Document them in TOOLS.md or AGENTS.md for consistency.

### What's inbox/ for?

Temporary staging area. Process items regularly and move to proper locations.

## Usage

### How does the agent remember things?

It reads system files at session start:
1. SOUL.md (philosophy)
2. IDENTITY.md (personality)
3. USER.md (your context)
4. AGENTS.md (workflows)
5. Recent diary/log files

### Can I use this with multiple projects?

Yes! Each project can have an entry in `database/projects/`. The agent can load project-specific context.

### How do I backup my brain?

It's just files! Use:
- Git (recommended)
- Cloud storage (Dropbox, Drive, etc.)
- Regular file backups

### Can I migrate from another system?

Yes. Import your data into the appropriate directories:
- People → `database/people/`
- Projects → `database/projects/`
- Notes → `diary/` (use tags to categorize)

## Customization

### Can I create custom workflows?

Yes! Add them to `AGENTS.md`:

```markdown
## Custom Workflows

### My Morning Routine
1. Check calendar
2. Review TODOs
3. Summarize yesterday
```

### Can I have different personalities for different contexts?

Yes! Define profiles in IDENTITY.md and switch between them.

### Can I add integrations (email, calendar, etc.)?

Yes! Document them in `TOOLS.md`. See examples in `docs/customization-guide.md`.

### How do I create custom entity templates?

Create templates in `database/{type}/.templates/`. See customization guide for details.

## Troubleshooting

### The agent isn't following my personality parameters

Check:
1. Did you edit `IDENTITY.md`?
2. Did you start a new session? (Changes take effect on restart)
3. Is `CLAUDE.md` loading the files correctly?

### The agent keeps asking for confirmation

Lower Security parameter or increase Proactivity in `IDENTITY.md`.

### The agent is too technical / not technical enough

Adjust Technicality parameter in `IDENTITY.md`.

### Files aren't being created with proper frontmatter

The agent should follow conventions in `AGENTS.md`. If not, remind it to read AGENTS.md.

## Intelligent Adaptation

### How does the template adapt to my role?

During setup (STEP 1.5), the agent:
1. **Researches your domain** using WebSearch
2. **Identifies specific needs** (privacy, workflows, tools)
3. **Adapts Dilts parameters** intelligently
4. **Tailors system files** with domain-specific context

Example: "Molecular Chef" → Agent researches precision requirements, food safety, creative workflows → Suggests Technicality 8/10, Warmth 7/10, adds relevant boundaries.

### Is every setup unique?

Yes! No static examples. The agent researches YOUR specific role and sector to create a truly personalized brain.

### What if my role is very niche?

Perfect! The agent will research it and adapt. "Nuclear Safety Inspector", "Quantum Computing Researcher", "Circus Performer" - all get tailored setups based on domain research.

## Advanced

### Can I use this in a team?

This template is for personal use. For team/multi-user:
- Each person has their own brain
- Or use ABChat architecture (enterprise multi-workspace)

### Can I integrate with external services?

Yes! Add wrappers in `tools/lib/` (Python) or document external tools in `TOOLS.md`.

### Can I version control my brain?

Recommended! Use git:

```bash
git init
git add .
git commit -m "Initial brain setup"
```

### Can I publish my brain publicly?

You can! But:
1. Remove all private data from USER.md
2. Sanitize diary/log entries
3. Check `.env` is gitignored
4. Consider using a separate "public brain"

## Support

### Where do I report bugs?

GitHub issues: https://github.com/giobibe/brain-template/issues

### Can I contribute improvements?

Yes! Pull requests welcome. Follow the existing structure.

### Who created this?

Based on the ABChat architecture by Giobi Fasoli. Personality framework inspired by Robert Dilts.

---

**Still have questions?** Open an issue on GitHub!
