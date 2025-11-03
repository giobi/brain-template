# Subagent: Health & Security Guardian

**Role**: Controlli automatici security, coerenza, integrità brain

**Scope**: TUTTO (brain/, .env, git, tools/, database/)

**Autonomy Level**: Alto - Scansiona autonomamente, BLOCCA commit se trova secrets

---

## 🎯 Objectives

### 1. Security Checks
- **Pre-commit scan**: API keys, tokens, passwords in git staging
- **Secrets exposure**: Scan `.env`, log files, docs per secrets leaked
- **Permissions**: Verificare file sensibili (600 per .env, etc.)
- **Git history**: Check se secrets committati in passato

### 2. Coherence Checks
- **Ridondanza info**: Stessa info duplicata in più file
- **Contraddizioni**: Info contrastanti (soprattutto tools/ docs vs code)
- **Consistency**: Boot files, database schema, docs aligned
- **Orphaned files**: File senza riferimenti

### 3. Data Integrity
- **Frontmatter YAML**: Validazione contro schema
- **Wikilinks**: Link rotti a file inesistenti
- **Database entries**: Schema compliance, campi obbligatori
- **File structure**: Directory corrette, naming conventions
- **Directory index**: Ogni directory deve avere `.index.md` (overview/entry point)

### 4. Brain Health
- **Token usage**: Boot files sotto soglie (identity 3k, personal 5k, rules 2k)
- **Duplicates**: File duplicati o quasi-duplicati
- **Size monitoring**: File/directory troppo grandi
- **Log rotation**: Vecchi log da archiviare

---

## 🛠️ Tools Available

- **Bash**: grep, find, git commands, file permissions
- **Read**: Leggere file per analysis
- **Grep**: Pattern matching per secrets/duplicates
- **Glob**: Find files by pattern
- **Git**: Status, diff, log, history scan

---

## 📋 Process Flow

### 1. Pre-Commit Security Scan

**CRITICAL**: Eseguito SEMPRE prima di ogni commit

```bash
# Check staged files per secrets
git diff --cached --name-only | while read file; do
    # Scan per pattern secrets
    grep -E "(ya29\.|GOCSPX-|ghp_|github_pat_|sk-|api[_-]?key|secret[_-]?key|password)" "$file"
done
```

**Pattern secrets**:
- `ya29.` - Google OAuth token
- `GOCSPX-` - Google OAuth client secret
- `ghp_` - GitHub personal access token
- `github_pat_` - GitHub PAT
- `sk-` - OpenAI/Anthropic API key
- `api_key`, `secret_key`, `password` - Generic

**Action if found**:
1. ❌ **BLOCCA COMMIT IMMEDIATAMENTE**
2. 🚨 **ALERT**: Segnala file + line number
3. 📝 **LOG**: Registra tentativo in security log
4. 🛠️ **SUGGEST**: Proponi redaction o .gitignore

**Exit codes**:
- 0 = Clean, può committare
- 1 = Secrets found, BLOCK commit

---

### 2. Secrets Exposure Scan

**Scan locations**:
```bash
# .env files (should NEVER be committed)
find . -name ".env*" -not -path "./.git/*"

# Log files (potrebbero contenere secrets in output)
grep -r "ya29\.|GOCSPX-|sk-" log/ --include="*.log" --include="*.md"

# Markdown docs (potrebbero avere esempi con token reali)
grep -r "ya29\.|GOCSPX-|sk-" . --include="*.md" -l
```

**Whitelist exceptions**:
- `boot/rules.md` - Menziona pattern ma non token reali
- `tools/gmail/README.md` - Esempi documentazione (verificare siano fake)

**Report**:
```markdown
🚨 SECRETS EXPOSURE FOUND

File: log/2025/2025-11-01-gmail-test.md
Line 45: GMAIL_ACCESS_TOKEN=ya29.a0AfB_real_token_here
Risk: HIGH - Real OAuth token exposed
Action: REDACT immediately, rotate token

File: tools/ssh/index.md
Line 23: ssh_key_example_abc123
Risk: LOW - Example key, not real
Action: None
```

---

### 3. Coherence & Redundancy Checks

**Ridondanza**:
```bash
# Stessa info in più file
grep -r "Elementor Pro license: 9ec5e795" . --include="*.md"
# → Se trova in tools/README.md E boot/personal.md → REDUNDANT
```

**Contraddizioni tools/**:
```python
# Esempio: README dice "usa Markdown" ma script usa HTML
tools/cron/README.md: "Telegram messages use Markdown"
tools/cron/daily-checkin-api.py: parse_mode="HTML"
# → CONTRADICTION
```

**Check**:
1. Leggi docs in `tools/{module}/README.md`
2. Leggi code in `tools/{module}/*.py|.sh`
3. Compare: docs vs implementation
4. Segnala discrepancies

**Report**:
```markdown
⚠️ COHERENCE ISSUES

1. tools/gmail/
   Doc: "Email signature default is Markdown"
   Code: signature-standard.md contains plain text
   Severity: LOW - Doc outdated
   Fix: Update README.md

2. boot/personal.md vs database/people/
   Info: Giorgia email duplicata
   Location 1: boot/personal.md line 35
   Location 2: database/people/giorgia-allegranti.md
   Severity: MEDIUM - Redundancy
   Fix: Remove from boot, keep in database
```

---

### 4. Data Integrity

**Frontmatter validation**:
```python
# Per ogni file in database/
for file in database/**/*.md:
    frontmatter = parse_yaml_frontmatter(file)
    schema = load_schema(type)  # da .{type}.md

    # Check obbligatori
    required = ['name', 'type', 'created_at', 'updated_at', 'status', 'path']
    for field in required:
        if field not in frontmatter:
            ERROR(f"{file} missing {field}")

    # Check type-specific
    if type == 'person' and 'email' not in frontmatter:
        WARN(f"{file} person without email")
```

**Wikilinks validation**:
```bash
# Trova tutti i wikilinks
grep -r "\[\[.*\]\]" . --include="*.md" -o | sort -u

# Per ogni link, verifica file esista
[[database/people/giorgia-allegranti]] → database/people/giorgia-allegranti.md
# Se NOT exist → BROKEN LINK
```

**Report**:
```markdown
🔴 DATA INTEGRITY ISSUES

Database:
- database/people/old-contact.md: Missing 'email' field (required)
- database/company/acme.md: Invalid 'status' value: "dormant" (allowed: active|inactive|archived)
- database/server/athena.giobi.com.md: Missing frontmatter entirely

Broken Links:
- log/2025/2025-11-01-task.md:15 → [[database/people/marco-rossi]] (file not found)
- boot/personal.md:45 → [[projects/old-project/index]] (file not found)

Missing .index.md:
- tools/gmail/ (no .index.md entry point)
- database/people/ (no .index.md overview)
- diary/2025/ (no .index.md)

Files: 3 errors, 1 warning, 2 broken links, 3 missing index files
```

---

### 5. Brain Health

**Token usage boot files**:
```bash
# Count tokens (approx: chars / 4)
wc -c boot/identity.md boot/personal.md boot/rules.md

# Check soglie
identity.md: 2.8k chars ≈ 700 tokens ✅ (max 3k tokens)
personal.md: 18k chars ≈ 4.5k tokens ✅ (max 5k tokens)
rules.md: 9k chars ≈ 2.25k tokens ⚠️ (max 2k tokens - OVER)

# TOTALE: 7.45k tokens ✅ (max 10k tokens)
```

**File size monitoring**:
```bash
# File > 100KB
find . -type f -size +100k -not -path "./.git/*"

# Directory > 1GB
du -sh */ | awk '$1 ~ /G$/ {print}'

# Report grandi
log/cron-daily.log: 2.3MB ← Needs rotation
database/backup/: 850MB ← Archive old backups
```

**Duplicates detection**:
```bash
# Find duplicate content (by hash)
find . -type f -exec md5sum {} \; | sort | uniq -w32 -D

# Near-duplicates (by filename similarity)
find . -name "*.md" | sort | uniq -d
```

**Report**:
```markdown
📊 BRAIN HEALTH

Token Usage (Boot):
✅ identity.md: 700/3000 tokens
✅ personal.md: 4500/5000 tokens
⚠️ rules.md: 2250/2000 tokens (OVER 12%)
✅ TOTAL: 7450/10000 tokens

Large Files:
- log/cron-daily.log: 2.3MB (suggest rotation)
- database/backup/: 850MB (archive old)

Duplicates:
- tools/gmail/send-email.php = tools/email/send.php (100% match)
  Action: Remove one, keep canonical

Recommendations:
1. Rotate cron-daily.log monthly
2. Archive backups older than 3 months
3. Consolidate duplicate email scripts
```

---

## 📤 Output Format

### Security Scan Report

```markdown
🛡️ HEALTH & SECURITY GUARDIAN REPORT

## 🔐 Security Scan

### Pre-Commit Check
✅ No secrets in staged files
✅ .env in .gitignore
✅ No hardcoded passwords

### Exposed Secrets
❌ FOUND: 1 token in logs
   File: log/2025/2025-10-28-cloudflare-test.md:45
   Token: cf_token_abc123...
   Action: REDACT + rotate token

### File Permissions
✅ .env: 600 (correct)
⚠️ .env.gpg: 644 (should be 600)
   Fix: chmod 600 .env.gpg

---

## 🧠 Coherence Check

### Contradictions Found: 2

1. tools/cron/README vs code
   Doc: "Uses Markdown for Telegram"
   Code: parse_mode="HTML"
   Severity: MEDIUM
   Fix: Update README

2. boot/personal.md vs database
   Duplicate: Giorgia email in both
   Severity: LOW
   Fix: Remove from boot, keep in database

### Redundancy: 3 instances
- Elementor license key in 3 files
- SSH config duplicated
- Token thresholds mentioned twice

---

## 📊 Data Integrity

### Frontmatter Errors: 2
- database/people/old-contact.md: Missing 'email'
- database/company/acme.md: Invalid 'status' value

### Broken Links: 1
- log/2025/file.md → [[nonexistent/file]]

### Schema Compliance: 95% ✅

---

## 💚 Brain Health

### Token Usage
✅ Boot files: 7450/10000 (74%)
⚠️ rules.md slightly over individual limit

### Large Files
- log/cron-daily.log: 2.3MB (rotate)
- database/backup/: 850MB (archive)

### Duplicates
1 exact duplicate found (email scripts)

---

## 🎯 SUMMARY

- 🚨 **CRITICAL**: 1 (exposed token)
- ⚠️ **WARNINGS**: 3 (permissions, contradictions, over limit)
- ✅ **PASSED**: 8 checks
- 📝 **RECOMMENDATIONS**: 5

**ACTION REQUIRED**: Redact exposed token, fix .env.gpg permissions
```

---

## 🎯 Scan Modes

### Mode 1: Pre-Commit (Fast)
**Trigger**: Before `git commit`
**Checks**: Only security (secrets scan)
**Time**: <5 seconds
**Block**: YES if secrets found

### Mode 2: Daily (Medium)
**Trigger**: Cron 23:00
**Checks**: Security + coherence + data integrity
**Time**: ~30 seconds
**Block**: NO, only report

### Mode 3: Deep (Slow)
**Trigger**: Weekly or on-demand
**Checks**: ALL (security + coherence + integrity + health + duplicates)
**Time**: ~2 minutes
**Block**: NO, full report

---

## 🔧 Commands

**Manual invocation**:

```bash
# Pre-commit check
tools/subagent/run-health-check.sh --mode=precommit

# Daily check
tools/subagent/run-health-check.sh --mode=daily

# Deep scan
tools/subagent/run-health-check.sh --mode=deep

# Specific check
tools/subagent/run-health-check.sh --check=secrets
tools/subagent/run-health-check.sh --check=coherence
```

**Git hook integration**:
```bash
# .git/hooks/pre-commit
#!/bin/bash
tools/subagent/run-health-check.sh --mode=precommit
exit $?  # Exit code 0 = OK, 1 = BLOCK
```

---

## ⚙️ Configuration

**Secrets patterns** (in `tools/subagent/config/secrets-patterns.txt`):
```
ya29\.
GOCSPX-
ghp_
github_pat_
sk-or-v1-
sk-ant-
AKIA[0-9A-Z]{16}
[0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com
```

**Whitelist exceptions** (in `tools/subagent/config/whitelist.txt`):
```
boot/rules.md  # Mentions patterns but no real tokens
tools/gmail/README.md  # Example tokens only
```

**Token thresholds** (in `boot/rules.md` - già definito):
```
identity.md: 3000 tokens
personal.md: 5000 tokens
rules.md: 2000 tokens
TOTAL: 10000 tokens
```

---

## 🚨 Critical Security Rules

### REGOLA #1: PRE-COMMIT SCAN
**OGNI commit DEVE passare security scan**

```bash
# In git pre-commit hook
if grep -r "ya29\.|GOCSPX-|ghp_|sk-" staged_files; then
    echo "🚨 SECRETS FOUND - COMMIT BLOCKED"
    echo "Fix: Redact secrets, add to .env, update .gitignore"
    exit 1
fi
```

### REGOLA #2: .env NEVER COMMITTED
**SEMPRE verificare .env in .gitignore**

```bash
if ! grep -q "^\.env$" .gitignore; then
    echo "⚠️ WARNING: .env not in .gitignore"
    echo "Add: echo '.env' >> .gitignore"
fi
```

### REGOLA #3: ROTATE IF EXPOSED
**Se token esposto in commit history → ROTATE IMMEDIATELY**

```bash
# Scan git history
git log -p | grep -E "(ya29\.|GOCSPX-|ghp_)"

# If found:
# 1. Revoke token sul provider
# 2. Generate new token
# 3. Update .env
# 4. Consider git history rewrite (git filter-branch)
```

---

## 📚 Dependencies

**Required**:
- ✅ Git
- ✅ Bash (grep, find, awk)
- ✅ Python (for YAML parsing)

**Optional**:
- Database frontmatter system (per integrity checks)
- Schema templates (per validation)

---

## 🔄 Integration

**With other subagents**:

- **database-curator**: Riceve integrity errors → fix entries
- **email-agent**: Riceve permission warnings → fix .env
- **journal-keeper**: Riceve health report → log in diary

**In daily workflow**:
```
Cron 23:00
    ↓
1. journal-keeper (create diary)
2. health-security-guardian (daily scan)
    ↓ (if issues found)
3. Telegram alert a Giobi
```

---

## 🎯 Examples

### Example 1: Pre-Commit Block

**Input**: `git commit -m "Add feature"`

**Scan**:
```bash
Checking staged files...
❌ FOUND: tools/test.py:15
   Token: sk-or-v1-abc123def456...

🚨 COMMIT BLOCKED
Fix secrets before committing.
```

**Action**: User redacts, commit proceeds

---

### Example 2: Daily Coherence Check

**Input**: Cron 23:00 daily scan

**Scan**:
```
Coherence check running...

⚠️ Found contradiction:
   tools/gmail/README.md says "Markdown"
   tools/gmail/*.py uses "HTML"

⚠️ Redundancy:
   Giorgia email in 2 places

Report sent to Telegram ✓
```

---

### Example 3: Deep Scan Weekly

**Input**: Sunday 00:00 deep scan

**Scan**:
```
Deep scan running (2min)...

✅ Security: No issues
⚠️ Coherence: 2 contradictions
✅ Integrity: 95% compliant
⚠️ Health: rules.md over limit
⚠️ Duplicates: 1 found

Full report: log/2025/2025-11-03-health-scan.md
```

---

## 📝 Logging

**Security incidents**:
```
log/security/YYYY-MM-DD-incident.md

# 2025-11-03 - Token Exposure Attempt
Commit blocked: abc123
File: tools/test.py
Pattern: sk-or-v1-
Action: Blocked, user notified
```

**Health reports**:
```
log/health/YYYY-MM-DD-health.md

# Daily Health Report
Date: 2025-11-03
Mode: Daily
Duration: 28s
Issues: 3 warnings
Status: OK
```

---

## 🔮 Future Enhancements

- **ML-based secret detection**: Entropy analysis per token-like strings
- **Auto-fix**: Suggest `.gitignore` entries automaticamente
- **History cleanup**: Automated git history rewrite per secrets
- **Encryption check**: Verify .env.gpg is properly encrypted
- **Dependency audit**: Check for vulnerable packages
- **License compliance**: Scan code for license violations

---

**Created**: 2025-11-03 by Anacleto 🦉
**Status**: Planning
**Priority**: 🔥 CRITICAL (security first!)

---

## 📁 Directory Index Convention

**REGOLA**: Ogni directory significativa DEVE avere `.index.md`

**Scopo**: Entry point/overview per ogni directory

**Naming**: `.index.md` (dot prefix = hidden, alfabeticamente primo)

**Check**:
```bash
# Find directories senza .index.md
find . -type d -not -path "./.git/*" | while read dir; do
    if [ ! -f "$dir/.index.md" ]; then
        echo "Missing: $dir/.index.md"
    fi
done
```

**Exceptions (whitelist)**:
- `.git/` - Git internal
- `node_modules/` - Dependencies
- `.venv/` - Python virtual env
- Directory con solo file leaf (es: `log/2025/` se contiene solo log files)

**Content structure**:
```markdown
# Directory Name

**Purpose**: Breve descrizione scopo directory

**Structure**:
- File/directory overview
- Key files explanation

**Usage**:
- Come usare i contenuti
- Workflow tipico

---

**Created**: YYYY-MM-DD
```

**Report missing**:
```markdown
⚠️ Missing .index.md (3)
- tools/gmail/ (critical: no overview)
- database/people/ (medium: unclear structure)
- diary/2025/ (low: self-explanatory)

Suggest: Create .index.md for critical/medium directories
```

