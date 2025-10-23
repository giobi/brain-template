#!/bin/bash

# Decrypt .env.gpg to .env
# Usage: ./decrypt-env.sh

cd /home/claude/brain

if [ ! -f .env.gpg ]; then
    echo "❌ .env.gpg not found in /home/claude/brain/"
    exit 1
fi

echo "🔓 Decrypting .env.gpg..."

gpg --batch --decrypt .env.gpg > .env 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ .env decrypted successfully!"
    echo "   Output: .env"
    ls -lh .env
    echo ""
    echo "⚠️  Remember: .env is gitignored (NEVER commit)"
else
    echo "❌ Decryption failed"
    echo "   Make sure you have the private key: claude@dioniso"
    exit 1
fi
