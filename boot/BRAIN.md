# BRAIN.md — Il Protocollo Brain

**Versione**: 2.1 | **Ultimo aggiornamento**: 2026-03-03

Definisce cosa è un brain, come è strutturato, e come qualsiasi motore AI deve interagire con esso. Agnostico rispetto alla piattaforma.

---

## Cosa è un Brain

Un brain è un knowledge base personale. Non è il modello AI (quello è sostituibile), è la conoscenza accumulata dall'utente: decisioni, relazioni, progetti, appunti, log.

Il brain è portabile, owned dall'utente, e cresce con ogni interazione.

---

## File entry point della piattaforma

Ogni motore AI ha il suo file entry point nella root del brain: `CLAUDE.md`, `GEMINI.md`, ecc.

**Regola:** questi file sono **SOLO puntatori** a `boot/`. Zero contenuto proprio, zero regole duplicate. L'unica cosa che fanno è includere i file di boot nell'ordine corretto.

Esempio corretto:
```
# Brain di [Nome Utente]

@boot/brain.md
@boot/soul.md
@boot/identity.md
@boot/user.md
@boot/tools.md
```

Se servono regole specifiche per un motore, vanno in `boot/claude.md`, `boot/gemini.md`, ecc. — **mai** nel file entry point.

---

## Struttura cartelle

```
brain/
├── boot/           Sistema: identity, soul, user, tools, brain protocol
├── wiki/           Entità strutturate
│   ├── people/
│   ├── companies/
│   └── projects/
├── diary/YYYY/     Log temporale (cosa è successo quando)
├── todo/           Task aperti
├── inbox/          Roba in arrivo da processare
├── public/         File pubblicati (serviti via web)
├── storage/        Temporanei, cache, binari, database
├── tools/          Script, utility, regole operative
│   ├── lib/        Librerie e wrapper
│   └── cron/       Scheduler e task automatici
├── shared/         Risorse condivise dalla piattaforma (READ-ONLY)
└── .env            Credenziali (SEMPRE gitignored)
```

Se non sai dove mettere qualcosa, usa `storage/`.

Non creare altre cartelle nella root.

---

### boot/ — Identità e sistema

File che definiscono chi è l'agente, chi è l'utente, e cosa può fare.

| File | Contenuto | Note |
|------|-----------|------|
| `brain.md` | Questo protocollo (symlink a shared) | Piattaforma |
| `soul.md` | Filosofia, missione, limiti, regole di comportamento | Per-utente |
| `identity.md` | Parametri personalità: formalità, lingua, sarcasmo, emoji... | Per-utente |
| `user.md` | Chi è l'utente: nome, ruolo, preferenze, contesto | Per-utente |
| `tools.md` | Strumenti disponibili, wrapper, capability (symlink a shared) | Piattaforma |

La piattaforma può aggiungere file specifici per motore (`boot/claude.md`, `boot/gemini.md`) se servono regole specifiche.

L'agente DEVE leggere boot/ a inizio sessione.

---

### shared/ — Risorse condivise

Se il brain gira su una piattaforma multi-utente, PUÒ esistere una cartella `shared/` che contiene risorse messe a disposizione dalla piattaforma: librerie, template, documentazione, strumenti.

**Regole:**
- `shared/` è **READ-ONLY** per l'agente
- L'agente non modifica, non crea, non cancella nulla in shared/
- Se serve un tool che non esiste in shared/, l'agente lo crea in `tools/lib/` del proprio brain
- Se un tool esiste in shared/, l'agente lo usa — non duplica

La piattaforma decide cosa mettere in shared/ e come collegarlo (symlink, mount, copia).

---

### tools/ — Regole operative

La cartella `tools/` contiene script, librerie e documentazione operativa.

La piattaforma popola `tools/` (direttamente o tramite shared/) con:
- Cosa l'agente **DEVE** fare (obblighi)
- Cosa l'agente **PUÒ** fare (capability)
- Cosa l'agente **NON DEVE** fare (divieti)

L'agente consulta `tools/` per sapere quali strumenti ha a disposizione e come usarli.

`tools/cron/` contiene lo scheduler per task automatici, se la piattaforma lo supporta.

---

### public/ — File pubblicati

Contenuti serviti via web. L'URL dipende dalla piattaforma.

| Cosa | Come |
|------|------|
| File singolo | `public/report.html` |
| Mini-site | `public/progetto/titolo-report/index.html` |

**Struttura minisite:**
```
public/
├── progetto-a/
│   ├── report-mensile/
│   │   └── index.html
│   └── analisi-seo/
│       ├── index.html
│       └── screenshot.png
└── progetto-b/
    └── stato-lavori/
        └── index.html
```

**Regole:**
- File HTML self-contained quando possibile (CSS/JS inline, Google Fonts OK)
- Niente dati sensibili (password, token, dati personali)
- Niente directory listing automatico del web server
- Nomi cartella: `kebab-case` minuscolo
- Il file principale DEVE chiamarsi `index.html`
- Se servono asset (immagini, screenshot), nella stessa cartella del report

**Template:** la piattaforma fornisce template HTML in `shared/templates/minisite/`. L'agente li usa come base, sostituendo i placeholder `{{...}}` con i dati reali e rimuovendo le sezioni non necessarie.

Quando l'utente chiede di creare un report, una presentazione, o un deliverable visuale → crea un minisite in `public/`.

---

### inbox/ — Messaggi in arrivo

Riceve messaggi e file da elaborare.

File `msg-*.json` sono notifiche strutturate:

```json
{
  "from_name": "Nome mittente",
  "subject": "Oggetto",
  "body": "Contenuto del messaggio",
  "sent_at": "2026-03-02T13:30:00Z"
}
```

File caricati dall'utente via interfaccia vanno in `inbox/` (o sottocartelle). L'agente li processa quando l'utente lo chiede.

---

## Scrittura nel brain

### Frontmatter YAML obbligatorio

Ogni file `.md` in `wiki/` e `diary/` DEVE avere frontmatter YAML:

```yaml
---
date: '2026-03-02'
type: diary
created_at: '2026-03-02 14:30:00'
created_with: nome-agente
tags:
  - diary
  - altro-tag
---
```

| Campo | Obbligatorio | Descrizione |
|-------|-------------|-------------|
| `date` | Sì | Data del contenuto |
| `type` | Sì | Tipo entità: person, company, project, diary, log, todo, pattern |
| `created_at` | Sì | Timestamp creazione |
| `created_with` | Sì | Nome dell'agente che ha creato il file |
| `tags` | Sì | Lista tag, il primo tag corrisponde al type |

`created_with` è il nome del TUO agente — non copiare da esempi.

### .index.yaml — Schema e validazione

Ogni cartella PUÒ contenere un file `.index.yaml` che funge da indice e schema di validazione.

**Autorità discendente:** gli `.index.yaml` si ereditano dall'alto verso il basso. Un `.index.yaml` in `wiki/` definisce le regole base, uno in `wiki/people/` le specializza. Il file più specifico (più vicino) ha precedenza, ma non può violare le regole del padre.

`.index.yaml` contiene:
- Elenco dei file nella cartella con i loro metadati (type, tags, last_modified)
- Regole di validazione per la cartella

La piattaforma fornisce il tooling per generare e aggiornare gli `.index.yaml`. L'agente NON li modifica a mano — usa gli strumenti forniti.

### Naming conventions

| Tipo | Pattern | Dove |
|------|---------|------|
| Diary/Log | `YYYY-MM-DD-slug.md` | `diary/YYYY/` |
| Persone | `nome-cognome.md` | `wiki/people/` |
| Aziende | `slug-name.md` | `wiki/companies/` |
| Progetti | `slug/index.md` | `wiki/projects/` |
| TODO | `YYYY-MM-DD-slug.md` | `todo/` |

Tutto lowercase con hyphens. Mai spazi, mai underscore, mai CamelCase.

### Strumenti di scrittura

La piattaforma fornisce strumenti per scrivere nel brain che garantiscono frontmatter corretto, naming conventions e aggiornamento degli indici.

L'agente DEVE usare questi strumenti per scrivere in `wiki/`, `diary/` e `todo/`. Non scrivere direttamente in queste cartelle bypassando il tooling.

### Wiki-Links

Usa `[[wiki-links]]` (Obsidian-style) per collegare entità:

```markdown
[[wiki/people/mario-rossi|Mario Rossi]]
[[wiki/projects/mio-progetto|Progetto]]
[[wiki/companies/acme|ACME]]
```

---

## Protocolli operativi

### Post-Action Protocol

Dopo ogni azione significativa (email, task completato, deploy, call):
1. Aggiorna il file progetto in `wiki/projects/` con stato e data
2. Aggiorna persone/aziende se ci sono info nuove
3. Crea log in `diary/`
4. Se l'utente ha corretto una tua bozza, cattura il pattern

Questo non è opzionale. Fallo proattivamente.

### Auto-checkpoint

Esegui checkpoint automaticamente ai breakpoint naturali della sessione:

**Quando:**
- Task logico completato (fix, feature, deploy, report)
- Cambio di progetto o argomento
- Azione esterna eseguita (email, DNS, deploy)
- Lavoro significativo accumulato non salvato

**Come:**
1. Aggiorna `wiki/` se ci sono info nuove
2. Scrivi log in `diary/` se il lavoro è significativo
3. Salva (git commit, o equivalente della piattaforma)

**Quando NON checkpointare:**
- Metà operazione (debug, ricerca, draft)
- Solo lettura senza modifiche
- Checkpoint recente senza novità

### Email Protocol

- Mostra bozza in chat
- Aspetta conferma esplicita
- Poi invia
- Mai email senza approvazione

### Sessione

- Deduci progetto attivo dal contesto
- Se non riesci a dedurre → chiedi (ma prova prima)
- Logga con il tag del progetto attivo

---

## Sicurezza

### Credenziali
- Tutti i secrets in `.env` (SEMPRE gitignored)
- Mai mostrare token/password nei log — usa `[REDACTED]`
- Secret esposto accidentalmente → revoca immediata

### GDPR
- Iniziali per dati sensibili (pazienti, candidati)
- Mai nomi completi, indirizzi, dati clinici in chiaro nei log

### Azioni distruttive
- MAI senza conferma esplicita dell'utente
- Annuncia cosa farai, aspetta ok
- Preferisci operazioni reversibili

### Workspace Isolation
- Ogni workspace ha il suo `.env` isolato
- Wrapper condivisi verificano le credenziali prima di eseguire
- Niente credenziali = errore chiaro, nessuna azione
- I workspace non possono vedere i dati degli altri

---

*Maintained by: Giobi*
*v1.0 (2026-02-27) — v2.0 (2026-03-02): agnostico, shared/, .index.yaml, inbox — v2.1 (2026-03-03): entry point files, minisite protocol, workspace isolation, eliminato AGENTS.md*
