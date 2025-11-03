#!/usr/bin/env php
<?php
/**
 * Create Gmail draft using OAuth2
 * Usage: php create-draft.php "to@example.com" "Subject" "Body"
 */

if ($argc < 4) {
    echo "Usage: php create-draft.php \"to@example.com\" \"Subject\" \"Body\"\n";
    exit(1);
}

$to = $argv[1];
$subject = $argv[2];
$body = $argv[3];

// Load credentials from .env
$envFile = '/home/claude/brain/.env';
$env = parse_ini_file($envFile);

$accessToken = $env['GMAIL_ACCESS_TOKEN'] ?? null;
$refreshToken = $env['GMAIL_REFRESH_TOKEN'] ?? null;
$clientId = $env['GMAIL_CLIENT_ID'] ?? null;
$clientSecret = $env['GMAIL_CLIENT_SECRET'] ?? null;

if (!$accessToken || !$refreshToken) {
    die("Error: Gmail credentials not found in .env\n");
}

// Refresh access token if needed
function refreshAccessToken($clientId, $clientSecret, $refreshToken) {
    $url = 'https://oauth2.googleapis.com/token';
    $data = [
        'client_id' => $clientId,
        'client_secret' => $clientSecret,
        'refresh_token' => $refreshToken,
        'grant_type' => 'refresh_token'
    ];

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($data));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($httpCode === 200) {
        $result = json_decode($response, true);
        return $result['access_token'] ?? null;
    }

    return null;
}

// Try to refresh token
$newToken = refreshAccessToken($clientId, $clientSecret, $refreshToken);
if ($newToken) {
    $accessToken = $newToken;
    // Update .env file
    $envContent = file_get_contents($envFile);
    $envContent = preg_replace(
        '/GMAIL_ACCESS_TOKEN=.*/',
        'GMAIL_ACCESS_TOKEN=' . $newToken,
        $envContent
    );
    file_put_contents($envFile, $envContent);
}

// Create email message
$message = "To: $to\r\n";
$message .= "Subject: $subject\r\n";
$message .= "Content-Type: text/plain; charset=utf-8\r\n\r\n";
$message .= $body;

// Base64url encode
$encodedMessage = rtrim(strtr(base64_encode($message), '+/', '-_'), '=');

// Create draft via API
$url = 'https://gmail.googleapis.com/gmail/v1/users/me/drafts';
$data = json_encode([
    'message' => [
        'raw' => $encodedMessage
    ]
]);

$ch = curl_init($url);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    'Authorization: Bearer ' . $accessToken,
    'Content-Type: application/json'
]);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $data);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$response = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($httpCode === 200) {
    $result = json_decode($response, true);
    echo "✅ Draft created successfully!\n";
    echo "Draft ID: " . ($result['id'] ?? 'unknown') . "\n";
    exit(0);
} else {
    echo "❌ Failed to create draft (HTTP $httpCode)\n";
    echo "Response: $response\n";
    exit(1);
}
