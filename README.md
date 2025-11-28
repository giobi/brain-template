# Brain Template

Un template per organizzare il tuo "second brain" con l'aiuto di AI agents (Claude Code, Codex CLI, ecc).

## Quick Start

1. Clona questa repo
2. Apri con il tuo agent CLI preferito (Claude Code o Codex)
3. L'agent ti fara' alcune domande per configurare il sistema
4. Inizia a usare il brain!

## Struttura

```
brain/
├── boot/           # Identita' e configurazione agent
├── database/
│   ├── people/     # Persone (contatti, relazioni)
│   └── projects/   # Progetti attivi e passati
├── diary/          # Diario personale (vita, emozioni)
├── log/            # Log di lavoro (task, tecnico)
├── todo/           # Task da completare
├── AGENTS.md       # Istruzioni per l'agent (cuore del sistema)
└── CLAUDE.md       # Puntatore per Claude Code
```

## Documentazione

Tutta la documentazione e' in `AGENTS.md`. L'agent la leggera' automaticamente.

## Compatibilita'

- Claude Code (Anthropic)
- Codex CLI (OpenAI)
- Qualsiasi agent che legge file markdown

## License

MIT
