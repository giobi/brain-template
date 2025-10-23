# GitHub Tools

Tool per interagire con GitHub API direttamente.

## 🔑 Setup

Il token GitHub è configurato in `/home/claude/brain/.env`:
```bash
GITHUB_TOKEN=github_pat_xxx...
```

Questo token ha permessi per gestire repository.

---

## 🛠️ Strumenti Disponibili

### rename-repo.sh

Rinomina una repository GitHub via API.

**Usage**:
```bash
./rename-repo.sh owner/old-name new-name
```

**Example**:
```bash
./rename-repo.sh giobi/ai-notes minerva
```

**Output**:
- ✅ Conferma rinomina
- 📋 Next steps (update local remote, rename directory)

**Note**:
- Dopo rename su GitHub, devi aggiornare local remote e rinominare directory locale
- GitHub fa auto-redirect da vecchio nome per un po', ma meglio aggiornare subito

---

## 📚 GitHub API Reference

**Rename Repository**:
```bash
curl -X PATCH \
  "https://api.github.com/repos/OWNER/REPO" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -d '{"name":"NEW_NAME"}'
```

**List Repositories**:
```bash
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.github.com/user/repos"
```

**Get Repository Info**:
```bash
curl -H "Authorization: Bearer $GITHUB_TOKEN" \
  "https://api.github.com/repos/OWNER/REPO"
```

**Create Repository**:
```bash
curl -X POST \
  "https://api.github.com/user/repos" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -d '{"name":"REPO_NAME","description":"Description","private":false}'
```

---

## 🔐 Security Notes

- Token stored in `/home/claude/brain/.env` (NOT committed to git)
- Token has `repo` scope (full control of repositories)
- Never commit token to public repos
- Token expires: check GitHub settings if commands fail

---

## 🚀 Future Tools

Possibili espansioni:
- [ ] Create new repository
- [ ] Archive repository
- [ ] Manage collaborators
- [ ] Create/manage issues
- [ ] Create/manage PRs
- [ ] Manage webhooks
- [ ] Repository topics/tags

---

*Created: 2025-10-23*
*Token configured and working*
