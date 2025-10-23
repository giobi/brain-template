#!/bin/bash

# GitHub Repository Rename Tool
# Usage: ./rename-repo.sh owner/old-name new-name

if [ -f /home/claude/brain/.env ]; then
    export $(grep -v '^#' /home/claude/brain/.env | xargs)
fi

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "❌ Usage: $0 owner/repo-old new-name"
    echo "   Example: $0 giobi/ai-notes minerva"
    exit 1
fi

REPO_FULL=$1
NEW_NAME=$2

# Split owner/repo
OWNER=$(echo $REPO_FULL | cut -d'/' -f1)
OLD_NAME=$(echo $REPO_FULL | cut -d'/' -f2)

echo "🔄 Renaming GitHub repository..."
echo "   Owner: $OWNER"
echo "   Old name: $OLD_NAME"
echo "   New name: $NEW_NAME"
echo ""

# Rename via GitHub API
RESPONSE=$(curl -s -X PATCH \
  "https://api.github.com/repos/$OWNER/$OLD_NAME" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  -d "{\"name\":\"$NEW_NAME\"}")

# Check success
if echo "$RESPONSE" | grep -q '"name"'; then
    NEW_URL=$(echo "$RESPONSE" | grep -o '"html_url":"[^"]*"' | cut -d'"' -f4)
    echo "✅ Repository renamed successfully!"
    echo "   New URL: $NEW_URL"
    echo ""
    echo "📋 Next steps:"
    echo "   1. Update local remote: cd /home/web/$OLD_NAME && git remote set-url origin git@github.com:$OWNER/$NEW_NAME.git"
    echo "   2. Rename local directory: cd /home/web && mv $OLD_NAME $NEW_NAME"
    echo "   3. Update any scripts/configs that reference old name"
else
    echo "❌ Failed to rename repository"
    echo "$RESPONSE"
    exit 1
fi
