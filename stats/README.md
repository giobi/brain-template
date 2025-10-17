# Brain Statistics

This directory contains auto-generated weekly statistics about your brain activity.

## What's Tracked

- Total markdown files
- Total word count
- Diary entries count
- Active todos count
- Project documentation count
- Commits per week
- Most active areas
- Daily averages

## Format

Files are named: `YYYY-WXX.md` (e.g., `2025-W42.md` for week 42 of 2025)

## Automation

Stats are generated automatically every **Monday at 9:00 AM UTC** by GitHub Actions.

You can also trigger manually:
1. Go to Actions tab in your GitHub repo
2. Select "Weekly Stats" workflow
3. Click "Run workflow"

## Example Output

```markdown
# Brain Stats - Week 2025-W42

Generated: 2025-10-16 09:00 UTC

## Content Metrics

- **Total markdown files**: 25
- **Total words**: 18,855
- **Diary entries**: 14
- **Active todos**: 2
- **Project docs**: 3

## Activity Metrics (Last 7 Days)

- **Commits this week**: 37
- **Average commits/day**: 5.2
- **Average words/day**: 2,693
- **Most active area**: diary

## Insight

Highly productive week! 🔥
```

## Customization

To modify what's tracked or change the schedule, edit:
`.github/workflows/weekly-stats.yml`
