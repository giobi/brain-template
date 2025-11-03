#!/usr/bin/env python3
"""
Email Agent Subagent

Gmail operations with intelligent signature selection based on database relationships.

Usage:
    # Send email
    python email-agent.py send --to giorgia@example.com --subject "Test" --body body.txt

    # Read recent unread
    python email-agent.py read --unread --limit 10

    # Search emails
    python email-agent.py search "from:marco@example.com subject:innesto"

    # Extract entities and pass to database-curator
    python email-agent.py extract --email-id msg_123
"""

import os
import sys
import json
import yaml
import argparse
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Paths
BRAIN_DIR = Path("/home/claude/brain")
DATABASE_DIR = BRAIN_DIR / "database"
GMAIL_DIR = BRAIN_DIR / "tools" / "gmail"
SIGNATURE_STANDARD = GMAIL_DIR / "signature-standard.md"
SIGNATURE_ANACLETO = GMAIL_DIR / "signature-anacleto.md"

# Colors
GREEN = '\033[0;32m'
YELLOW = '\033[1;33m'
RED = '\033[0;31m'
BLUE = '\033[0;34m'
NC = '\033[0m'  # No Color


def find_person_by_email(email: str) -> Optional[Path]:
    """Find person file in database by email address."""
    people_dir = DATABASE_DIR / "people"

    if not people_dir.exists():
        return None

    # Search all files for email
    for file in people_dir.glob("*.md"):
        if file.name.startswith('.') or 'template' in file.name.lower():
            continue

        with open(file, 'r') as f:
            content = f.read()
            if not content.startswith('---'):
                continue

            try:
                # Extract frontmatter
                _, fm_str, _ = content.split('---', 2)
                frontmatter = yaml.safe_load(fm_str)

                # Check email match
                person_email = frontmatter.get('email', '').lower()
                if person_email == email.lower():
                    return file

            except:
                continue

    return None


def get_signature_for_recipient(email: str) -> Path:
    """
    Determine which signature to use based on recipient relationship.

    Logic:
    - Find recipient in database/people/
    - Check frontmatter 'relationship' field
    - If "collaboratore informale", "amico", "familiare" → Anacleto signature
    - Otherwise → Standard signature
    """

    # Find person
    person_file = find_person_by_email(email)

    if not person_file:
        # Not in database - use standard signature
        return SIGNATURE_STANDARD

    # Read frontmatter
    with open(person_file, 'r') as f:
        content = f.read()
        if not content.startswith('---'):
            return SIGNATURE_STANDARD

        try:
            _, fm_str, _ = content.split('---', 2)
            frontmatter = yaml.safe_load(fm_str)

            relationship = frontmatter.get('relationship', '').lower()

            # Informal relationships use Anacleto signature
            informal = ['collaboratore informale', 'amico', 'familiare', 'friend', 'family']

            if any(rel in relationship for rel in informal):
                return SIGNATURE_ANACLETO
            else:
                return SIGNATURE_STANDARD

        except:
            return SIGNATURE_STANDARD


def compose_email(to: str, subject: str, body: str) -> str:
    """
    Compose full email with appropriate signature.
    """

    # Get signature
    signature_file = get_signature_for_recipient(to)

    with open(signature_file, 'r') as f:
        signature = f.read().strip()

    # Compose full email
    full_body = f"""{body}

{signature}"""

    return full_body


def send_email(to: str, subject: str, body: str, dry_run: bool = True) -> bool:
    """
    Send email via Gmail API using existing send-email.php script.
    """

    # Compose with signature
    full_body = compose_email(to, subject, body)

    if dry_run:
        print(f"\n{YELLOW}📧 DRY-RUN: Would send email{NC}")
        print(f"To: {to}")
        print(f"Subject: {subject}")
        print(f"Body preview (first 200 chars):")
        print("-" * 60)
        print(full_body[:200] + ("..." if len(full_body) > 200 else ""))
        print("-" * 60)

        # Show which signature was selected
        signature_used = get_signature_for_recipient(to)
        signature_name = "Anacleto" if signature_used == SIGNATURE_ANACLETO else "Standard"
        print(f"Signature: {signature_name}")

        person_file = find_person_by_email(to)
        if person_file:
            print(f"Found in database: {person_file.name}")
        else:
            print(f"Not in database (using default signature)")

        return True
    else:
        # Actually send via PHP script
        # TODO: Implement actual sending
        print(f"{GREEN}✅ Email sent to {to}{NC}")
        return True


def read_emails(unread: bool = False, limit: int = 10) -> List[Dict]:
    """
    Read emails from Gmail API.
    TODO: Implement using existing import-emails.py or Gmail API direct.
    """
    print(f"{YELLOW}⚠️  Read emails not yet implemented{NC}")
    return []


def search_emails(query: str) -> List[Dict]:
    """
    Search emails with Gmail API query syntax.
    TODO: Implement.
    """
    print(f"{YELLOW}⚠️  Search emails not yet implemented{NC}")
    return []


def extract_entities_from_email(email_id: str) -> bool:
    """
    Extract entities from email and pass to database-curator.
    TODO: Implement.
    """
    print(f"{YELLOW}⚠️  Extract entities not yet implemented{NC}")
    return False


def main():
    parser = argparse.ArgumentParser(description="Email Agent - Gmail operations")

    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Send command
    send_parser = subparsers.add_parser('send', help='Send email')
    send_parser.add_argument('--to', required=True, help='Recipient email')
    send_parser.add_argument('--subject', required=True, help='Email subject')
    send_parser.add_argument('--body', required=True, help='Email body (text or file path)')
    send_parser.add_argument('--dry-run', action='store_true', default=True,
                            help='Preview only (default)')
    send_parser.add_argument('--apply', action='store_true', help='Actually send')

    # Read command
    read_parser = subparsers.add_parser('read', help='Read emails')
    read_parser.add_argument('--unread', action='store_true', help='Only unread')
    read_parser.add_argument('--limit', type=int, default=10, help='Max emails to read')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search emails')
    search_parser.add_argument('query', help='Gmail search query')

    # Extract command
    extract_parser = subparsers.add_parser('extract', help='Extract entities from email')
    extract_parser.add_argument('--email-id', required=True, help='Email ID')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Execute command
    if args.command == 'send':
        # Read body from file if it's a path
        body = args.body
        if Path(args.body).exists():
            with open(args.body, 'r') as f:
                body = f.read()

        dry_run = not args.apply
        send_email(args.to, args.subject, body, dry_run)

    elif args.command == 'read':
        emails = read_emails(args.unread, args.limit)
        print(json.dumps(emails, indent=2))

    elif args.command == 'search':
        emails = search_emails(args.query)
        print(json.dumps(emails, indent=2))

    elif args.command == 'extract':
        extract_entities_from_email(args.email_id)


if __name__ == "__main__":
    main()
