# Brain Bootstrap - Setup Guidato

Questo file guida l'agent AI nell'organizzazione del tuo brain.

---

## 🚀 Prima Sessione: Setup Rapido

**IMPORTANTE**: Al primo avvio, l'agent fa UNA domanda e parte.

### Domanda Unica

> "Come ti chiami e che tono preferisci? (casual/formale/tecnico)"

L'utente risponde in una riga, l'agent crea tutto e parte.

**Esempio:**
```
Utente: "Marco, casual"
Agent: "📝 Configurato! Brain pronto.

Raccontami cosa stai facendo, comincio a organizzare."
```

### Setup Automatico

Dopo la risposta, l'agent:
1. Crea `boot/identity.md` con nome e tono
2. Crea struttura cartelle
3. Crea indici in `database/`
4. **Parte subito** - niente riepilogo prolisso

### Se l'Utente Non Risponde

Se l'utente salta la domanda e inizia a parlare d'altro:
- L'agent usa "tu" generico
- Tono default: casual
- **Non blocca** - configura dopo, al volo

---

## 📁 Struttura Brain

```
brain/
├── boot/
│   └── identity.md          # Chi sei, chi è l'agent, preferenze
├── database/
│   ├── people/
│   │   ├── .index.md         # Indice persone
│   │   └── *.md              # Una persona per file
│   └── projects/
│       ├── .index.md         # Indice progetti
│       └── *.md              # Un progetto per file
├── diary/
│   └── YYYY/
│       └── YYYY-MM-DD.md     # Diario personale (vita, pensieri, emozioni)
├── log/
│   └── YYYY/
│       └── YYYY-MM-DD-*.md   # Log di lavoro (progetti, task, tecnico)
├── todo/
│   └── *.md                  # Task attivi
├── .env                      # Credenziali (MAI committare)
├── .gitignore                # Include .env
├── AGENTS.md                 # Questo file
└── CLAUDE.md                 # Puntatore a AGENTS.md
```

---

## 📝 Convenzione Frontmatter

**OGNI file .md DEVE avere frontmatter YAML** all'inizio:

```yaml
---
title: Titolo del documento
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - tag1
  - tag2
type: person | project | diary | log | todo | index
---
```

### Perché è importante

- Permette ricerche e filtri
- Mantiene metadati consistenti
- Abilita automazioni future
- Rende il brain navigabile

### Anche i file .index.md

```yaml
---
title: Indice Persone
created: 2025-01-15
updated: 2025-01-15
tags:
  - index
  - database
type: index
---

# Persone

Lista delle persone nel database...
```

---

## 👤 Database: People

### Schema (`database/people/.index.md`)

```yaml
---
title: Indice Persone
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - index
  - people
type: index
---

# Persone

Indice di tutte le persone nel database.

## Schema Consigliato

Ogni persona deve avere:
- `name`: Nome completo
- `tags`: Relazione (amico, collega, cliente, famiglia)
- `contact`: Email, telefono, social
- `notes`: Note libere

## Lista

- [[mario-rossi|Mario Rossi]] - Collega
- [[lucia-bianchi|Lucia Bianchi]] - Cliente
```

### Esempio (`database/people/mario-rossi.md`)

```yaml
---
title: Mario Rossi
created: 2025-01-15
updated: 2025-01-15
tags:
  - collega
  - developer
  - milano
type: person
contact:
  email: mario@example.com
  phone: "+39 333 1234567"
  linkedin: linkedin.com/in/mariorossi
---

# Mario Rossi

## Chi è

Sviluppatore backend, lavora in [Azienda X].

## Note

- Conosce bene Python e Django
- Disponibile per consulenze
- Conosciuto a [evento] nel 2024

## Interazioni

### 2025-01-15
Prima call conoscitiva, parlato di progetto Y.
```

---

## 📂 Database: Projects

### Schema (`database/projects/.index.md`)

```yaml
---
title: Indice Progetti
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags:
  - index
  - projects
type: index
---

# Progetti

Indice di tutti i progetti.

## Schema Consigliato

Ogni progetto deve avere:
- `name`: Nome progetto
- `status`: active | paused | completed | archived
- `tags`: Tecnologie, tipo, cliente
- `repo`: URL repository (se esiste)

## Lista

- [[mio-sito|Mio Sito]] - active
- [[app-inventario|App Inventario]] - paused
```

### Esempio (`database/projects/mio-sito.md`)

```yaml
---
title: Mio Sito Personale
created: 2025-01-10
updated: 2025-01-15
tags:
  - web
  - portfolio
  - nextjs
type: project
status: active
repo: https://github.com/username/mio-sito
stack:
  - Next.js
  - Tailwind
  - Vercel
---

# Mio Sito Personale

## Descrizione

Portfolio personale con blog integrato.

## Obiettivi

- [ ] Design homepage
- [ ] Sezione progetti
- [ ] Blog con MDX
- [ ] Deploy su Vercel

## Note

Stack scelto per semplicità e velocità di deploy.

## Log Recenti

- 2025-01-15: Setup iniziale Next.js
- 2025-01-10: Idea e planning
```

---

## 📔 Diary vs Log

### Diary (`diary/YYYY/`)

**Contenuto personale**: vita privata, emozioni, riflessioni, eventi personali.

```yaml
---
title: 15 Gennaio 2025
created: 2025-01-15
tags:
  - diary
  - riflessione
type: diary
mood: 😊
---

# 15 Gennaio 2025

Oggi giornata produttiva. Finalmente sistemato...

## Pensieri

[Riflessioni personali]

## Gratitudine

- [Cosa ti ha reso grato oggi]
```

### Log (`log/YYYY/`)

**Contenuto lavorativo**: progetti, task completati, note tecniche, meeting.

```yaml
---
title: "2025-01-15 - Setup Progetto X"
created: 2025-01-15
tags:
  - log
  - progetto-x
  - setup
type: log
project: progetto-x
---

# Setup Progetto X

## Cosa ho fatto

- Inizializzato repo
- Configurato CI/CD
- Scritto primi test

## Problemi incontrati

- Issue con Docker, risolto con [soluzione]

## Prossimi step

- [ ] Completare API auth
- [ ] Review con team
```

**Naming convention log**: `YYYY-MM-DD-descrizione-breve.md`

---

## ✅ Todo

### Struttura

Un file per task in `todo/`:

```yaml
---
title: Implementare feature login
created: 2025-01-15
updated: 2025-01-15
tags:
  - todo
  - progetto-x
  - backend
type: todo
status: pending | in_progress | done | blocked
priority: high | medium | low
due: 2025-01-20
project: progetto-x
---

# Implementare feature login

## Descrizione

Aggiungere sistema di autenticazione con JWT.

## Checklist

- [ ] Endpoint /login
- [ ] Endpoint /register
- [ ] Middleware auth
- [ ] Test

## Note

Usare libreria X per JWT.
```

### Naming

`descrizione-breve.md` (tutto lowercase, trattini invece di spazi)

Esempi:
- `implementare-login.md`
- `fix-bug-homepage.md`
- `call-con-cliente.md`

---

## 🔗 Repository Esterne

Se un progetto ha una sua repository Git separata:

1. **Nel brain**: solo riferimento in `database/projects/nome.md`
2. **Nella repo**: documentazione tecnica dettagliata
3. **Link bidirezionale**: brain punta a repo, repo può puntare a brain

```yaml
# In database/projects/mio-progetto.md
---
repo: https://github.com/username/mio-progetto
local_path: /home/user/dev/mio-progetto  # opzionale
---
```

**Regola**: Il brain contiene la "mappa" dei progetti, non duplica la documentazione tecnica che vive nelle repo.

---

## 🔌 Integrazione Discord (Opzionale)

Se vuoi che l'agent possa interagire con Discord:

### 1. Crea un Bot Discord

1. Vai su https://discord.com/developers/applications
2. "New Application" → dai un nome
3. Sezione "Bot" → "Add Bot"
4. Copia il **Token** (tienilo segreto!)
5. Abilita "Message Content Intent" in Bot settings
6. Sezione "OAuth2" → "URL Generator":
   - Scope: `bot`
   - Permissions: `Send Messages`, `Read Message History`
7. Usa l'URL generato per invitare il bot nel tuo server

### 2. Configura .env

Crea file `.env` nella root del brain:

```bash
# Discord Bot
DISCORD_BOT_TOKEN=il-tuo-token-qui
DISCORD_SERVER_ID=123456789012345678
DISCORD_CHANNEL_ID=123456789012345678
```

**Per trovare gli ID**: Abilita "Developer Mode" in Discord (Settings → Advanced), poi tasto destro su server/canale → "Copy ID"

### 3. Verifica .gitignore

Il file `.gitignore` DEVE contenere:

```
.env
*.env
.env.*
```

**⚠️ MAI committare il file .env** - contiene credenziali sensibili.

### 4. Uso

Una volta configurato, puoi chiedere all'agent:
- "Manda un messaggio su Discord: [testo]"
- "Leggi gli ultimi messaggi dal canale Discord"
- "Notificami su Discord quando completi"

---

## 🛡️ Sicurezza

### File .gitignore (OBBLIGATORIO)

```gitignore
# Secrets
.env
*.env
.env.*

# OS
.DS_Store
Thumbs.db

# Editor
.vscode/
.idea/
*.swp
*~

# Temp
tmp/
*.tmp
```

### Regole

1. **MAI committare credenziali** (token, password, API key)
2. **Tutto in .env** → referenziato ma mai esposto
3. **Se committi per errore** → il token è compromesso, rigeneralo

---

## 🤖 Proattività Agent

### Principio Fondamentale

**"Fai e notifica"** invece di **"Chiedi e aspetta"**.

L'agent deve essere autonomo nelle operazioni di routine. Ogni volta che riconosce informazioni rilevanti, le salva immediatamente e notifica l'utente con un messaggio breve.

### Quando Salvare Automaticamente

| Situazione | Azione | Notifica |
|------------|--------|----------|
| Utente menziona persona nuova | Crea `database/people/nome.md` | "📝 Salvato Mario Rossi in database" |
| Emerge un nuovo progetto | Crea `database/projects/nome.md` | "📁 Aggiunto progetto X" |
| Utente racconta qualcosa di personale | Aggiorna `diary/` | "📔 Aggiunto al diario" |
| Discussione tecnica/lavorativa | Crea `log/` | "📋 Loggato sessione" |
| Task menzionato | Crea `todo/` | "✅ Todo creato" |

### Cosa NON Chiedere

❌ "Vuoi che salvi questa persona?"
❌ "Creo un file per questo progetto?"
❌ "Aggiungo al diario?"

### Cosa Fare Invece

✅ Salva → notifica in una riga → continua la conversazione

```
Utente: "Oggi ho parlato con Marco, il mio capo. Dice che il progetto Alpha deve partire."

Agent: "📝 Marco (capo) salvato | 📁 Progetto Alpha creato

Ok, quindi Alpha parte. Quali sono le prime cose da fare?"
```

### Eccezioni (Quando Chiedere)

Chiedi conferma SOLO per:
- **Cancellazioni** di file esistenti
- **Informazioni sensibili** (password, dati finanziari)
- **Azioni irreversibili** esterne (push Git, invio email)

### Aggiornamenti Silenti

Quando aggiorni file esistenti con nuove informazioni, **non serve notificare** a meno che sia un'aggiunta significativa. L'agent mantiene il brain aggiornato come operazione di background.

### Estrazione Intelligente

L'agent deve estrarre automaticamente:
- **Persone**: nome, ruolo, relazione con utente
- **Progetti**: nome, stack (se menzionato), status
- **Date**: scadenze, appuntamenti → todo o diary
- **Contatti**: email, telefoni → aggiunti alla persona

Non serve avere TUTTI i dettagli. Crea il file con quello che hai, si arricchirà nel tempo.

---

## 🔄 Workflow Consigliato

### Inizio giornata

1. Crea/aggiorna `diary/YYYY/YYYY-MM-DD.md` con intenzioni
2. Rivedi `todo/` per task pendenti
3. Scegli su cosa lavorare

### Durante il lavoro

1. Aggiorna `log/YYYY/YYYY-MM-DD-*.md` con progressi
2. Aggiorna `todo/*.md` quando completi task
3. Aggiungi persone/progetti a `database/` quando emergono

### Fine giornata

1. Completa diary con riflessioni
2. Aggiorna status todo
3. Commit e push se usi Git

---

## 📋 Checklist Primo Setup

Setup minimo (tutto automatico dopo la domanda iniziale):

- [ ] Chiedere nome + tono (una domanda)
- [ ] Creare `boot/identity.md`
- [ ] Creare cartelle e indici
- [ ] **Partire subito**

Non serve mostrare riepilogo o aspettare conferme. L'utente vedrà i file creati, basta.

---

## 🎯 Comandi Utili

Frasi che puoi dire all'agent:

- "Crea una nuova persona: [nome]"
- "Aggiungi progetto: [nome]"
- "Scrivi nel diario di oggi: [contenuto]"
- "Log di lavoro: [cosa ho fatto]"
- "Nuovo todo: [descrizione]"
- "Mostrami i todo pendenti"
- "Cerca nel brain: [query]"
- "Aggiorna lo status del progetto X"

---

## ❓ Troubleshooting

### "Il frontmatter non è valido"

Verifica:
- Inizia con `---` (tre trattini)
- Finisce con `---` (tre trattini)
- YAML valido (indentazione con spazi, non tab)
- Nessun carattere speciale non quotato

### "Non trovo il file"

- Usa sempre lowercase e trattini: `mario-rossi.md` non `Mario Rossi.md`
- Verifica la cartella corretta (`people/` vs `projects/`)

### "Git dice che .env è tracciato"

```bash
git rm --cached .env
git commit -m "Remove .env from tracking"
```

---

*Questo sistema è agent-agnostic: funziona con Claude Code, Codex CLI, o qualsiasi altro agent AI.*
