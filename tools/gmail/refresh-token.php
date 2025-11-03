#!/usr/bin/env php
<?php
/**
 * Gmail OAuth Token Refresh Script
 *
 * Refreshes Gmail OAuth access token using refresh token.
 * Updates brain/.env automatically with new token.
 *
 * Usage:
 *   php refresh-token.php
 *
 * Cron (every 45 minutes):
 *   (asterisk)/45 * * * * /usr/bin/php /home/claude/brain/tools/gmail/refresh-token.php >> /tmp/gmail-token-refresh.log 2>&1
 */

require_once '/home/web/circus/vendor/autoload.php';

use Google\Client as Google_Client;

// Load environment variables from brain/.env
$envFile = '/home/claude/brain/.env';
if (!file_exists($envFile)) {
    die("❌ Error: .env not found at $envFile\n");
}

$envVars = parse_ini_file($envFile);
foreach ($envVars as $key => $value) {
    putenv("$key=$value");
}

echo "🔄 Gmail OAuth Token Refresh\n";
echo "==============================\n\n";

// Setup Google Client
$client = new Google_Client();
$client->setClientId(getenv('GMAIL_CLIENT_ID'));
$client->setClientSecret(getenv('GMAIL_CLIENT_SECRET'));
$client->setAccessType('offline');

// Set current token
$token = [
    'access_token' => getenv('GMAIL_ACCESS_TOKEN'),
    'refresh_token' => getenv('GMAIL_REFRESH_TOKEN'),
    'expires_in' => 3600,
    'created' => time() - 3700, // Force expired to trigger refresh
];

$client->setAccessToken($token);

echo "🔍 Checking token status...\n";

// Check if expired
if (!$client->isAccessTokenExpired()) {
    echo "✅ Token still valid (expires in ~" . ($token['created'] + 3600 - time()) . "s)\n";
    echo "   No refresh needed.\n";
    exit(0);
}

echo "⚠️  Token expired, refreshing...\n\n";

try {
    // Refresh token
    $newToken = $client->fetchAccessTokenWithRefreshToken($client->getRefreshToken());

    if (isset($newToken['error'])) {
        throw new Exception($newToken['error_description'] ?? $newToken['error']);
    }

    $newAccessToken = $newToken['access_token'];

    echo "✅ Token refreshed successfully!\n\n";
    echo "📝 New access token (first 40 chars): " . substr($newAccessToken, 0, 40) . "...\n";

    // Update .env file
    $envContents = file_get_contents($envFile);
    $oldToken = getenv('GMAIL_ACCESS_TOKEN');

    if (strpos($envContents, $oldToken) !== false) {
        $envContents = str_replace($oldToken, $newAccessToken, $envContents);
        file_put_contents($envFile, $envContents);
        echo "✅ Updated $envFile\n";
    } else {
        echo "⚠️  Could not find old token in .env, manual update required\n";
        echo "   Set GMAIL_ACCESS_TOKEN=$newAccessToken\n";
    }

    // Update encrypted .env.gpg
    echo "\n🔐 Re-encrypting .env.gpg...\n";
    $encryptCmd = "cd /home/claude/brain && /home/claude/brain/tools/security/encrypt-env.sh";
    exec($encryptCmd, $output, $returnCode);

    if ($returnCode === 0) {
        echo "✅ .env.gpg updated\n";
    } else {
        echo "⚠️  Could not re-encrypt .env.gpg: " . implode("\n", $output) . "\n";
    }

    echo "\n✅ Token refresh complete!\n";
    echo "   Expires at: " . date('Y-m-d H:i:s', time() + 3600) . " (in 1 hour)\n";

} catch (Exception $e) {
    echo "❌ Error refreshing token: " . $e->getMessage() . "\n";
    exit(1);
}
