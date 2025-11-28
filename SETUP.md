# Brain Setup

Questo file guida l'agent nel setup iniziale del tuo brain.

---

## Istruzioni per l'Agent

**LEGGI ATTENTAMENTE E SEGUI QUESTI STEP:**

### Step 1: Fai queste domande all'utente

1. "Come ti chiami?" (nome che usero' per riferirti)
2. "Come vuoi che mi chiami?" (es. Jarvis, Alfred, Brain, o nessun nome)
3. "Che tono preferisci?" (formale / casual / tecnico / sarcastico)
4. "Vuoi che abbia una personalita' particolare?" (se si', chiedi di descriverla)

**ASPETTA LE RISPOSTE PRIMA DI CONTINUARE.**

---

### Step 2: Crea la struttura

Crea queste cartelle e file:

```
boot/
  identity.md        <- crea con le risposte dello Step 1
database/
  people/
    .index.md        <- crea vuoto con frontmatter
  projects/
    .index.md        <- crea vuoto con frontmatter
diary/
  .gitkeep
log/
  .gitkeep
todo/
  .gitkeep
.gitignore           <- IMPORTANTE: deve contenere .env
```

---

### Step 3: Crea boot/identity.md

Usa questo template, riempiendo con le risposte:

```markdown
---
title: Identity
created: [DATA OGGI]
updated: [DATA OGGI]
tags:
  - boot
  - identity
type: config
---

# Identity

## Utente
- **Nome**: [RISPOSTA 1]

## Agent
- **Nome**: [RISPOSTA 2, o "nessuno"]
- **Tono**: [RISPOSTA 3]
- **Personalita'**: [RISPOSTA 4, o "neutra"]
```

---

### Step 4: Crea .gitignore

```
.env
*.env
.env.*
.DS_Store
Thumbs.db
.vscode/
.idea/
*.swp
*~
```

---

### Step 5: Crea database/people/.index.md

```markdown
---
title: Indice Persone
created: [DATA OGGI]
updated: [DATA OGGI]
tags:
  - index
  - people
type: index
---

# Persone

*Nessuna persona ancora.*

## Come aggiungere

Chiedi: "Aggiungi persona: [nome]"
```

---

### Step 6: Crea database/projects/.index.md

```markdown
---
title: Indice Progetti
created: [DATA OGGI]
updated: [DATA OGGI]
tags:
  - index
  - projects
type: index
---

# Progetti

*Nessun progetto ancora.*

## Come aggiungere

Chiedi: "Aggiungi progetto: [nome]"
```

---

### Step 7: Conferma all'utente

Mostra:

```
Setup completato!

Struttura creata:
- boot/identity.md (tue preferenze)
- database/people/ (contatti)
- database/projects/ (progetti)
- diary/ (diario personale)
- log/ (log di lavoro)
- todo/ (task)

Comandi utili:
- "Aggiungi persona: Mario Rossi"
- "Aggiungi progetto: Mio Sito"
- "Scrivi nel diario: [testo]"
- "Log di lavoro: [cosa ho fatto]"
- "Nuovo todo: [descrizione]"

Per la documentazione completa, vedi AGENTS.md
```

---

## Regole per dopo il setup

### Ogni file .md DEVE avere frontmatter

```yaml
---
title: Titolo
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - tag1
type: person | project | diary | log | todo | index
---
```

### Naming convention

- Tutto lowercase
- Trattini invece di spazi
- Esempi: `mario-rossi.md`, `mio-progetto.md`

### Differenza diary vs log

- **diary/**: vita personale, emozioni, riflessioni
- **log/**: lavoro, progetti, note tecniche

---

## Discord (opzionale)

Se l'utente chiede integrazione Discord:

1. Vai su https://discord.com/developers/applications
2. New Application → Bot → copia Token
3. Crea `.env` con:
   ```
   DISCORD_BOT_TOKEN=xxx
   DISCORD_SERVER_ID=xxx
   DISCORD_CHANNEL_ID=xxx
   ```
4. **MAI committare .env**
