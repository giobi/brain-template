#!/usr/bin/env python3
"""
Consolidate database/person/ → database/people/

Moves all files from person/ to people/, handling duplicates intelligently.
If file exists in both locations, keeps the one with frontmatter or most recent.

Usage:
    python consolidate-person-to-people.py           # dry-run mode
    python consolidate-person-to-people.py --apply   # apply changes
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
import argparse

# Paths
BRAIN_DIR = Path("/home/claude/brain")
DATABASE_DIR = BRAIN_DIR / "database"
PERSON_DIR = DATABASE_DIR / "person"
PEOPLE_DIR = DATABASE_DIR / "people"
BACKUP_DIR = DATABASE_DIR / "backup" / "consolidation"

# Colors
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color


def has_frontmatter(file_path: Path) -> bool:
    """Check if file has YAML frontmatter."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()
    return content.startswith('---')


def get_file_size(file_path: Path) -> int:
    """Get file size in bytes."""
    return file_path.stat().st_size


def get_modification_time(file_path: Path) -> float:
    """Get file modification timestamp."""
    return file_path.stat().st_mtime


def choose_better_file(old_file: Path, new_file: Path) -> Path:
    """
    Decide which file to keep when duplicate exists.
    Priority:
    1. File with frontmatter
    2. Larger file (more content)
    3. Most recently modified
    """
    old_has_fm = has_frontmatter(old_file)
    new_has_fm = has_frontmatter(new_file)

    # If one has frontmatter and other doesn't, choose frontmatter
    if new_has_fm and not old_has_fm:
        return new_file
    if old_has_fm and not new_has_fm:
        return old_file

    # Both have or both don't have frontmatter - compare size
    old_size = get_file_size(old_file)
    new_size = get_file_size(new_file)

    if new_size > old_size:
        return new_file
    if old_size > new_size:
        return old_file

    # Same size - choose most recent
    if get_modification_time(new_file) > get_modification_time(old_file):
        return new_file

    return old_file


def consolidate_files(dry_run: bool = True):
    """Consolidate all files from person/ to people/."""

    if not PERSON_DIR.exists():
        print(f"{RED}❌ Directory not found: {PERSON_DIR}{NC}")
        return

    if not PEOPLE_DIR.exists():
        PEOPLE_DIR.mkdir(parents=True, exist_ok=True)
        print(f"{GREEN}✅ Created directory: {PEOPLE_DIR}{NC}")

    # Get all .md files from person/ (exclude templates and hidden)
    person_files = [f for f in PERSON_DIR.glob("*.md")
                    if not f.name.startswith('.') and 'template' not in f.name.lower()]

    if not person_files:
        print(f"{YELLOW}⚠️  No files to consolidate in {PERSON_DIR}{NC}")
        return

    print(f"\n{BLUE}📁 Consolidating {len(person_files)} files from person/ to people/{NC}\n")

    stats = {
        'moved': 0,
        'merged_kept_new': 0,
        'merged_kept_old': 0,
        'skipped': 0
    }

    for source_file in sorted(person_files):
        dest_file = PEOPLE_DIR / source_file.name

        # Case 1: File doesn't exist in people/ - simple move
        if not dest_file.exists():
            if dry_run:
                print(f"  {YELLOW}MOVE{NC} {source_file.name} → people/")
            else:
                shutil.move(source_file, dest_file)
                print(f"  {GREEN}MOVED{NC} {source_file.name} → people/")
            stats['moved'] += 1

        # Case 2: File exists in both - need to choose
        else:
            better_file = choose_better_file(dest_file, source_file)

            if better_file == source_file:
                # New file is better - replace
                if dry_run:
                    print(f"  {YELLOW}REPLACE{NC} {source_file.name} (person/ version better)")
                    print(f"    Reason: ", end='')
                    if has_frontmatter(source_file) and not has_frontmatter(dest_file):
                        print("has frontmatter")
                    elif get_file_size(source_file) > get_file_size(dest_file):
                        print(f"larger ({get_file_size(source_file)} vs {get_file_size(dest_file)} bytes)")
                    else:
                        print("more recent")
                else:
                    # Backup old version
                    backup_path = BACKUP_DIR / datetime.now().strftime("%Y-%m-%d_%H%M%S") / dest_file.name
                    backup_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(dest_file, backup_path)

                    # Replace with new
                    shutil.move(source_file, dest_file)
                    print(f"  {GREEN}REPLACED{NC} {source_file.name} (person/ version better)")
                    print(f"    Backup: {backup_path}")

                stats['merged_kept_new'] += 1

            else:
                # Old file is better - keep it, delete source
                if dry_run:
                    print(f"  {BLUE}KEEP{NC} {source_file.name} (people/ version better)")
                    print(f"    Reason: ", end='')
                    if has_frontmatter(dest_file) and not has_frontmatter(source_file):
                        print("has frontmatter")
                    elif get_file_size(dest_file) > get_file_size(source_file):
                        print(f"larger ({get_file_size(dest_file)} vs {get_file_size(source_file)} bytes)")
                    else:
                        print("more recent")
                else:
                    # Backup person/ version before deleting
                    backup_path = BACKUP_DIR / datetime.now().strftime("%Y-%m-%d_%H%M%S") / "person" / source_file.name
                    backup_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(source_file, backup_path)

                    # Delete source
                    source_file.unlink()
                    print(f"  {BLUE}KEPT{NC} {source_file.name} (people/ version better)")
                    print(f"    Backup of person/ version: {backup_path}")

                stats['merged_kept_old'] += 1

    # Report
    print("\n" + "="*60)
    print("📊 Consolidation Summary")
    print("="*60)
    print(f"  Moved (new): {stats['moved']}")
    print(f"  Merged (kept person/ version): {stats['merged_kept_new']}")
    print(f"  Merged (kept people/ version): {stats['merged_kept_old']}")
    print(f"  Total files processed: {len(person_files)}")
    print("="*60)

    # Delete person/ directory if empty and not dry-run
    if not dry_run:
        remaining = list(PERSON_DIR.glob("*"))
        if not remaining:
            PERSON_DIR.rmdir()
            print(f"\n{GREEN}✅ Deleted empty directory: {PERSON_DIR}{NC}")
        else:
            print(f"\n{YELLOW}⚠️  Directory not empty (has {len(remaining)} files): {PERSON_DIR}{NC}")


def main():
    parser = argparse.ArgumentParser(description="Consolidate person/ to people/")
    parser.add_argument('--apply', action='store_true', help="Apply changes (default is dry-run)")
    args = parser.parse_args()

    dry_run = not args.apply

    print("🔄 Database Consolidation: person/ → people/")
    print(f"Mode: {YELLOW}DRY-RUN (preview only){NC}" if dry_run else f"Mode: {RED}APPLY CHANGES{NC}")
    print(f"Source: {PERSON_DIR}")
    print(f"Dest: {PEOPLE_DIR}")
    print()

    if not dry_run:
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        print(f"📦 Backups: {BACKUP_DIR}\n")

    consolidate_files(dry_run)

    print("\n" + "="*60)
    if dry_run:
        print(f"{YELLOW}✨ Preview complete. Run with --apply to make changes.{NC}")
    else:
        print(f"{GREEN}✅ Consolidation complete!{NC}")
    print("="*60)


if __name__ == "__main__":
    main()
