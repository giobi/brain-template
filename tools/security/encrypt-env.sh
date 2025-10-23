#!/bin/bash

# Encrypt .env with GPG key claude@dioniso
# Usage: ./encrypt-env.sh

cd /home/claude/brain

if [ ! -f .env ]; then
    echo "❌ .env not found in /home/claude/brain/"
    exit 1
fi

echo "🔐 Encrypting .env with GPG key claude@dioniso..."

gpg --batch --yes --trust-model always \
  --encrypt --recipient claude@dioniso \
  --armor --output .env.gpg .env

if [ $? -eq 0 ]; then
    echo "✅ .env encrypted successfully!"
    echo "   Output: .env.gpg"
    ls -lh .env.gpg
    echo ""
    echo "📋 Next steps:"
    echo "   git add .env.gpg"
    echo "   git commit -m 'Update .env.gpg'"
    echo "   git push"
else
    echo "❌ Encryption failed"
    exit 1
fi
