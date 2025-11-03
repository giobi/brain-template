# Subagent System - Architecture

**Sistema modulare di subagent specializzati per task complessi/autonomi.**

Organizzazione per **DOMINIO FUNZIONALE**, non per directory.

---

## 🎯 Filosofia

**Minimale (5 core) + espandibile**:
- Pochi subagent = facile gestione
- Domini chiari e separati
- Security-first
- Scalabile quando serve

**Quando usare subagent vs diretto**:

✅ **USA SUBAGENT**:
- Task multi-step complesso
- Richiede context building (leggere molti file)
- Può essere fatto autonomamente
- Si ripete spesso

❌ **USA DIRETTO**:
- Task singolo veloce
- Hai già il context caricato
- Richiede interazione user
- Uso sporadico

---

## 🤖 Subagent Core

### 1. health-security-guardian 🛡️

**File**: `health-security-guardian.md`
**Scope**: Security, coherence, integrity TUTTO il brain
**Trigger**: Pre-commit (SEMPRE), daily, weekly, on-demand
**Priority**: 🔥 CRITICAL

**Pre-commit**: Blocca se trova secrets. **Daily**: Coherence + integrity. **Weekly**: Deep scan completo.

Scan secrets, contraddizioni docs/code, frontmatter validation, broken links, token usage, duplicates.

---

### 2. database-curator

**File**: `database-curator.md`
**Scope**: Gestione `database/` (entities, frontmatter, auto-population)
**Trigger**: Sempre (proattivo), cron, email, on-demand

Estrae entities da conversazioni/email, valida schema YAML, crea/aggiorna file database.

---

### 3. email-agent

**File**: `email-agent.md`
**Scope**: Operazioni email (`tools/gmail/`)
**Trigger**: Read/send email, cron check-in

Legge/manda email, sceglie signature giusta da database frontmatter, estrae info per database-curator.

---

### 4. journal-keeper

**File**: `journal-keeper.md`
**Scope**: Gestione `log/` + `diary/`
**Trigger**: Fine giornata, post-sessioni, on-demand

Organizza log lavoro, crea diary da email/eventi, riassunti, link entities.

---

### 5. Explore (built-in)

**Scope**: Codebase exploration
**Trigger**: Ricerca codice, "come funziona X?"

Find files, search code, understand architecture. Già disponibile in Claude Code.

---

## 🏗️ Struttura File

```
tools/subagent/
├── README.md                      # Questa overview
├── health-security-guardian.md    # 🛡️ Security + coherence + integrity
├── database-curator.md            # Prompt + docs curator
├── email-agent.md                 # Prompt + docs email
└── journal-keeper.md              # Prompt + docs journal
```

Ogni file contiene:
- Prompt completo per il subagent
- Documentazione obiettivi/compiti
- Tool disponibili
- Output format
- Esempi uso

---

## 📡 Communication Flow

```
User Request
    ↓
Anacleto (main)
    ↓
├─→ email-agent (legge email)
│       ↓ (output: email data)
├─→ database-curator (estrae entities)
│       ↓ (output: entities created/updated)
└─→ journal-keeper (crea log)
        ↓ (output: log file created)
    ↓
Anacleto riporta a User
```

---

## 🚀 Invocazione

**Via Task tool** in Claude Code:

```python
Task(
    subagent_type="general-purpose",
    description="Update database entities from recent emails",
    prompt=f"""
    {open("tools/subagent/database-curator.md").read()}

    CONTEXT:
    - Recent emails: {email_list}
    - Current database state: {db_state}

    TASK: Extract all mentioned people/companies and update database
    """
)
```

**Via comando diretto**:

Quando Anacleto (io) vede task complesso → lancio subagent appropriato automaticamente.

---

## 📋 Implementation Status

- ✅ **Architecture designed** (questo file)
- ⏳ **health-security-guardian** - 🔥 PRIORITY #1 (security first!)
- ⏳ **database-curator** - Depends on database refactoring
- ⏳ **email-agent** - Depends on database-curator
- ⏳ **journal-keeper** - Can be standalone
- ✅ **Explore** - Already built-in

**Next**: health-security-guardian (pre-commit hook) → Database refactoring frontmatter → database-curator → email-agent → journal-keeper

---

## 🔄 Future Expansions

**Possibili subagent futuri** (aggiungi solo se necessario):

- **system-admin**: Server/SSH/WordPress operations
- **content-writer**: Batch content creation, editorial planning
- **code-analyzer**: Refactoring, documentation generation

**Regola**: Aggiungi nuovo subagent solo quando task è ricorrente, domain ben definito, complexity alta.

---

## 📚 References

- **Planning**: `todo/2025-11-03-subagent-architecture.md`
- **Database refactoring**: `todo/2025-11-03-database-refactoring-frontmatter.md`

---

**Created**: 2025-11-03 by Anacleto 🦉
**Architecture**: Minimale, scalabile, domain-driven
