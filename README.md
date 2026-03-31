# Brain Template

Un template per creare il tuo **brain** — knowledge base personale strutturato, progettato per funzionare con AI agent (Claude Code, Gemini CLI, Cursor, qualsiasi cosa legga markdown).

Il brain non è l'AI. L'AI è il motore, sostituibile. Il brain è la conoscenza: decisioni, relazioni, progetti, appunti, log. Portabile, di proprietà dell'utente.

## Quick Start

```bash
git clone https://github.com/giobi/brain-template.git my-brain
cd my-brain
cp .env.example .env
```

Apri con il tuo AI agent (es. `claude` o `gemini`). L'agent leggerà `boot/soul.md` e avvierà l'onboarding automaticamente.

## Struttura

```
brain/
├── boot/                ← sistema: protocollo, soul, identity, user
│   ├── BRAIN.md         ← protocollo brain (immutabile)
│   ├── soul.md          ← valori, limiti, continuità
│   ├── identity.md      ← parametri personalità (scala 1-10)
│   └── user.md          ← informazioni sull'utente
├── wiki/                ← entità strutturate
│   ├── projects/        ← progetti (obbligatorio)
│   ├── people/          ← contatti
│   └── companies/       ← aziende
├── diary/               ← log temporale (cosa è successo quando)
├── todo/                ← task aperti
├── inbox/               ← input in arrivo da processare
├── public/              ← file pubblicati (serviti via web, opzionale)
├── storage/             ← temporanei, cache, database
├── tools/lib/           ← script e wrapper
├── .env                 ← credenziali (gitignored, MAI committare)
├── manifest.json        ← versione protocollo e template
```

## Come funziona

### Boot Sequence

All'avvio, l'agent legge i file in ordine:

1. `boot/BRAIN.md` — protocollo (struttura, regole, sicurezza)
2. `boot/soul.md` — filosofia e limiti
3. `boot/identity.md` — parametri personalità
4. `boot/user.md` — chi è l'utente

### Frontmatter YAML

Ogni file `.md` nel brain ha un frontmatter YAML:

```yaml
---
date: '2026-03-01'
type: diary
tags:
  - session
  - progetto-x
---
```

Il campo `type` è obbligatorio. Il frontmatter garantisce che il brain sia navigabile e indicizzabile.

### Personalità

L'agent ha parametri configurabili (scala 1-10):

| Parametro | Cosa controlla |
|-----------|---------------|
| Formalità | Stile comunicazione |
| Emoji | Uso di emoji |
| Verbosità | Lunghezza risposte |
| Tecnicismo | Livello di gergo tecnico |
| Proattività | Autonomia vs. chiedere prima |
| Sarcasmo | Livello di ironia |

Modificabili al volo: "sii più formale", "zero emoji", "massima proattività".

## Naming Conventions

| Tipo | Pattern | Dove |
|------|---------|------|
| Diary/Log | `YYYY-MM-DD-slug.md` | `diary/YYYY/` |
| Entità | `slug-name.md` | `wiki/{tipo}/` |
| Progetti | `slug/index.md` | `wiki/projects/` |
| TODO | `YYYY-MM-DD-slug.md` | `todo/` |

Tutto lowercase con hyphens. Mai spazi, mai underscore.

## Sicurezza

- Secrets in `.env`, sempre fuori da version control
- Mai dati identificativi + dati sensibili in chiaro
- Azioni distruttive mai senza conferma esplicita

## Versioning

Il file `manifest.json` traccia la versione del protocollo e del template. Le installazioni possono verificare se sono aggiornate confrontando con questo repo.

```json
{
  "brain_protocol": { "version": "2.0" },
  "template": { "version": "2.0" }
}
```

## Estensibilità

Il protocollo è **additive-only**:

- Puoi aggiungere sottocartelle a `wiki/`
- Puoi aggiungere regole in `boot/local.md`
- Puoi aggiungere nuovi `type` nel frontmatter
- Puoi aggiungere wrapper in `tools/`

Non puoi rimuovere cartelle obbligatorie, cambiare il formato del frontmatter, o sovrascrivere regole di sicurezza.

## Compatibilità

Funziona con qualsiasi AI agent che legge markdown:
- Claude Code (Anthropic)
- Gemini CLI (Google)
- Cursor, Windsurf, Aider
- Qualsiasi cosa legga file `.md`

Ogni motore ha il suo file di configurazione nella root (es. `CLAUDE.md`, `GEMINI.md`) che include i file di boot.

## License

MIT — vedi [LICENSE](LICENSE)

---

Brain Protocol v2.0 — [giobi.com](https://giobi.com)
