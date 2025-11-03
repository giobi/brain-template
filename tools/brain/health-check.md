# System Health Check

Checklist periodica per verificare che non hai committato secrets, che il brain non sia esploso, e che in generale tutto non sia andato a puttane.

---

## 🔐 Pre-Commit Security Scan

Prima di ogni `git commit` (se ti ricordi, che poi te lo dimentichi sempre):

### Check rapido

```bash
# 1. Verifica che .env non sia staged (classico errore da pivello)
git status | grep "\.env"
# Se appare → RIMUOVILO SUBITO CAZZO

# 2. Scan per possibili token nei file staged
git diff --cached | grep -E "[A-Za-z0-9_-]{32,}"
# Se match → VERIFICA che non sia un token vero

# 3. Se in dubbio
# NON committare, chiedi conferma
```

### Scan approfondito

Se vuoi fare il precisino:

```bash
# Scan completo staged files per pattern sospetti
git diff --cached | grep -iE "(token|secret|password|api[_-]?key|access[_-]?key)" | grep -v "REDACTED"

# Controlla che non ci siano path assoluti con dati sensibili
git diff --cached | grep -E "/home/[^/]+/\.(env|secret|key)"
```

**Regola d'oro**: Se sembra un token, probabilmente è un token. Se non sei sicuro, è un token. Quando hai dubbi, è sempre un token.

---

## 📊 Boot Files Token Budget

Verifica che i boot files non siano diventati dei mattoni:

```bash
# Check dimensioni
wc -c /home/claude/brain/boot/*.md

# Output atteso:
# ~9000  identity.md  (soglia: 12k)
# ~3000  personal.md  (soglia: 20k)
# ~8000  rules.md     (soglia: 8k)
# ~20000 total        (soglia: 40k)
```

**Soglie**:
- identity.md: **< 12,000 char**
- personal.md: **< 20,000 char**
- rules.md: **< 8,000 char**
- **TOTALE: < 40,000 char**

**Se superi**: Refactoring time, non "alziamo la soglia" (non siamo al governo).

**Dove spostare**:
- Roba tecnica → `tools/brain/`
- Context specifici → file dedicati
- Ripetizioni → elimina una delle due (geniale eh?)

---

## 🗂️ Git Repository Integrity

### Check secrets in history

```bash
# Cerca token pattern in tutta la history (preparati al peggio)
git log -p | grep -E "[A-Za-z0-9_-]{40,}" | head -20

# Cerca riferimenti espliciti a secrets
git log -p | grep -i "token\|secret\|password" | grep -v "REDACTED" | head -20
```

**Se trovi qualcosa**: Il token è COMPROMESSO. Fine. Non "ah ma l'ho tolto dopo", è nella history FOREVER.

**Soluzione**:
1. Revoca il token sul provider
2. Genera nuovo token
3. Aggiorna .env
4. Piangere un po'
5. Non farlo mai più (spoiler: lo rifarai)

### Check .gitignore

```bash
# Verifica che .env sia ignorato
cat .gitignore | grep "\.env"

# Test pratico (deve dare 0 risultati)
git status --ignored | grep "\.env"
```

**Se .env appare in `git status`**: Houston abbiamo un problema. Aggiungi al .gitignore SUBITO.

---

## 🧠 Brain Structure Check

### Directory essenziali

```bash
# Verifica che esistano le directory base
ls -la /home/claude/brain/

# Deve contenere:
# boot/           - Config base
# tools/          - Scripts e utility
# log/            - Log professionali
# diary/          - Diary personali
# database/       - Entità (companies, people, etc)
# sketch/         - Note veloci
# todo/           - TODO files
```

**Se manca qualcosa**: O hai cancellato per sbaglio, o sei in un universo parallelo.

### Cross-references validity

```bash
# Trova tutti i wikilinks
grep -r "\[\[.*\]\]" /home/claude/brain/boot/ /home/claude/brain/tools/ | head -20

# Verifica manualmente che i file esistano
# (Sì, devi farlo a mano. No, non c'è script automatico. Spiace.)
```

---

## 🔄 Cron Jobs Status

```bash
# Verifica cron jobs attivi
crontab -l

# Deve contenere:
# - Gmail token refresh (ogni 45 min)
# - Daily check-in (ogni ora)

# Check log recenti
tail -20 /tmp/gmail-token-refresh.log
tail -20 /home/claude/brain/log/cron-daily.log
```

**Se qualcosa non gira**: Verifica che cron service sia attivo, che i path siano giusti, che la luna sia in fase crescente.

---

## 📈 Disk Usage

```bash
# Check disk space
df -h /home | tail -1

# Se > 80%: è ora di fare pulizia
# Se > 90%: comincia a preoccuparti
# Se > 95%: panico totale
```

**Dove pulire**:
- `/tmp/` - file temporanei vecchi
- Log files > 30 giorni
- `.next/` build directories
- `node_modules/` che non usi più

---

## 🎯 Frequency

**Consigliato**:
- **Pre-commit**: Sempre (se sei diligente)
- **Settimanale**: Boot size + cron check
- **Mensile**: Git history scan + disk usage

**Realtà**: Quando ti ricordi, quando rompe qualcosa, o quando Claude ti rompe i coglioni che è ora di fare check.

---

## 🚨 Red Flags

Segni che qualcosa non va:

- ❌ Boot files > 40k total
- ❌ .env staged in git
- ❌ Token in git history
- ❌ Cron jobs non girano da giorni
- ❌ Disk > 90%
- ❌ Contraddizioni documentazione (vedi coherence.md)
- ❌ 3 metodi "ufficiali" diversi per fare la stessa cosa

**Se vedi red flags**: Fix immediately. Non "poi", non "dopo", non "quando ho tempo". **ORA**.

---

*"An ounce of prevention is worth a pound of 'porcoddio chi ha committato il token?!'"*
