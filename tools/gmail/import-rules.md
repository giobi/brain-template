# Gmail Import Rules - Processing Guidelines

**LEGGI QUESTO FILE PRIMA DI OGNI IMPORT** per evitare di fare cazzate diverse ogni volta.

---

## 🎯 Obiettivo

Processare email Gmail e generare:
1. **Log file** (professionale): progetti, clienti, lavoro, tech
2. **Diary file** (personale): vita privata, emozioni, eventi, riflessioni

Con **massimo dettaglio possibile**, non riassunti compact a meno che esplicitamente richiesto.

---

## 🚫 Script Policy

**Regola ferrea**: Script esterni per processing vanno tenuti SOLO se hanno **trade-off estremamente positivo di efficienza** (10x+ risparmio tempo/token).

### Metodo Ufficiale

**Claude Direct Processing**: Claude legge JSON email e genera markdown direttamente in sessione.

- ✅ **Download**: curl diretto Gmail API → `/tmp/YYYY-MM-emails.json`
- ✅ **Processing**: Claude legge JSON con Read tool e genera markdown
- ❌ **NO Gemini API**, **NO Circus**, **NO Python scripts**, **NO external tools**

### Script Eliminati

**`import-emails.py`** (2025-10-28): curl fa la stessa cosa, no beneficio
**`process-month.py`** (2025-10-28): usava Gemini, contraddice metodo ufficiale

### Quando Aggiungere Script

Considera uno script SOLO se:
1. **Efficienza 10x+**: risparmio massiccio tempo/token
2. **Non sostituibile**: impossibile con tool esistenti
3. **Allineato**: non contraddice Claude direct processing
4. **Documentato**: trade-off spiegato in `tools/gmail/index.md`

**Vedi**: `tools/gmail/index.md` per dettagli completi script policy

---

## 📁 Struttura File

### Naming Convention

**File mensili**:
```
log/YYYY/YYYY-MM-gmail-log.md
diary/YYYY/YYYY-MM-gmail-diary.md
```

**File conversazioni importanti** (quando una conversazione/progetto merita file dedicato):
```
log/YYYY/YYYY-MM-DD-topic-name.md
diary/YYYY/YYYY-MM-DD-event-name.md
```

**Esempi**:
- `log/2017/2017-07-sammontana-b2b-project.md` - Progetto Sammontana che dura tutto luglio
- `diary/2017/2017-04-sardegna-is-molas.md` - Acquisto/gestione proprietà Sardegna
- `log/2017/2017-10-meti-employment.md` - Cambio da freelance a employee METI

### Quando creare file dedicato?

**Criteri**:
1. **Thread lungo** (10+ email IMPORTANT nello stesso thread)
2. **Evento significativo** (nuovo cliente grosso, cambio lavoro, progetto importante)
3. **Conversazione complessa** che nel file mensile sarebbe dispersiva
4. **Milestone professionale/personale** che merita focus

**NON creare** file dedicato per:
- Thread corti (< 5 email)
- Conversazioni banali/amministrative
- Email singole anche se IMPORTANT

---

## 🔍 Processing Method

### Step 1: Analisi Mese

Prima di processare, leggi il JSON completo del mese e identifica:

1. **Email IMPORTANT** (labelIds contiene "IMPORTANT")
2. **Thread lunghi** (stesso subject, multiple email)
3. **Stakeholders ricorrenti** (persone/aziende che appaiono 5+ volte)
4. **Eventi chiave** (primi contatti, chiusure progetti, milestone)

### Step 2: Decisione Struttura

**Opzione A - File mensile unico** (default):
- Mese con < 300 email
- Nessun thread particolarmente lungo
- Attività variegata senza focus specifico

**Opzione B - File mensile + file dedicati**:
- Mese con eventi importanti (nuovo cliente, progetto grosso, vita personale)
- Thread 10+ email sullo stesso topic
- Milestone professionali (cambio lavoro, nuova azienda)

### Step 3: Processing Dettagliato

**NON usare "compact" o "summary" a meno che esplicitamente richiesto.**

**Per ogni email IMPORTANT**:
1. Estrai: data, from, to, subject, snippet (prime righe body se disponibile)
2. Ricostruisci contesto: cosa sta succedendo?
3. Identifica: progetto, cliente, tipo attività
4. Annota: sentiment, urgenza, outcome

**Per thread (multiple email stesso subject)**:
1. Raggruppa tutte le email del thread
2. Ricostruisci timeline completa
3. Estrai decisioni prese, outcome, next steps

### Step 4: Struttura Log File

```markdown
# Gmail Log - [Mese] YYYY

**Periodo**: 1-31 [mese] YYYY
**Fonte**: Gmail API import
**Email totali**: XXX
**IMPORTANT**: YYY (ZZ%)
**Metodo**: Claude direct processing

---

## 📊 Overview

[Paragrafo riassuntivo del mese: cosa è successo in generale]

---

## 🏢 Progetti Principali

### [Nome Progetto/Cliente]

**Periodo**: [date range]
**Thread**: "[Subject principale]" (IMPORTANT)
**Stakeholders**: [nomi persone coinvolte]

**Timeline**:
- **[data]** - [evento]
- **[data]** - [evento]

**Attività**:
- [cosa è stato fatto]
- [deliverable]
- [outcome]

**Contesto**: [spiegazione cosa significa questo progetto]

**Tag**: #project-name #client-name #tech-used

---

## 💼 Nuovi Contatti

### [Nome Persona/Azienda]

**Data**: [primo contatto]
**Email**: [indirizzo]
**Subject**: "[oggetto prima email]"

**Contesto**: [chi è, perché contatto, cosa vuole]

**Tag**: #contact-name #company-name

---

## 📧 Thread Significativi

[Per conversazioni che non rientrano in progetti ma sono importanti]

---

## 🔗 Collegamenti

### Aziende
- [[database/companies/nome-azienda|Nome Azienda]]

### Persone
- [[database/people/nome-persona|Nome Persona]]

### Progetti
- [[database/projects/nome-progetto|Nome Progetto]]

---

*Generato automaticamente da Gmail API - Claude Direct Processing*
```

### Step 5: Struttura Diary File

```markdown
# Diary - [Mese] YYYY

**Periodo**: 1-31 [mese] YYYY
**Fonte**: Gmail API import
**Email**: XXX totali
**Focus**: [tema principale del mese]

---

## 📅 Eventi Chiave

### [Titolo Evento]

**Data/Periodo**: [quando]

[Narrazione in prima persona di cosa è successo]

**Significato personale**: [riflessione su cosa significa per Giobi]

**Emozione**: [come si è sentito]

---

## 💭 Riflessioni [Periodo/Tema]

[Riflessioni più ampie su pattern del mese]

**Pattern**: [cosa emerge guardando il mese intero]

**Crescita**: [come è cambiato/evoluto]

**Identità**: [impatto su chi è Giobi]

---

## 📊 Metriche Personali

- **Email**: XXX
- **IMPORTANT**: YYY (ZZ%)
- **Nuovi contatti**: N
- **Progetti attivi**: N
- **Mood generale**: [keyword mood]

---

*Generato automaticamente da Gmail API - Claude Direct Processing*
```

---

## 🎨 Stile e Tono

### Log File (Professionale)

- **Tono**: Neutro, professionale, fattuale
- **Focus**: Cosa, chi, quando, deliverable, outcome
- **Linguaggio**: Tecnico quando appropriato
- **Struttura**: Timeline cronologica, raggruppata per progetto/cliente

### Diary File (Personale)

- **Tono**: Narrativo, riflessivo, emotivo
- **Focus**: Perché, significato, emozioni, impatto personale
- **Linguaggio**: Colloquiale, prima persona, espressivo
- **Struttura**: Tematica, per eventi significativi

---

## 📊 Volume Processing Guidelines

### Mese piccolo (< 150 email)
- Processing completo, ogni email IMPORTANT analizzata
- File mensile unico sufficiente
- Dettaglio massimo

### Mese medio (150-300 email)
- Processing dettagliato email IMPORTANT
- Grouping per thread/progetto
- File mensile + file dedicati se thread lunghi

### Mese grande (300+ email)
- Processing in batch di 50 email
- Focus su IMPORTANT + thread significativi
- File mensile + multipli file dedicati per progetti/eventi chiave
- Considera split se ci sono progetti intensi

**REGOLA**: Mai saltare dettagli per risparmiare token. Se il mese è grosso, crea file multipli invece di fare summary.

---

## 🔗 Wikilinks e Database

### Quando creare entity in database/

**Persone** (`database/people/nome-cognome.md`):
- Appare in 3+ email IMPORTANT
- O è stakeholder chiave anche se 1-2 email

**Aziende** (`database/companies/nome-azienda.md`):
- Cliente/fornitore ricorrente
- O progetto significativo anche se breve

**Progetti** (`database/projects/nome-progetto.md`):
- Solo progetti SENZA repo GitHub
- O progetti che meritano documentazione cross-anno

### Wikilink Usage

**Sempre usare wikilinks** per referenziare:
- Persone: `[[database/people/paolo-sappino|Paolo Sappino]]`
- Aziende: `[[database/companies/digitag|DIGITAG]]`
- Progetti: `[[database/projects/food-truckers|Food Truckers Italia]]`

**Anche usare hashtag** per tagging (Obsidian auto-link):
- `#company-digitag`
- `#project-sammontana`
- `#person-diego-dotari`

---

## ⚠️ Errori Comuni da Evitare

### ❌ SBAGLIATO

1. **"Compact summary"** senza richiesta esplicita
   - Non fare mai riassunti per risparmiare token
   - Se il volume è grosso, splitta in file multipli

2. **Naming ambiguo**: `2017-03-12-gmail-log.md`
   - Sembra "12 marzo" invece è "marzo-dicembre"
   - Usa `2017-03-gmail-log.md` per mese singolo
   - Usa `2017-03-15-topic.md` per evento specifico del 15 marzo

3. **Mixare log e diary**
   - Log = professionale, diary = personale
   - Non mescolare i due toni/contenuti

4. **Perdere contesto**
   - Ogni email IMPORTANT deve avere contesto spiegato
   - Non dare per scontato che il lettore conosca i progetti

5. **Ignorare thread**
   - Email multiple stesso subject = ricostruire conversazione intera
   - Non trattare come email separate

### ✅ CORRETTO

1. **Dettaglio completo** anche se costa token
2. **Naming chiaro**: mese = `YYYY-MM-`, evento specifico = `YYYY-MM-DD-`
3. **Separazione log/diary** rigorosa
4. **Contesto sempre presente** per ogni email/thread
5. **Thread ricostruiti** come conversazioni complete

---

## 🔄 Workflow Completo

```bash
# 1. Download email JSON (se non già fatto)
curl "https://gmail.googleapis.com/gmail/v1/users/me/messages?..." > /tmp/YYYY-MM-emails.json

# 2. Analisi preliminare
# - Leggere JSON completo
# - Contare IMPORTANT
# - Identificare thread lunghi
# - Identificare stakeholders ricorrenti

# 3. Decisione struttura
# - File mensile unico?
# - File mensile + file dedicati?
# - Quali file dedicati creare?

# 4. Processing
# - Creare log file (professionale)
# - Creare diary file (personale)
# - Creare file dedicati se necessario

# 5. Database entities
# - Creare/aggiornare database/people/
# - Creare/aggiornare database/companies/
# - Creare/aggiornare database/projects/

# 6. Git
# - Stage tutti i file creati
# - Commit descrittivo
# - Push
```

---

## 📋 Checklist Pre-Processing

Prima di processare un mese, verifica:

- [ ] Ho letto questo file `import-rules.md`?
- [ ] Ho il JSON completo del mese?
- [ ] Ho fatto analisi preliminare (IMPORTANT, thread, stakeholders)?
- [ ] Ho deciso la struttura (file unico vs multipli)?
- [ ] Ho chiaro il tono (log = professionale, diary = personale)?
- [ ] Sto usando naming corretto (`YYYY-MM-` vs `YYYY-MM-DD-`)?
- [ ] Sto usando dettaglio completo (NO compact a meno che richiesto)?

---

**Ultima modifica**: 2025-10-28 (dopo cazzata marzo-dicembre compact)
**Motivo**: Evitare di fare metodi diversi ogni volta e perdere dettaglio
