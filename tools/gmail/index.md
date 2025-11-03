# Gmail Tools - Brain Import System

Sistema per importare email Gmail e generare log/diary nel brain.

---

## 🎯 Metodo Ufficiale: Claude Direct Processing

**UNICO metodo approvato**: Claude processa tutto direttamente in sessione.

### Step 1: Download Email JSON

```bash
# Refresh OAuth token
ACCESS_TOKEN=$(curl -s -X POST https://oauth2.googleapis.com/token \
  -d "client_id=$GMAIL_CLIENT_ID" \
  -d "client_secret=$GMAIL_CLIENT_SECRET" \
  -d "refresh_token=$GMAIL_REFRESH_TOKEN" \
  -d "grant_type=refresh_token" | jq -r '.access_token')

# Download emails for specific month
YEAR=2017
MONTH=03
curl -s "https://gmail.googleapis.com/gmail/v1/users/me/messages?maxResults=500&q=after:${YEAR}/${MONTH}/01+before:${YEAR}/${MONTH}/31" \
  -H "Authorization: Bearer $ACCESS_TOKEN" > /tmp/${YEAR}-${MONTH}-emails.json
```

### Step 2: Processing con Claude

1. **Leggi** `import-rules.md` - regole complete processing
2. **Analizza** JSON preliminare (IMPORTANT count, thread, stakeholders)
3. **Decidi** struttura (file mensile unico o multipli dedicati)
4. **Processa** con dettaglio completo:
   - Leggi JSON in batch (Read tool)
   - Estrai contesto ogni email IMPORTANT
   - Genera log (professionale) + diary (personale)
5. **Commit** risultati a git

### Step 3: Output

File generati:
- `log/YYYY/YYYY-MM-gmail-log.md` (professionale)
- `diary/YYYY/YYYY-MM-gmail-diary.md` (personale)
- Opzionali: `log/YYYY/YYYY-MM-DD-topic.md` per eventi specifici

---

## ⚠️ Script Policy

**Regola ferrea**: Script esterni vanno tenuti SOLO se hanno **trade-off estremamente positivo di efficienza**.

### ✅ Script Tenuti

Nessuno. Curl + Claude direct processing è il metodo ufficiale.

### ❌ Script Eliminati

**`import-emails.py`** (eliminato 2025-10-28):
- **Motivo**: curl fa la stessa cosa in una riga, più trasparente
- **Trade-off negativo**: dipendenza Python senza beneficio

**`process-month.py`** (eliminato 2025-10-28):
- **Motivo**: usa Gemini API invece di Claude direct
- **Trade-off negativo**: contraddice metodo ufficiale, meno dettaglio

### 🤔 Quando Aggiungere Script

Considera uno script SOLO se:
1. **Efficienza 10x+**: risparmio massiccio tempo/token
2. **Non sostituibile**: impossibile fare con tool esistenti
3. **Allineato**: non contraddice metodo ufficiale
4. **Documentato**: spiegazione chiara trade-off in questo file

**Esempio ipotetico script OK**:
- Script che parallelizza download 12 mesi (risparmio 10x tempo)
- Ma mantiene processing Claude direct

**Esempio script NO**:
- Script che processa con Gemini (contraddice metodo)
- Script Python che fa curl (nessun beneficio)

---

## 📚 File Documentazione

- **`import-rules.md`** - Regole complete processing (LEGGI SEMPRE)
- **`import.md`** - Note tecniche OAuth/API
- **`README.md`** - Overview OAuth setup
- **`index.md`** (questo file) - Metodo ufficiale + script policy

---

## 🔧 Utility OAuth (PHP)

Script PHP per setup/gestione OAuth:
- `generate-oauth-url.php` - URL autorizzazione Google
- `exchange-code.php` - Scambia code → refresh token
- `refresh-token.php` - Test refresh token
- `send-email.php`, `create-draft.php` - Utility invio email

**Nota**: Questi sono utility di setup, non processing. Sono OK.

---

## 📊 Status Import

Vedi todo list attiva in sessione Claude Code per status corrente.

**Import completati**:
- 2017-01 (Gennaio) ✅
- 2017-02 (Febbraio) ✅

**In progress**:
- 2017-03 (Marzo) 🔄

**Todo**:
- 2017-04 → 2017-12 (9 mesi)

---

## 🚫 Cosa NON Fare

❌ **NON usare Circus/Gemini**: processing deve essere Claude direct
❌ **NON usare Python scripts**: curl + Claude è il metodo ufficiale
❌ **NON fare compact**: dettaglio completo sempre, salvo richiesta esplicita
❌ **NON inventare metodi**: esiste un solo metodo ufficiale sopra

**Nota**: Circus email commands (`php artisan emails:*`) sono DEPRECATI e non vanno usati.

---

**Ultimo aggiornamento**: 2025-10-28
**Metodo validato**: Claude Direct Processing (curl + Claude)
