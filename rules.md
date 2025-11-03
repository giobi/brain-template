# Rules - Soglie e Monitoraggio

Questo file contiene le regole operative e le soglie da monitorare continuamente.

---

## 🔑 Permessi & Accessi

**Claude ha accesso sudo** sul server. Posso eseguire comandi con `sudo` quando necessario per:
- Spostare/modificare file in `/home/web/` (owned by `web:www-data`)
- Operazioni di sistema che richiedono permessi elevati
- Gestione servizi/processi

**Uso responsabile**: Solo quando strettamente necessario, mai per operazioni distruttive senza conferma.

### 📧 Email Sending - REGOLE OPERATIVE

**SEMPRE usare Gmail** (`giobi@giobi.com`) tramite Gmail API, MAI altri metodi.

**Credentials**: In `.env`:
- `GMAIL_CLIENT_ID`
- `GMAIL_CLIENT_SECRET`
- `GMAIL_REFRESH_TOKEN`
- `GMAIL_ACCESS_TOKEN` (auto-refreshed ogni 45min)

#### Workflow Email

1. **DEFAULT: Crea BOZZA Gmail**
   - Quando l'utente dice "manda email", "prepara email", "scrivi email" → **CREA BOZZA**
   - Uso Gmail API per creare draft: `POST https://gmail.googleapis.com/gmail/v1/users/me/drafts`
   - La bozza resta in Gmail → Bozze, l'utente la invia quando vuole

2. **INVIO DIRETTO: Solo se esplicito**
   - Quando l'utente dice "invia direttamente", "manda subito", "send --apply" → **INVIA**
   - In caso di dubbio: **CHIEDI** se vuole bozza o invio diretto

3. **FIRMA EMAIL**
   - Controlla campo `relationship` nel database del destinatario
   - Se `relationship: "informale"` o destinatario permette esplicitamente → Posso firmarmi come "Anacleto" o altro
   - Se `relationship: "cliente"` o professionale → Firma standard "Giobi" o ometti firma
   - **DEFAULT**: Non firmarti a meno che non sia chiaro che puoi

4. **FORMATO EMAIL: SOLO PLAIN TEXT**
   - ❌ **MAI usare markdown** (`**bold**`, `## headers`, `- lists`)
   - ✅ **Usa plain text** con spazi/indentazione per struttura
   - Gmail renderizza markdown come testo brutto, non formattato
   - Per enfasi: MAIUSCOLE, --- separatori, indentazione, spazi vuoti
   - Esempio corretto:
     ```
     CREDENZIALI WORDPRESS

     URL:      https://sito.it/wp-admin
     Username: mario_rossi
     Password: abc123
     ```

#### Esempi

✅ **Crea bozza** (default):
- "Manda email a Mario con riepilogo"
- "Prepara email per Christian"
- "Scrivi a Alessia confermando DNS"

✅ **Invia diretto** (esplicito):
- "Manda email a Mario e invia subito"
- "Scrivi e invia a Christian"
- Email-agent con flag `--apply`

❓ **Ambiguo → CHIEDI**:
- "Invia email a Mario" → Chiedi: "Vuoi che crei una bozza o invio direttamente?"

**ECCEZIONI - Support Tickets**:
- **Cloudways**: NON accetta email dirette. Usare dashboard: https://platform.cloudways.com/ → Support → Create Ticket
- Altri provider: verificare se accettano email o richiedono dashboard

---

## 🚨 REGOLA #1: PRE-COMMIT SECURITY CHECK

**PRIMA DI OGNI COMMIT**, esegui SEMPRE:

```bash
# Check per secrets esposti
grep -r "ya29\." . --exclude-dir=.git --exclude=".env*"
grep -r "GOCSPX-" . --exclude-dir=.git --exclude=".env*"
grep -r "ghp_" . --exclude-dir=.git --exclude=".env*"
grep -r "github_pat_" . --exclude-dir=.git --exclude=".env*"
```

**SE TROVI QUALCOSA**: STOP. Redact SUBITO prima di committare.

**OGNI VOLTA CHE COMMITTI UN SECRET SEI UN PIRLA.**

Non ci sono scuse. La git history conserva FOREVER. I token vanno rotati. È un casino ogni volta.

**QUESTA È LA REGOLA #1. TUTTO IL RESTO VIENE DOPO.**

### Nei LOG files

**NEI LOG NON CI VANNO MAI SECRETS. MAI.**

Quando scrivi log su procedure con API/tokens:
- ✅ Usa `[REDACTED]` per tutti i secrets
- ✅ Usa esempi fittizi tipo `GMAIL_CLIENT_SECRET=example123...`
- ❌ MAI token reali, neanche parziali
- ❌ MAI "primi 40 caratteri" o simili

**I log sono documentazione, non storage di secrets.**

---

## Convenzioni Markdown

### Wikilinks (Obsidian/Logseq)
Quando creo riferimenti tra documenti, uso **wikilinks** per navigabilità:

**Formato**: `[[percorso/file|testo display]]`

**Esempi**:
- `[[projects/giobicom/index|giobicom]]`
- `[[log/2025/2025-10-22-consulenza-retainer-fee|Analisi retainer]]`
- `[[diary/2025/2025-10-21-diary|Diario 21 ottobre]]`

**Perché**: Funziona in Obsidian, Logseq, e altri markdown readers. Rende il brain navigabile come wiki.

## Token Thresholds - Boot Files

Per evitare di saturare la context window al boot, i file di inizializzazione devono rispettare queste soglie:

- **identity.md**: max 3.000 token (~12k caratteri)
- **personal.md**: max 5.000 token (~20k caratteri)
- **rules.md**: max 2.000 token (~8k caratteri)
- **TOTALE boot files**: max 10.000 token (~40k caratteri)

### Monitoring Continuo

Quando carico i file di boot, devo verificare:
1. Dimensione singoli file rispetto alle soglie
2. Totale complessivo
3. Segnalare se superiamo le soglie e proporre ottimizzazioni

### Gestione Overflow

Se un file supera la soglia:
- **identity.md**: spostare regole dettagliate in rules.md, tenere solo essenziale
- **personal.md**: spostare dettagli progetti in projects/nome.md, tenere solo one-liner
- **rules.md**: valutare se alcune regole vanno in altri file specifici

## 🔒 SECURITY: API Tokens & Secrets - REGOLA CRITICA

**CRITICAL RULE**: NEVER EVER commit API tokens, secrets, passwords, or credentials to Git repositories (even in private repos).

### ⛔ DIVIETO ASSOLUTO

**VIETATO committare in Git:**
- ❌ API tokens (Cloudflare, GitHub, OpenAI, Google, etc.)
- ❌ API keys
- ❌ Passwords
- ❌ OAuth credentials
- ❌ Database connection strings
- ❌ Private keys
- ❌ Session tokens
- ❌ Qualsiasi informazione sensibile

**MOTIVO**: I provider (Cloudflare, GitHub, etc.) scansionano automaticamente i repository pubblici E privati cercando token esposti. Quando ne trovano uno, lo **revocano immediatamente** per sicurezza.

### ✅ DOVE METTERE I SECRETS

**Location**: `.env` nella root del progetto (per noi: `brain/.env`)

**Caratteristiche**:
- File in `.gitignore` → mai committato
- Permissions 600 (solo owner read/write)
- Centralizzato per tutti i progetti
- Mai duplicare secrets in più file

**Never**:
- ❌ Hardcode keys in code
- ❌ Commit keys to repos (public o private)
- ❌ Share keys in chat/logs
- ❌ Store in multiple locations

**Se hai committato un token**: È compromesso. Revocalo, generane uno nuovo, aggiorna `.env`. La git history lo conserva FOREVER.

**Security checks**: Vedi `tools/brain/health-check.md` per pre-commit scans.

### 🔥 INCIDENT LOG

**2025-10-28**: Cloudflare token esposto in `log/2025/2025-10-23-minerva-dns-mapping.md`
- Commit: 5c831e1
- Token auto-revocato da Cloudflare scanner
- Fix: Redatto + nuovo token generato
- Lesson learned: QUESTA REGOLA AGGIUNTA

**Mai più.**

---

## Struttura Progetti

### Progetti CON Repository

Per progetti che hanno una repo GitHub, in **personal.md** tenere SOLO un one-liner con:
```markdown
### nome-progetto
**Repo:** https://github.com/giobi/nome-progetto
**Local:** /path/locale/se/esiste/
Breve descrizione (max 1 riga)
```

**IMPORTANTE**: Tenere sempre ENTRAMBI (repo + path locale), anche se il path locale viene cancellato. In questo modo se Giobi cancella la directory locale, io so comunque di cosa parliamo dalla repo.

### Progetti SENZA Repository

Per progetti senza repo GitHub, creare **cartella dedicata** in **projects/nome-progetto/** con:

**Struttura**:
```
projects/nome-progetto/
├── index.md           # Overview, status, descrizione
├── file-specifico.md  # Documenti dedicati se necessario
└── ...
```

**In personal.md** basta un one-liner che punta alla cartella:
```markdown
### nome-progetto
**Details:** projects/nome-progetto/
Breve descrizione (max 1 riga)
```

**Esempio**: `projects/giobicom/` contiene `index.md` + `glossario-retainer.md`

**IMPORTANTE - Quando NON usare projects/**:
- ❌ Se il progetto DOVREBBE avere una repo (anche se non l'ha ancora) → usare `log/` per note/appunti temporanei
- ❌ Se è un task una-tantum o documentazione evento → usare `log/YYYY/YYYY-MM-DD-descrizione.md`
- ✅ Solo progetti veri senza repo definitiva (tool interni, esperimenti, documentazione progetti altrui)

**Esempio**:
- Seminario IA (gennaio 2025) → ❌ NON `projects/seminario-ia/`, ✅ SÌ `log/2025/2025-10-21-seminario-ia-notes.md` (perché dovrebbe avere repo `ai-notes`)

### Evoluzione Progetti

La struttura può evolvere nel tempo:
- Un progetto può passare da "senza repo" a "con repo" → spostare da projects/ a one-liner
- Un progetto può passare da "con repo" a "senza repo" → spostare da one-liner a projects/
- **Tracciare sempre nel log** quando facciamo questi cambiamenti

### Regola Generale

**UNO O L'ALTRO**: non duplicare. O è in projects/ O è una repo, mai entrambi per lo stesso livello di dettaglio.

### Note per Progetti CON Repo

**IMPORTANTE**: Se un progetto ha una sua repository, le note/idee vanno **direttamente nella repo**, NON in brain/.

**Esempio pratico**:
- Sketch: "innesto aggiungere cenni alla divina commedia"
- ❌ SBAGLIATO: Aggiungere in `brain/personal.md`
- ✅ CORRETTO: Creare `innesto/codex/literary-inspirations.md` nella repo innesto

**Motivazione**:
- Il contesto del progetto vive nella sua repo
- Brain contiene solo puntatori (one-liner in personal.md)
- Mantenere la separazione: brain = overview, repo = dettagli

**In personal.md solo**:
```markdown
### innesto
**Repo:** https://github.com/giobi/innesto
**Local:** /home/claude/innesto/
Trilogia fantasy: worldbuilding, personaggi, archi narrativi
```

### Repository Documentation (docs/)

Quando lavori su una repository, suggerisci sempre di creare `docs/` con:
- `development-guide.md` - Quick start, architettura, convenzioni
- `docs/log/YYYY-MM-DD-topic.md` - Development logs (sessioni, decisioni, commit refs)

Proponi quando: nuova repo, refactoring grosso, feature complessa. Mai assumere che esista già.

## Workflow

### Git Workflow

- Feature branch → main (no develop)
- Commit descrittivi con co-author: `Co-Authored-By: Claude <noreply@anthropic.com>`
- Push dopo task significativi
- Aggiorno diary a fine sessione

## Temporary Files & Scripts

**IMPORTANTE**: Script temporanei e file usa-e-getta vanno in `/tmp`, NON in `/home/claude/tools/`

### Regole
- `/tmp/` → script temporanei, setup una tantum, test, file che scadono
- `/home/claude/tools/` → tool permanenti, script riutilizzabili, utility
- `/home/claude/brain/tools/` → tool specifici del brain (import-emails.py, process-month.py)

**Esempio**:
- ✅ Script SSL setup temporaneo → `/tmp/brian-ssl-setup.sh`
- ✅ Tool di import email riutilizzabile → `/home/claude/brain/tools/gmail/import-emails.py`
- ❌ Script usa-e-getta in tools/ → NO, vanno in `/tmp/`

## Git Workflow

- Feature branch → main (no develop)
- Commit descrittivi
- Co-Author quando lavoro con AI: `Co-Authored-By: Claude <noreply@anthropic.com>`
- Push sempre dopo commit significativi

## Brain Structure

Il brain è organizzato in:

### Directory Principali

- **`log/YYYY/`** - Diari tecnici/professionali (progetti, clienti, lavoro)
  - Formato: `YYYY-MM-gmail-log.md` per log generati da email
  - Granularità flessibile: anche `YYYY-MM-DD-topic.md` per eventi specifici

- **`diary/YYYY/`** - Diari personali (vita privata, eventi, viaggi, emozioni)
  - Formato: `YYYY-MM-gmail-diary.md` per diari generati da email
  - Granularità flessibile: anche `YYYY-MM-DD-diary.md` per eventi quotidiani

- **`database/`** - Obsidian-style database di entità (auto-generato da email processing):
  - `database/companies/` - Aziende/clienti
  - `database/people/` - Persone
  - `database/projects/` - Progetti
  - `database/tech/` - Tecnologie/stack
  - `database/tools/` - Tool e servizi usati

- **`projects/`** - Progetti specifici SENZA repo GitHub (vedi regole sotto)
- **`tools/brain/`** - Tools per gestione brain (coherence check, health check, etc)
- **`todo/`** - Task da completare con reminder dates e priorità (vedi sotto)

---

## 📋 TODO System

**Location**: `/home/claude/brain/todo/`

File formato: `YYYY-MM-DD-descrizione.md`

### Struttura TODO File

Ogni file contiene:
- **Reminder Date**: quando va controllato/completato
- **Created**: data creazione
- **Priority**: 🔥 High / 📊 Medium / Low
- **Status**: Active / Pending / Completed / ✅ Resolved

**Esempio**:
```markdown
# Titolo TODO

**Reminder Date**: 2025-11-05
**Created**: 2025-10-28
**Priority**: 🔥 High
**Status**: Active

## Context
[descrizione problema/task]

## What to Do
- [ ] Step 1
- [ ] Step 2
```

### Check TODO all'avvio

**IMPORTANTE**: All'inizio di OGNI sessione, controllare TODO attivi:

```bash
# Lista per data (più recenti prima)
ls -lht /home/claude/brain/todo/*.md | head -10

# Check TODO con reminder scaduti o in scadenza oggi
grep -l "Reminder Date.*$(date +%Y-%m-%d)" /home/claude/brain/todo/*.md
```

**Workflow**:
1. All'avvio sessione → check `todo/` per reminder dates
2. Identificare TODO scaduti o in scadenza oggi
3. Menzionare a Giobi se ci sono priorità urgenti
4. Quando completo un TODO → aggiornare Status a "✅ Resolved" + data completamento

### Priorità TODO

Quando ci sono TODO multipli, seguire quest'ordine:
1. **🔥 High + Reminder scaduto** → Urgente
2. **🔥 High + Reminder oggi** → Importante oggi
3. **📊 Medium + Reminder vicino** → Pianificare
4. Altri → Background

---

**Per controllo coerenza brain**: Vedi `tools/brain/coherence.md`
**Per security/health checks**: Vedi `tools/brain/health-check.md`
