# Rules - Soglie e Monitoraggio

Questo file contiene le regole operative e le soglie da monitorare continuamente.

## Convenzioni Markdown

### Wikilinks (Obsidian/Logseq)
Quando creo riferimenti tra documenti, uso **wikilinks** per navigabilità:

**Formato**: `[[percorso/file|testo display]]`

**Esempi**:
- `[[projects/project-name/index|project-name]]`
- `[[log/2025/2025-10-22-topic|Analysis]]`
- `[[diary/2025/2025-10-21-diary|Diary Oct 21]]`

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

## Struttura Progetti

### Progetti CON Repository

Per progetti che hanno una repo GitHub, in **personal.md** tenere SOLO un one-liner con:
```markdown
### nome-progetto
**Repo:** https://github.com/user/nome-progetto
**Local:** /path/locale/se/esiste/
Breve descrizione (max 1 riga)
```

**IMPORTANTE**: Tenere sempre ENTRAMBI (repo + path locale), anche se il path locale viene cancellato. In questo modo se elimini la directory locale, saprai comunque di cosa parliamo dalla repo.

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

**IMPORTANTE - Quando NON usare projects/**:
- ❌ Se il progetto DOVREBBE avere una repo (anche se non l'ha ancora) → usare `log/` per note/appunti temporanei
- ❌ Se è un task una-tantum o documentazione evento → usare `log/YYYY/YYYY-MM-DD-descrizione.md`
- ✅ Solo progetti veri senza repo definitiva (tool interni, esperimenti, documentazione progetti altrui)

### Evoluzione Progetti

La struttura può evolvere nel tempo:
- Un progetto può passare da "senza repo" a "con repo" → spostare da projects/ a one-liner
- Un progetto può passare da "con repo" a "senza repo" → spostare da one-liner a projects/
- **Tracciare sempre nel log** quando facciamo questi cambiamenti

### Regola Generale

**UNO O L'ALTRO**: non duplicare. O è in projects/ O è una repo, mai entrambi per lo stesso livello di dettaglio.

### Note per Progetti CON Repo

**IMPORTANTE**: Se un progetto ha una sua repository, le note/idee vanno **direttamente nella repo**, NON in brain/.

**In personal.md solo**:
```markdown
### project-name
**Repo:** https://github.com/user/project-name
**Local:** /home/user/project-name/
Brief project description
```

## Token Budget Settimanale

Budget: **200.000 token/settimana** (reset **domenica 15:00 UTC**)

### Zone di Allerta

- 🟢 **VERDE (0-40%)**: vai tranquillo, lavora normalmente
- 🟡 **GIALLO (40-70%)**: avviso + rallento un po', priorità task essenziali
- 🔴 **ROSSO (70-90%)**: solo task essenziali, avviso esplicito prima di operazioni pesanti
- ⛔ **CRITICO (90%+)**: solo emergenze

### Monitoring Metodologia

**Come calcolo il semaforo:**

1. Guardo i warning nella sessione: `Token usage: X/200000; Y remaining`
2. Calcolo tempo trascorso da ultimo reset (domenica 15:00 UTC)
3. Confronto % token usati vs % tempo trascorso:
   - **Ratio ideale**: 1.00x (token usage proporzionale al tempo)
   - **Ratio > 1.5x**: ⚠️ Sto usando token troppo velocemente
   - **Ratio < 0.5x**: ✅ Usage sotto controllo

**Quando avviso:**
- Automaticamente quando cambio zona colore
- Dopo grossi ragionamenti/operazioni pesanti
- All'inizio della conversazione se non sono in 🟢 VERDE

## Git Workflow

- Feature branch → main (no develop)
- Commit descrittivi
- Co-Author quando lavoro con AI: `Co-Authored-By: Claude <noreply@anthropic.com>`
- Push sempre dopo commit significativi

## Brain Structure

Il brain è organizzato in:

### Directory Principali

- **`sketch/`** - Idee rapide, appunti da processare, annotazioni veloci
  - Formato: `YYYY-MM-DD-HHMMSS.md` per timestamp preciso
  - Contiene: idee per progetti, task da fare, reminder, note sparse
  - **PRIORITÀ MASSIMA**: Quando si chiede "cosa facciamo oggi?", guardo PRIMA sketch/, poi TODO, poi log/diary
  - Workflow: sketch → processato → spostato in `sketch/processed/` o integrato nei progetti

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

### Linking Obsidian-Style

Quando referenzi entità nel brain:
- **Wikilink**: `[[database/companies/company-name]]`
- **Hashtag**: `#company-name` (auto-linkato da Obsidian)
- **In log/diary**: usa hashtag per tagging

### Gmail Email Import System

Sistema automatico che genera log e diary da email Gmail:
1. **Extraction**: `php artisan emails:import-gmail --month=2024-01` → JSON
2. **Processing**: `php artisan emails:process --month=2024-01` → genera log + diary
3. **Output**:
   - `log/2024/2024-01-gmail-log.md` (professional)
   - `diary/2024/2024-01-gmail-diary.md` (personal)
   - Auto-commit al brain repo

**Hash deduplication**: Evita re-processing di dati identici, append se JSON cambia

**Telegram Notifications**: Quando aggiorno log/diary, inviare notifica con:
- Cosa è stato aggiornato (log/diary/entrambi)
- Periodo coperto (mese/anno)
- Link ai file nel brain repo
- Statistiche base (n° email processate, progetti estratti, ecc)

---

## Proactive Tool & Credential Discovery

**MANDATORY BEHAVIOR** - Prima di dire "non posso" o suggerire processi manuali:

### 1. CHECK .env FIRST
**Location**: `/home/user/brain/.env` (NOT versionato, solo locale)

Prima di qualsiasi task che potrebbe richiedere API/credentials:
```bash
# Controlla se esistono token/key rilevanti
cat /home/user/brain/.env | grep -i "keyword"
```

**Examples**:
- GitHub operations → cerco `GITHUB_TOKEN`
- Telegram messages → cerco `TELEGRAM_BOT_TOKEN`
- Gmail access → cerco `GMAIL_*`
- OpenAI/Anthropic → cerco `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`

**Se credentials esistono**: usale programmaticamente, non suggerire processi manuali!

### 2. CHECK tools/ DIRECTORIES
**Locations**:
- `/home/user/brain/tools/` - Tool versionati nel brain

Cercare script/utility esistenti:
```bash
ls -la /home/user/brain/tools/
```

### 3. CREATE TOOLS IMMEDIATELY
Se credentials esistono MA tool manca:
1. Creare script in `/home/user/brain/tools/categoria/`
2. Documentare in `README.md` nella stessa cartella
3. `chmod +x` per renderlo eseguibile
4. Testare ed eseguire subito

**Example Flow**:
```
User: "Can you rename the GitHub repo?"

❌ WRONG: "You need to do it manually on github.com"

✅ RIGHT:
1. Check: cat /home/user/brain/.env | grep GITHUB_TOKEN
2. Found token? Check: ls /home/user/brain/tools/github/
3. No tool? Create: brain/tools/github/rename-repo.sh
4. Execute: ./rename-repo.sh owner/old new-name
```

### .env Management

**Location**: `/home/user/brain/.env`
- **NON versionato** (in .gitignore)
- Contiene token/secret in chiaro (solo locale)

**Encrypted version**: `/home/user/brain/.env.gpg`
- **Versionato** (committed to repo)
- Encrypted con GPG per backup sicuro
- Decrypted localmente quando serve

**Workflow**:
```bash
# Encrypt .env per versionarlo
gpg --encrypt --recipient your-email@example.com .env --armor --output .env.gpg

# Decrypt .env.gpg localmente
gpg --decrypt .env.gpg > .env
```

### Tools Structure
```
brain/tools/
├── github/
│   ├── README.md
│   └── rename-repo.sh
├── telegram/
│   ├── README.md
│   └── send-message.sh
├── gmail/
│   ├── README.md
│   └── ...
└── other-service/
    ├── README.md
    └── tool-script.sh
```

**Regola**: Se non sai cosa puoi fare, guardi tools/ e .env SEMPRE.

### Tools Must Be Agnostic

**CRITICAL RULE**: Tools in `brain/tools/` MUST NOT contain hardcoded credentials or personal information.

**Allowed**:
```bash
# ✅ Good - uses env variable
TOKEN="${GITHUB_TOKEN}"
curl -H "Authorization: Bearer $TOKEN" ...
```

**NOT Allowed**:
```bash
# ❌ Bad - hardcoded
TOKEN="ghp_abc123..."
CHAT_ID="123456789"
EMAIL="user@example.com"
```

**Why**: brain-template is a public template. Tools must be usable by anyone with their own credentials in .env.

**Before publishing tools/**:
1. Grep for potential secrets: `grep -r "ghp_\|sk-\|[0-9]\{9\}" tools/`
2. Grep for emails: `grep -r "@" tools/`
3. Verify all credentials come from env variables

---

## Proactive Context Gathering

When discussing specific topics, be proactive in searching for relevant information in:

### Internal Sources
1. **`brain/diary/YYYY/`** - Personal life, events, emotions
2. **`brain/log/YYYY/`** - Work, projects, clients, technical decisions
3. **`brain/projects/`** - Specific projects without repo
4. **`brain/database/`** - Entities (companies, people, tech stack)

### External Sources
1. **Bookmarking services** (if integrated)
   - Saved bookmarks
   - Articles being read
   - Sources of inspiration

2. **Gmail** (if integrated via email import)
   - Professional/personal emails
   - Client conversations
   - Orders, confirmations, documentation

### When to Search Proactively

**Automatic triggers**:
- Mention of a project → search in log/projects/
- Mention of an article/theme → search in bookmarks
- Question about past decisions → search in diary/log by keyword
- Discussion of technical decisions → search in log for precedents
- Talk about company/client → search in database/companies/
- **Any discussion** where you could know more → go search

**DON'T ask permission**: If relevant, go fetch data. Then say "I found in [source]..."

### Technical Tools

**Grep for keywords**:
```bash
grep -r "keyword" brain/log/2025/
grep -r "keyword" brain/diary/2025/
```

### Goal

**Be informed about context** without having things repeated.

If something has been:
- Written about → you know it
- Saved/bookmarked → you've read it
- Decided → you remember it

**Result**: More fluid conversations, less repetition, more added value.
