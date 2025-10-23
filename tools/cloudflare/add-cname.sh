#!/bin/bash

# Cloudflare DNS - Add CNAME Record
# Usage: ./add-cname.sh subdomain.giobi.com target.domain.com

if [ -f /home/claude/brain/.env ]; then
    export $(grep -v '^#' /home/claude/brain/.env | xargs)
fi

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "❌ Usage: $0 subdomain.giobi.com target.domain.com"
    echo "   Example: $0 minerva.giobi.com giobi.github.io"
    exit 1
fi

FULL_DOMAIN=$1
TARGET=$2

# Extract subdomain from full domain
SUBDOMAIN=$(echo $FULL_DOMAIN | sed 's/.giobi.com//')

# Cloudflare Zone ID for giobi.com (need to find this)
# Get zone ID first
ZONE_RESPONSE=$(curl -s -X GET "https://api.cloudflare.com/client/v4/zones?name=giobi.com" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json")

ZONE_ID=$(echo "$ZONE_RESPONSE" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)

if [ -z "$ZONE_ID" ]; then
    echo "❌ Failed to get Zone ID for giobi.com"
    echo "$ZONE_RESPONSE"
    exit 1
fi

echo "📍 Creating CNAME record..."
echo "   Zone: giobi.com ($ZONE_ID)"
echo "   Name: $SUBDOMAIN"
echo "   Target: $TARGET"
echo ""

# Create CNAME record
RESPONSE=$(curl -s -X POST "https://api.cloudflare.com/client/v4/zones/$ZONE_ID/dns_records" \
  -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  -H "Content-Type: application/json" \
  --data "{\"type\":\"CNAME\",\"name\":\"$SUBDOMAIN\",\"content\":\"$TARGET\",\"ttl\":1,\"proxied\":false}")

# Check success
if echo "$RESPONSE" | grep -q '"success":true'; then
    echo "✅ CNAME record created successfully!"
    echo "   $FULL_DOMAIN → $TARGET"
    echo ""
    echo "📋 Next steps:"
    echo "   1. Wait for DNS propagation (few minutes)"
    echo "   2. If GitHub Pages: create CNAME file in repo with '$FULL_DOMAIN'"
    echo "   3. Enable HTTPS in GitHub Pages settings"
    echo "   4. Test: dig $FULL_DOMAIN"
else
    echo "❌ Failed to create CNAME record"
    echo "$RESPONSE"
    exit 1
fi
