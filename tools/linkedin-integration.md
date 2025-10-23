# LinkedIn Integration - Implementation Plan

**Data**: 2025-10-22
**Obiettivo**: Auto-post contenuti su LinkedIn dai log professionali + evoluzione AI

---

## 🎯 Cosa Postare

### 1. **Estratti Log Professionali**
Dal brain log mensile:
- Progetti completati (con tech stack)
- Milestone rilevanti
- Case study mini
- Tech insights

### 2. **AI Evolution Updates**
- Nuove feature implementate (es: Gmail import system)
- Problem solving interessanti (es: rsync --delete bug)
- Lessons learned
- Behind-the-scenes development

---

## 🔧 LinkedIn Share API - Setup

### Step 1: Creare LinkedIn App

1. Vai su https://www.linkedin.com/developers/apps
2. **Create app**:
   - App name: `Giobi Personal Brain`
   - LinkedIn Page: (tuo profilo o company page)
   - Privacy policy URL: https://giobi.com/privacy (o placeholder)
   - App logo: (optional)
3. **Products** → Request access to:
   - ✅ **Share on LinkedIn**
   - ✅ **Sign In with LinkedIn using OpenID Connect**
4. **Auth** tab:
   - OAuth 2.0 settings
   - Redirect URLs: `https://giobi.com/linkedin/callback` (o localhost per dev)
   - Save **Client ID** e **Client Secret**

### Step 2: OAuth Flow

**Authorization URL**:
```
https://www.linkedin.com/oauth/v2/authorization?
  response_type=code&
  client_id={CLIENT_ID}&
  redirect_uri={REDIRECT_URI}&
  scope=profile%20email%20w_member_social
```

**Scopes necessari**:
- `profile` - Info base profilo
- `email` - Email (optional)
- `w_member_social` - Permesso di postare

**Token Exchange**:
```bash
curl -X POST https://www.linkedin.com/oauth/v2/accessToken \
  -d grant_type=authorization_code \
  -d code={AUTH_CODE} \
  -d client_id={CLIENT_ID} \
  -d client_secret={CLIENT_SECRET} \
  -d redirect_uri={REDIRECT_URI}
```

**Response**:
```json
{
  "access_token": "AQV...",
  "expires_in": 5184000,
  "refresh_token": "...",
  "refresh_token_expires_in": 31536000
}
```

### Step 3: Get User Profile URN

```bash
curl -X GET 'https://api.linkedin.com/v2/userinfo' \
  -H 'Authorization: Bearer {ACCESS_TOKEN}'
```

Response contiene `sub` (user URN): `urn:li:person:ABC123`

---

## 📝 Post API

### Endpoint
```
POST https://api.linkedin.com/v2/ugcPosts
```

### Headers
```
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json
X-Restli-Protocol-Version: 2.0.0
```

### Payload - Text Post
```json
{
  "author": "urn:li:person:{USER_ID}",
  "lifecycleState": "PUBLISHED",
  "specificContent": {
    "com.linkedin.ugc.ShareContent": {
      "shareCommentary": {
        "text": "Your post content here\n\n#hashtag #hashtag2"
      },
      "shareMediaCategory": "NONE"
    }
  },
  "visibility": {
    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
  }
}
```

### Payload - Post with Link
```json
{
  "author": "urn:li:person:{USER_ID}",
  "lifecycleState": "PUBLISHED",
  "specificContent": {
    "com.linkedin.ugc.ShareContent": {
      "shareCommentary": {
        "text": "Check out this article!"
      },
      "shareMediaCategory": "ARTICLE",
      "media": [
        {
          "status": "READY",
          "originalUrl": "https://example.com/article"
        }
      ]
    }
  },
  "visibility": {
    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
  }
}
```

---

## 🤖 Implementazione Laravel

### File: `app/Console/Commands/LinkedInPostCommand.php`

```php
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Http;

class LinkedInPostCommand extends Command
{
    protected $signature = 'linkedin:post
                            {--content= : Post content}
                            {--url= : Optional link URL}
                            {--draft : Save as draft instead of publishing}';

    protected $description = 'Post to LinkedIn';

    public function handle()
    {
        $content = $this->option('content');
        $url = $this->option('url');
        $draft = $this->option('draft');

        if (!$content) {
            $this->error('Content required!');
            return 1;
        }

        $accessToken = env('LINKEDIN_ACCESS_TOKEN');
        $userUrn = env('LINKEDIN_USER_URN');

        $payload = [
            'author' => $userUrn,
            'lifecycleState' => $draft ? 'DRAFT' : 'PUBLISHED',
            'specificContent' => [
                'com.linkedin.ugc.ShareContent' => [
                    'shareCommentary' => [
                        'text' => $content
                    ],
                    'shareMediaCategory' => $url ? 'ARTICLE' : 'NONE',
                ]
            ],
            'visibility' => [
                'com.linkedin.ugc.MemberNetworkVisibility' => 'PUBLIC'
            ]
        ];

        if ($url) {
            $payload['specificContent']['com.linkedin.ugc.ShareContent']['media'] = [
                [
                    'status' => 'READY',
                    'originalUrl' => $url
                ]
            ];
        }

        $response = Http::withHeaders([
            'Authorization' => 'Bearer ' . $accessToken,
            'Content-Type' => 'application/json',
            'X-Restli-Protocol-Version' => '2.0.0'
        ])->post('https://api.linkedin.com/v2/ugcPosts', $payload);

        if ($response->successful()) {
            $this->info('✅ Posted to LinkedIn!');
            return 0;
        } else {
            $this->error('❌ Failed: ' . $response->body());
            return 1;
        }
    }
}
```

### File: `app/Console/Commands/GenerateLinkedInPostCommand.php`

Comando che genera contenuti LinkedIn-friendly dai log usando Gemini:

```php
<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Storage;

class GenerateLinkedInPostCommand extends Command
{
    protected $signature = 'linkedin:generate
                            {--month= : Month to analyze (YYYY-MM)}
                            {--type= : Type: project|insight|milestone|evolution}';

    protected $description = 'Generate LinkedIn post from brain logs';

    public function handle()
    {
        $month = $this->option('month') ?: date('Y-m');
        $type = $this->option('type') ?: 'project';

        // Read log file
        $logPath = "/home/claude/brain/log/" . substr($month, 0, 4) . "/$month-gmail-log.md";

        if (!file_exists($logPath)) {
            $this->error("Log not found: $logPath");
            return 1;
        }

        $logContent = file_get_contents($logPath);

        // Generate LinkedIn post with Gemini
        $prompt = $this->buildPrompt($logContent, $type);
        $post = $this->generateWithGemini($prompt);

        $this->info("📝 Generated LinkedIn Post:\n");
        $this->line("---");
        $this->line($post);
        $this->line("---");

        if ($this->confirm('Post to LinkedIn?', false)) {
            $this->call('linkedin:post', ['--content' => $post]);
        }

        return 0;
    }

    private function buildPrompt(string $logContent, string $type): string
    {
        $prompts = [
            'project' => "Analizza questo log professionale ed estrai UN PROGETTO interessante per LinkedIn.

Crea un post LinkedIn (max 1300 char) con:
- Hook iniziale accattivante
- Problema risolto
- Soluzione tecnica (1-2 tech stack)
- Risultato/impatto
- Call to action
- 3-5 hashtag rilevanti

Tono: professionale ma accessibile, prima persona.

Log:
$logContent",

            'insight' => "Analizza questo log ed estrai UN INSIGHT TECNICO interessante per LinkedIn.

Crea post (max 1300 char) su:
- Lezione tecnica imparata
- Problema comune che risolve
- Best practice
- Consiglio pratico

Tono: educational, condivisione esperienza.

Log:
$logContent",

            'milestone' => "Analizza questo log ed estrai UN MILESTONE/ACHIEVEMENT per LinkedIn.

Post celebrativo (max 1300 char):
- Cosa hai raggiunto
- Perché è importante
- Percorso
- Next steps

Tono: celebrativo ma umile.

Log:
$logContent",

            'evolution' => "Analizza come questo sistema AI si è evoluto.

Post meta (max 1300 char) su:
- Feature nuova implementata
- Problema tecnico risolto
- Behind-the-scenes dello sviluppo
- Learning experience

Tono: tech enthusiast, trasparente.

Log:
$logContent"
        ];

        return $prompts[$type] ?? $prompts['project'];
    }

    private function generateWithGemini(string $prompt): string
    {
        $response = Http::timeout(30)->post(
            'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key=' . env('GEMINI_API_KEY'),
            [
                'contents' => [
                    ['parts' => [['text' => $prompt]]]
                ],
                'generationConfig' => [
                    'temperature' => 0.7,
                    'maxOutputTokens' => 800
                ]
            ]
        );

        return $response->json()['candidates'][0]['content']['parts'][0]['text'] ?? 'ERROR';
    }
}
```

---

## 🔐 Credentials in .env

```bash
# LinkedIn API
LINKEDIN_CLIENT_ID=your_client_id
LINKEDIN_CLIENT_SECRET=your_client_secret
LINKEDIN_ACCESS_TOKEN=your_access_token
LINKEDIN_REFRESH_TOKEN=your_refresh_token
LINKEDIN_USER_URN=urn:li:person:YOUR_ID
```

---

## 🚀 Usage

```bash
# Generate post from log
php artisan linkedin:generate --month=2024-01 --type=project

# Post directly
php artisan linkedin:post --content="Your content here"

# Post with link
php artisan linkedin:post --content="Check this out" --url="https://example.com"

# Save as draft
php artisan linkedin:post --content="Draft content" --draft
```

---

## 📊 Content Strategy

### Frequenza
- **Weekly**: 1 post tecnico dai log
- **Monthly**: 1 milestone/retrospettiva
- **Occasional**: AI evolution updates quando implemento cose fighe

### Tipi di Post
1. **Project showcase** - Progetto client (anonimizzato se necessario)
2. **Tech insight** - Best practice, lessons learned
3. **Milestone** - Numeri, achievements
4. **Behind-the-scenes** - Come lavoro con AI, tool evolution
5. **Quick tips** - Snippet, command utili

### Hashtag Strategy
- `#webdevelopment` `#php` `#laravel` (tech stack)
- `#freelance` `#consulting` (business)
- `#ai` `#automation` `#productivity` (AI stuff)
- `#buildinpublic` (evolution posts)

---

## ✅ Next Steps

1. [ ] Creare LinkedIn App
2. [ ] OAuth flow + salvare token
3. [ ] Implementare comandi Laravel
4. [ ] Testare con draft post
5. [ ] Schedulare primo post real
6. [ ] Setup cron settimanale

---

Co-Authored-By: Claude <noreply@anthropic.com>
