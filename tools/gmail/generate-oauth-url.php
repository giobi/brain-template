#!/usr/bin/env php
<?php
/**
 * Generate Gmail OAuth Authorization URL
 *
 * Creates URL for user to authorize app with GMAIL_READONLY + GMAIL_SEND scopes
 */

// Load .env for client credentials
$envFile = '/home/claude/brain/.env';
if (!file_exists($envFile)) {
    die("❌ Error: .env not found\n");
}

$envVars = parse_ini_file($envFile);
$clientId = $envVars['GMAIL_CLIENT_ID'] ?? null;

if (!$clientId) {
    die("❌ Error: GMAIL_CLIENT_ID not found in .env\n");
}

echo "🔐 Gmail OAuth Authorization URL Generator\n";
echo "==========================================\n\n";

// Build authorization URL
$params = [
    'client_id' => $clientId,
    'redirect_uri' => 'urn:ietf:wg:oauth:2.0:oob',  // OOB = out-of-band (shows code in browser)
    'response_type' => 'code',
    'scope' => implode(' ', [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.send',
        'https://www.googleapis.com/auth/gmail.compose',
        'https://www.googleapis.com/auth/gmail.modify',
        'https://www.googleapis.com/auth/gmail.labels'
    ]),
    'access_type' => 'offline',  // Get refresh token
    'prompt' => 'consent'        // Force consent screen (ensures new refresh_token)
];

$authUrl = 'https://accounts.google.com/o/oauth2/v2/auth?' . http_build_query($params);

echo "📋 INSTRUCTIONS:\n";
echo "===============\n\n";
echo "1. Open this URL in your browser:\n\n";
echo "   \033[1;34m$authUrl\033[0m\n\n";
echo "2. Login with your Gmail account\n";
echo "3. Click 'Allow' to grant permissions:\n";
echo "   - Read email (gmail.readonly)\n";
echo "   - Send email (gmail.send)\n";
echo "   - Create drafts (gmail.compose)\n";
echo "   - Modify email (gmail.modify) - mark read, archive, trash\n";
echo "   - Manage labels (gmail.labels) - create/edit labels\n\n";
echo "4. Copy the AUTHORIZATION CODE shown in browser\n\n";
echo "5. Run: php exchange-code.php YOUR_CODE_HERE\n\n";

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n";

// Also save to file for easy copy-paste
$urlFile = '/tmp/gmail-oauth-url.txt';
file_put_contents($urlFile, $authUrl);
echo "💾 URL also saved to: $urlFile\n";
echo "   (in case terminal truncates)\n\n";
