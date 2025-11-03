#!/bin/bash
# Health & Security Guardian - Runner Script
# Runs security, coherence, integrity checks based on mode

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BRAIN_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
MODE="${1:-precommit}"

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo "🛡️ Health & Security Guardian"
echo "Mode: $MODE"
echo "Brain: $BRAIN_DIR"
echo ""

# Change to brain directory
cd "$BRAIN_DIR"

###########################################
# MODE: PRE-COMMIT (Fast, BLOCKING)
###########################################
if [ "$MODE" = "precommit" ]; then
    echo "🔐 Pre-commit Security Scan (BLOCKING)"

    # Get staged files
    STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

    if [ -z "$STAGED_FILES" ]; then
        echo "✅ No staged files"
        exit 0
    fi

    echo "Scanning $(echo "$STAGED_FILES" | wc -l) staged files..."

    # Secrets patterns
    SECRETS_FOUND=0

    # Pattern list (common API keys/tokens)
    PATTERNS=(
        "ya29\."                    # Google OAuth token
        "GOCSPX-"                   # Google OAuth client secret
        "ghp_"                      # GitHub personal access token
        "github_pat_"               # GitHub PAT
        "sk-or-v1-"                 # OpenRouter API key
        "sk-ant-"                   # Anthropic API key
        "AKIA[0-9A-Z]{16}"          # AWS access key
        "[0-9]+-[0-9A-Za-z_]{32}\.apps\.googleusercontent\.com"  # Google client ID
        "\"password\":\s*\"[^\"]+\"" # Password in JSON
        "\"api_key\":\s*\"[^\"]+\""  # API key in JSON
    )

    for file in $STAGED_FILES; do
        # Skip binary files
        if ! file "$file" | grep -q text; then
            continue
        fi

        # Whitelist: files che DEVONO contenere pattern (documentazione)
        if echo "$file" | grep -qE "(tools/subagent/.*\.sh|tools/subagent/.*security.*\.md|log/.*health.*\.md|boot/rules\.md)"; then
            continue
        fi

        # Check each pattern
        for pattern in "${PATTERNS[@]}"; do
            if git diff --cached "$file" | grep -qE "$pattern"; then
                echo -e "${RED}❌ SECRETS FOUND: $file${NC}"
                echo "   Pattern: $pattern"
                git diff --cached "$file" | grep -E "$pattern" --color=always | head -3
                echo ""
                SECRETS_FOUND=1
            fi
        done
    done

    # Check .env files (should NEVER be staged)
    # ALLOW: .env.gpg (encrypted), .env.example (template)
    # BLOCK: .env, .env.local, .env.production, etc.
    if echo "$STAGED_FILES" | grep -qE "^\.env($|\.local|\.production|\.staging|\.development)"; then
        echo -e "${RED}❌ .env FILE STAGED${NC}"
        echo "   Files: $(echo "$STAGED_FILES" | grep -E "^\.env")"
        echo "   .env files should NEVER be committed!"
        SECRETS_FOUND=1
    fi

    if [ $SECRETS_FOUND -eq 1 ]; then
        echo ""
        echo -e "${RED}🚨 COMMIT BLOCKED - SECRETS DETECTED${NC}"
        echo ""
        echo "Fix:"
        echo "1. Remove secrets from files"
        echo "2. Add to .env instead"
        echo "3. Ensure .env in .gitignore"
        echo "4. git add <fixed files>"
        echo ""
        exit 1
    fi

    echo -e "${GREEN}✅ No secrets detected - commit allowed${NC}"
    exit 0

###########################################
# MODE: DAILY (Medium, non-blocking)
###########################################
elif [ "$MODE" = "daily" ]; then
    echo "📊 Daily Health Check"

    ISSUES_FOUND=0

    # 1. Security scan (like precommit but on all files)
    echo ""
    echo "🔐 Security scan..."
    if grep -r "ya29\.|GOCSPX-|ghp_|sk-" . --include="*.md" --include="*.log" --exclude-dir=.git -q 2>/dev/null; then
        echo -e "${YELLOW}⚠️  Possible secrets in files${NC}"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    else
        echo "✅ No exposed secrets"
    fi

    # 2. .env permissions
    echo ""
    echo "🔒 File permissions..."
    if [ -f .env ]; then
        PERM=$(stat -c "%a" .env 2>/dev/null || stat -f "%A" .env 2>/dev/null)
        if [ "$PERM" != "600" ]; then
            echo -e "${YELLOW}⚠️  .env permissions: $PERM (should be 600)${NC}"
            ISSUES_FOUND=$((ISSUES_FOUND + 1))
        else
            echo "✅ .env permissions correct"
        fi
    fi

    # 3. Check .gitignore
    echo ""
    echo "📝 .gitignore check..."
    if ! grep -q "^\.env$" .gitignore 2>/dev/null; then
        echo -e "${YELLOW}⚠️  .env not in .gitignore${NC}"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    else
        echo "✅ .env in .gitignore"
    fi

    # 4. Missing .index.md files
    echo ""
    echo "📁 Directory index check..."
    MISSING_INDEX=0
    for dir in tools/* database/* ; do
        if [ -d "$dir" ] && [ ! -f "$dir/.index.md" ]; then
            echo -e "${YELLOW}   Missing: $dir/.index.md${NC}"
            MISSING_INDEX=$((MISSING_INDEX + 1))
        fi
    done
    if [ $MISSING_INDEX -eq 0 ]; then
        echo "✅ All directories have .index.md"
    else
        echo -e "${YELLOW}⚠️  $MISSING_INDEX directories missing .index.md${NC}"
        ISSUES_FOUND=$((ISSUES_FOUND + 1))
    fi

    # 5. Token usage boot files
    echo ""
    echo "📊 Boot files token usage..."
    for file in boot/identity.md boot/personal.md boot/rules.md; do
        if [ -f "$file" ]; then
            CHARS=$(wc -c < "$file")
            TOKENS=$((CHARS / 4))  # Rough estimate
            echo "   $file: ~$TOKENS tokens"
        fi
    done

    echo ""
    if [ $ISSUES_FOUND -eq 0 ]; then
        echo -e "${GREEN}✅ Daily check passed - no issues${NC}"
    else
        echo -e "${YELLOW}⚠️  Daily check found $ISSUES_FOUND issues (non-blocking)${NC}"
    fi

    exit 0

###########################################
# MODE: DEEP (Slow, comprehensive)
###########################################
elif [ "$MODE" = "deep" ]; then
    echo "🔍 Deep Health Scan (this may take a while...)"

    # Run daily checks first
    echo "Running daily checks..."
    $0 daily

    echo ""
    echo "Additional deep checks:"

    # Large files
    echo ""
    echo "📦 Large files (>10MB)..."
    find . -type f -size +10M -not -path "./.git/*" -exec ls -lh {} \; 2>/dev/null | awk '{print "   " $9 " (" $5 ")"}'

    # Duplicate files
    echo ""
    echo "🔄 Checking for duplicates..."
    # Simple filename duplicate check
    find . -type f -not -path "./.git/*" | awk -F/ '{print $NF}' | sort | uniq -d | head -5

    echo ""
    echo -e "${GREEN}✅ Deep scan completed${NC}"
    exit 0

else
    echo "Unknown mode: $MODE"
    echo "Usage: $0 [precommit|daily|deep]"
    exit 1
fi
