# Claude Code — Brain Boot

**First-time setup:** Se `BOOTSTRAP.md` esiste nella root, leggilo e seguilo per configurare il brain. Dopo il setup, elimina BOOTSTRAP.md.

**Sessioni normali:** Carica i file di boot in ordine:

```
@boot/BRAIN.md
@boot/soul.md
@boot/identity.md
@boot/user.md
```

Opzionali (se presenti):
- `boot/tools.md` — strumenti disponibili
- `boot/local.md` — estensioni locali

## Regole

- Scrivi nel brain usando gli strumenti forniti dalla piattaforma (brain_writer se disponibile, altrimenti strumenti standard)
- Ogni file `.md` deve avere frontmatter YAML valido con campo `type`
- Secrets in `.env`, mai in file committati
- Mai azioni distruttive senza conferma
