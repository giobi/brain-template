#!/usr/bin/env php
<?php
/**
 * Exchange OAuth Authorization Code for Tokens
 *
 * Takes authorization code from browser, exchanges for access + refresh tokens
 */

if ($argc < 2) {
    echo "❌ Usage: php exchange-code.php AUTHORIZATION_CODE\n";
    echo "\n";
    echo "Example:\n";
    echo "  php exchange-code.php 4/0AanRRrvXsP9k...\n";
    echo "\n";
    exit(1);
}

$authCode = $argv[1];

// Load .env for client credentials
$envFile = '/home/claude/brain/.env';
if (!file_exists($envFile)) {
    die("❌ Error: .env not found\n");
}

$envVars = parse_ini_file($envFile);
$clientId = $envVars['GMAIL_CLIENT_ID'] ?? null;
$clientSecret = $envVars['GMAIL_CLIENT_SECRET'] ?? null;

if (!$clientId || !$clientSecret) {
    die("❌ Error: GMAIL_CLIENT_ID or GMAIL_CLIENT_SECRET not found in .env\n");
}

echo "🔄 Exchanging authorization code for tokens...\n\n";

// Exchange code for tokens
$tokenUrl = 'https://oauth2.googleapis.com/token';
$postData = [
    'code' => $authCode,
    'client_id' => $clientId,
    'client_secret' => $clientSecret,
    'redirect_uri' => 'urn:ietf:wg:oauth:2.0:oob',
    'grant_type' => 'authorization_code'
];

$ch = curl_init($tokenUrl);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($postData));
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($httpCode !== 200) {
    echo "❌ Failed to exchange code\n";
    echo "HTTP Code: $httpCode\n";
    echo "Response: $response\n";
    exit(1);
}

$data = json_decode($response, true);

if (!isset($data['access_token']) || !isset($data['refresh_token'])) {
    echo "❌ Invalid response from OAuth server\n";
    echo "Response: $response\n";
    exit(1);
}

$accessToken = $data['access_token'];
$refreshToken = $data['refresh_token'];
$expiresIn = $data['expires_in'] ?? 3600;
$scope = $data['scope'] ?? '';

echo "✅ Tokens obtained successfully!\n\n";

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n";
echo "📋 NEW TOKENS\n";
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n";

echo "ACCESS TOKEN (expires in $expiresIn seconds):\n";
echo "$accessToken\n\n";

echo "REFRESH TOKEN (permanent):\n";
echo "$refreshToken\n\n";

echo "SCOPES GRANTED:\n";
echo "$scope\n\n";

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n";
echo "📝 NEXT STEPS\n";
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n";

echo "1. Update /home/claude/brain/.env:\n\n";
echo "   GMAIL_ACCESS_TOKEN=$accessToken\n";
echo "   GMAIL_REFRESH_TOKEN=$refreshToken\n\n";

echo "2. Re-encrypt .env.gpg:\n";
echo "   /home/claude/brain/tools/security/encrypt-env.sh\n\n";

echo "3. Commit changes:\n";
echo "   git add .env.gpg\n";
echo "   git commit -m 'Update Gmail OAuth with SEND scope'\n";
echo "   git push\n\n";

echo "4. Test send:\n";
echo "   php /home/claude/brain/tools/gmail/send-email.php\n\n";

// Save tokens to temp file for easy copy-paste
$tokenFile = '/tmp/gmail-new-tokens.txt';
file_put_contents($tokenFile, "GMAIL_ACCESS_TOKEN=$accessToken\nGMAIL_REFRESH_TOKEN=$refreshToken\n");
echo "💾 Tokens also saved to: $tokenFile\n\n";
