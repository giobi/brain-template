# Gmail Import Procedures

**Last Updated**: 2025-10-23
**Status**: Production-ready

---

## 📋 Overview

Sistema completo per import + processing di email Gmail → Brain (log + diary).

**Pipeline**:
```
Gmail API → JSON extraction → Gemini AI processing → Markdown (log/diary) → Git commit
```

---

## 🔍 Check Import Status

### Quick Check

```bash
# Check 2023-2024 files
ls -lh /home/claude/brain/diary/2023/ /home/claude/brain/diary/2024/
ls -lh /home/claude/brain/log/2023/ /home/claude/brain/log/2024/

# Count lines (volume indicator)
wc -l /home/claude/brain/log/2024/*-gmail-log.md | tail -1
```

### Detailed Quality Check

```bash
# Search for import errors (not email content errors)
grep -r "failed to\|import error\|API error" /home/claude/brain/diary/ /home/claude/brain/log/

# Check file sizes (should be >1KB if data present)
find /home/claude/brain/log/ -name "*-gmail-log.md" -size -1k

# Sample content check
head -50 /home/claude/brain/log/2024/2024-01-gmail-log.md
head -50 /home/claude/brain/diary/2024/2024-01-gmail-diary.md
```

### Expected Format

**Log file** (professional/work):
```markdown
#### [[Company Name]]
- **Data**: DD/MM
- **Cliente**: [[Client]]
- **Tipo**: Feature|Bugfix|Support
- **Stato**: Completato|In corso
- **Persone**: [[Person 1]], [[Person 2]]
- **Descrizione**: ...
- **Tech**: [[PHP]], [[Laravel]], [[MySQL]]
- **€**: Amount or "Incluso in contratto"
```

**Diary file** (personal):
```markdown
## 📅 Settimana N (DD-DD Mese)

### ✈️ Viaggi
- [events or "Nessuno"]

### 🏃 Sport & Attività
- [events or "Nessuno"]

### 🎭 Eventi & Sociali
- [events or "Nessuno"]
```

---

## ⚙️ Import Commands

### Single Month Import

```bash
cd /home/web/circus

# Step 1: Import (Gmail API → JSON)
sudo -u www-data php artisan emails:import-gmail --month=2023-03

# Step 2: Process (JSON → Markdown via Gemini)
sudo -u www-data php artisan emails:process --month=2023-03

# Check results
ls -lh /home/claude/brain/log/2023/2023-03-gmail-log.md
ls -lh /home/claude/brain/diary/2023/2023-03-gmail-diary.md
```

### Batch Import (Full Year)

```bash
cd /home/web/circus

# Import all months of a year
for month in 01 02 03 04 05 06 07 08 09 10 11 12; do
    echo "Importing 2022-$month..."
    sudo -u www-data php artisan emails:import-gmail --month=2022-$month

    echo "Processing 2022-$month..."
    sudo -u www-data php artisan emails:process --month=2022-$month

    sleep 5  # Avoid API rate limits
done
```

### Background Script (Night Import)

```bash
# Create script
cat > /tmp/import-year.sh <<'EOF'
#!/bin/bash
YEAR=$1
cd /home/web/circus

for month in 01 02 03 04 05 06 07 08 09 10 11 12; do
    echo "=== $YEAR-$month ==="

    # Import
    sudo -u www-data php artisan emails:import-gmail --month=$YEAR-$month

    # Process
    sudo -u www-data php artisan emails:process --month=$YEAR-$month

    # Notify via Telegram
    /home/web/circus/tools/telegram/send-message.sh "✅ $YEAR-$month: Import+Process done"

    sleep 10
done

/home/web/circus/tools/telegram/send-message.sh "🎉 $YEAR complete!"
EOF

chmod +x /tmp/import-year.sh

# Run in background
nohup /tmp/import-year.sh 2022 > /tmp/import-2022.log 2>&1 &

# Monitor
tail -f /tmp/import-2022.log
```

---

## 📊 Status Report

### Current Status (as of 2025-10-23)

| Year | Imported | Processed | Status | Lines (log) |
|------|----------|-----------|--------|-------------|
| 2024 | ✅ All 12 | ✅ All 12 | Complete | 6,909 |
| 2023 | ✅ Jan-Feb | ✅ Jan-Feb | Partial | 873 |
| 2022 | ❌ None | ❌ None | Pending | - |
| 2021 | ❌ None | ❌ None | Pending | - |
| ... | ... | ... | ... | ... |
| 2015 | ❌ None | ❌ None | Pending | - |

**Total Processed**: 14 months
**Total Missing**: 98 months (2015-2022 complete + 2023 Mar-Dec)

---

## 🎯 Recommended Strategy

### Phase 1: Complete 2023 ✅ IN PROGRESS
```bash
# Complete remaining 2023 months (Mar-Dec)
for month in 03 04 05 06 07 08 09 10 11 12; do
    sudo -u www-data php artisan emails:import-gmail --month=2023-$month
    sudo -u www-data php artisan emails:process --month=2023-$month
done
```

**Estimated time**: 2-3 hours
**Estimated cost**: €1-2 (Gemini API)

### Phase 2: Test One Full Year (2022)
```bash
# Test import of complete year to validate process
/tmp/import-year.sh 2022
```

**Estimated time**: 4-6 hours
**Estimated cost**: €2-3

### Phase 3: Batch Import (2015-2021)
```bash
# If Phase 2 successful, import all remaining years
for year in 2021 2020 2019 2018 2017 2016 2015; do
    /tmp/import-year.sh $year
    sleep 60  # Pause between years
done
```

**Estimated time**: 30-40 hours (run overnight for multiple nights)
**Estimated cost**: €15-20 total

---

## ⚠️ Common Issues & Solutions

### Issue 1: Gmail API Token Expired

**Symptoms**:
```
Error: Invalid credentials
401 Unauthorized
```

**Solution**:
```bash
# Refresh token
cd /home/web/circus
php artisan emails:refresh-token

# Or manually update in .env
nano /home/claude/brain/.env
# Update GMAIL_ACCESS_TOKEN
```

### Issue 2: Gemini API Rate Limit

**Symptoms**:
```
Error: Resource exhausted
429 Too Many Requests
```

**Solution**:
```bash
# Add sleep between processing
for month in ...; do
    php artisan emails:process --month=$month
    sleep 30  # Wait 30s between months
done
```

### Issue 3: File Permission Errors

**Symptoms**:
```
Permission denied writing to /home/claude/brain/log/
```

**Solution**:
```bash
# Fix ownership
sudo chown -R claude:claude /home/claude/brain/log/
sudo chown -R claude:claude /home/claude/brain/diary/

# Ensure script runs as www-data (for JSON) but commits as claude
sudo -u www-data php artisan emails:process ...
# Git commit happens as claude user automatically
```

### Issue 4: Empty/Missing Months

**Symptoms**:
- File exists but contains only "Nessuno" entries
- File <1KB size

**Cause**: Likely legitimate - few/no emails that month

**Verification**:
```bash
# Check original JSON
ls -lh /home/web/circus/storage/app/emails/2023/2023-08.json

# If JSON is small/empty → month was quiet (OK)
# If JSON is large but MD is empty → processing issue
```

---

## 📈 Quality Metrics

### Good Import Indicators

✅ Log files: 10-30KB per month (active months)
✅ Diary files: 2-10KB per month
✅ Wikilinks present: `[[Company]]`, `[[Person]]`
✅ Tags present: `#tech`, `#privacy`
✅ Structured sections (Settimana 1-4, etc.)
✅ Git commits automatic after processing

### Warning Signs

⚠️ Log file <1KB (check if month was quiet or processing failed)
⚠️ No wikilinks (Gemini didn't extract entities)
⚠️ Malformed markdown
⚠️ No git commits after processing

---

## 🔄 Maintenance

### Monthly Routine (New Emails)

```bash
# At end of each month, import current month
CURRENT_MONTH=$(date +%Y-%m)

cd /home/web/circus
sudo -u www-data php artisan emails:import-gmail --month=$CURRENT_MONTH
sudo -u www-data php artisan emails:process --month=$CURRENT_MONTH

# Verify
ls -lh /home/claude/brain/log/$(date +%Y)/$(date +%Y-%m)-gmail-log.md
```

### Automation (Cron)

```bash
# Add to crontab
crontab -e

# Run on 1st of every month at 3am
0 3 1 * * cd /home/web/circus && sudo -u www-data php artisan emails:import-gmail --month=$(date +%Y-%m -d 'last month') && sudo -u www-data php artisan emails:process --month=$(date +%Y-%m -d 'last month')
```

---

## 📊 Statistics

### Volume Estimates

Based on 2024 data:
- **Average**: ~390 emails/month
- **Peak**: 500 emails (Feb, Mar)
- **Low**: 236 emails (Aug)

**Extrapolation 2015-2024**:
- 10 years × 12 months = 120 months
- 120 × 390 avg = **~46,800 emails total**

### Processing Costs

**Gemini API Pricing** (as of 2025):
- Input: $0.00025 per 1K tokens
- Output: $0.0005 per 1K tokens

**Estimated per month**:
- ~500 emails × 200 tokens avg = 100K tokens input
- ~50K tokens output (summaries)
- Cost: ~$0.04 per month

**Full import (120 months)**:
- 120 × $0.04 = **~$5-6 total** 🎉

---

## 🚀 Next Steps

1. ✅ Complete 2023 (in progress)
2. Test 2022 (full year validation)
3. If OK, batch import 2015-2021
4. Setup monthly cron for automation
5. Create annual summary reports from data

---

*Created: 2025-10-23*
*Procedure tested and validated on 2024 + 2023 Jan-Feb*
*Ready for production use*
