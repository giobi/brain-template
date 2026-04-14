---
type: tech
tags:
  - tech
  - system
  - rating
  - session
created_at: 2026-01-19
---

# EWAF — Session Rating

Sistema di valutazione delle sessioni di lavoro su 4 dimensioni. Integrato nativamente in `/bye`.

## Dimensioni

Rating 1–10:

| Dim | Sigla | Domanda |
|-----|-------|---------|
| 🌍 Earth | E | Quanto valore concreto è stato prodotto? |
| 💧 Water | W | L'agente ha dato energia o l'ha drenata? |
| 🔥 Fire | F | Quanta friction ha incontrato l'utente? |
| 💨 Air | A | Quanto è riutilizzabile/generalizzabile il lavoro fatto? |

## Trigger automatici

| Condizione | Azione |
|-----------|--------|
| Fire > 7 | Proponi fix per ridurre friction |
| Water < 4 | Chiedi feedback esplicito su cosa è andato storto |
| Earth > 8 o Air > 8 | Proponi di documentare il pattern in `wiki/` |

## Schema SQLite

Tabella `sessions` in `brain.sqlite` (root del brain):

```sql
CREATE TABLE IF NOT EXISTS sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    session TEXT,
    project TEXT,
    human_estimate_min INTEGER,
    prompting_time_min INTEGER,
    time_saved_min INTEGER,
    earth INTEGER,
    water INTEGER,
    fire INTEGER,
    air INTEGER,
    note TEXT
);
```

## Salvataggio (da /bye)

```python
import os, sqlite3
from datetime import datetime

brain_root = os.environ.get('BRAIN_ROOT', os.getcwd())
db_path = os.path.join(brain_root, 'brain.sqlite')

if os.path.exists(db_path):
    db = sqlite3.connect(db_path)
    db.execute('''
        INSERT INTO sessions (date, session, project,
            human_estimate_min, prompting_time_min, time_saved_min,
            earth, water, fire, air, note)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (datetime.now().isoformat(), session_name, project,
          human_min, prompting_min, saved_min,
          earth, water, fire, air, note))
    db.commit()
    db.close()
# se brain.sqlite non esiste → no-op
```

## Ispirazione

Basato su **Earth, Wind & Fire** (Water al posto di Wind per enfatizzare il flow energetico).
Il rating non è un voto — è un segnale per migliorare la collaborazione nel tempo.
