#!/usr/bin/env php
<?php
require_once '/home/web/circus/vendor/autoload.php';

use Google\Client as Google_Client;
use Google\Service\Gmail as Google_Service_Gmail;
use Google\Service\Gmail\Message;

// Load .env
$envFile = '/home/claude/brain/.env';
$envVars = parse_ini_file($envFile);
foreach ($envVars as $key => $value) {
    putenv("$key=$value");
}

echo "📧 Sending email via Gmail API...\n\n";

// Setup Gmail API client
$client = new Google_Client();
$client->setApplicationName('Brain Email Sender');
$client->setScopes([
    Google_Service_Gmail::GMAIL_SEND,
    Google_Service_Gmail::GMAIL_READONLY,
    Google_Service_Gmail::GMAIL_COMPOSE,
    Google_Service_Gmail::GMAIL_MODIFY,
    Google_Service_Gmail::GMAIL_LABELS
]);
$client->setAuthConfig([
    'client_id' => getenv('GMAIL_CLIENT_ID'),
    'client_secret' => getenv('GMAIL_CLIENT_SECRET'),
]);
$client->setAccessType('offline');

$token = [
    'access_token' => getenv('GMAIL_ACCESS_TOKEN'),
    'refresh_token' => getenv('GMAIL_REFRESH_TOKEN'),
    'expires_in' => 3600,
    'created' => time(),
];

$client->setAccessToken($token);

// Refresh if expired
if ($client->isAccessTokenExpired()) {
    echo "⚠️  Token expired, refreshing...\n";
    $client->fetchAccessTokenWithRefreshToken($client->getRefreshToken());
}

$service = new Google_Service_Gmail($client);

// Find original message ID from Web Awesome
echo "🔍 Finding Web Awesome email...\n";
$results = $service->users_messages->listUsersMessages('me', [
    'q' => 'from:hello@m.fontawesome.com subject:"Code so good"',
    'maxResults' => 1
]);

$messages = $results->getMessages();
if (empty($messages)) {
    echo "❌ Original email not found\n";
    exit(1);
}

$originalMsgId = $messages[0]->getId();
$originalMsg = $service->users_messages->get('me', $originalMsgId);

// Get original headers
$headers = $originalMsg->getPayload()->getHeaders();
$originalSubject = '';
$originalMessageId = '';
$references = '';

foreach ($headers as $header) {
    $name = $header->getName();
    $value = $header->getValue();

    if ($name === 'Subject') {
        $originalSubject = $value;
    } elseif ($name === 'Message-ID') {
        $originalMessageId = $value;
    } elseif ($name === 'References') {
        $references = $value;
    }
}

echo "✓ Found original: $originalSubject\n";
echo "✓ Thread ID: " . $originalMsg->getThreadId() . "\n\n";

// Build reply
$to = 'hello@m.fontawesome.com';
$subject = 'Re: ' . str_replace('Re: ', '', $originalSubject);
$body = "Looking forward to the storm! ⚡

Always excited for new tools from the Font Awesome team. Let me know when you're ready to unleash the awesomeness.

Cheers,
Giobi";

// Create email message
$emailContent = "To: $to\r\n";
$emailContent .= "Subject: $subject\r\n";
$emailContent .= "In-Reply-To: $originalMessageId\r\n";
$emailContent .= "References: $originalMessageId\r\n";
$emailContent .= "Content-Type: text/plain; charset=utf-8\r\n\r\n";
$emailContent .= $body;

// Encode in base64URL
$encodedMessage = rtrim(strtr(base64_encode($emailContent), '+/', '-_'), '=');

// Create message object
$message = new Message();
$message->setRaw($encodedMessage);
$message->setThreadId($originalMsg->getThreadId());

echo "📤 Sending reply...\n";

try {
    $sentMessage = $service->users_messages->send('me', $message);

    echo "\n✅ Email sent successfully!\n";
    echo "   Message ID: " . $sentMessage->getId() . "\n";
    echo "   Thread ID: " . $sentMessage->getThreadId() . "\n";
    echo "\n📋 Content sent:\n";
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n";
    echo "TO: $to\n";
    echo "SUBJECT: $subject\n";
    echo "\nBODY:\n$body\n";
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n";

} catch (Exception $e) {
    echo "\n❌ Failed to send email: " . $e->getMessage() . "\n";
    exit(1);
}
