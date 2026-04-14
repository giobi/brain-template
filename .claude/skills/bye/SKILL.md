---
name: bye
description: "Session closing (log, commit, push)"
user-invocable: true
argument-hint: "[open]"
---

**Session Closer** - Quick session exit

## What it does:

1. Create minimal session log
2. Git commit + push
3. Track time saved (auto-estimate)
4. Segnala pendenze rimaste aperte

## Instructions:

### Step 1: Session Log

Create log via brain_writer:

```python
from brain_writer import create_log

create_log('YYYY-MM-DD', 'project-descrizione', """
## Work Done
- [bullet points]

## Time Saved
~XXmin (auto-estimate)
""", tags=['session', '{project}'], project='{project}')
```

**Naming**: `YYYY-MM-DD-{project}-{descrizione}.md`
**Status**: `closed` default. Se ci sono pendenze esplicite → `open`.

### Step 2: EWAF Rating (Auto-Stima)

**Stima tu** rating 1-10 su 4 dimensioni:

- Earth: Valore concreto prodotto
- Water: Energia data vs drenata
- Fire: Friction/costo per utente
- Air: Potenziale futuro/pattern riutilizzabile

**Trigger azioni**:
- **Fire > 7** → Proponi fix per ridurre friction
- **Water < 4** → Chiedi feedback su cosa e andato storto
- **Earth > 8 o Air > 8** → Proponi documentare pattern

### Step 3: Update Project

Se c'e un progetto attivo, aggiorna `wiki/projects/{project}/index.md`.

**REGOLE DI SALVATAGGIO**:
- **Stato attuale**: UNA riga con data. Si SOSTITUISCE, non si appende.
- **Eventi datati**: vanno in `diary/YYYY/` con tag progetto, NON in index.
- **Issue tracking**: in `{progetto}/issues.md`, NON in index.

### Step 4: Diary Update

Se la sessione ha prodotto lavoro concreto, scrivi il diary.

### Step 4.5: Cleanup Backup Files

```bash
ls -t .claude.json.backup.* 2>/dev/null | tail -n +3 | xargs rm -f 2>/dev/null
```

### Step 5: Git

```bash
git add -A && git commit -m "Session: {project} - {summary}

Co-Authored-By: Claude <noreply@anthropic.com>"

git checkout main
git merge {branch-corrente} --no-edit
git push origin main
```

### Step 6: Time Tracking + EWAF Save

Spec EWAF: `wiki/tech/ewaf.md`.

```python
import os, sqlite3
from datetime import datetime

brain_root = os.environ.get('BRAIN_ROOT', os.getcwd())
db_path = os.path.join(brain_root, 'brain.sqlite')

if os.path.exists(db_path):
    db = sqlite3.connect(db_path)
    db.execute('''
        INSERT INTO sessions (
            date, session, project,
            human_estimate_min, prompting_time_min, time_saved_min,
            earth, water, fire, air, note
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        datetime.now().isoformat(),
        session_name, project,
        human_min, prompting_min, saved_min,
        earth_rating, water_rating, fire_rating, air_rating,
        "EWAF reasoning"
    ))
    db.commit()
    db.close()
# se brain.sqlite non esiste → no-op
```

### Step 7: Pendenze Check

Verifica se restano cose in sospeso:
1. TODO aperti del progetto attivo
2. Inbox non processato
3. Roba emersa in sessione non completata
4. Task list Claude Code pending

### Output

```
log/2025/2025-01-14-project-summary.md
Pushed (3 files)
~45min saved
Earth: 8 | Water: 7 | Fire: 3 | Air: 9

Resta in sospeso:
- Verificare report Radar fasolipiante
- Budget da inviare a Fasoli

bye
```

## Varianti

- `/bye open` → forza status: open nel log

## Args Provided:
```
$ARGUMENTS
```
