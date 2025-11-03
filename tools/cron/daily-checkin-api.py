#!/usr/bin/env python3
"""
Daily Check-in Script - API-based
Uses OpenRouter API to run Claude autonomously for daily check-ins
"""

import os
import json
import requests
from pathlib import Path
from datetime import datetime

# Paths
BRAIN_DIR = Path("/home/claude/brain")
ENV_FILE = BRAIN_DIR / ".env"
PROMPT_FILE = BRAIN_DIR / "tools" / "cron" / "daily.md"

# Current time
now = datetime.now()
current_hour = now.hour

# Load environment
env_vars = {}
with open(ENV_FILE) as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            key, value = line.split('=', 1)
            env_vars[key] = value

OPENROUTER_API_KEY = env_vars.get('OPENROUTER_API_KEY')
TELEGRAM_BOT_TOKEN = env_vars.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = env_vars.get('TELEGRAM_CHAT_ID')

if not all([OPENROUTER_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID]):
    print("ERROR: Missing required environment variables")
    exit(1)

# Read prompt from daily.md
with open(PROMPT_FILE) as f:
    prompt = f.read()

# Add current time context to prompt
prompt_with_context = f"""{prompt}

---

**CONTESTO ESECUZIONE**:
- Ora corrente: {now.strftime('%H:%M')}
- Giorno: {now.strftime('%A %d %B %Y')}
- Ore recap obbligatori: 9:00, 14:00, 17:00

**REMINDER**: Se ora corrente NON è 09:00, 14:00, 17:00 E non ci sono urgenze → esci senza mandare Telegram (stampa solo "No urgenze - silenzio").

**IMPORTANTE LUNGHEZZA**: Telegram ha limite 4096 caratteri. Il tuo messaggio DEVE essere **MAX 3000 caratteri** (circa 600 parole). Sii conciso, usa bullet points, NO spiegazioni lunghe.

**FORMATTAZIONE**: Usa HTML per Telegram (NON Markdown):
- <b>grassetto</b> (non **grassetto**)
- <i>corsivo</i> (non _corsivo_)
- <code>codice</code> (non `codice`)
- • per bullet points
"""

# Call OpenRouter API (Claude Sonnet 4.5)
print(f"Calling OpenRouter API... (current hour: {current_hour:02d}:00)")

response = requests.post(
    "https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://brain.giobi.com",
        "X-Title": "Anacleto Daily Check-in"
    },
    json={
        "model": "anthropic/claude-sonnet-4.5",
        "messages": [
            {
                "role": "user",
                "content": prompt_with_context
            }
        ],
        "max_tokens": 4096,
        "temperature": 0.7
    }
)

if response.status_code != 200:
    print(f"ERROR: OpenRouter API failed: {response.status_code}")
    print(response.text)
    exit(1)

result = response.json()
ai_message = result['choices'][0]['message']['content']

# Check if Claude decided to stay silent (no urgencies outside recap hours)
if "No urgenze - silenzio" in ai_message or "SILENZIO" in ai_message:
    print("✅ No urgenze, silenzio mantenuto (nessun messaggio Telegram inviato)")
    exit(0)

print("AI response received, sending to Telegram...")

# Split message if too long (Telegram limit: 4096 chars)
def split_message(text, max_length=4096):
    """Split long message into chunks respecting Telegram limit"""
    if len(text) <= max_length:
        return [text]

    chunks = []
    current_chunk = ""

    for line in text.split('\n'):
        if len(current_chunk) + len(line) + 1 <= max_length:
            current_chunk += line + '\n'
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = line + '\n'

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

# Send to Telegram (split if necessary)
message_chunks = split_message(ai_message)

for i, chunk in enumerate(message_chunks):
    if len(message_chunks) > 1:
        # Add part indicator for multi-part messages
        header = f"📨 Parte {i+1}/{len(message_chunks)}\n\n"
        chunk = header + chunk

    telegram_response = requests.post(
        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
        data={
            "chat_id": TELEGRAM_CHAT_ID,
            "text": chunk,
            "parse_mode": "HTML"
        }
    )

    if telegram_response.status_code != 200:
        print(f"ERROR: Telegram API failed on chunk {i+1}: {telegram_response.status_code}")
        print(telegram_response.text)
        exit(1)

print(f"✅ Daily check-in sent successfully! ({len(message_chunks)} message(s))")
