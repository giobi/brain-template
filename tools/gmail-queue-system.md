# Gmail Monthly Processing Queue System

**Created**: 2025-10-22
**Status**: ✅ Active
**Type**: Laravel Schedule + Telegram Notifications

---

## 🎯 Overview

Sistema automatico per processare mesi di email dalla queue con rate limiting, notifiche Telegram e tracking overhead.

**Frequenza**: Ogni 5 minuti
**Timezone**: Europe/Rome
**Lock**: Prevenzione esecuzioni concorrenti con `withoutOverlapping()`

---

## 📋 Queue Management

### Aggiungere Mesi alla Queue

```bash
# Singolo mese
php artisan emails:queue add 2024-01

# Multipli mesi
php artisan emails:queue add 2024-01 2024-02 2024-03

# Anno intero
php artisan emails:queue add-year 2024
```

### Gestire la Queue

```bash
# Visualizzare queue
php artisan emails:queue list

# Stato sistema
php artisan emails:queue status

# Statistiche overhead
php artisan emails:queue stats

# Pulire queue
php artisan emails:queue clear
```

---

## 🤖 Funzionamento Automatico

### Laravel Schedule

Configurato in `routes/console.php`:

```php
Schedule::command('emails:process-queue')
    ->everyFiveMinutes()
    ->withoutOverlapping()
    ->onFailure(function () {
        // Telegram notification already sent by command
    });
```

### Flow Esecuzione

1. **Check lock**: Previene esecuzioni concorrenti
2. **Legge queue**: Prende primo mese dalla lista
3. **Notifica inizio**: Telegram con mese e remaining
4. **Import**: `php artisan emails:import-gmail --month=YYYY-MM`
5. **Process**: `php artisan emails:process --month=YYYY-MM --replace`
6. **Track overhead**: Conta errori 429/RESOURCE_EXHAUSTED
7. **Notifica fine**: Telegram con stats (emails, overhead, duration)
8. **Log overhead**: Salva in `storage/app/email-queue/overhead-stats.log`

---

## 📱 Notifiche Telegram

### Start Notification

```
🚀 Gmail Processing Started

📅 Month: `2024-05`
📊 Remaining: 7

⏰ 20:15:30
```

### Completion Notification

```
✅ Gmail Processing Completed

📅 Month: `2024-05`
📧 Emails: 364
⚠️ Overhead: 0
⏱️ Duration: 45s
📊 Remaining: 6

Next run in 5 minutes...
```

### Error Notification

```
⚠️ Processing Completed with Issues

📅 Month: `2024-05`
⚠️ Overhead hits: 3
📧 Emails: 364
⏱️ Duration: 52s
```

---

## 📊 Overhead Tracking

Il sistema traccia automaticamente:
- **Overhead hits**: Numero di errori 429/rate limit per mese
- **Email count**: Totale email processate
- **Duration**: Tempo impiegato

### Log Format

```
[2025-10-22 20:15:00] 2024-05 | Overhead: 0 | Emails: 364
[2025-10-22 20:20:00] 2024-06 | Overhead: 2 | Emails: 323
[2025-10-22 20:25:00] 2024-07 | Overhead: 0 | Emails: 401
```

### Statistiche

```bash
php artisan emails:queue stats

# Output:
📊 Overhead Statistics:

  Months processed: 12
  Total emails: 5400
  Total overhead hits: 5
  Overhead rate: 0.09%
```

---

## 🔧 Comandi Laravel

### ProcessMonthlyQueueCommand

**Signature**: `emails:process-queue`
**Schedule**: Every 5 minutes
**File**: `app/Console/Commands/ProcessMonthlyQueueCommand.php`

**Features**:
- Lock management (prevent concurrent runs)
- Telegram notifications (start + end)
- Overhead counting and logging
- Duration tracking
- Auto-retry on failure

### QueueManageCommand

**Signature**: `emails:queue {action} {values?*}`
**Actions**: add, add-year, list, clear, stats, status
**File**: `app/Console/Commands/QueueManageCommand.php`

---

## 📁 File Locations

**Queue File**: `storage/app/private/email-queue/months-queue.txt`
**Overhead Log**: `storage/app/private/email-queue/overhead-stats.log`
**Lock File**: `storage/app/private/email-queue/processing.lock`
**Process Logs**: `storage/logs/process-YYYY-MM.log`

---

## ⚙️ Configuration

### Timezone

`config/app.php`:
```php
'timezone' => 'Europe/Rome',
```

### Environment Variables

Già configurate in `.env`:
```
TELEGRAM_BOT_TOKEN=...
TELEGRAM_CHAT_ID=...
GMAIL_CLIENT_ID=...
GMAIL_CLIENT_SECRET=...
GMAIL_ACCESS_TOKEN=...
GMAIL_REFRESH_TOKEN=...
GEMINI_API_KEY=...
```

---

## 🚨 Rate Limiting

Il sistema è progettato per **rispettare il rate limit Gemini**:

- **Limite**: 250K token/minuto
- **Soluzione**: sleep(10s) tra batch in ProcessEmailsCommand
- **Processing time**: ~3-5 minuti per mese medio (300-400 email)
- **Queue interval**: 5 minuti → **NESSUN overlap possibile**

Con 5 minuti tra esecuzioni, anche mesi grossi completano prima del prossimo run.

---

## 📖 Esempi d'Uso

### Processare Anno Intero

```bash
# 1. Aggiungere 2023 alla queue
php artisan emails:queue add-year 2023

# 2. Verificare queue
php artisan emails:queue list
# Output: 12 months in queue

# 3. Monitorare progress
watch -n 30 "php artisan emails:queue status"

# 4. Dopo ~1 ora, verificare stats
php artisan emails:queue stats
```

### Riprocessare Mese Specifico

```bash
# Aggiungere mese già processato (verrà sostituito con --replace)
php artisan emails:queue add 2024-05

# Monitorare
tail -f storage/logs/process-2024-05.log
```

---

## 🔍 Troubleshooting

### Lock Bloccato

```bash
# Rimuovere lock manualmente
rm storage/app/private/email-queue/processing.lock
```

### Queue Non Processa

```bash
# Verificare scheduler attivo
php artisan schedule:list

# Verificare cron di sistema
sudo cat /etc/cron.d/laravel-scheduler-circus
# Deve contenere: * * * * * www-data cd /home/web/circus && php artisan schedule:run
```

### Overhead Alto

Se overhead rate > 1%:
- Aumentare delay in ProcessEmailsCommand (attualmente 10s)
- Ridurre batch size (attualmente 50 email)
- Aumentare intervallo schedule da 5 a 10 minuti

---

## 📚 Related Documentation

- `tools/gmail-email-import-system.md` - Sistema import base
- `log/2025/2025-10-22-gmail-import-system-implementation.md` - Implementation log
- `tools/linkedin-integration.md` - LinkedIn auto-posting

---

## 🎓 Lessons Learned

1. **Laravel Schedule > Cron Bash**: Più pulito, integrato, gestione errori migliore
2. **withoutOverlapping()**: Previene race conditions automaticamente
3. **Overhead tracking**: Essenziale per monitorare rate limiting Gemini
4. **Telegram notifications**: Visibilità real-time senza dover controllare log
5. **Queue-based**: Permette retry facile e prioritizzazione futura

---

Co-Authored-By: Claude <noreply@anthropic.com>
