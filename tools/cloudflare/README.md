# Cloudflare Tools

Tool per gestire DNS e configurazioni Cloudflare per giobi.com.

## 🔑 Setup

Il token Cloudflare è configurato in `/home/claude/brain/.env`:
```bash
CLOUDFLARE_API_TOKEN=XXX...
```

Questo token ha permessi per gestire DNS records.

---

## 🛠️ Strumenti Disponibili

### add-cname.sh

Aggiunge un record CNAME per un sottodominio di giobi.com.

**Usage**:
```bash
./add-cname.sh subdomain.giobi.com target.domain.com
```

**Example - GitHub Pages**:
```bash
./add-cname.sh minerva.giobi.com giobi.github.io
```

**Example - Altro server**:
```bash
./add-cname.sh api.giobi.com myapp.herokuapp.com
```

**Output**:
- ✅ Conferma creazione record
- 📋 Next steps (GitHub CNAME file, DNS propagation)

**Note**:
- DNS propagation richiede qualche minuto
- Per GitHub Pages, creare file `CNAME` nella repo con il dominio custom
- Proxied è `false` (direct DNS, no Cloudflare proxy)
- TTL automatic (1 = auto)

---

## 📚 Cloudflare API Reference

**Base URL**: `https://api.cloudflare.com/client/v4`

**Authentication**:
```bash
-H "Authorization: Bearer $CLOUDFLARE_API_TOKEN"
```

### Get Zone ID

```bash
curl -X GET "https://api.cloudflare.com/client/v4/zones?name=giobi.com" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json"
```

### List DNS Records

```bash
curl -X GET "https://api.cloudflare.com/client/v4/zones/ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json"
```

### Create CNAME Record

```bash
curl -X POST "https://api.cloudflare.com/client/v4/zones/ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data '{"type":"CNAME","name":"subdomain","content":"target.com","ttl":1,"proxied":false}'
```

### Delete DNS Record

```bash
curl -X DELETE "https://api.cloudflare.com/client/v4/zones/ZONE_ID/dns_records/RECORD_ID" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN"
```

---

## 🚀 GitHub Pages Setup

**Complete flow** per mappare repo GitHub a custom domain:

### Step 1: Create CNAME in Cloudflare
```bash
./add-cname.sh minerva.giobi.com giobi.github.io
```

### Step 2: Create CNAME file in GitHub repo
```bash
cd /home/web/minerva
echo "minerva.giobi.com" > CNAME
git add CNAME
git commit -m "Add custom domain"
git push
```

### Step 3: Enable in GitHub Settings
- Repo → Settings → Pages
- Custom domain: `minerva.giobi.com`
- ✅ Enforce HTTPS

### Step 4: Wait & Test
```bash
# Wait 5-10 minutes for DNS propagation
dig minerva.giobi.com

# Test HTTPS
curl -I https://minerva.giobi.com
```

---

## 🔐 Security Notes

- Token stored in `/home/claude/brain/.env` (NOT committed to git)
- Token has DNS edit permissions for giobi.com zone
- Never commit token to public repos
- Token can be regenerated in Cloudflare dashboard

---

## 🚀 Future Tools

Possibili espansioni:
- [ ] Delete DNS record
- [ ] Update existing record
- [ ] List all DNS records
- [ ] Add A record (IP mapping)
- [ ] Manage page rules
- [ ] Purge cache
- [ ] SSL/TLS settings

---

*Created: 2025-10-23*
*Token configured and working*
