# Brain Template 🧠

A comprehensive template for organizing your "second brain" with AI agents (Claude Code, Codex CLI, etc.) using the **Dilts Framework** for personality customization.

## ✨ Features

- **Interactive onboarding** with 20+ questions
- **Dilts Framework** - 8-parameter personality system
- **Modular system files** (SOUL, IDENTITY, USER, AGENTS, TOOLS)
- **Example configurations** for different roles
- **Privacy-first** design
- **Agent-agnostic** - works with any AI assistant

## 🚀 Quick Start

1. **Clone this repository**
   ```bash
   git clone https://github.com/giobibe/brain-template.git my-brain
   cd my-brain
   ```

2. **Open with your AI agent**
   ```bash
   claude chat  # or your preferred AI CLI
   ```

3. **Follow the onboarding**
   - The agent will read `BOOTSTRAP.md`
   - Answer 20 questions about yourself and preferences
   - System files will be auto-generated
   - `BOOTSTRAP.md` gets deleted after setup

4. **Start using your brain!**

## 📁 Structure

After setup, your brain will have:

```
brain/
├── SOUL.md          # Agent philosophy and boundaries
├── IDENTITY.md      # Personality parameters (Dilts framework)
├── USER.md          # Your context and preferences
├── AGENTS.md        # Operational rules and workflows
├── TOOLS.md         # Reference and integrations
├── database/        # Structured knowledge
│   ├── people/      # Contacts and relationships
│   ├── companies/   # Organizations
│   ├── projects/    # Active and past projects
│   └── tech/        # Technical documentation
├── diary/           # All chronological entries (personal + work)
├── todo/            # Task management
├── inbox/           # Temporary staging area
└── .claude/         # Agent configuration
```

## 🎭 Dilts Framework

Your agent's personality is defined by **8 independent parameters** (1-10 scale):

| Parameter | What it controls |
|-----------|------------------|
| **Formality** | Communication style (casual ↔ professional) |
| **Profanity** | Swearing allowance (clean ↔ creative profanity) |
| **Verbosity** | Response length (concise ↔ thorough) |
| **Technicality** | Jargon level (ELI5 ↔ maximum precision) |
| **Proactivity** | Autonomy (ask first ↔ do without asking) |
| **Security** | Risk tolerance (very cautious ↔ YOLO) |
| **Warmth** | Engagement level (cold ↔ very warm) |
| **Sarcasm** | Irony level (sincere ↔ caustic wit) |

You can adjust these **dynamically** during conversations:
- "Be more formal"
- "Less technical"
- "Zero swearing"

## 📚 Example Configurations

Check `examples/` for complete setups:

- **Developer** (Alex Chen) - Technical, autonomous, casual
  - Formality: 3/10, Technicality: 9/10, Proactivity: 9/10

- **Recruiter** (Sarah Miller) - Warm, professional, GDPR-focused
  - Formality: 6/10, Warmth: 9/10, Security: 4/10 (cautious)

- **Writer** (Marco Bianchi) - Creative, encouraging, Italian
  - Warmth: 9/10, Verbosity: 7/10, Formality: 4/10

- **Project Manager** (Julia Rodriguez) - Organized, balanced
  - Formality: 6/10, Proactivity: 8/10, Warmth: 7/10

## 🔧 Customization

### During Setup
Answer the 20 onboarding questions to customize:
- Agent name, creature, emoji
- Your role, sector, timezone
- All 8 personality parameters
- Privacy rules
- Working style preferences

### After Setup
Edit the system files directly:
- `SOUL.md` - Philosophy and boundaries
- `IDENTITY.md` - Personality parameters
- `USER.md` - Your context
- `AGENTS.md` - Workflows and rules
- `TOOLS.md` - Local notes and integrations

Changes take effect immediately in the next session.

## 🔒 Privacy & Security

- All data stays **local** by default
- **Environment variables** - Store API keys in `.env` (gitignored, never committed)
- `.env.example` provided with common integrations (safe to commit)
- Customizable privacy rules per use case
- GDPR-compliant example (recruiter)
- No external sharing without permission

### Using .env for Secrets

```bash
# 1. Copy example to .env
cp .env.example .env

# 2. Edit .env and add your API keys
# OPENAI_API_KEY=sk-...
# ANTHROPIC_API_KEY=sk-ant-...
# DISCORD_BOT_TOKEN=...

# 3. .env is gitignored - your secrets stay local!
```

**NEVER commit .env to git.** Always use `.env.example` with placeholder values for sharing configurations.

## 📖 Documentation

- [Dilts Framework Guide](docs/dilts-framework.md) - Deep dive into personality parameters
- [Customization Guide](docs/customization-guide.md) - How to tailor your brain
- [FAQ](docs/faq.md) - Common questions

## 🤝 Compatible With

- **Claude Code** (Anthropic) - Primary target
- **Codex CLI** (OpenAI)
- **Aider**
- **Cursor**
- Any AI agent that reads markdown files

## 🛠️ Advanced Features

### Memory System
- **Daily entries**: `diary/YYYY/YYYY-MM-DD.md` (use tags: personal, work, technical)
- **Structured data**: `database/{people,companies,projects}/`

### Dynamic Personality
Change communication style on the fly:
```
User: "Be more formal for this email"
Agent: [adjusts Formality to 8/10]

User: "Back to normal"
Agent: [reverts to default Formality: 5/10]
```

### Multi-Context Support
Different personality profiles for:
- Work contexts
- Personal contexts
- Group chats
- External communications

## 🌟 What Makes This Different

1. **Personality System**: 8-parameter Dilts framework (not just "tone")
2. **Interactive Setup**: Guided onboarding, not manual file editing
3. **Privacy-First**: GDPR examples, local-first design
4. **Agent-Agnostic**: Works with any AI assistant
5. **Production-Ready**: Based on real multi-user deployments (ABChat)

## 📝 License

MIT License - see [LICENSE](LICENSE) file

## 🙏 Credits

Based on the **ABChat** multi-workspace architecture by Giobi Fasoli.

Personality framework inspired by **Robert Dilts** Logical Levels model.

## 🐛 Issues & Feedback

Found a bug? Have a suggestion?

Open an issue at: https://github.com/giobibe/brain-template/issues

---

**Ready to build your second brain? Clone this repo and let's go! 🚀**
