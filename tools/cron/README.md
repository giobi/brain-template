# Cron - Claude Intelligent Check-in System

Sistema di check-in **intelligente** dove Claude analizza autonomamente log, diary, email e TODO per mandare update contestuali via Telegram ogni ora.

---

## 📁 Files

- **`daily.md`** - Prompt per Claude con istruzioni complete
- **`daily-checkin.sh`** - Script bash che esegue Claude con il prompt
- **`daily-checkin.py`** - Script Python alternativo (non usato, opzione A)

---

## 🚀 Setup

### 1. Test Manuale

```bash
cd /home/claude/brain
./tools/cron/daily-checkin.sh
```

Deve:
- ✅ Analizzare TODO
- ✅ Controllare sketch/
- ✅ Controllare disk usage
- ✅ Inviare messaggio Telegram
- ✅ Uscire senza prompt

### 2. Installare Cron

```bash
# Edita crontab dell'utente claude
crontab -e

# Aggiungi questa riga (ogni ora)
0 * * * * /home/claude/brain/tools/cron/daily-checkin.sh >> /home/claude/brain/log/cron-daily.log 2>&1
```

**Oppure** crea un file system cron:

```bash
sudo nano /etc/cron.d/claude-daily-checkin

# Contenuto:
0 * * * * claude /home/claude/brain/tools/cron/daily-checkin.sh >> /home/claude/brain/log/cron-daily.log 2>&1
```

### 3. Verifica Cron Attivo

```bash
# Lista cron jobs dell'utente claude
crontab -l

# Oppure controlla system cron
ls -la /etc/cron.d/claude*
```

---

## 📱 Telegram Output

**NON** un report meccanico, ma un **paragrafo intelligente** scritto da Claude che ha letto log, diary, email.

Esempio:

```
🤖 Check-in [14:00]

Ho visto che hai completato l'analisi New Relic con ottimi risultati: riduzione
45% dei costi (da $349 a ~$165/mese). Nelle ultime ore sono arrivate 5 email,
di cui una da Cloudways (oggetto: "Server Update") che potrebbe richiedere azione.
Il TODO più urgente è SgravoQuest fermo da una settimana - forse vale la pena
dedicarci un'ora oggi. Il 2 novembre ricordati di controllare la fattura New Relic
per confermare i savings. Per oggi: 1) email Cloudways, 2) SgravoQuest se hai tempo.
Niente urgenze critiche.
```

**Caratteristiche**:
- Contestuale (cita fatti specifici da log/diary)
- Actionable (suggerisce priorità)
- Narrativo (non liste meccaniche)
- Intelligente (ragiona su cosa è importante)

---

## 🔧 Customizzazione

### Cambiare Frequenza

Esempi di schedule cron:

```bash
# Ogni ora (attuale)
0 * * * * ...

# 4 volte al giorno (se preferisci ridurre)
0 8,12,16,20 * * * ...

# Solo giorni feriali
0 * * * 1-5 ...

# Solo una volta al giorno (mattina)
0 9 * * * ...
```

### Modificare il Prompt

Edita `/home/claude/brain/tools/cron/daily.md`:

- Aggiungi nuovi check (es: GitHub notifications, server status)
- Cambia formato messaggio
- Aggiungi logica condizionale

**Esempio**: Aggiungere check GitHub

```markdown
### 7. Check GitHub Notifications

```bash
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/notifications | jq 'length'
```

Se > 0: menziona nel messaggio
```

---

## 📊 Logs

### Visualizzare Log

```bash
# Ultimi check-in
tail -50 /home/claude/brain/log/cron-daily.log

# Log in real-time
tail -f /home/claude/brain/log/cron-daily.log

# Filtra solo errori
grep -i error /home/claude/brain/log/cron-daily.log

# Log di oggi
grep "$(date +%Y-%m-%d)" /home/claude/brain/log/cron-daily.log
```

### Rotazione Log

Per evitare log troppo grandi:

```bash
# Aggiungi a /etc/logrotate.d/claude-brain
/home/claude/brain/log/cron-daily.log {
    daily
    rotate 30
    compress
    missingok
    notifempty
}
```

---

## 🐛 Troubleshooting

### Cron non esegue

```bash
# Verifica cron service attivo
sudo systemctl status cron

# Controlla permessi script
ls -la /home/claude/brain/tools/cron/daily-checkin.sh
# Deve essere executable: -rwxr-xr-x

# Test manuale
/home/claude/brain/tools/cron/daily-checkin.sh
```

### Telegram non invia

```bash
# Verifica credentials
cat /home/claude/brain/.env | grep TELEGRAM

# Test API manualmente
source /home/claude/brain/.env
curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getMe"
```

### Claude Code non trovato

```bash
# Verifica path
which claude

# Se non trovato, aggiungi al PATH nel cron:
PATH=/usr/local/bin:/usr/bin:/bin
0 9,14,20 * * * /home/claude/brain/tools/cron/daily-checkin.sh
```

### Timeout o troppo lento

Claude Code può impiegare 30-60 secondi. Se troppo lento:

**Opzione 1**: Aumenta timeout nel script
```bash
timeout 120 claude --dangerously-skip-permissions code -p "$PROMPT"
```

**Opzione 2**: Usa lo script Python (più veloce)
```bash
0 9,14,20 * * * /home/claude/brain/tools/cron/daily-checkin.py
```

---

## 🎯 Filosofia

Questo sistema segue il principio **"AI as a teammate"**:

- Claude non è solo uno strumento, è un assistente attivo
- Proattivo: Manda update senza aspettare che tu chieda
- Contextual: Conosce lo stato del sistema e cosa è urgente
- Actionable: Non solo report, ma suggerimenti

**Goal**: Ridurre cognitive load. Tu sai sempre cosa c'è da fare, senza dover controllare manualmente.

---

## 📚 Related

- `tools/telegram/` - Telegram API scripts
- `boot/rules.md` - Brain structure and workflow
- `todo/*.md` - Managed TODO files

---

Co-Authored-By: Claude <noreply@anthropic.com>
