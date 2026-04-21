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

Session evaluation system across 4 dimensions. Natively integrated in `/bye`.

## Dimensions

Rating 1–10:

| Dim | Code | Question |
|-----|------|----------|
| Earth | E | How much concrete value was produced? |
| Water | W | Did the agent give energy or drain it? |
| Fire | F | How much friction did the user encounter? |
| Air | A | How reusable/generalizable is the work done? |

## Automatic triggers

| Condition | Action |
|-----------|--------|
| Fire > 7 | Suggest fix to reduce friction |
| Water < 4 | Ask for explicit feedback on what went wrong |
| Earth > 8 or Air > 8 | Suggest documenting the pattern in `wiki/` |

## SQLite Schema

Table `sessions` in `brain.sqlite` (brain root):

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

## Saving (from /bye)

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
# if brain.sqlite doesn't exist → no-op
```

## Inspiration

Based on **Earth, Wind & Fire** (Water instead of Wind to emphasize energetic flow).
The rating is not a grade — it's a signal to improve collaboration over time.
