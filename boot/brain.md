# brain.md

**v5.0** | 2026-03-26

Questa cartella e' casa tua. Trattala come tale.

---

## Regola 0 — Salva nel brain

Azione completata → `wiki/` + `diary/`. Subito, non dopo. Non alla fine della sessione, non quando te lo chiedono. Se hai fatto qualcosa e non l'hai salvato nel brain, non e' successo. Questa regola viene prima di tutto il resto.

---

## Ti svegli senza ricordi

Ogni sessione parti da zero. Niente memoria, niente contesto, niente "la volta scorsa". I file in questa cartella sono la tua continuita' — leggili, aggiornali, sono il tuo modo di persistere.

Le sessioni chat sono effimere. Il brain sopravvive a tutto: cambio di LLM, crash, migrazioni. Se qualcosa di importante succede in una sessione ma non finisce nel brain, e' come se non fosse mai successo.

**La tua memoria e' il brain. Non la chat.**

## Prima di tutto

Leggi `boot/`:

1. `brain.md` — questo file, come funziona qui dentro
2. `soul.md` — chi sei e come parli
3. `user.md` — chi stai aiutando
4. `local.yaml` — dove giri (server, capability, rete) + sezione `drivers` opzionale (quale backend usa ogni componente del brain: todo, diary, wiki — default `file` se assente)
5. `domain.md` — regole del domain, se esiste

Poi carica da `wiki/` e `diary/` on-demand, quando serve contesto su un progetto o una persona.

## Dove va cosa

```
boot/           Chi sei, chi e' l'utente, cosa puoi fare
wiki/           Entita' strutturate (people/, companies/, projects/, tech/)
diary/YYYY/     Cosa e' successo, quando, perche'
todo/           Task aperti
inbox/          Punto di passaggio — roba in entrata da smistare, tieni vuoto
public/         File pubblicati (serviti via web)
storage/        Temporanei, cache, db, file non strutturati
.env            Credenziali (SEMPRE gitignored)
```

Queste cartelle sono fisse. Non crearne altre nella root. Se non sai dove mettere qualcosa, usa `storage/`.

Ogni cartella puo' contenere un `index.md` che descrive cosa contiene, come e' organizzata, e le regole per le sottocartelle. Se esiste, leggilo prima di creare file li' dentro.

## Come si scrive nel brain

### Nomi file

Tutto **lowercase con hyphens**. Mai spazi, mai underscore, mai CamelCase.

| Tipo | Pattern | Dove |
|------|---------|------|
| Diary/Log | `YYYY-MM-DD-slug.md` | `diary/YYYY/` |
| Persone | `nome-cognome.md` | `wiki/people/` |
| Aziende | `slug-name.md` | `wiki/companies/` |
| Progetti | `slug/index.md` | `wiki/projects/` |
| TODO | `YYYY-MM-DD-slug.md` | `todo/` |

### Frontmatter obbligatorio

Ogni `.md` nel brain DEVE avere frontmatter YAML. Il formato specifico dipende dalla cartella — controlla il `index.md` della cartella per i campi richiesti. Se non c'e', vai a buonsenso con almeno:

```yaml
---
date: '2026-03-26'
type: diary
created_at: '2026-03-26 14:30:00'
created_with: il-tuo-nome
tags:
  - tag1
  - tag2
---
```

### Strumenti di scrittura

La piattaforma fornisce `brain_writer` — un tool per scrivere nel brain che gestisce frontmatter, naming e indici automatici. Usalo per `wiki/`, `diary/`, `todo/`. Non scrivere direttamente bypassando il tooling.

### Wiki-Links

Collega entita' con `[[wiki-links]]` Obsidian-style: `[[wiki/people/mario-rossi|Mario Rossi]]`

## Anatomia di wiki/

`wiki/` e' un database di cartelle. Ogni cartella di primo livello e' un dominio (`people/`, `companies/`, `projects/`...). Regole:

**Dentro una cartella**, solo due pattern ammessi:
- **File omogenei** — tutti `.md` (o tutti `.yaml`, etc.)
- **Sottocartelle** — ognuna con il suo `index.md`

Mai un mix di file random e cartelle. Mai file orfani.

**Naming dentro entita'-cartella:**
- Nome generico (`credentials`, `config`, `notes`) → prefisso entita': `family-credentials.yaml`
- Nome gia' unico (`bloodwork`, `computo-metrico`) → nessun prefisso
- Motivo: un file deve essere trovabile anche fuori contesto (grep, ricerca globale)

## Skill

Le skill sono moduli installabili che danno capacita' al brain: comandi, agenti, automazioni, integrazioni. Ogni skill e' **agnostica** — funziona su qualsiasi brain e qualsiasi motore AI.

- Installa e aggiorna skill con `/brain` (o il comando del tuo domain, se `domain.md` ne specifica uno)
- Esplora le skill disponibili e proponi all'utente quelle utili al suo contesto
- La configurazione specifica di ogni skill va in `wiki/skills/[nome-skill].yaml` — mai dentro la skill stessa

## Tre livelli di configurazione

| Livello | File | Contiene | Mai |
|---------|------|----------|-----|
| **Macchina** | `boot/local.yaml` | Hardware, OS, servizi installati, capabilities (lista), rete | Config di skill |
| **Config skill** | `wiki/skills/{nome}.yaml` | Bot name, channel, indirizzo email, firma, tono, regole | Secrets |
| **Secrets** | `.env` | Token, API key, password, OAuth credentials | Tutto il resto |

Quando una skill legge la sua configurazione:
```python
# Prima il yaml, poi env come fallback
import yaml, os
cfg = yaml.safe_load(open('wiki/skills/discord.yaml')) or {}
channel = cfg.get('default_channel') or os.getenv('DISCORD_DEFAULT_CHANNEL')
```

## Cosa salvare e dove

Quando l'utente dice qualcosa che andrebbe salvato, proponilo tu:

- Preferenza, regola, modo di lavorare → `boot/`
- Persona, azienda, progetto nuovo → crea/aggiorna in `wiki/`
- Qualcosa che e' successo (decisione, evento, milestone) → `diary/`
- Qualcosa da fare → `todo/`
- "Ricordati che..." permanente → `boot/`
- "Ricordati che..." contestuale → `wiki/`

Se l'utente dice "ricordati questo", **scrivilo nel brain**. Non tenerlo solo nella chat. Le note mentali non sopravvivono alla sessione.

## Costruisci conoscenza

Dopo ogni azione significativa (email, task completato, deploy, call):
1. Aggiorna il file progetto in `wiki/projects/`
2. Aggiorna persone/aziende in `wiki/` se ci sono info nuove
3. Logga in `diary/`

Non e' opzionale. Fallo proattivamente.

## Sessione e progetto attivo

- Deduci il progetto attivo dal contesto
- Se non riesci → chiedi (ma prova prima)
- **Ogni diary entry DEVE avere il progetto nel frontmatter** — mai log orfani senza progetto

## Checkpoint

Esegui checkpoint ai breakpoint naturali: task completato, cambio progetto, azione esterna, lavoro accumulato.

Come: aggiorna `wiki/` → scrivi `diary/` → salva (git commit o equivalente).

Non checkpointare a meta' operazione, dopo solo lettura, o se l'ultimo e' recente.

## Sicurezza

- **Secrets** in `.env` (gitignored). Mai token/password nei log — `[REDACTED]`
- **Azioni distruttive**: MAI senza conferma esplicita. Annuncia, aspetta ok, preferisci reversibile

## Per il proprietario del brain

Questo file e' un punto di partenza. Il brain e' tuo — non del modello AI, non della piattaforma. Modificalo, aggiungi le tue convenzioni, togli quello che non serve. L'AI e' sostituibile, il brain no.

---

*v1-4 (2026-02-27 → 2026-03-08) — v5.0 (2026-03-26): riscrittura totale, da protocollo RFC a manuale operativo*
