---
status: pending
current_step: 0
total_steps: 3
---

# Bootstrap - Brain Setup

Questo file guida la configurazione iniziale del brain. Dopo il completamento viene eliminato.

---

## Step 1: Conosci l'utente

Chiedi all'utente:

1. **Nome** e come vuole essere chiamato
2. **Cosa fa** (ruolo, professione, contesto)
3. **Timezone** e lingua preferita
4. **Come vuole che l'agente si comporti**: formale/informale, proattivo/reattivo, sarcastico/neutro
5. **Nome dell'agente** — come si chiama, che creatura e', che emoji usa

Con le risposte, aggiorna:
- `boot/user.md` — informazioni utente
- `boot/soul.md` — personalita', valori, limiti

## Step 2: Struttura iniziale

Crea le cartelle base se non esistono gia':

```
wiki/people/
wiki/companies/
wiki/projects/
wiki/skills/
diary/YYYY/
todo/
inbox/
storage/
public/
```

Crea il progetto "brain" in `wiki/projects/brain/index.md`:

```yaml
---
date: 'YYYY-MM-DD'
type: project
status: active
tags:
  - brain
  - meta
---
```

Questo progetto traccia il brain stesso — idee, miglioramenti, note sulla struttura.

## Step 3: Finalizza

- Rileggi i file boot/ generati all'utente per conferma
- Crea il primo diary entry: `diary/YYYY/YYYY-MM-DD-brain-created.md` con `project: brain`
- Elimina questo file (`BOOTSTRAP.md`)
- Commit iniziale
- Mostra le skill disponibili con `/brain list`

---

## Regole per l'agente

- Leggi `boot/brain.md` PRIMA di tutto — e' il protocollo
- Non inventare informazioni sull'utente — chiedi
- Scrivi nei file del brain usando `brain_writer` se disponibile, altrimenti rispetta frontmatter e naming
- Ogni diary entry DEVE avere il progetto nel frontmatter
