#!/usr/bin/env python3
"""
Journal Keeper Subagent

Automatically generates log/ and diary/ entries from sessions, conversations, emails.

Usage:
    # Generate log from session transcript
    python journal-keeper.py log --input session.txt --topic "Database refactoring"

    # Generate diary from personal notes
    python journal-keeper.py diary --input notes.txt --date 2025-11-03

    # Auto-generate from current session
    python journal-keeper.py auto --mode log
"""

import os
import sys
import json
import argparse
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Paths
BRAIN_DIR = Path("/home/claude/brain")
LOG_DIR = BRAIN_DIR / "log"
DIARY_DIR = BRAIN_DIR / "diary"

# Load environment
from dotenv import load_dotenv
load_dotenv(BRAIN_DIR / ".env")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Colors
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color


def generate_log_entry_with_ai(content: str, topic: str, date: str = None) -> str:
    """
    Generate structured log entry from session content using AI.
    """

    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    prompt = f"""Generate a technical log entry from this session transcript.

Date: {date}
Topic: {topic}

Session content:
```
{content}
```

Create a structured markdown log following this format:

# {{Topic}} - {{Descriptive Title}}

**Date**: {date}
**Projects**: [List relevant projects]
**People**: [List people mentioned]
**Tags**: #tag1 #tag2

---

## Context

[Brief overview of why this work was done]

## What We Did

[Bullet points of concrete actions taken, code written, files modified]

## Technical Details

[Important technical decisions, architectures, patterns used]

## Decisions Made

[Key decisions and their rationale]

## Next Steps

- [ ] Task 1
- [ ] Task 2

---

**Files modified**: {{commit_info}}

Keep it concise but complete. Focus on WHAT was done and WHY, not play-by-play.
Use bullet points liberally. Reference specific files with paths.

Return ONLY the markdown, no wrapper or explanation."""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "anthropic/claude-3.5-sonnet",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 4000
    }

    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=data, timeout=60)
        response.raise_for_status()

        result = response.json()
        content = result['choices'][0]['message']['content']

        # Clean up markdown wrapper if present
        if content.startswith('```markdown'):
            content = content[len('```markdown'):].strip()
        if content.endswith('```'):
            content = content[:-3].strip()

        return content

    except Exception as e:
        print(f"{RED}❌ AI generation failed: {e}{NC}", file=sys.stderr)
        return None


def generate_diary_entry_with_ai(content: str, date: str = None) -> str:
    """
    Generate personal diary entry from notes using AI.
    """

    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    prompt = f"""Generate a personal diary entry from these notes.

Date: {date}

Notes:
```
{content}
```

Create a diary entry following this format:

# Diary - {date}

**Date**: {date}
**Mood**: [Describe overall mood/energy]
**Tags**: #personal #life #tag

---

## Today

[What happened today - events, people, places]

## Thoughts

[Personal reflections, feelings, insights]

## Highlights

- Positive moment 1
- Positive moment 2

## Challenges

[Any difficulties or concerns]

## Gratitude

[Things to be grateful for]

---

Keep it personal, honest, reflective. This is PRIVATE.
Focus on experiences, emotions, relationships, personal growth.

Return ONLY the markdown, no wrapper or explanation."""

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "anthropic/claude-3.5-sonnet",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5,  # Slightly higher for personal writing
        "max_tokens": 4000
    }

    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=data, timeout=60)
        response.raise_for_status()

        result = response.json()
        content = result['choices'][0]['message']['content']

        # Clean up markdown wrapper
        if content.startswith('```markdown'):
            content = content[len('```markdown'):].strip()
        if content.endswith('```'):
            content = content[:-3].strip()

        return content

    except Exception as e:
        print(f"{RED}❌ AI generation failed: {e}{NC}", file=sys.stderr)
        return None


def save_log_entry(content: str, date: str, topic: str, dry_run: bool = True) -> Optional[Path]:
    """Save log entry to log/YYYY/ directory."""

    year = date[:4]
    log_year_dir = LOG_DIR / year

    if not dry_run:
        log_year_dir.mkdir(parents=True, exist_ok=True)

    # Slugify topic for filename
    slug = topic.lower().replace(' ', '-').replace('/', '-')
    filename = f"{date}-{slug}.md"
    file_path = log_year_dir / filename

    if dry_run:
        print(f"\n{YELLOW}📝 DRY-RUN: Would create log entry{NC}")
        print(f"Path: {file_path.relative_to(BRAIN_DIR)}")
        print(f"Preview (first 300 chars):")
        print("-" * 60)
        print(content[:300] + ("..." if len(content) > 300 else ""))
        print("-" * 60)
        return file_path
    else:
        with open(file_path, 'w') as f:
            f.write(content)

        print(f"{GREEN}✅ Log entry created{NC}")
        print(f"Path: {file_path.relative_to(BRAIN_DIR)}")
        return file_path


def save_diary_entry(content: str, date: str, dry_run: bool = True) -> Optional[Path]:
    """Save diary entry to diary/YYYY/ directory."""

    year = date[:4]
    diary_year_dir = DIARY_DIR / year

    if not dry_run:
        diary_year_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{date}-diary.md"
    file_path = diary_year_dir / filename

    if dry_run:
        print(f"\n{YELLOW}📔 DRY-RUN: Would create diary entry{NC}")
        print(f"Path: {file_path.relative_to(BRAIN_DIR)}")
        print(f"Preview (first 300 chars):")
        print("-" * 60)
        print(content[:300] + ("..." if len(content) > 300 else ""))
        print("-" * 60)
        return file_path
    else:
        with open(file_path, 'w') as f:
            f.write(content)

        print(f"{GREEN}✅ Diary entry created{NC}")
        print(f"Path: {file_path.relative_to(BRAIN_DIR)}")
        return file_path


def main():
    parser = argparse.ArgumentParser(description="Journal Keeper - Auto-generate log/diary entries")

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Log command
    log_parser = subparsers.add_parser('log', help='Generate log entry')
    log_parser.add_argument('--input', required=True, help='Input file with session content')
    log_parser.add_argument('--topic', required=True, help='Topic/title for the log')
    log_parser.add_argument('--date', help='Date (YYYY-MM-DD), default today')
    log_parser.add_argument('--dry-run', action='store_true', default=True)
    log_parser.add_argument('--apply', action='store_true', help='Actually create file')

    # Diary command
    diary_parser = subparsers.add_parser('diary', help='Generate diary entry')
    diary_parser.add_argument('--input', required=True, help='Input file with notes')
    diary_parser.add_argument('--date', help='Date (YYYY-MM-DD), default today')
    diary_parser.add_argument('--dry-run', action='store_true', default=True)
    diary_parser.add_argument('--apply', action='store_true', help='Actually create file')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Read input
    input_file = Path(args.input)
    if not input_file.exists():
        print(f"{RED}❌ Input file not found: {args.input}{NC}", file=sys.stderr)
        sys.exit(1)

    with open(input_file, 'r') as f:
        input_content = f.read()

    dry_run = not args.apply
    date = args.date or datetime.now().strftime("%Y-%m-%d")

    print(f"\n{BLUE}📖 Journal Keeper{NC}")
    print(f"Mode: {YELLOW}DRY-RUN{NC}" if dry_run else f"Mode: {GREEN}APPLY{NC}")
    print()

    # Execute command
    if args.command == 'log':
        print("📝 Generating log entry with AI...")

        entry_content = generate_log_entry_with_ai(input_content, args.topic, date)

        if entry_content:
            save_log_entry(entry_content, date, args.topic, dry_run)
        else:
            print(f"{RED}❌ Failed to generate log entry{NC}")
            sys.exit(1)

    elif args.command == 'diary':
        print("📔 Generating diary entry with AI...")

        entry_content = generate_diary_entry_with_ai(input_content, date)

        if entry_content:
            save_diary_entry(entry_content, date, dry_run)
        else:
            print(f"{RED}❌ Failed to generate diary entry{NC}")
            sys.exit(1)

    if dry_run:
        print(f"\n{YELLOW}💡 Run with --apply to create the file{NC}")


if __name__ == "__main__":
    main()
