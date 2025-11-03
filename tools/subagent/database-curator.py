#!/usr/bin/env python3
"""
Database Curator Subagent

Extracts entities from text (emails, conversations, logs) and automatically
creates/updates database entries with proper frontmatter YAML.

Usage:
    # From file
    python database-curator.py --file email.txt

    # From stdin
    echo "Met with Marco from DigitalCo" | python database-curator.py

    # Specific entity type
    python database-curator.py --type person --file conversation.txt

    # Dry-run mode (preview only)
    python database-curator.py --dry-run < input.txt
"""

import os
import sys
import json
import yaml
import re
import argparse
import requests
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Paths
BRAIN_DIR = Path("/home/claude/brain")
DATABASE_DIR = BRAIN_DIR / "database"
SCHEMAS_DIR = DATABASE_DIR / ".schemas"

# Load environment variables
from dotenv import load_dotenv
load_dotenv(BRAIN_DIR / ".env")

# OpenRouter API
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Colors
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color


def load_schema(entity_type: str) -> Dict:
    """Load schema for entity type."""
    schema_file = SCHEMAS_DIR / f"{entity_type}.schema.yaml"

    if not schema_file.exists():
        return None

    with open(schema_file, 'r') as f:
        # Parse YAML, skip comments
        content = f.read()
        # Extract only the structured part (after comments)
        lines = [l for l in content.split('\n') if not l.strip().startswith('#')]
        schema_yaml = '\n'.join(lines)

        try:
            return yaml.safe_load(schema_yaml)
        except:
            return None


def extract_entities_with_ai(text: str, entity_type: Optional[str] = None) -> List[Dict]:
    """
    Use AI to extract entities from text.
    Returns list of entities with metadata.
    """

    prompt = f"""Extract entities from this text and return as JSON.

Entity types to extract: {"all types (people, companies, servers, places, technologies)" if not entity_type else entity_type}

Text:
```
{text}
```

Return JSON array with this structure:
[
  {{
    "type": "person|company|server|place|tech",
    "name": "Full name",
    "email": "email if mentioned",
    "role": "role/description if mentioned",
    "relationship": "cliente|collaboratore informale|fornitore|amico|familiare",
    "company": "associated company if mentioned",
    "confidence": 0.0-1.0
  }}
]

Only extract REAL entities mentioned in the text. Be conservative - if not explicitly mentioned, don't include it.
For people, try to infer relationship type from context.
Return ONLY valid JSON, no markdown formatting."""

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
        "max_tokens": 2000
    }

    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()

        result = response.json()
        content = result['choices'][0]['message']['content']

        # Extract JSON from response (might be wrapped in markdown)
        json_match = re.search(r'```(?:json)?\s*(\[.*?\])\s*```', content, re.DOTALL)
        if json_match:
            content = json_match.group(1)

        entities = json.loads(content)
        return entities

    except Exception as e:
        print(f"{RED}❌ AI extraction failed: {e}{NC}", file=sys.stderr)
        return []


def slugify(text: str) -> str:
    """Convert text to filesystem-safe slug."""
    # Convert to lowercase
    text = text.lower()
    # Replace spaces and special chars with hyphens
    text = re.sub(r'[^a-z0-9]+', '-', text)
    # Remove leading/trailing hyphens
    text = text.strip('-')
    return text


def entity_exists(entity_type: str, name: str) -> Optional[Path]:
    """Check if entity already exists in database. Returns path if found."""
    entity_dir = DATABASE_DIR / entity_type

    if not entity_dir.exists():
        return None

    # Try exact filename match
    slug = slugify(name)
    exact_file = entity_dir / f"{slug}.md"

    if exact_file.exists():
        return exact_file

    # Try fuzzy match (search in files)
    for file in entity_dir.glob("*.md"):
        if file.name.startswith('.') or 'template' in file.name.lower():
            continue

        with open(file, 'r') as f:
            content = f.read()
            # Check frontmatter name field
            if content.startswith('---'):
                try:
                    # Extract frontmatter
                    _, fm, _ = content.split('---', 2)
                    frontmatter = yaml.safe_load(fm)
                    if frontmatter.get('name', '').lower() == name.lower():
                        return file
                except:
                    pass

    return None


def create_entity(entity: Dict, dry_run: bool = True) -> Optional[Path]:
    """Create new entity file with frontmatter."""

    entity_type = entity.get('type')
    name = entity.get('name')

    if not entity_type or not name:
        print(f"{RED}❌ Missing type or name{NC}", file=sys.stderr)
        return None

    # Map type to directory
    type_map = {
        'person': 'people',
        'company': 'company',
        'server': 'server',
        'place': 'place',
        'tech': 'tech'
    }

    dir_name = type_map.get(entity_type, entity_type)
    entity_dir = DATABASE_DIR / dir_name

    if not entity_dir.exists():
        print(f"{YELLOW}⚠️  Directory not found: {entity_dir}{NC}", file=sys.stderr)
        return None

    # Load schema
    schema_name = 'person' if entity_type == 'person' else entity_type
    schema = load_schema(schema_name)

    # Create frontmatter
    today = datetime.now().strftime("%Y-%m-%d")

    frontmatter = {
        "name": name,
        "created_at": today,
        "updated_at": today
    }

    # Add optional fields from entity
    optional_fields = ['email', 'role', 'relationship', 'company', 'phone',
                       'website', 'location', 'tags', 'type', 'status']

    for field in optional_fields:
        if field in entity and entity[field]:
            frontmatter[field] = entity[field]

    # Create file content
    frontmatter_yaml = yaml.dump(frontmatter, default_flow_style=False,
                                  allow_unicode=True, sort_keys=False)

    content = f"""---
{frontmatter_yaml}---

# {name}

## Info

[Auto-generated by database-curator on {today}]

"""

    # Determine filename
    slug = slugify(name)
    file_path = entity_dir / f"{slug}.md"

    if dry_run:
        print(f"{YELLOW}CREATE{NC} {file_path.relative_to(DATABASE_DIR)}")
        print(f"  Fields: {list(frontmatter.keys())}")
        return file_path
    else:
        with open(file_path, 'w') as f:
            f.write(content)

        print(f"{GREEN}✅ CREATED{NC} {file_path.relative_to(DATABASE_DIR)}")
        print(f"  Fields: {list(frontmatter.keys())}")
        return file_path


def update_entity(file_path: Path, entity: Dict, dry_run: bool = True) -> bool:
    """Update existing entity with new information."""

    with open(file_path, 'r') as f:
        content = f.read()

    if not content.startswith('---'):
        print(f"{RED}❌ No frontmatter in {file_path.name}{NC}", file=sys.stderr)
        return False

    try:
        # Split frontmatter and content
        _, fm_str, body = content.split('---', 2)
        frontmatter = yaml.safe_load(fm_str)

        # Update fields
        updated = False
        changes = []

        update_fields = ['email', 'role', 'relationship', 'company', 'phone',
                        'website', 'location', 'tags', 'type', 'status']

        for field in update_fields:
            if field in entity and entity[field]:
                # Only update if field is empty or different
                if field not in frontmatter or frontmatter[field] != entity[field]:
                    frontmatter[field] = entity[field]
                    updated = True
                    changes.append(field)

        if updated:
            # Update timestamp
            frontmatter['updated_at'] = datetime.now().strftime("%Y-%m-%d")
            changes.append('updated_at')

            # Recreate content
            frontmatter_yaml = yaml.dump(frontmatter, default_flow_style=False,
                                        allow_unicode=True, sort_keys=False)
            new_content = f"---\n{frontmatter_yaml}---{body}"

            if dry_run:
                print(f"{YELLOW}UPDATE{NC} {file_path.relative_to(DATABASE_DIR)}")
                print(f"  Changes: {changes}")
            else:
                with open(file_path, 'w') as f:
                    f.write(new_content)

                print(f"{GREEN}✅ UPDATED{NC} {file_path.relative_to(DATABASE_DIR)}")
                print(f"  Changes: {changes}")

            return True
        else:
            print(f"{BLUE}SKIP{NC} {file_path.relative_to(DATABASE_DIR)} - no changes needed")
            return False

    except Exception as e:
        print(f"{RED}❌ Update failed for {file_path.name}: {e}{NC}", file=sys.stderr)
        return False


def process_entities(text: str, entity_type: Optional[str] = None,
                     dry_run: bool = True) -> Dict[str, int]:
    """
    Process text and extract/create/update entities.
    Returns stats dict.
    """

    print(f"\n{BLUE}🤖 Database Curator{NC}")
    print(f"Mode: {YELLOW}DRY-RUN{NC}" if dry_run else f"Mode: {GREEN}APPLY{NC}")
    print()

    # Extract entities with AI
    print("📝 Extracting entities from text...")
    entities = extract_entities_with_ai(text, entity_type)

    if not entities:
        print(f"{YELLOW}⚠️  No entities found{NC}")
        return {'created': 0, 'updated': 0, 'skipped': 0}

    print(f"Found {len(entities)} potential entities\n")

    stats = {'created': 0, 'updated': 0, 'skipped': 0, 'failed': 0}

    for entity in entities:
        # Skip low confidence
        if entity.get('confidence', 1.0) < 0.5:
            print(f"{YELLOW}⚠️  Skipping {entity.get('name')} - low confidence{NC}")
            stats['skipped'] += 1
            continue

        entity_type = entity.get('type')
        name = entity.get('name')

        # Map person -> people directory
        dir_type = 'people' if entity_type == 'person' else entity_type

        # Check if exists
        existing = entity_exists(dir_type, name)

        if existing:
            # Update
            if update_entity(existing, entity, dry_run):
                stats['updated'] += 1
            else:
                stats['skipped'] += 1
        else:
            # Create
            result = create_entity(entity, dry_run)
            if result:
                stats['created'] += 1
            else:
                stats['failed'] += 1

        print()

    # Summary
    print("="*60)
    print("📊 Summary")
    print("="*60)
    print(f"  Created: {stats['created']}")
    print(f"  Updated: {stats['updated']}")
    print(f"  Skipped: {stats['skipped']}")
    print(f"  Failed: {stats['failed']}")
    print("="*60)

    return stats


def main():
    parser = argparse.ArgumentParser(description="Database Curator - Extract and manage entities")
    parser.add_argument('--file', type=str, help="Read text from file")
    parser.add_argument('--type', choices=['person', 'company', 'server', 'place', 'tech'],
                       help="Extract only specific entity type")
    parser.add_argument('--dry-run', action='store_true', default=True,
                       help="Preview only (default)")
    parser.add_argument('--apply', action='store_true',
                       help="Apply changes")

    args = parser.parse_args()

    # Determine dry-run mode
    dry_run = not args.apply

    # Get input text
    if args.file:
        with open(args.file, 'r') as f:
            text = f.read()
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        print("Error: Provide input via --file or stdin", file=sys.stderr)
        sys.exit(1)

    if not text.strip():
        print("Error: Empty input", file=sys.stderr)
        sys.exit(1)

    # Process
    stats = process_entities(text, args.type, dry_run)

    if dry_run:
        print(f"\n{YELLOW}💡 Run with --apply to make changes{NC}")

    sys.exit(0)


if __name__ == "__main__":
    main()
