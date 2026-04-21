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
4. Flag remaining open items

## Instructions:

### Step 1: Session Log

Create log via brain_writer:

```python
from brain_writer import create_log

create_log('YYYY-MM-DD', 'project-description', """
## Work Done
- [bullet points]

## Time Saved
~XXmin (auto-estimate)
""", tags=['session', '{project}'], project='{project}')
```

**Naming**: `YYYY-MM-DD-{project}-{description}.md`
**Status**: `closed` by default. If there are explicit pending items → `open`.

### Step 2: EWAF Rating (Auto-Estimate)

**Estimate yourself** a 1-10 rating on 4 dimensions:

- Earth: Concrete value produced
- Water: Energy given vs drained
- Fire: Friction/cost for user
- Air: Future potential/reusable pattern

**Trigger actions**:
- **Fire > 7** → Suggest fix to reduce friction
- **Water < 4** → Ask for feedback on what went wrong
- **Earth > 8 or Air > 8** → Suggest documenting the pattern

### Step 3: Update Project

If there's an active project, update `wiki/projects/{project}/index.md`.

**SAVING RULES**:
- **Current status**: ONE line with date. REPLACE, don't append.
- **Dated events**: go in `diary/YYYY/` with project tag, NOT in index.
- **Issue tracking**: in `{project}/issues.md`, NOT in index.

### Step 4: Diary Update

If the session produced concrete work, write the diary.

### Step 4.5: Cleanup Backup Files

```bash
ls -t .claude.json.backup.* 2>/dev/null | tail -n +3 | xargs rm -f 2>/dev/null
```

### Step 5: Git

```bash
git add -A && git commit -m "Session: {project} - {summary}

Co-Authored-By: Claude <noreply@anthropic.com>"

git checkout main
git merge {current-branch} --no-edit
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
# if brain.sqlite doesn't exist → no-op
```

### Step 7: Pending Items Check

Check if anything remains open:
1. Open TODOs for the active project
2. Unprocessed inbox
3. Things that came up in session but weren't completed
4. Pending Claude Code task list

### Output

```
log/2025/2025-01-14-project-summary.md
Pushed (3 files)
~45min saved
Earth: 8 | Water: 7 | Fire: 3 | Air: 9

Still pending:
- Verify Radar report for fasolipiante
- Send budget to Fasoli

bye
```

## Variants

- `/bye open` → forces status: open in the log

## Args Provided:
```
$ARGUMENTS
```
