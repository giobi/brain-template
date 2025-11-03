#!/usr/bin/env python3
"""
Database Frontmatter Migration Script

Aggiunge frontmatter YAML a tutti i file del database che non ce l'hanno.
Analizza il contenuto esistente per estrarre metadati dove possibile.

Usage:
    python migrate-add-frontmatter.py           # dry-run mode (preview only)
    python migrate-add-frontmatter.py --apply   # apply changes
    python migrate-add-frontmatter.py --entity-type people  # migrate only people
"""

import os
import re
import yaml
from pathlib import Path
from datetime import datetime
import argparse
import shutil

# Paths
BRAIN_DIR = Path("/home/claude/brain")
DATABASE_DIR = BRAIN_DIR / "database"
BACKUP_DIR = DATABASE_DIR / "backup" / "migrations"

# Entity types
ENTITY_TYPES = ["people", "company", "server", "place", "tech"]

# Colors
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color


def has_frontmatter(content: str) -> bool:
    """Check if file already has YAML frontmatter."""
    return content.strip().startswith('---')


def extract_name_from_content(content: str, filename: str) -> str:
    """Extract entity name from first H1 heading or filename."""
    # Try to find first H1
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()

    # Fallback: beautify filename
    name = filename.replace('.md', '').replace('-', ' ').title()
    return name


def extract_email_from_content(content: str) -> str:
    """Extract email address from content."""
    match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
    return match.group(0) if match else None


def extract_tags_from_content(content: str) -> list:
    """Extract tags from content (looks for #tag patterns)."""
    tags = re.findall(r'#(\w+)', content)
    # Remove common markdown headers that aren't tags
    excluded = ['h1', 'h2', 'h3', 'h4', 'overview', 'info', 'note', 'notes']
    return [tag for tag in tags if tag.lower() not in excluded]


def generate_person_frontmatter(content: str, filename: str) -> dict:
    """Generate frontmatter for person entity."""
    name = extract_name_from_content(content, filename)
    email = extract_email_from_content(content)
    tags = extract_tags_from_content(content)

    today = datetime.now().strftime("%Y-%m-%d")

    frontmatter = {
        "name": name,
        "created_at": today,
        "updated_at": today
    }

    if email:
        frontmatter["email"] = email
    if tags:
        frontmatter["tags"] = tags

    return frontmatter


def generate_company_frontmatter(content: str, filename: str) -> dict:
    """Generate frontmatter for company entity."""
    name = extract_name_from_content(content, filename)
    email = extract_email_from_content(content)
    tags = extract_tags_from_content(content)

    # Try to extract type
    type_match = re.search(r'\*\*Tipo[:\*]*\s*(.+)', content, re.IGNORECASE)
    entity_type = type_match.group(1).strip() if type_match else None

    # Try to extract first contact date
    date_match = re.search(r'\*\*Primo contatto[:\*]*\s*(\d{4}-\d{2}(?:-\d{2})?)', content, re.IGNORECASE)
    first_contact = date_match.group(1) if date_match else None

    # Try to extract status
    status_match = re.search(r'\*\*Status[:\*]*\s*(.+)', content, re.IGNORECASE)
    status = status_match.group(1).strip() if status_match else None

    today = datetime.now().strftime("%Y-%m-%d")

    frontmatter = {
        "name": name,
        "created_at": today,
        "updated_at": today
    }

    if entity_type:
        frontmatter["type"] = entity_type
    if first_contact:
        frontmatter["first_contact"] = first_contact
    if status:
        frontmatter["status"] = status
    if email:
        frontmatter["email"] = email
    if tags:
        frontmatter["tags"] = tags

    return frontmatter


def generate_server_frontmatter(content: str, filename: str) -> dict:
    """Generate frontmatter for server entity."""
    name = extract_name_from_content(content, filename)

    # Try to extract IP
    ip_match = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', content)
    ip_address = ip_match.group(0) if ip_match else None

    # Try to extract provider
    providers = ["digitalocean", "aws", "cloudways", "vultr", "hetzner", "linode"]
    provider = None
    for p in providers:
        if p.lower() in content.lower():
            provider = p
            break

    today = datetime.now().strftime("%Y-%m-%d")

    frontmatter = {
        "name": name,
        "created_at": today,
        "updated_at": today
    }

    if ip_address:
        frontmatter["ip_address"] = ip_address
    if provider:
        frontmatter["provider"] = provider

    return frontmatter


def generate_place_frontmatter(content: str, filename: str) -> dict:
    """Generate frontmatter for place entity."""
    name = extract_name_from_content(content, filename)
    tags = extract_tags_from_content(content)

    today = datetime.now().strftime("%Y-%m-%d")

    frontmatter = {
        "name": name,
        "created_at": today,
        "updated_at": today
    }

    if tags:
        frontmatter["tags"] = tags

    return frontmatter


def generate_tech_frontmatter(content: str, filename: str) -> dict:
    """Generate frontmatter for tech entity."""
    name = extract_name_from_content(content, filename)
    tags = extract_tags_from_content(content)

    today = datetime.now().strftime("%Y-%m-%d")

    frontmatter = {
        "name": name,
        "created_at": today,
        "updated_at": today
    }

    if tags:
        frontmatter["tags"] = tags

    return frontmatter


def generate_frontmatter(entity_type: str, content: str, filename: str) -> dict:
    """Generate appropriate frontmatter based on entity type."""
    generators = {
        "people": generate_person_frontmatter,
        "company": generate_company_frontmatter,
        "server": generate_server_frontmatter,
        "place": generate_place_frontmatter,
        "tech": generate_tech_frontmatter
    }

    generator = generators.get(entity_type)
    if not generator:
        raise ValueError(f"Unknown entity type: {entity_type}")

    return generator(content, filename)


def add_frontmatter_to_file(file_path: Path, entity_type: str, dry_run: bool = True) -> bool:
    """
    Add frontmatter to a single file.
    Returns True if file was modified (or would be in dry-run).
    """
    # Read current content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already has frontmatter
    if has_frontmatter(content):
        print(f"  {BLUE}SKIP{NC} {file_path.name} - already has frontmatter")
        return False

    # Generate frontmatter
    frontmatter = generate_frontmatter(entity_type, content, file_path.name)

    # Create new content with frontmatter
    frontmatter_yaml = yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True, sort_keys=False)
    new_content = f"---\n{frontmatter_yaml}---\n\n{content}"

    if dry_run:
        print(f"  {YELLOW}PREVIEW{NC} {file_path.name}")
        print(f"    Would add: {list(frontmatter.keys())}")
        return True
    else:
        # Backup original
        backup_path = BACKUP_DIR / datetime.now().strftime("%Y-%m-%d_%H%M%S") / file_path.relative_to(DATABASE_DIR)
        backup_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file_path, backup_path)

        # Write new content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        print(f"  {GREEN}MIGRATED{NC} {file_path.name}")
        print(f"    Added: {list(frontmatter.keys())}")
        print(f"    Backup: {backup_path}")
        return True


def migrate_entity_type(entity_type: str, dry_run: bool = True):
    """Migrate all files for a specific entity type."""
    entity_dir = DATABASE_DIR / entity_type

    if not entity_dir.exists():
        print(f"{YELLOW}⚠️  Directory not found: {entity_dir}{NC}")
        return

    print(f"\n{BLUE}📁 {entity_type.upper()}{NC}")

    # Get all .md files (exclude templates and hidden files)
    md_files = [f for f in entity_dir.glob("*.md")
                if not f.name.startswith('.') and not f.name.startswith('template')]

    if not md_files:
        print(f"  No files to migrate")
        return

    modified_count = 0
    for file_path in sorted(md_files):
        if add_frontmatter_to_file(file_path, entity_type, dry_run):
            modified_count += 1

    print(f"\n  Total: {len(md_files)} files, {modified_count} {'would be ' if dry_run else ''}modified")


def main():
    parser = argparse.ArgumentParser(description="Migrate database files to frontmatter YAML")
    parser.add_argument('--apply', action='store_true', help="Apply changes (default is dry-run)")
    parser.add_argument('--entity-type', choices=ENTITY_TYPES, help="Migrate only specific entity type")
    args = parser.parse_args()

    dry_run = not args.apply

    print("🔄 Database Frontmatter Migration")
    print(f"Mode: {YELLOW}DRY-RUN (preview only){NC}" if dry_run else f"Mode: {RED}APPLY CHANGES{NC}")
    print(f"Database: {DATABASE_DIR}")
    print()

    if not dry_run:
        # Create backup directory
        BACKUP_DIR.mkdir(parents=True, exist_ok=True)
        print(f"📦 Backups: {BACKUP_DIR}\n")

    # Migrate specific type or all
    if args.entity_type:
        migrate_entity_type(args.entity_type, dry_run)
    else:
        for entity_type in ENTITY_TYPES:
            migrate_entity_type(entity_type, dry_run)

    print("\n" + "="*60)
    if dry_run:
        print(f"{YELLOW}✨ Preview complete. Run with --apply to make changes.{NC}")
    else:
        print(f"{GREEN}✅ Migration complete!{NC}")
    print("="*60)


if __name__ == "__main__":
    main()
