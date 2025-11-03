#!/bin/bash
# Brain Template Sync
#
# Syncs public/reusable files from brain/ to brain-template/ repo
# Excludes private data (personal.md, database/, log/, diary/, etc.)
#
# Usage:
#   ./sync-brain-template.sh           # dry-run (preview only)
#   ./sync-brain-template.sh --apply   # actually sync and commit

set -e

BRAIN_DIR="/home/claude/brain"
TEMPLATE_DIR="/home/claude/brain-template"
MODE="${1:-preview}"

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔄 Brain Template Sync${NC}"
echo "Brain: $BRAIN_DIR"
echo "Template: $TEMPLATE_DIR"

if [ "$MODE" = "--apply" ]; then
    echo -e "Mode: ${GREEN}APPLY (will commit changes)${NC}"
else
    echo -e "Mode: ${YELLOW}PREVIEW (dry-run)${NC}"
fi

echo ""

# Check directories exist
if [ ! -d "$BRAIN_DIR" ]; then
    echo -e "${RED}❌ Brain directory not found: $BRAIN_DIR${NC}"
    exit 1
fi

if [ ! -d "$TEMPLATE_DIR" ]; then
    echo -e "${RED}❌ Template directory not found: $TEMPLATE_DIR${NC}"
    echo "Clone it with: git clone git@github.com:giobi/brain-template.git ~/brain-template"
    exit 1
fi

# Change to template dir
cd "$TEMPLATE_DIR"

# Pull latest
if [ "$MODE" = "--apply" ]; then
    echo -e "${BLUE}📥 Pulling latest from origin...${NC}"
    git pull --rebase
    echo ""
fi

CHANGES=0

###########################################
# SYNC FILES
###########################################

# Function to sync file
sync_file() {
    local SRC="$1"
    local DEST="$2"

    if [ ! -f "$SRC" ]; then
        echo -e "${YELLOW}⚠️  Source not found: $SRC${NC}"
        return
    fi

    # Check if file differs
    if diff -q "$SRC" "$DEST" >/dev/null 2>&1; then
        echo -e "${BLUE}SKIP${NC} $DEST - no changes"
        return
    fi

    if [ "$MODE" = "--apply" ]; then
        cp "$SRC" "$DEST"
        echo -e "${GREEN}✅ SYNCED${NC} $DEST"
    else
        echo -e "${YELLOW}WOULD SYNC${NC} $DEST"
    fi

    CHANGES=$((CHANGES + 1))
}

# Function to sync directory recursively
sync_directory() {
    local SRC_DIR="$1"
    local DEST_DIR="$2"
    local EXCLUDE_PATTERN="$3"

    if [ ! -d "$SRC_DIR" ]; then
        echo -e "${YELLOW}⚠️  Source directory not found: $SRC_DIR${NC}"
        return
    fi

    # Create dest if doesn't exist
    if [ "$MODE" = "--apply" ] && [ ! -d "$DEST_DIR" ]; then
        mkdir -p "$DEST_DIR"
    fi

    # Sync all files
    while IFS= read -r -d '' file; do
        # Skip excluded patterns
        if [ -n "$EXCLUDE_PATTERN" ] && echo "$file" | grep -qE "$EXCLUDE_PATTERN"; then
            continue
        fi

        # Get relative path
        rel_path="${file#$SRC_DIR/}"
        dest_file="$DEST_DIR/$rel_path"

        # Create parent dir if needed
        dest_parent=$(dirname "$dest_file")
        if [ "$MODE" = "--apply" ] && [ ! -d "$dest_parent" ]; then
            mkdir -p "$dest_parent"
        fi

        # Sync file
        if [ ! -f "$dest_file" ] || ! diff -q "$file" "$dest_file" >/dev/null 2>&1; then
            if [ "$MODE" = "--apply" ]; then
                cp "$file" "$dest_file"
                echo -e "${GREEN}✅ SYNCED${NC} ${rel_path}"
            else
                echo -e "${YELLOW}WOULD SYNC${NC} ${rel_path}"
            fi
            CHANGES=$((CHANGES + 1))
        fi
    done < <(find "$SRC_DIR" -type f -print0)
}

echo -e "${BLUE}📋 Syncing files...${NC}\n"

# 1. Sync boot/rules.md → rules.md (root)
echo "📄 rules.md"
sync_file "$BRAIN_DIR/boot/rules.md" "$TEMPLATE_DIR/rules.md"

# 2. Sync .gitignore
echo ""
echo "📄 .gitignore"
sync_file "$BRAIN_DIR/.gitignore" "$TEMPLATE_DIR/.gitignore"

# 3. Sync tools/ directory (exclude sensitive files)
echo ""
echo -e "${BLUE}📁 tools/${NC}"

# List of tools directories to sync
TOOL_DIRS=(
    "tools/subagent"
    "tools/database"
    "tools/gmail"
    "tools/cron"
    "tools/brain"
)

for tool_dir in "${TOOL_DIRS[@]}"; do
    if [ -d "$BRAIN_DIR/$tool_dir" ]; then
        echo ""
        echo "  → $tool_dir/"

        # Exclude patterns: backup dirs, __pycache__, .pyc, sensitive data
        EXCLUDE_PATTERN="(__pycache__|\.pyc$|backup/|\.log$)"

        src="$BRAIN_DIR/$tool_dir"
        dest="$TEMPLATE_DIR/$tool_dir"

        # Manual file-by-file sync for better control
        while IFS= read -r -d '' file; do
            # Skip excluded
            if echo "$file" | grep -qE "$EXCLUDE_PATTERN"; then
                continue
            fi

            # Get relative path
            rel_path="${file#$BRAIN_DIR/$tool_dir/}"
            dest_file="$dest/$rel_path"

            # Create parent dir
            dest_parent=$(dirname "$dest_file")
            if [ "$MODE" = "--apply" ] && [ ! -d "$dest_parent" ]; then
                mkdir -p "$dest_parent"
            fi

            # Check if differs
            if [ ! -f "$dest_file" ] || ! diff -q "$file" "$dest_file" >/dev/null 2>&1; then
                if [ "$MODE" = "--apply" ]; then
                    cp "$file" "$dest_file"
                    echo -e "    ${GREEN}✅${NC} $rel_path"
                else
                    echo -e "    ${YELLOW}~${NC} $rel_path"
                fi
                CHANGES=$((CHANGES + 1))
            fi
        done < <(find "$src" -type f -print0 2>/dev/null || true)
    fi
done

echo ""
echo "="*60
echo -e "${BLUE}📊 Summary${NC}"
echo "="*60

if [ $CHANGES -eq 0 ]; then
    echo -e "${GREEN}✅ All files up to date - no changes${NC}"
    exit 0
fi

echo "Files changed: $CHANGES"

if [ "$MODE" = "--apply" ]; then
    echo ""
    echo -e "${BLUE}📝 Committing changes...${NC}"

    git add -A

    # Check if there are changes to commit
    if git diff --cached --quiet; then
        echo -e "${GREEN}✅ No changes to commit (possibly whitespace only)${NC}"
        exit 0
    fi

    # Create commit
    TIMESTAMP=$(date +"%Y-%m-%d %H:%M")
    git commit -m "Sync from brain - $TIMESTAMP

Auto-sync of public/template files from main brain repository.

Changes: $CHANGES files updated

🤖 Generated by sync-brain-template.sh"

    echo ""
    echo -e "${GREEN}✅ Changes committed${NC}"
    echo ""
    echo -e "${YELLOW}📤 Push with: cd ~/brain-template && git push${NC}"

else
    echo ""
    echo -e "${YELLOW}💡 Run with --apply to sync and commit${NC}"
fi

echo "="*60
