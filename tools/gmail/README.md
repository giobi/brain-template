# Gmail Tools

Strumenti per gestione email Gmail via API e processing con Claude direct.

**⚠️ METODO UFFICIALE**: Claude Direct Processing (NO Circus, NO Gemini, NO scripts)

**📚 Documentazione completa**: Vedi `index.md` per metodo ufficiale e `import-rules.md` per regole processing

---

## 📋 Tools Available

### 1. refresh-token.php

**Purpose**: Automatic Gmail OAuth token refresh

**Usage**:
```bash
php /home/claude/brain/tools/gmail/refresh-token.php
```

**What it does**:
1. Checks if GMAIL_ACCESS_TOKEN is expired
2. Uses GMAIL_REFRESH_TOKEN to get new access token
3. Updates `/home/claude/brain/.env` automatically
4. Re-encrypts `.env.gpg` for backup

**Cron**: Runs automatically every 45 minutes
```bash
*/45 * * * * /usr/bin/php /home/claude/brain/tools/gmail/refresh-token.php >> /tmp/gmail-token-refresh.log 2>&1
```

**Logs**: `/tmp/gmail-token-refresh.log`

---

## 🔧 Setup

### Required Environment Variables

In `/home/claude/brain/.env`:

```bash
GMAIL_CLIENT_ID=your-client-id.apps.googleusercontent.com
GMAIL_CLIENT_SECRET=GOCSPX-your-secret
GMAIL_REFRESH_TOKEN=1//your-refresh-token
GMAIL_ACCESS_TOKEN=ya29.a0...  # Auto-updated by refresh-token.php
```

### How to Get OAuth Credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project or select existing
3. Enable Gmail API
4. Create OAuth 2.0 credentials (Desktop app)
5. Use OAuth playground or custom flow to get refresh_token

**OAuth Flow**:
```bash
# Generate authorization URL
php /home/claude/brain/tools/gmail/generate-oauth-url.php

# Follow instructions to get authorization code
# Exchange code for tokens
php /home/claude/brain/tools/gmail/exchange-code.php YOUR_CODE_HERE
```

### Current OAuth Scopes

- ✅ `gmail.readonly` - Read all resources and metadata
- ✅ `gmail.send` - Send messages
- ✅ `gmail.compose` - Create and update drafts
- ✅ `gmail.modify` - Modify messages (mark read/unread, archive, trash, add/remove labels)
- ✅ `gmail.labels` - Create and manage custom labels

**Use cases**:
- Import emails → process with AI → mark as read + add "brain-processed" label
- Create drafts programmatically (tickets, responses, etc.)
- Archive processed emails automatically

---

## 📊 Email Import & Processing

**⚠️ METODO UFFICIALE**: Claude Direct Processing

Vedi documentazione completa:
- **`index.md`** - Metodo ufficiale e workflow completo
- **`import-rules.md`** - Regole processing dettagliate

**Quick reference**:
```bash
# 1. Download email JSON
curl "https://gmail.googleapis.com/gmail/v1/users/me/messages?..." \
  -H "Authorization: Bearer $ACCESS_TOKEN" > /tmp/2017-03-emails.json

# 2. Processing con Claude
# Claude legge JSON direttamente e genera markdown
# (NO Circus, NO Gemini, NO external tools)
```

**Output**:
- `log/YYYY/YYYY-MM-gmail-log.md` (professionale)
- `diary/YYYY/YYYY-MM-gmail-diary.md` (personale)

---

## 🔐 Security

**Never hardcode credentials** in scripts!

All scripts use environment variables:
```bash
getenv('GMAIL_ACCESS_TOKEN')
getenv('GMAIL_REFRESH_TOKEN')
```

**.env** (local, not versioned):
- Plain text credentials
- Only on local machine
- In .gitignore

**.env.gpg** (versioned):
- Encrypted backup
- Safe to commit to repo
- Auto-updated by refresh-token.php

---

## 🚨 Troubleshooting

### Token Expired Error

**Error**: `401 UNAUTHENTICATED` or `Invalid Credentials`

**Solution**:
```bash
# Manual refresh
php /home/claude/brain/tools/gmail/refresh-token.php

# Check cron is running
crontab -l | grep gmail
tail -f /tmp/gmail-token-refresh.log
```

### Refresh Token Invalid

**Error**: `invalid_grant` when refreshing

**Cause**: Refresh token revoked or expired (rare, usually permanent)

**Solution**: Re-authorize and get new refresh_token

---

## 📈 Monitoring

**Check token status**:
```bash
php /home/claude/brain/tools/gmail/refresh-token.php
```

Output:
- ✅ Token still valid → no refresh needed
- ⚠️ Token expired → automatic refresh + .env update

**Check cron logs**:
```bash
tail -50 /tmp/gmail-token-refresh.log
```

---

*Last updated: 2025-10-28*
*Metodo ufficiale: Claude Direct Processing (NO Circus, NO Gemini)*
*Auto token refresh enabled via cron*
