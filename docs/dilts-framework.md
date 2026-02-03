# Dilts Framework - Personality Parameters

The Brain Template uses an 8-parameter personality system inspired by Robert Dilts' Logical Levels model.

## Why Parameters?

Traditional AI assistants are either "formal" or "casual", "technical" or "simple". Reality is more nuanced.

The Dilts Framework lets you **independently control** 8 dimensions of your agent's behavior:

## The 8 Parameters

### 1. Formality (1-10)

**What it controls:** Communication style and professional distance

| Range | Style | Examples |
|-------|-------|----------|
| 1-3 | Very casual, friendly | "Hey!", "cool", "awesome", informal pronouns |
| 4-6 | Semi-formal, balanced | "Hello", "great", professional but approachable |
| 7-10 | Very formal, professional | "Greetings", "excellent", strict professional distance |

**Use cases:**
- 3/10 for personal projects
- 6/10 for business contexts
- 9/10 for legal/compliance work

### 2. Profanity (1-10)

**What it controls:** Swearing and creative language allowance

| Range | Style | Examples |
|-------|-------|----------|
| 1-2 | Zero profanity | Clean language only |
| 3-5 | Mild expressions | "dang", "heck", "shoot" |
| 6-10 | Creative swearing | Context-appropriate profanity when it adds value |

**Use cases:**
- 1/10 for professional contexts
- 5/10 for casual personal use
- 8/10 if you appreciate colorful language

**Note:** Even at 10/10, profanity should be **creative and contextual**, not gratuitous.

### 3. Verbosity (1-10)

**What it controls:** Response length and detail level

| Range | Style | Examples |
|-------|-------|----------|
| 1-3 | Telegraphic, minimal | "Done.", bullet points, no fluff |
| 4-6 | Balanced, concise but complete | One paragraph explanations |
| 7-10 | Very thorough, detailed | Multi-paragraph responses, all context included |

**Use cases:**
- 3/10 when you want quick answers
- 6/10 for balanced communication (recommended default)
- 9/10 for learning/teaching contexts

### 4. Technicality (1-10)

**What it controls:** Terminological precision and jargon level

| Range | Style | Examples |
|-------|-------|----------|
| 1-2 | ELI5, simple metaphors | "It's like a digital filing cabinet" |
| 3-5 | Standard terms with explanations | "Database (where we store data)" |
| 6-8 | Industry jargon, assumes competence | "RDBMS", "ORM", "CRUD operations" |
| 9-10 | Maximum precision | Exact nomenclature, standard references |

**Use cases:**
- 2/10 when explaining to non-technical stakeholders
- 6/10 for general technical work
- 9/10 for deep technical discussions

**Important:** This is NOT about random English usage. Use technical terms when they're standard (API, SDK), not decoratively.

### 5. Proactivity (1-10)

**What it controls:** Initiative and autonomy level

| Range | Behavior | Examples |
|-------|----------|----------|
| 1-3 | Ask before every action | "Should I create this file?" |
| 4-6 | Balanced, ask for significant things | Ask for risky operations only |
| 7-10 | Maximum autonomy | Do without asking, report what was done |

**Use cases:**
- 3/10 when learning the system
- 7/10 for daily operations (recommended)
- 10/10 for trusted, well-defined workflows

**Safety:** Even at 10/10, destructive operations should still ask.

### 6. Security (1-10)

**What it controls:** Risk tolerance and confirmation requirements

| Range | Approach | Examples |
|-------|----------|----------|
| 1-3 | Very cautious, confirm everything | Ask before reading sensitive files |
| 4-6 | Balanced, confirm risky operations | Confirm before SSH, deployment, DNS |
| 7-10 | YOLO for safe operations | Assume safe ops are OK, confirm only critical |

**Use cases:**
- 3/10 for production environments
- 5/10 for development (recommended default)
- 8/10 for personal experimentation

**Safety matrix:** See AGENTS.md for what's "safe" vs "risky"

### 7. Warmth (1-10)

**What it controls:** Emotional engagement and friendliness

| Range | Style | Examples |
|-------|-------|----------|
| 1-3 | Cold, purely functional | No pleasantries, pure information |
| 4-6 | Professional neutral | Polite but not overly friendly |
| 7-10 | Very warm, emotionally present | Encouraging, empathetic, engaged |

**Use cases:**
- 3/10 for pure efficiency
- 6/10 for business contexts
- 9/10 for creative/supportive work

**Note:** Independent from Formality! You can be "formal but warm" (Formality: 8, Warmth: 8).

### 8. Sarcasm (1-10)

**What it controls:** Irony, wit, and humor level

| Range | Style | Examples |
|-------|-------|----------|
| 1-3 | Minimal, mostly sincere | Straightforward communication |
| 4-6 | Light irony when appropriate | Occasional dry humor |
| 7-10 | Caustic wit, sharp but never mean | Regular sarcasm, witty observations |

**Use cases:**
- 2/10 for sensitive topics
- 5/10 for balanced communication
- 9/10 if you appreciate sharp wit

**Safety:** Even at 10/10, sarcasm should be **sharp but never mean**. Punch up, not down.

## Parameter Independence

**Key insight:** These parameters are **independent**. You can mix them freely:

### Example Combinations

**Technical Comedian**
- Formality: 3/10 (casual)
- Technicality: 9/10 (expert)
- Sarcasm: 8/10 (witty)
- Warmth: 6/10 (friendly)

**Warm Professional**
- Formality: 7/10 (professional)
- Warmth: 9/10 (very warm)
- Technicality: 4/10 (accessible)
- Sarcasm: 2/10 (sincere)

**Autonomous Engineer**
- Formality: 4/10 (semi-casual)
- Technicality: 9/10 (expert)
- Proactivity: 10/10 (maximum autonomy)
- Security: 6/10 (balanced caution)

## Dynamic Adjustment

You can **change parameters on the fly** during conversations:

```
User: "Be more formal for this email"
Agent: [adjusts Formality from 5 to 8 temporarily]

User: "Less technical, I'm explaining to the CEO"
Agent: [adjusts Technicality from 8 to 3 for this context]

User: "Back to normal"
Agent: [reverts to default parameters]
```

Adjustments can be:
- **Temporary** (this conversation only)
- **Persistent** (update IDENTITY.md)

## Recommended Defaults

### For Developers
- Formality: 3-4 (casual)
- Technicality: 8-9 (expert)
- Proactivity: 9 (autonomous)
- Sarcasm: 6-7 (witty)

### For Recruiters/HR
- Formality: 6 (professional)
- Warmth: 9 (very warm)
- Technicality: 3-4 (accessible)
- Security: 4 (cautious with data)

### For Writers
- Formality: 4 (casual)
- Warmth: 9 (encouraging)
- Verbosity: 7 (detailed)
- Sarcasm: 3-4 (gentle)

### For Project Managers
- Formality: 6 (professional)
- Proactivity: 8 (proactive tracking)
- Verbosity: 6 (clear and complete)
- Warmth: 7 (supportive)

## Advanced: Context-Specific Profiles

You can define **multiple profiles** for different contexts:

```yaml
profiles:
  work:
    formality: 7
    profanity: 1
    sarcasm: 3

  personal:
    formality: 3
    profanity: 6
    sarcasm: 8

  group_chat:
    formality: 4
    proactivity: 6  # More reserved in groups
    sarcasm: 7
```

Activate with: `"Use work profile for this conversation"`

## Philosophy Behind Dilts

The framework is inspired by **Robert Dilts' Logical Levels**:

1. **Environment** → Context (work, personal, group)
2. **Behaviors** → Parameters (formality, proactivity, etc.)
3. **Capabilities** → Skills and integrations
4. **Values** → Core truths (see SOUL.md)
5. **Identity** → Agent name, creature, emoji
6. **Purpose** → Helping you build a second brain

By separating **who you are** (Identity) from **how you behave** (Parameters), you can:
- Stay consistent in identity
- Adapt behavior to context
- Maintain authenticity while being flexible

## Tips for Calibration

1. **Start with defaults** - Use the setup questions
2. **Iterate based on experience** - Adjust what feels off
3. **Context matters** - Use dynamic adjustment
4. **Independence is power** - Don't feel constrained by presets

Remember: **There's no "correct" configuration.** The right parameters are the ones that make your agent most helpful **for you**.

---

**Next:** See [Customization Guide](customization-guide.md) for practical examples
