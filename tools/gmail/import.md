# Gmail Import - Claude Direct Processing

**Created**: 2025-10-28
**Method**: Claude diretto con curl, NO tool esterni

---

## ✅ Procedura Corretta

### Step 1: Download Email JSON (Gmail API con curl)

**Claude chiama Gmail API direttamente via bash/curl**:

```bash
# ⚠️ CRITICAL: DO NOT use "source .env" in bash one-liner
# It does NOT work properly in single Bash tool calls
# ALWAYS read token directly with grep:

TOKEN=$(grep "^GMAIL_ACCESS_TOKEN=" /home/claude/brain/.env | cut -d'=' -f2)

# Get message IDs per mese
YEAR=2017
MONTH=01

curl -s "https://gmail.googleapis.com/gmail/v1/users/me/messages?maxResults=500&q=after:${YEAR}/${MONTH}/01+before:${YEAR}/${MONTH}/31" \
  -H "Authorization: Bearer $TOKEN" > /tmp/${YEAR}-${MONTH}-ids.json

# Loop per scaricare dettagli di ogni email
# (Implementare loop bash che per ogni ID chiama /messages/{id})
```

**⚠️ IMPORTANTE - Token Access Pattern**:
- ❌ `source /home/claude/brain/.env` → NON funziona in Bash one-liner
- ✅ `TOKEN=$(grep "^GMAIL_ACCESS_TOKEN=" /home/claude/brain/.env | cut -d'=' -f2)` → Funziona sempre
- **Motivo**: Ogni Bash tool call è shell separata, source non persiste
- **Questo bug è ricorrente**: 20+ volte stesso errore, SEMPRE usare grep

**Output**: `/tmp/YYYY-MM-emails.json` (array di email complete)

### Step 2: Processing con Claude Diretto

**NO Gemini, NO OpenRouter, NO script Python esterni**

**Claude legge JSON a chunk** e genera markdown:

1. Se JSON troppo grande: split in batch da 10-20 email (Python inline)
2. Claude Read ogni batch con Read tool
3. Claude analizza e genera markdown
4. Append incrementale ai file finali

**Output**:
- `diary/YYYY/YYYY-MM-gmail-diary.md`
- `log/YYYY/YYYY-MM-gmail-log.md`

### Step 3: Commit

```bash
cd /home/claude/brain
git add diary/YYYY/ log/YYYY/
git commit -m "Add YYYY-MM gmail import (Claude direct)"
git push
```

---

## ❌ DA NON USARE

- ❌ `/home/web/circus` → Circus è per altro
- ❌ `php artisan emails:*` → Laravel commands obsoleti
- ❌ `python3 tools/gmail/import-emails.py` → Usa Gemini (fallisce)
- ❌ `python3 tools/gmail/process-month.py` → Usa Gemini (fallisce)
- ❌ Gemini API / OpenRouter → Non servono, Claude fa tutto

**Regola**: Claude fa TUTTO direttamente in chat. No deleghe a script esterni.

---

## 📊 Status 2017

### JSON Disponibili

- ✅ `/tmp/2017-02-emails.json` (da script precedente)
- ✅ `/tmp/2017-03-emails.json`
- ✅ ... fino a `/tmp/2017-12-emails.json`
- ❌ `/tmp/2017-01-emails.json` → DA SCARICARE

### TODO

1. Download gennaio 2017 con curl
2. Claude process tutti i 12 mesi (lettura + analisi + markdown)
3. Git commit

---

## 📝 Formato Output

### Log (Professionale)

```markdown
## 💼 Settimana N (DD-DD mese)

### Progetti & Clienti

**Nome Cliente/Progetto**
- **Attività**: Descrizione
- **Tech**: PHP, Laravel, etc.
- **Persone**: [[Nome]], [[Nome]]
- **Status**: Completato/In corso
- **€**: Importo o "Incluso"
```

### Diary (Personale)

```markdown
## Settimana N (DD-DD mese)

### 🤝 Collaborazioni & Clienti
- Eventi, incontri, email significative

### 💼 Attività Professionale
- Lavori tecnici, setup, configurazioni

### 🎭 Eventi & Sociali
- Vita privata, viaggi, sport
```

---

## 🎯 Next Steps

1. Download 2017-01 con curl
2. Process batch da 10 email alla volta
3. Genera markdown completo
4. Ripeti per feb-dic
5. Commit tutto

---

## 🔗 Riferimenti

- `tools/gmail/import-emails.py` → SOLO come riferimento API calls, NON usare
- `tools/gmail/IMPORT-PROCEDURES.md` → DA RIMUOVERE (obsoleto, usa Gemini)
- `projects/gmail-import/` → DA RIMUOVERE (era approach sbagliato)

---

**Principio**: Claude è l'unico processor. Bash/curl solo per download, tutto il resto in chat.
