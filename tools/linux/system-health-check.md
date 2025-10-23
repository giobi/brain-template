# System Health Check - Prassi di Controllo Sistema

Questa è la procedura standard per verificare lo stato qualitativo del server web.

## 1. Overview Sistema Base

```bash
# Informazioni sistema operativo
cat /etc/os-release | grep -E "^(NAME|VERSION)="
uname -r

# Uptime e load average
uptime
```

**Interpretazione Load Average:**
- Con 4 core, valori OK: < 4.0
- Warning: 4.0 - 6.0
- Critical: > 6.0

---

## 2. Risorse: CPU e RAM

```bash
# Memoria RAM
free -h

# Top processi per RAM
ps aux --sort=-%mem | head -10

# Top processi per CPU
ps aux --sort=-%cpu | head -10
```

**Cosa guardare:**
- **MemAvailable** > 1 GB = OK
- **MemAvailable** < 500 MB = WARNING (rischio swap/OOM)
- Se un processo usa > 20% RAM costante = indagare
- CPU idle < 10% costante = sovraccarico

---

## 3. Storage e I/O

```bash
# Spazio disco
df -h

# Inode (file system entries)
df -i

# I/O disk usage (se iotop installato)
sudo iotop -o -b -n 3
```

**Soglie critiche:**
- **Uso disco** > 85% = WARNING
- **Uso disco** > 95% = CRITICAL
- **Inode** > 90% = problema (troppi file piccoli)

---

## 4. Servizi Web Essenziali

```bash
# Nginx
sudo systemctl status nginx
sudo nginx -t

# PHP-FPM
sudo systemctl status php8.2-fpm
sudo systemctl status php8.3-fpm 2>/dev/null

# Database (se presente)
sudo systemctl status mysql 2>/dev/null
sudo systemctl status postgresql 2>/dev/null
```

**Check veloce:**
- Tutti i servizi devono essere `active (running)`
- `nginx -t` deve dire "syntax is ok"

---

## 5. Connettività e Rete

```bash
# Porte in ascolto
sudo ss -tlnp | grep -E ":(80|443|3306|5432)"

# Connessioni attive
sudo ss -s

# Test DNS
dig google.com +short
```

**Cosa verificare:**
- Nginx ascolta su :80 e :443
- DB ascolta solo su 127.0.0.1 (non esposto)
- DNS funziona (dig restituisce IP)

---

## 6. Log Errors e Problemi

```bash
# Errori critici nel syslog (ultime 24h)
sudo journalctl -p err -S today

# Nginx errors (ultimi 50)
sudo tail -50 /var/log/nginx/error.log

# PHP errors
sudo tail -50 /var/log/php8.2-fpm.log
sudo tail -50 /var/log/php8.3-fpm.log 2>/dev/null

# Laravel logs (esempio emicar)
tail -50 /home/claude/app/emicar/storage/logs/laravel.log
```

**Pattern da cercare:**
- `OOM` / `Out of memory` = RAM insufficiente
- `502 Bad Gateway` = PHP-FPM morto/sovraccarico
- `Permission denied` = problemi permessi file
- `Connection refused` = servizio non in ascolto

---

## 7. Sicurezza Base

```bash
# Tentativi SSH falliti (ultimi 100)
sudo journalctl -u ssh -S today | grep "Failed password" | tail -20

# Utenti loggati
who

# Processi sospetti (non di sistema)
ps aux | grep -vE "root|www-data|mysql|postgres|claude|copilot"
```

**Red flags:**
- Troppi failed password da stesso IP = attacco brute force
- Utenti sconosciuti loggati
- Processi con nomi strani (cryptominer, etc)

---

## 8. Performance Web (Quick Test)

```bash
# Response time Nginx
time curl -I https://emicar.giobi.net 2>&1 | grep "HTTP\|real"

# PHP-FPM pool status (se configurato)
curl http://localhost/fpm-status 2>/dev/null
```

**Tempi OK:**
- `real` < 0.5s = eccellente
- `real` 0.5-2s = accettabile
- `real` > 2s = problema

---

## 9. Backup e Aggiornamenti

```bash
# Pacchetti da aggiornare
apt list --upgradable 2>/dev/null | wc -l

# Ultimo backup (se configurato)
ls -lht /backup/ 2>/dev/null | head -5
```

**Best practice:**
- Aggiornamenti > 50 = fare update presto
- Backup giornalieri automatici

---

## 10. Report Sintetico (One-liner)

```bash
echo "=== SYSTEM HEALTH CHECK ===" && \
echo "Uptime: $(uptime -p)" && \
echo "RAM: $(free -h | awk '/^Mem:/{print $3"/"$2" used ("$7" available)"}')" && \
echo "Disk: $(df -h / | awk 'NR==2{print $3"/"$2" ("$5" used)"}')" && \
echo "Load: $(uptime | awk -F'load average:' '{print $2}')" && \
echo "Nginx: $(systemctl is-active nginx)" && \
echo "PHP-FPM: $(systemctl is-active php8.2-fpm)" && \
echo "=========================="
```

---

## Interpretazione Qualitativa Complessiva

### 🟢 Sistema Sano
- Load < 4.0
- RAM disponibile > 2 GB
- Disk < 70%
- Tutti i servizi running
- Nessun errore critico nei log

### 🟡 Sistema Warning
- Load 4-6
- RAM disponibile 500MB - 2GB
- Disk 70-85%
- Errori sporadici nei log
- **Azione**: monitorare, ottimizzare

### 🔴 Sistema Critico
- Load > 6
- RAM disponibile < 500 MB
- Disk > 90%
- Servizi down
- Errori continui
- **Azione**: intervento immediato

---

## Script Automatico (opzionale)

Salvare come `/usr/local/bin/health-check`:

```bash
#!/bin/bash
echo "=== HEALTH CHECK $(date) ==="
echo ""
echo "--- RESOURCES ---"
uptime
free -h | grep Mem
df -h / | grep -v Filesystem
echo ""
echo "--- SERVICES ---"
systemctl is-active nginx php8.2-fpm mysql 2>/dev/null | paste - - - -
echo ""
echo "--- ERRORS (last 10) ---"
sudo journalctl -p err -n 10 --no-pager
echo ""
echo "=== END ==="
```

Rendere eseguibile: `sudo chmod +x /usr/local/bin/health-check`

Uso: `sudo health-check`
