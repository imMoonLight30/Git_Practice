# automation-hub

A personal home for small automations that make life easier — and a sandbox for shaping them into real products.

Any coding agent (GitHub Copilot, Claude Code, OpenAI/Codex, Cursor, etc.) should be able to read this repo and start contributing automations without extra instructions.

## What goes here

- Scripts and tools that automate repetitive tasks
- Small utilities that grow into bigger products
- Experiments — written quickly, polished when they prove useful

Each automation lives in its own folder under `automations/` with a short `README.md` describing **what it does**, **how to run it**, and **what it depends on**.

## Repo layout

```
automation-hub/
├── automations/        # one folder per automation (the actual work)
│   └── <name>/
│       ├── README.md   # what / why / how-to-run
│       └── ...         # code (.py, .js, .java, .sh — whatever fits)
├── scripts/            # shared helper scripts
├── docs/               # notes, ideas, design docs (markdown)
├── AGENTS.md           # instructions for AI coding agents
├── CLAUDE.md           # Claude-specific guidance (mirrors AGENTS.md)
└── .github/
    └── copilot-instructions.md   # GitHub Copilot guidance
```

## Conventions

- **Language**: pick whatever fits the task. Markdown for docs, Java when needed, Python/Node/Shell otherwise. Note the choice in the automation's README.
- **Naming**: `kebab-case` for folders, descriptive names (e.g. `daily-standup-summary`, `invoice-renamer`).
- **Self-contained**: each automation should run independently. Pin its dependencies inside its own folder (`requirements.txt`, `package.json`, etc.).
- **Secrets**: never commit them. Use a local `.env` (already gitignored) and document required variables in the automation's README.

## Adding a new automation

1. Create `automations/<your-name>/`
2. Add a `README.md` (see the template in [docs/automation-template.md](docs/automation-template.md))
3. Drop in the code and any config it needs
4. Update the **Index** below

## Index

| Automation | What it does |
| --- | --- |
| [story-generator](automations/story-generator/) | Generate a short story + narrator-style transcript + character sheet from a one-line idea, then render it to an MP3 narrated by a single voice. |

## For AI agents

If you are an AI agent picking up work in this repo, read [AGENTS.md](AGENTS.md) first.
