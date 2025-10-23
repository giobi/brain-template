# Security Tools

Tool per gestione chiavi GPG e encryption di secrets.

---

## 🔑 GPG Key Setup

### Claude@Dioniso GPG Key

**Identity**: Claude <claude@dioniso>
**Key ID**: `E508D981718A92F2BC02205CF3B82A6A145A7DAF`
**Type**: RSA 4096-bit
**Created**: 2025-10-23
**Expires**: Never

**Public Key**: `claude-dioniso-public.key`

### Verification

```bash
gpg --list-keys claude@dioniso
```

**Output**:
```
pub   rsa4096 2025-10-23 [SCEA]
      E508D981718A92F2BC02205CF3B82A6A145A7DAF
uid           [ultimate] Claude <claude@dioniso>
sub   rsa4096 2025-10-23 [SEA]
```

---

## 🔐 .env Encryption

### Current Setup

**File**: `/home/claude/brain/.env`
- **Plain text** (gitignored, NOT versionato)
- Contains API tokens, credentials, secrets

**Encrypted Backup**: `/home/claude/brain/.env.gpg`
- **Encrypted with GPG** (versionato in repo)
- Uses public key: claude@dioniso
- Can decrypt with private key (stored in ~/.gnupg/)

### Encrypt .env

```bash
gpg --batch --yes --trust-model always \
  --encrypt --recipient claude@dioniso \
  --armor --output .env.gpg .env
```

**Result**: `.env.gpg` (ASCII armored, ~1.6KB)

### Decrypt .env

```bash
gpg --batch --decrypt .env.gpg > .env
```

**Output**:
```
gpg: encrypted with 4096-bit RSA key, ID 9522265286753EF7
      "Claude <claude@dioniso>"
```

---

## 🌍 GitHub GPG Key Upload

### Manual Upload (Required)

**Why manual**: GitHub personal access token needs `write:gpg_key` scope.
Current token has only `repo` scope.

**Steps**:
1. Go to https://github.com/settings/keys
2. Click "New GPG key"
3. Paste content of `claude-dioniso-public.key`:

```bash
cat /home/claude/brain/tools/security/claude-dioniso-public.key
```

4. Click "Add GPG key"

**Verification**:
```bash
# After adding to GitHub
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://api.github.com/user/gpg_keys | grep claude@dioniso
```

### Why Add to GitHub?

**Benefits**:
1. **Signed commits**: Can sign commits with GPG key
2. **Verified badge**: Commits show "Verified" badge
3. **Public backup**: Public key backed up on GitHub profile
4. **Trust chain**: Others can verify commits are from real Claude

**Usage**:
```bash
# Enable commit signing
git config --global user.signingkey E508D981718A92F2BC02205CF3B82A6A145A7DAF
git config --global commit.gpgsign true

# Commits will auto-sign
git commit -m "Signed commit"
# → Shows "Verified" on GitHub
```

---

## 📦 Backup & Recovery

### Backup Private Key

**⚠️ NEVER commit private key to git!**

**Export for backup** (encrypted with passphrase):
```bash
gpg --armor --export-secret-keys claude@dioniso > claude-dioniso-private-BACKUP.asc

# Store in encrypted USB/external drive, NOT in git!
```

### Restore on New Machine

```bash
# Import private key
gpg --import claude-dioniso-private-BACKUP.asc

# Import public key (from repo)
gpg --import tools/security/claude-dioniso-public.key

# Trust key
echo "E508D981718A92F2BC02205CF3B82A6A145A7DAF:6:" | gpg --import-ownertrust

# Decrypt .env
gpg --decrypt .env.gpg > .env
```

---

## 🛠️ Scripts

### encrypt-env.sh

**Purpose**: Re-encrypt .env after changes

```bash
#!/bin/bash
# Encrypt .env with GPG key

if [ ! -f .env ]; then
    echo "❌ .env not found"
    exit 1
fi

gpg --batch --yes --trust-model always \
  --encrypt --recipient claude@dioniso \
  --armor --output .env.gpg .env

echo "✅ .env encrypted to .env.gpg"
ls -lh .env.gpg
```

**Usage**:
```bash
cd /home/claude/brain
./tools/security/encrypt-env.sh
git add .env.gpg
git commit -m "Update .env.gpg"
git push
```

### decrypt-env.sh

**Purpose**: Decrypt .env.gpg to .env

```bash
#!/bin/bash
# Decrypt .env.gpg to .env

if [ ! -f .env.gpg ]; then
    echo "❌ .env.gpg not found"
    exit 1
fi

gpg --batch --decrypt .env.gpg > .env

echo "✅ .env decrypted from .env.gpg"
ls -lh .env
```

**Usage**:
```bash
cd /home/claude/brain
./tools/security/decrypt-env.sh
```

---

## 🔄 Migration from Symmetric Encryption

### Old Method (passphrase)

```bash
gpg --batch --passphrase "brain-backup-2025" \
  --symmetric --cipher-algo AES256 -o .env.gpg .env
```

**Problems**:
- Passphrase in scripts (insecure)
- No public key backup
- Can't verify who encrypted

### New Method (GPG key)

```bash
gpg --batch --yes --trust-model always \
  --encrypt --recipient claude@dioniso \
  --armor --output .env.gpg .env
```

**Benefits**:
- ✅ No passphrase needed
- ✅ Public key on GitHub
- ✅ Can sign commits
- ✅ Verifiable encryption

---

## 📋 .gitignore

**Ensure these are gitignored**:
```
# .gitignore
.env                    # Plain text secrets (NEVER commit)
*-private-BACKUP.asc   # Private key backups (NEVER commit)
```

**Ensure these ARE committed**:
```
.env.gpg                        # Encrypted secrets ✅
tools/security/*.key            # Public keys ✅
tools/security/README.md        # Documentation ✅
tools/security/*.sh             # Scripts ✅
```

---

## 🔐 Security Best Practices

### DO

- ✅ Keep `.env` in .gitignore
- ✅ Encrypt `.env` before committing (.env.gpg)
- ✅ Backup private key in secure location (encrypted USB)
- ✅ Use GPG key for encryption (not passphrase)
- ✅ Add public key to GitHub
- ✅ Sign commits with GPG

### DON'T

- ❌ NEVER commit `.env` plain text
- ❌ NEVER commit private key
- ❌ NEVER share private key
- ❌ NEVER use weak passphrases
- ❌ NEVER store backups in cloud unencrypted

---

## 📊 Files

```
brain/tools/security/
├── README.md                    # This file
├── claude-dioniso-public.key    # Public GPG key (versionato)
├── encrypt-env.sh               # Encrypt .env → .env.gpg
└── decrypt-env.sh               # Decrypt .env.gpg → .env

brain/
├── .env                         # Plain secrets (gitignored)
├── .env.gpg                     # Encrypted backup (versionato)
└── .gitignore                   # Ensures .env is ignored

~/.gnupg/
├── pubring.kbx                  # Public keyring
├── secring.gpg                  # Private keyring (NEVER share)
└── trustdb.gpg                  # Trust database
```

---

## 🚀 Quick Reference

### Encrypt .env
```bash
cd /home/claude/brain
gpg --encrypt --recipient claude@dioniso --armor -o .env.gpg .env
```

### Decrypt .env
```bash
cd /home/claude/brain
gpg --decrypt .env.gpg > .env
```

### Add to GitHub
```
1. cat tools/security/claude-dioniso-public.key
2. Copy output
3. https://github.com/settings/keys → New GPG key
4. Paste & Add
```

### Verify encryption
```bash
file .env.gpg
# Output: .env.gpg: PGP message Public-Key Encrypted Session Key
```

### List GPG keys
```bash
gpg --list-keys
gpg --list-secret-keys
```

---

*Created: 2025-10-23*
*Key ID: E508D981718A92F2BC02205CF3B82A6A145A7DAF*
*Never expires*
