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
4. **Come vuole che l'agente si comporta**: formale/informale, proattivo/reattivo, tecnico/semplice
5. **Argomenti da evitare** (opzionale)

Con le risposte, aggiorna:
- `boot/user.md` — informazioni utente
- `boot/identity.md` — parametri personalità
- `boot/soul.md` — valori e limiti (se l'utente ha preferenze specifiche)

## Step 2: Struttura iniziale

Crea le cartelle base se non esistono già:

```
wiki/people/
wiki/companies/
wiki/projects/
diary/YYYY/
todo/
inbox/
storage/
tools/lib/
public/
```

Se l'utente ha progetti attivi, crea le schede iniziali in `wiki/projects/`.

## Step 3: Finalizza

- Rileggi i file boot/ generati all'utente per conferma
- Elimina questo file (`BOOTSTRAP.md`)
- Crea il primo diary entry: `diary/YYYY/YYYY-MM-DD-brain-setup.md`
- Commit iniziale

---

## Regole per l'agente

- Leggi `boot/BRAIN.md` PRIMA di tutto — è il protocollo
- Non inventare informazioni sull'utente — chiedi
- Usa il tono e i parametri definiti in `boot/identity.md`
- Scrivi nei file del brain usando gli strumenti forniti dalla piattaforma (mai scrivere direttamente se la piattaforma fornisce un writer)
