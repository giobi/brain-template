#!/usr/bin/env python3
"""
Daily Check-in Script - Autonomous Claude Update
Runs 2-3 times a day and sends Telegram update
"""

import os
import sys
import glob
import requests
from datetime import datetime, timedelta
from pathlib import Path
import re

BRAIN_DIR = Path("/home/claude/brain")

def load_env():
    """Load environment variables from .env"""
    env = {}
    env_file = BRAIN_DIR / ".env"
    if env_file.exists():
        for line in env_file.read_text().split('\n'):
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env[key] = value.strip('"')
    return env

def check_todos():
    """Check TODO files for deadlines"""
    todos = []
    todo_dir = BRAIN_DIR / "todo"

    if not todo_dir.exists():
        return []

    today = datetime.now().date()

    for todo_file in sorted(todo_dir.glob("*.md")):
        content = todo_file.read_text()

        # Extract reminder date from filename (YYYY-MM-DD-*.md)
        match = re.match(r'(\d{4})-(\d{2})-(\d{2})', todo_file.name)
        if match:
            reminder_date = datetime(int(match.group(1)), int(match.group(2)), int(match.group(3))).date()
            days_diff = (reminder_date - today).days

            if days_diff < 0:
                status = f"⚠️ Scaduto {abs(days_diff)} giorni fa"
            elif days_diff == 0:
                status = "📅 Oggi!"
            elif days_diff <= 3:
                status = f"📅 Tra {days_diff} giorni"
            else:
                continue  # Skip future TODOs beyond 3 days

            # Extract title from first # header
            title_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
            title = title_match.group(1) if title_match else todo_file.stem

            todos.append({
                'status': status,
                'title': title[:50],  # Truncate long titles
                'days_diff': days_diff
            })

    return todos

def check_sketch():
    """Check for recent sketch files"""
    sketch_dir = BRAIN_DIR / "sketch"

    if not sketch_dir.exists():
        return None

    recent_files = []
    cutoff = datetime.now() - timedelta(hours=24)

    for sketch_file in sketch_dir.glob("*.md"):
        mtime = datetime.fromtimestamp(sketch_file.stat().st_mtime)
        if mtime > cutoff:
            recent_files.append(sketch_file.name)

    return recent_files

def check_disk():
    """Check disk usage"""
    import subprocess
    result = subprocess.run(['df', '-h', '/home'], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')
    if len(lines) > 1:
        parts = lines[1].split()
        usage_percent = parts[4].rstrip('%')
        return int(usage_percent)
    return 0

def get_status_emoji(disk_usage, todos):
    """Determine system status emoji"""
    if disk_usage > 90:
        return "🔴"

    overdue_todos = [t for t in todos if t['days_diff'] < -3]
    if overdue_todos:
        return "🟡"

    return "🟢"

def build_message(todos, sketch_files, disk_usage):
    """Build Telegram message"""
    now = datetime.now().strftime('%H:%M')

    lines = [f"🤖 Daily Check-in [{now}]", ""]

    # TODOs
    lines.append("📋 TODO:")
    if todos:
        for todo in todos[:5]:  # Max 5 TODOs
            lines.append(f"- [{todo['status']}] {todo['title']}")
    else:
        lines.append("- Nessun TODO in scadenza")

    lines.append("")

    # Sketch
    lines.append("✍️ Sketch:")
    if sketch_files:
        lines.append(f"- {len(sketch_files)} nuove note (ultime 24h)")
        for f in sketch_files[:3]:  # Max 3
            lines.append(f"  • {f}")
    else:
        lines.append("- Nessuna nota recente")

    lines.append("")

    # Disk
    lines.append(f"💾 Disk: {disk_usage}% used")
    lines.append("")

    # Status
    status_emoji = get_status_emoji(disk_usage, todos)

    if status_emoji == "🟢":
        status_text = "Tutto ok"
    elif status_emoji == "🟡":
        status_text = "Alcuni TODO scaduti"
    else:
        status_text = "ATTENZIONE: Disk space critico"

    lines.append(f"{status_emoji} {status_text}")
    lines.append("")
    lines.append("---")
    lines.append("Cosa facciamo?")

    return "\n".join(lines)

def send_telegram(message, env):
    """Send message via Telegram API"""
    bot_token = env.get('TELEGRAM_BOT_TOKEN')
    chat_id = env.get('TELEGRAM_CHAT_ID')

    if not bot_token or not chat_id:
        print("❌ Missing Telegram credentials in .env")
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    response = requests.post(url, data={
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    })

    if response.status_code == 200 and response.json().get('ok'):
        print("✅ Telegram message sent successfully")
        return True
    else:
        print(f"❌ Failed to send Telegram: {response.text}")
        return False

def main():
    """Main execution"""
    print(f"[{datetime.now()}] Starting daily check-in...")

    # Load environment
    env = load_env()

    # Gather data
    todos = check_todos()
    sketch_files = check_sketch()
    disk_usage = check_disk()

    # Build message
    message = build_message(todos, sketch_files, disk_usage)

    print("\n" + "="*50)
    print(message)
    print("="*50 + "\n")

    # Send to Telegram
    success = send_telegram(message, env)

    if success:
        print(f"[{datetime.now()}] Check-in completed successfully")
        return 0
    else:
        print(f"[{datetime.now()}] Check-in failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
