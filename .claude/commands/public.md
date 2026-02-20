# /public - Publish files to public web

Gestione dei file pubblici del brain. I file in `public/` sono serviti su web all'''URL configurato in `.env`.

## Setup

Leggi PUBLIC_BASE_URL da `.env` prima di dare link all'''utente:
```bash
grep PUBLIC_BASE_URL .env | cut -d= -f2
```

## Usage

```
/public list          → lista file pubblicati con URL completo
/public new <name>    → crea nuova pagina HTML in public/
/public url <file>    → mostra URL pubblico di un file
/public remove <file> → rimuovi un file da public/
```

## Come funziona

I file in `public/` sono serviti direttamente via nginx senza autenticazione.

```
public/
  index.html     → $PUBLIC_BASE_URL/
  report.html    → $PUBLIC_BASE_URL/report.html
```

## Workflow tipico

1. Crea il file in `public/`
2. L'''URL è subito accessibile — nessun deploy, nessun login
3. Condividi il link

## Notes

- Non mettere dati sensibili in public/ — è pubblico senza auth
- Stile HTML consigliato: dark monospace
