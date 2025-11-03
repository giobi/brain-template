# Gmail OAuth Re-Authorization - Add SEND Scope

**Current scopes**: `GMAIL_READONLY` (solo lettura)
**Needed scopes**: `GMAIL_READONLY` + `GMAIL_SEND` (lettura + invio)

---

## 🔧 Problema

Il refresh token attuale ha solo scope `readonly`. Per inviare email serve scope `send`.

**Non basta aggiungere scope al codice** - serve re-autorizzare completamente.

---

## 📋 Procedura Re-Authorization

### Step 1: Prepare Authorization URL

```bash
php /home/claude/brain/tools/gmail/generate-oauth-url.php
```

Questo script genererà un URL tipo:
```
https://accounts.google.com/o/oauth2/v2/auth?
  client_id=[YOUR_CLIENT_ID].apps.googleusercontent.com
  &redirect_uri=urn:ietf:wg:oauth:2.0:oob
  &response_type=code
  &scope=https://www.googleapis.com/auth/gmail.readonly%20https://www.googleapis.com/auth/gmail.send
  &access_type=offline
  &prompt=consent
```

### Step 2: Browser Authorization

1. Apri URL in browser
2. Login con account Gmail
3. **Accetta permessi** (leggi + invia email)
4. Ricevi **authorization code**

### Step 3: Exchange Code for Tokens

```bash
php /home/claude/brain/tools/gmail/exchange-code.php YOUR_AUTHORIZATION_CODE
```

Questo ti darà:
- **New access_token** (expires in 1h)
- **New refresh_token** (permanent, with both scopes)

### Step 4: Update .env

```bash
# Backup current
cp /home/claude/brain/.env /home/claude/brain/.env.backup

# Update manually or via script
nano /home/claude/brain/.env

# Replace:
GMAIL_REFRESH_TOKEN=1//03FWaiNs16EClCgYIARAAGAMSNw...  # OLD
GMAIL_ACCESS_TOKEN=ya29.a0ATi6K2uNrkpWllOO7os...      # OLD

# With new values from exchange-code.php output
```

### Step 5: Re-encrypt .env.gpg

```bash
/home/claude/brain/tools/security/encrypt-env.sh
git add .env.gpg
git commit -m "Update Gmail OAuth with SEND scope"
git push
```

### Step 6: Test Send

```bash
php /home/claude/brain/tools/gmail/send-email.php
# Should work now! ✅
```

---

## 🔐 Security Notes

**Important**: Il nuovo refresh_token invalida il vecchio.

- ✅ Nuovo token: `GMAIL_READONLY` + `GMAIL_SEND`
- ❌ Vecchio token: stops working dopo re-auth

**Backup**: `.env.backup` contiene vecchio token se serve rollback.

---

## 📊 Scope Comparison

### Before (Current)
```
https://www.googleapis.com/auth/gmail.readonly
```
- ✅ Leggi email
- ✅ Cerca messaggi
- ❌ Invia email
- ❌ Modifica label

### After (New)
```
https://www.googleapis.com/auth/gmail.readonly
https://www.googleapis.com/auth/gmail.send
```
- ✅ Leggi email
- ✅ Cerca messaggi
- ✅ **Invia email** 🎉
- ❌ Modifica label (non serve)

---

## 🚀 Quick Start

**One-liner** (interactive):
```bash
echo "1. Generate URL:"
php /home/claude/brain/tools/gmail/generate-oauth-url.php

echo "2. Open URL in browser, authorize, copy code"
echo "3. Exchange code:"
read -p "Enter authorization code: " CODE
php /home/claude/brain/tools/gmail/exchange-code.php "$CODE"

echo "4. Update .env with output above, then:"
/home/claude/brain/tools/security/encrypt-env.sh
```

---

*Created: 2025-10-23*
*Required for email sending functionality*
